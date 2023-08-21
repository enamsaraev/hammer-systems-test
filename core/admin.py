from django.contrib import admin

from core.models import User, UserProfile, ActiveUser


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'phone',)
    list_filter = ('id', 'phone',)
    search_fields = ('id', 'phone',)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user',)
    list_filter = ('id', 'user',)
    search_fields = ('id', 'user',)


@admin.register(ActiveUser)
class ActiveUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'user_profile',)
    list_filter = ('id', 'user', 'user_profile',)
    search_fields = ('id', 'user', 'user_profile',)
