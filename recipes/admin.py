from django.contrib import admin

# models
from .models import Recipe, RecipeCategory, RecipeLike

# Register your models here.
admin.site.register(Recipe)
admin.site.register(RecipeCategory)
admin.site.register(RecipeLike)
