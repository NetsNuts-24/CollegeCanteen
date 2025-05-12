from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views

app_name = "account"

urlpatterns = [
    path("", views.index, name="index"),
    path("inregister", views.inregister, name="inregister"),
    path("login_attempt" , views.login_attempt , name="login_attempt"),
    path("forgot-password/", views.forgot_password, name="forgot_password"),
    path("reset-password/", views.reset_password, name="reset_password"),
]