from . import views
from django.urls import path


urlpatterns = [
    path('add', views.CandidateFormView.as_view())
]