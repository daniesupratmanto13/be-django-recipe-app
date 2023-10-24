from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    DestroyAPIView,
    RetrieveAPIView,
)
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

# models
from .models import Recipe, RecipeLike

# serializers
from .serializers import RecipeSerializer, RecipeLikeSerilizer


class RecipeListAPI(ListAPIView):

    permission_classes = (AllowAny,)
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


class RecipeCreateAPI(CreateAPIView):

    permission_classes = (IsAuthenticated,)
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class RecipeDetailAPI(RetrieveAPIView):

    permission_classes = (AllowAny,)
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


class RecipeUpdateDestroyAPI(UpdateModelMixin, DestroyAPIView):

    permission_classes = (IsAuthenticated,)
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


class RecipeLikeAPI(CreateAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = RecipeLikeSerilizer

    def post(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        recipe_like, created = RecipeLike.objects.get_or_create(
            recipe=recipe, user=self.request.user
        )
