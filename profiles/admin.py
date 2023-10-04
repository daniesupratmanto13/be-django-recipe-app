from django.contrib import admin

# models
from .models import UserAccount, Profile

# Register your models here.
admin.site.register(UserAccount)
admin.site.register(Profile)
