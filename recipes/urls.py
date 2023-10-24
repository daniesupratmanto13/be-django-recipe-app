from django.urls import path

# views
from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.RecipeListAPI.as_view(), name='list'),
    path('create/', views.RecipeCreateAPI.as_view(), name='create'),
    path('like/<int:pk>/', views.RecipeLikeAPI.as_view(), name='like'),
    path('detail/<int:pk>/', views.RecipeDetailAPI.as_view(), name='detail'),
    path('update/<int:pk>/', views.RecipeUpdateDestroyAPI.as_view(), name='update'),
    path('delete/<int:pk>/', views.RecipeUpdateDestroyAPI.as_view(), name='delete'),
]
