from django.db import models
from django.utils.translation import gettext_lazy as _

class Candidate(models.Model):
    first_name = models.CharField(max_length=100, verbose_name=_('Prénom'))
    last_name = models.CharField(max_length=100, verbose_name=_('Nom'))
    birth_date = models.DateField(verbose_name=_('Date de naissance'))
    email = models.EmailField(verbose_name=_('Courriel'))

    class Meta:
        verbose_name = _('Candidat')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


DIPLOMA_CHOICES = [
    ('PSE1', 'Premiers Secours en Equipe de niveau 1'),
    ('PSE2', 'Premiers Secours en Equipe de niveau 2')
]


class Diploma(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='diploma')
    type = models.CharField(choices=DIPLOMA_CHOICES, max_length=10, verbose_name=_('Type'))
    date = models.DateField(verbose_name=_("Date d'obtention"))
    continuous_training_date = models.DateField(blank=True, null=True, verbose_name=_("Dernière formation continue"))
    diploma_file = models.FileField(verbose_name=_('Diplôme'))
    continuous_training_file = models.FileField

    class Meta:
        verbose_name = _('Diplôme')

class QuestionTemplate(models.Model):
    text = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.text}'

    class Meta:
        verbose_name = _('Modèle de question')
        verbose_name_plural = _('Modèles de question')


class QuestionCandidate(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    question = models.CharField(max_length=200, verbose_name=_('Question'))
    text = models.TextField(verbose_name=_('Réponse'))

    class Meta:
        verbose_name = _('Réponse des candidats')
        verbose_name_plural = _('Réponses des candidats')
