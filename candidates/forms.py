from django import forms
from django.forms import TextInput, CharField, inlineformset_factory

from candidates.models import Candidate, Answer, Question, Diploma

DiplomaFormset = inlineformset_factory(Candidate, Diploma, fields=['type', 'date', 'diploma_file', 'continuous_training_date'])
QuestionsFormset = inlineformset_factory(Candidate, Answer, fields=['question', 'text'], extra=0)
