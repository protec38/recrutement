# Generated by Django 4.1.3 on 2022-11-06 23:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidates', '0005_alter_diploma_continuous_training_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='question1',
            field=models.TextField(default='', verbose_name='Pourquoi ?'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='candidate',
            name='question2',
            field=models.TextField(default='', verbose_name='Comment ?'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='candidate',
            name='question3',
            field=models.TextField(default='', verbose_name='A quelle heure ?'),
            preserve_default=False,
        ),
    ]
