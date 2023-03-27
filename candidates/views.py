from django.forms import inlineformset_factory
from django.http import HttpResponseForbidden, HttpResponseServerError, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy

from django.views.generic import FormView, CreateView

from .forms import DiplomaFormset, QuestionsFormset
from .models import Candidate, Diploma, QuestionTemplate, QuestionCandidate


class CandidateCreateView(CreateView):
    model = Candidate
    fields = ['first_name', 'last_name', 'birth_date', 'email']
    success_url = reverse_lazy('candidates:questions')

    def get_context_data(self, **kwargs):
        """ Add the diploma formset to the context data in order to use it in the template.

        """
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

        # After saving the candidate, adding the questions they need to answer to their profile
        questions_templates = QuestionTemplate.objects.all()
        for q in questions_templates:
            QuestionCandidate(candidate=candidate, question=q.text).save()

        # Saving the candidate id in the session
        self.request.session['candidate_id'] = candidate.id

        return super().form_valid(form)


def questions(request):
    """ Allows the user to answer the questions assigned to them

    """
    if 'candidate_id' not in request.session:
        return HttpResponseForbidden()

    candidate = Candidate.objects.get(id=request.session['candidate_id'])  # FIXME: What happens if the id doesn't exist?

    if request.method == 'GET':
        formset = QuestionsFormset(instance=candidate)
    else:
        formset = QuestionsFormset(request.POST, instance=candidate)

        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect(reverse_lazy('candidates:confirmation'))

    return render(request, 'candidates/questions_form.html', context={'formset': formset})
