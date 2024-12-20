from django.urls import path, include
from users import views

urlpatterns = [
    path("users/register", views.UserRegister.as_view(), name="register"),
    path("users/profile/<int:pk>", views.ProfileView.as_view(), name="profile"),
]
