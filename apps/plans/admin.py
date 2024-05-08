from django.contrib import admin

from .models import Exercise, MaxAngles, MinAngles

admin.site.register(Exercise)
admin.site.register(MinAngles)
admin.site.register(MaxAngles)