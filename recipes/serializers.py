from rest_framework import serializers

# models
from .models import RecipeCategory, Recipe, RecipeLike


class RecipeCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RecipeCategory
        fields = ('id', 'name', 'slug')


class RecipeSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    username = serializers.ReadOnlyField(source='author.username')
    category = RecipeCategorySerializer(many=True, read_only=True)
    total_like = serializers.SerializerMethodField()
    total_unlike = serializers.SerializerMethodField()
    total_bookmark = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'category', 'picture', 'title', 'desc',
            'cook_time', 'ingredients', 'procedure', 'author', 'username',
            'total__like', 'total__unlike', 'total_bookmark'
        )

    def get_total_like(self, obj):
        return obj.get_total_like()

    def get_total_bookmark(self, obj):
        return obj.get_total_bookmark()

    def create(self, validated_data):
        categories = validated_data.pop('category', [])
        recipe = Recipe.objects.create(**validated_data)
        for category in categories:
            category_instance, created = RecipeCategory.objects.get_or_create(
                **category)
            recipe.category.add(category_instance)

        recipe.save()

        return recipe

    def update(self, instance, validated_data):
        categories = validated_data.pop('category', [])
        instance.category.clear()

        for category in categories:
            category_instance, created = RecipeCategory.objects.get_or_create(
                **category)
            instance.category.add(category_instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        return instance


class RecipeLikeSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = RecipeLike
        fields = ('id', 'user', 'recipe')
