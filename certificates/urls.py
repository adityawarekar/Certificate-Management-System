from django.urls import path
from . import views

app_name = "certificates"

urlpatterns = [
    path("", views.home, name="home"),
    path("lookup/", views.lookup_participant, name="lookup"),
    path("download/<uuid:participant_id>/", views.download_certificate, name="download_certificate"),
    path("verify/<uuid:token>/", views.verify_certificate, name="verify_certificate"),
    
]
