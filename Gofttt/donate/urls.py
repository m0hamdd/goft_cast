from django.urls import path
from .views import DonateView, DonateVerifyView

app_name = "donate"

urlpatterns = [
    path("", DonateView.as_view(), name="donate"),
    path("verify/", DonateVerifyView.as_view(), name="verify"),
]
