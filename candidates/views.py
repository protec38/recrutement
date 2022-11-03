from django.forms import inlineformset_factory
from django.shortcuts import render

from django.views.generic import FormView, CreateView

from .forms import CandidateForm, AnswerForm
from .models import Question, Candidate, Answer


class CandidateFormView(CreateView):
    template_name = 'candidates/candidate.html'
    form_class = CandidateForm
    
    def get_context_data(self, **kwargs):
        context = super(CandidateFormView, self).get_context_data(**kwargs)

        initial = [{'question': q.text} for q in Question.objects.all()]
        AnswerInlineFormset = inlineformset_factory(Candidate, Answer, form=AnswerForm, can_delete=False, extra=len(initial))
        context['answers_formset'] = AnswerInlineFormset(initial=initial)
        return context

