from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

# views
from . import views

app_name = 'profiles'

urlpatterns = [
    path('register/', views.RegistrationAPI.as_view(), name='register'),
    path('login/', views.LoginAPI.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', views.LogoutAPI.as_view(), name='logout'),
    path('', views.MyProfileAPI.as_view(), name='profile'),
    path('detail/<str:pk>/', views.ProfileDetailAPI.as_view(), name='profile-detail'),
    path('bookmark/<str:pk>', views.ProfileBookmarkApi.as_view(),
         name='profile-bookmark'),
    path('password/change/', views.PasswordChangeAPI.as_view(),
         name='password-change'),
]
