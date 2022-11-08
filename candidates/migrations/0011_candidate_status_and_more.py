# Generated by Django 4.1.3 on 2022-11-07 23:59

import candidates.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidates', '0010_alter_diploma_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='status',
            field=models.CharField(choices=[('NEW', 'Nouveau'), ('COMPLETE', 'Complet'), ('VALIDATED', 'Validé')], default='NEW', max_length=100),
        ),
        migrations.AlterField(
            model_name='diploma',
            name='continuous_training_file',
            field=models.FileField(blank=True, null=True, upload_to=candidates.models.user_directory_path, verbose_name='Attestation de formation continue'),
        ),
        migrations.AlterField(
            model_name='diploma',
            name='diploma_file',
            field=models.FileField(help_text='Fichiers acceptés *.pdf, *.jpg. Taille maximale XXX Go', upload_to=candidates.models.user_directory_path, verbose_name='Diplôme'),
        ),
    ]
