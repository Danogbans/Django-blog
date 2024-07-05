from django.contrib import admin
from .models import UserProfile


# Admin interface for the UserProfile model.
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio', 'profile_picture')
    search_fields = ('user__username', 'bio')
    list_filter = ['user']
    ordering = ['user']


admin.site.register(UserProfile, UserProfileAdmin)