from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from candidates.state_machine import CandidateStatus, CandidateStateMachineMixin


class Candidate(CandidateStateMachineMixin, models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, verbose_name=_('Prénom'))
    last_name = models.CharField(max_length=100, verbose_name=_('Nom'))
    birth_date = models.DateField(verbose_name=_('Date de naissance'))
    email = models.EmailField(verbose_name=_('Courriel'))

    status = models.CharField(verbose_name=_('Statut'), choices=CandidateStatus.STATE_CHOICES, default=CandidateStatus.SM_INITIAL_STATE,
                              max_length=100)
    update = models.DateTimeField(verbose_name=_('Dernière mise à jour'), null=False, blank=False, default=datetime.now)

    class Meta:
        verbose_name = _('Candidat')
        permissions = CandidateStatus.permissions.items()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


DIPLOMA_CHOICES = [
    ('Secourisme grand public', (
        ('PSC1', 'PSC1 - Prévention et Secours Civiques de niveau 1'),
        ('SST', 'SST - Sauveteur Secouriste du Travail')
    )
     ),
    ('Secours opérationnel', (
        ('PSE1', 'PSE1 - Premiers Secours en Equipe de niveau 1'),
        ('PSE2', 'PSE2 - Premiers Secours en Equipe de niveau 2'),
    )
     ),
    ('Formation', (
        ('PAE FPS', "PAE FPS - Pédagogie Appliquée à l'emploi de Formateur Premiers Secours"),
        ('PAE FPSC', "PAE FPSC - Pédagogie Appliquée à l'emploi de Formateur Prévention et Secours Civiques"),
        ('PAE FF', "PAE FF - Pédagogie Appliquée à l'emploi de Formateur de Formateur"),
        ('CEAF', "CEAF - Conception et Encadrement d'Activité de Formation"),
    )
     )
]


def user_directory_path(instance, filename):
    return f'diploma/{instance.candidate.last_name} {instance.candidate.first_name}/{filename}'


class Diploma(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='diploma')
    type = models.CharField(choices=DIPLOMA_CHOICES, max_length=10, verbose_name=_('Type'),
                            help_text="Seuls les diplômes reconnus par le ministère de l'Intérieur sont disponibles")
    date = models.DateField(verbose_name=_("Date d'obtention"))
    continuous_training_date = models.DateField(blank=True, null=True, verbose_name=_("Dernière formation continue"),
                                                help_text="Date de la dernière formation continue, si applicable")
    diploma_file = models.FileField(verbose_name=_('Diplôme'),
                                    help_text=_('Fichiers acceptés *.pdf, *.jpg. Taille maximale XXX Go'),
                                    upload_to=user_directory_path)
    continuous_training_file = models.FileField(blank=True, null=True,
                                                verbose_name=_('Attestation de formation continue'),
                                                upload_to=user_directory_path)

    class Meta:
        verbose_name = _('Diplôme')


class QuestionTemplate(models.Model):
    text = models.CharField(max_length=200, verbose_name="Texte de la question")

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
