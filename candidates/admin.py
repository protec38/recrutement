from django.contrib import admin

from . import models
from . import forms
from .models import Candidate


class QuestionCandidateInline(admin.TabularInline):
    model = models.QuestionCandidate


class DiplomaInline(admin.TabularInline):
    model = models.Diploma


class CandidateAdmin(admin.ModelAdmin):
    model = Candidate
    fields = ['first_name', 'last_name', 'birth_date', 'email']
    inlines = [DiplomaInline, QuestionCandidateInline]


admin.site.register(models.Candidate, CandidateAdmin)
admin.site.register(models.QuestionTemplate)
admin.site.register(models.QuestionCandidate)
