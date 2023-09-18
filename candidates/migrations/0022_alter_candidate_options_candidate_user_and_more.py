# Generated by Django 4.2.5 on 2023-09-18 22:41

import candidates.state_machine
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('candidates', '0021_alter_candidate_options_alter_questiontemplate_text'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='candidate',
            options={'permissions': (('record_completion', 'Marquer comme complet'), ('record_rejection', 'Marquer comme incomplet'), ('record_acception', 'Accepter le dossier'), ('meeting_proposition', 'Proposer un entretien'), ('meeting_rejection', "Refuser la date d'entretien"), ('meeting_acception', "Accepter la date d'entretien"), ('meeting_absence', "Absent à l'entretien"), ('meeting_presence', "Présent à l'entretien"), ('candidate_resignation', 'Renoncer à la candidature'), ('candidate_rejection', 'Rejeter la candidature'), ('candidate_confirmation', 'Confirmer la candidature'), ('candidate_acception', 'Accepter la candidature'), ('account_creation', 'Compte créé'), ('closing', 'Clôre le dossier'), ('destruction', 'Destruction du dossier')), 'verbose_name': 'Candidat'},
        ),
        migrations.AddField(
            model_name='candidate',
            name='user',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='candidate',
            name='status',
            field=models.CharField(choices=[('RECORD_CREATED', 'Dossier créé'), ('RECORD_COMPLETED', 'Dossier complété'), ('RECORD_ACCEPTED', 'Dossier complet'), ('MEETING_PROPOSED', "Date d'entretien proposée"), ('WAITING_MEETING', "En attente de l'entretien"), ('WAITING_CANDIDATE', 'En attente de retour du candidat'), ('CANDIDATE_CONFIRMED', 'En attente de retour du recrutement'), ('REJECTED', 'Candidature refusée'), ('WAITING_CREATION', 'En attente de la création des accès'), ('WAITING_TRAINING', "En attente de l'ajout des compétences"), ('CLOSURE', 'Dossier clôturé')], default=candidates.state_machine.CandidateStatus.States['RECORD_CREATED'], max_length=100, verbose_name='Statut'),
        ),
    ]