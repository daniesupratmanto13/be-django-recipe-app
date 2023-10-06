from rest_framework import serializers

# models
from .models import RecipeCategory


class RecipeCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeCategory
        fields = ('id', 'name', 'slug')
