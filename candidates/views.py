from django.forms import inlineformset_factory
from django.shortcuts import render
from django.urls import reverse_lazy

from django.views.generic import FormView, CreateView

from .forms import DiplomaFormset
from .models import Candidate, Diploma


class CandidateCreateView(CreateView):
    model = Candidate
    fields = ['first_name', 'last_name', 'birth_date', 'email']
    success_url = reverse_lazy('candidates:questions')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.POST:
            context['diploma_formset'] = DiplomaFormset(self.request.POST, self.request.FILES)
        else:
            context['diploma_formset'] = DiplomaFormset()

        return context

    def form_valid(self, form):
        diploma_formset = DiplomaFormset(self.request.POST, self.request.FILES)

        if not diploma_formset.is_valid() or not form.is_valid():
            return self.form_invalid(form)

        candidate = form.save()
        diploma_formset.instance = candidate
        diploma_formset.save()

        return super().form_valid(form)
