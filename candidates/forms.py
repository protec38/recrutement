from django import forms
from django.forms import TextInput, CharField

from candidates.models import Candidate, Answer, Question


class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ['first_name', 'last_name', 'birth_date', 'email']


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['question', 'text']

    question = CharField()


# AnswerInlineFormset = forms.inlineformset_factory(Candidate, Answer, form=AnswerForm, can_delete=False, extra=0)
