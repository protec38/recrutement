from django.contrib import admin

from . import models
from . import forms
from .models import Candidate


class QuestionCandidateInline(admin.TabularInline):
    model = models.QuestionCandidate
    extra = 0
    readonly_fields = ['question', 'text']
    can_delete = False


class DiplomaInline(admin.TabularInline):
    model = models.Diploma
    extra = 0


class CandidateAdmin(admin.ModelAdmin):
    model = Candidate
    fields = ['first_name', 'last_name', 'birth_date', 'email']
    inlines = [DiplomaInline, QuestionCandidateInline]


admin.site.register(models.Candidate, CandidateAdmin)
admin.site.register(models.QuestionTemplate)
