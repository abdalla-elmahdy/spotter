import { PoseLandmarker, FilesetResolver, DrawingUtils } from "https://cdn.skypack.dev/@mediapipe/tasks-vision@0.10.0";

const session = document.getElementById("session");
const feedbackPanel = document.getElementById("feedback_panel");
const counterPanel = document.getElementById("counter");
let stage;
let poseLandmarker = null;
let sessionData = null;
let utterance = null;
let currentWorkout = 0;
let currentSet = 0;
let correct_joints = 0;
let rep_counter = 0;
let is_break = 0;
let break_time = 0;
let runningMode = "IMAGE";
let enableWebcamButton;
let webcamRunning = false;
const videoHeight = "70vh";
const videoWidth = "70vw";

const JOINTS_KEYPOINTS = {
  right_wrist: [18,16,14],
  left_wrist: [17,15,13],
  right_elbow: [16,14,12],
  left_elbow: [15,13,11],
  right_shoulder: [14,12,24],
  left_shoulder: [13,11,23],
  right_hip: [12,24,26],
  left_hip: [11,23,25],
  right_knee: [24,26,28],
  left_knee: [23,25,27],
  right_ankle: [26,28,32],
  left_ankle: [25, 27, 31],
}

// Loading and initializing the model
const createPoseLandmarker = async () => {
    const vision = await FilesetResolver.forVisionTasks("https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.0/wasm");
    poseLandmarker = await PoseLandmarker.createFromOptions(vision, {
        baseOptions: {
            modelAssetPath: `https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_lite/float16/1/pose_landmarker_lite.task`,
            delegate: "GPU"
        },
        runningMode: runningMode,
        numPoses: 1,
		minPoseDetectionConfidence: 0.8,
		minPosePresenceConfidence: 0.8,
		minTrackingConfidence: 0.8,
        
    });
    session.classList.remove("invisible");
};
createPoseLandmarker();

// Loading the session data
const loadSessionData = async () => {
  let s = await fetch("/sessions/api/")
  sessionData = await s.json();
}
loadSessionData();
   
// Grabbing the image from webcam stream and running the pipeline
    
const video = document.getElementById("webcam");
const canvasElement = document.getElementById("output_canvas");
const canvasCtx = canvasElement.getContext("2d");
const drawingUtils = new DrawingUtils(canvasCtx);
// Check if webcam access is supported.
const hasGetUserMedia = () => { var _a; return !!((_a = navigator.mediaDevices) === null || _a === void 0 ? void 0 : _a.getUserMedia); };
// If webcam supported, add event listener to button for when user
// wants to activate it.
if (hasGetUserMedia()) {
    enableWebcamButton = document.getElementById("webcamButton");
    enableWebcamButton.addEventListener("click", enableCam);
}
else {
    console.warn("getUserMedia() is not supported by your browser");
}
// Enable the live webcam view and start detection.
function enableCam(event) {
    
    if (!poseLandmarker && !sessionData) {
        feedbackPanel.innerText = "Wait! Data still loading";
        return;
    }
    if (webcamRunning === true) {
        webcamRunning = false;
      }
    else {
        feedbackPanel.innerText = "Session starting...";
        utterance = new SpeechSynthesisUtterance("Session starting...");
        speechSynthesis.speak(utterance);
        webcamRunning = true;
        enableWebcamButton.innerText = "Stop";
    }
    // getUsermedia parameters.
    const constraints = {
        video: true
    };
    // Activate the webcam stream.
    navigator.mediaDevices.getUserMedia(constraints).then((stream) => {
        video.srcObject = stream;
        video.addEventListener("loadeddata", predictWebcam);
    });
}

let lastVideoTime = -1;
async function predictWebcam() {
    canvasElement.style.height = videoHeight;
    video.style.height = videoHeight;
    canvasElement.style.width = videoWidth;
    video.style.width = videoWidth;
	
	//start detecting the stream.
    if (is_break) {
      	is_break = 0;
	  	utterance = new SpeechSynthesisUtterance(`Take a break for ${break_time} seconds`);
    	speechSynthesis.speak(utterance);
	  	setTimeout(pipeline, break_time*1000);
    }
	else {
		pipeline();
	}
    
    
}

function calculateAngel(start, mid, end) {
  let radians = Math.atan2(end.y-mid.y,end.x-mid.x) - Math.atan2(start.y-mid.y,start.x-mid.x);
  let angle = Math.abs(radians*180/Math.PI);
  if (angle>180) {
    angle = 360 - angle;
  }
  return angle;
}

