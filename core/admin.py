from django.contrib import admin

from core.models import User, UserProfile, ActiveUser


admin.site.register(User)
admin.site.register(UserProfile)
admin.site.register(ActiveUser)
