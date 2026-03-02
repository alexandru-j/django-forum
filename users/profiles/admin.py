from django.contrib import admin

from .models import UserProfile, ProfileComment


admin.site.register(UserProfile)
admin.site.register(ProfileComment)
