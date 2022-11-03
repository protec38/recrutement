from django.db import models


class Candidate(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    email = models.EmailField()
    answers = models.ManyToManyField('Question', through='Answer')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


DIPLOMA_CHOICES = [
    ('PSE1', 'Premiers Secours en Equipe de niveau 1'),
    ('PSE2', 'Premiers Secours en Equipe de niveau 2')
]


class Diploma(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='diploma')
    type = models.CharField(choices=DIPLOMA_CHOICES, max_length=10)
    date = models.DateField()
    continuous_training_date = models.DateField()
    diploma_file = models.FileField()
    continuous_training_file = models.FileField


class Question(models.Model):
    text = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.text}'


class Answer(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.CharField(max_length=100)
