from django.views.generic import TemplateView

from . import views
from django.urls import path

app_name = 'candidates'
urlpatterns = [
    path('add', views.CandidateCreateView.as_view(), name='add'),
    path('questions', views.answers, name='questions'),
    path('confirmation', TemplateView.as_view(template_name='candidates/confirmation.html'), name='confirmation'),
]
