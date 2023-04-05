# Generated by Django 4.1.7 on 2023-04-05 23:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('candidates', '0019_alter_candidate_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='candidate',
            options={'permissions': (('record_completion', 'Marquer comme complet'), ('record_rejection', 'Marquer comme incomplet'), ('record_acception', 'Accepter le dossier'), ('meeting_proposition', 'Proposer un entretien'), ('meeting_rejection', "Refuser la date d'entretien"), ('meeting_acception', "Accepter la date d'entretien"), ('meeting_absence', "Absent à l'entretien"), ('meeting_presence', "Présent à l'entretien"), ('candidate_resignation', 'Renoncer à la candidature'), ('candidate_rejection', 'Rejeter la candidature'), ('candidate_confirmation', 'Confirmer la candidature'), ('candidate_acception', 'Accepter la candidature'), ('account_creation', 'Compte créé'), ('closing', 'Clôre le dossier'), ('destruction', 'Destruction du dossier')), 'verbose_name': 'Candidat'},
        ),
    ]
