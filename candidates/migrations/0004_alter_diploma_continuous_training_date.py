# Generated by Django 4.1.3 on 2022-11-05 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('candidates', '0003_remove_candidate_answers_alter_answer_question_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diploma',
            name='continuous_training_date',
            field=models.DateField(null=True),
        ),
    ]