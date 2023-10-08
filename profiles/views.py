from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    GenericAPIView,
    RetrieveUpdateAPIView
)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

# models
from .models import Profile

# serializers
from .serializers import (
    UserAccountSerializer,
    UserRegisterSerializer,
    UserLoginSerializer,
    ProfileSerializer
)

# Create your views here.


class RegistrationAPI(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
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


class ProfileAPI(RetrieveUpdateAPIView):

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user.profile
