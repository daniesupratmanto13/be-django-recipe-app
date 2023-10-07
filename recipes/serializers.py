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

    def get_total_unlike(self, obj):
        return obj.get_total_unlike()

    def get_total_bookmark(self, obj):
        return obj.get_total_bookmark()

    def create(self, validated_data):
        category = validated_data.pop('category')
        category_instance, created = RecipeCategory.objects.get_or_create(
            **category)
        recipe = Recipe.objects.create(
            **validated_data, category=category_instance)

        return recipe

    def update(self, instance, validated_data):
        pass


class RecipeLikeSerilizer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = RecipeLike
        fields = ('id', 'user', 'value', 'recipe')
