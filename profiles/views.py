from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    GenericAPIView,
    ListCreateAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView,
    UpdateAPIView
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

# models
from .models import Profile
from recipes.models import Recipe

# serializers
from .serializers import (
    UserAccountSerializer,
    UserRegisterSerializer,
    UserLoginSerializer,
    ProfileSerializer,
    PasswordChangeSerializer
)
from recipes.serializers import RecipeSerializer

#  models
User = get_user_model()


class RegistrationAPI(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserRegisterSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = RefreshToken.for_user(user)
            data = serializer.data
            data['token'] = {
                'refresh': str(token),
                'access': str(token.access_token)
            }

            return Response(data, status=status.HTTP_201_CREATED)


class LoginAPI(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data
            serializer = UserAccountSerializer(user)
            token = RefreshToken.for_user(user)
            data = serializer.data
            data['tokens'] = {
                'refresh': str(token),
                'access': str(token.access_token)
            }

            return Response(data, status=status.HTTP_200_OK)


class LogoutAPI(GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class MyProfileAPI(RetrieveUpdateAPIView):

    permission_classes = (IsAuthenticated,)
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user.profile


class ProfileDetailAPI(RetrieveAPIView):

    permission_classes = (IsAuthenticated,)
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class ProfileBookmarkApi(ListCreateAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = RecipeSerializer
    profiles = Profile.objects.all()

    def get_queryset(self):
        user = User.objects.get(id=self.kwargs['pk'])
        profile = get_object_or_404(self.profiles, user=user)
        return profile.bookmarks.all()

    def post(self, request, pk):
        user = User.objects.get(id=pk)
        profile = get_object_or_404(self.profiles, user=user)
        recipe = Recipe.objects.get(id=request.data['id'])
        if profile:
            profile.bookmarks.add(recipe)
            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = User.objects.get(id=pk)
        profile = get_object_or_404(self.profiles, user=user)
        recipe = Recipe.objects.get(id=request.data['id'])
        if profile:
            profile.bookmarks.remove(recipe)
            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class PasswordChangeAPI(UpdateAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = PasswordChangeSerializer

    def get_object(self):
        return self.request.user
