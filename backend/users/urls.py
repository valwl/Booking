from django.urls import path

from . import views

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="custom_register"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("token/refresh/", views.TokenRefreshView.as_view(), name="refresh"),
    path("user/me/", views.UserProfileView.as_view(), name="get_user_data"),
    path("user/password/change/", views.PasswordChangeView.as_view(), name="password_change"),
]
