from django.views.generic import TemplateView

from . import views
from django.urls import path

app_name = 'candidates'
urlpatterns = [
    path('add', views.CandidateCreateView.as_view(), name='add'),
    path('questions', TemplateView.as_view(template_name='candidates/next.html'), name='questions')
]
