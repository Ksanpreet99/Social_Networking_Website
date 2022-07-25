from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from socialapp.forms import CreateUserForm
from socialapp.models import Friend_Request, Post, Profile, user_interest,Comments

# Register your models here.
class CustomUserAdmin(UserAdmin):
    add_form = CreateUserForm

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile)
admin.site.register(user_interest)
admin.site.register(Post)
admin.site.register(Comments)
admin.site.register(Friend_Request)