function inAcceptableRange(angle, reference, difficulty=5) {
  return angle >= reference-(reference*(difficulty/100)) && angle <= reference+(reference*(difficulty/100));
}

async function pipeline() {
	if (runningMode === "IMAGE") {
        runningMode = "VIDEO";
        await poseLandmarker.setOptions({ runningMode: "VIDEO" });
    }
    let startTimeMs = performance.now();
    if (lastVideoTime !== video.currentTime) {
        lastVideoTime = video.currentTime;
        poseLandmarker.detectForVideo(video, startTimeMs, (result) => {
            let landmarks = result.landmarks[0];
            feedbackPanel.innerText = sessionData.workouts[currentWorkout].exercise.name
		feedbackPanel.innerText += ` - Set : ${currentSet+1}`
		// Calculating the angle for each required joint
		const joints = {};
		const min_angles = sessionData.workouts[currentWorkout].exercise.min[0];
    const max_angles = sessionData.workouts[currentWorkout].exercise.max[0];
		for (const joint_name of Object.keys(min_angles)) {
      if (typeof(min_angles[joint_name])==="number" && typeof(max_angles[joint_name])==="number")
			joints[joint_name] = {
				angle: calculateAngel(
				landmarks[JOINTS_KEYPOINTS[joint_name][0]],
				landmarks[JOINTS_KEYPOINTS[joint_name][1]],
				landmarks[JOINTS_KEYPOINTS[joint_name][2]],
				),
				correct: 0,
			}
		}
	// Counting logic
		for (const joint in joints) {
			if (inAcceptableRange(joints[joint].angle, min_angles[joint])) {
				stage = "min";
			}
			if (inAcceptableRange(joints[joint].angle, max_angles[joint]) && stage == "min") {
				stage = "max";
				correct_joints++;
				joints[joint].correct = 1;
			}
		}

		if (correct_joints === Object.keys(joints).length) {
			rep_counter++;
			utterance = new SpeechSynthesisUtterance(rep_counter);
        	speechSynthesis.speak(utterance);
			if (rep_counter >= sessionData.workouts[currentWorkout].reps_per_set) {  
        rep_counter = 0;
        is_break = 1;
        break_time = sessionData.workouts[currentWorkout].sets_break;
        currentSet++;
        utterance = new SpeechSynthesisUtterance(`Set number ${currentSet+1}`);
        speechSynthesis.speak(utterance);
			}
			if (currentSet >= sessionData.workouts[currentWorkout].sets) {
        currentSet = 0;
        rep_counter = 0;
        is_break = 1;
        break_time = sessionData.workouts_break;
        currentWorkout++;
        utterance = new SpeechSynthesisUtterance(sessionData.workouts[currentWorkout].exercise.name);
        speechSynthesis.speak(utterance);
        utterance = new SpeechSynthesisUtterance(sessionData.workouts[currentWorkout].exercise.starting_prompt);
        speechSynthesis.speak(utterance);
			}
			if (currentWorkout >= sessionData.workouts.length){
			feedbackPanel.innerText = "Congratulations!! you just finished your training session.";
			utterance = new SpeechSynthesisUtterance("Congratulations!! you just finished your training session.");
        	speechSynthesis.speak(utterance);
			webcamRunning = false;
			return;
			}
			correct_joints = 0;
			console.log(rep_counter);
			counterPanel.innerText = ` ${rep_counter}`; 
		} else if (correct_joints !== 0) {
      for (const joint in joints) {
        if (joints[joint].correct === 0) {
          let feedback = `Keep your ${joint.replace("_", " ")} at ${min_angles[joint]} degrees in the start of the rep and ${max_angles[joint]} in the end of it`;
          feedbackPanel.innerText = feedback;
          utterance = new SpeechSynthesisUtterance(feedback);
          speechSynthesis.speak(utterance);
        }
      }
    }
				// Drawing logic
		canvasCtx.save();
		canvasCtx.clearRect(0, 0, canvasElement.width, canvasElement.height);
		for (const landmark of result.landmarks) {
			drawingUtils.drawLandmarks(landmark, {
				radius: (data) => DrawingUtils.lerp(data.from.z, -0.15, 0.1, 5, 1)
			});
			drawingUtils.drawConnectors(landmark, PoseLandmarker.POSE_CONNECTIONS);
		}
		canvasCtx.restore();
		});
		}

		// Call this function again to keep predicting when the browser is ready.
		if (webcamRunning === true) {
			window.requestAnimationFrame(predictWebcam);
		}
}
