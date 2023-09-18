from django.views.generic import TemplateView

from . import views
from django.urls import path

app_name = 'candidates'
urlpatterns = [
    path('add', views.CandidateCreateView.as_view(), name='add'),
    path('profile', views.CandidateProfileView.as_view(), name='profile'),
    path('questions', views.questions, name='questions'),
]
