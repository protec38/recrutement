from django.contrib import admin

from . import models
from . import forms
from .models import Candidate


class AnswerInline(admin.TabularInline):
    model = models.Answer


class CandidateAdmin(admin.ModelAdmin):
    model = Candidate
    fields = ['first_name', 'last_name', 'birth_date', 'email']
    inlines = [AnswerInline]


admin.site.register(models.Candidate, CandidateAdmin)
admin.site.register(models.Question)
admin.site.register(models.Answer)
