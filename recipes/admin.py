from django.contrib import admin

# models
from .models import Recipe, RecipeCategory, Like

# Register your models here.
admin.site.register(Recipe)
admin.site.register(RecipeCategory)
admin.site.register(Like)
