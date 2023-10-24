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
from .serializers import RecipeSerializer, RecipeLikeSerializer

# permissions
from .permissions import IsAuthor


class RecipeListAPI(ListAPIView):

    permission_classes = (AllowAny,)
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


class RecipeCreateAPI(CreateAPIView):

    permission_classes = (IsAuthor,)
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class RecipeDetailAPI(RetrieveAPIView):

    permission_classes = (AllowAny,)
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


class RecipeUpdateDestroyAPI(UpdateModelMixin, DestroyAPIView):

    permission_classes = (IsAuthor,)
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


class RecipeLikeAPI(CreateAPIView):

    serializer_class = RecipeLikeSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        recipe = get_object_or_404(Recipe, id=self.kwargs['pk'])
        new_like, created = RecipeLike.objects.get_or_create(
            user=request.user, recipe=recipe)
        if created:
            new_like.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        recipe = get_object_or_404(Recipe, id=self.kwargs['pk'])
        like = RecipeLike.objects.filter(user=request.user, recipe=recipe)
        if like.exists():
            like.delete()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
