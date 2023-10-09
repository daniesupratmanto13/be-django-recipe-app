from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    DestroyAPIView,
    RetrieveAPIView,
    UpdateAPIView
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

# models
from .models import Recipe, RecipeLike

# serializers
from .serializers import RecipeSerializer, RecipeLikeSerilizer

# Create your views here.


class RecipeListAPI(ListAPIView):

    queryset = Recipe.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RecipeSerializer


class RecipeCreateAPI(CreateAPIView):

    queryset = Recipe.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = RecipeSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class RecipeDetailAPI(RetrieveAPIView):

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


class RecipeUpdateDestroyAPI(UpdateAPIView, DestroyAPIView):

    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthenticated,)
