from django.db import models


class Candidate(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    email = models.EmailField()
    question1 = models.TextField(verbose_name="Pourquoi ?")
    question2 = models.TextField(verbose_name="Comment ?")
    question3 = models.TextField(verbose_name="A quelle heure ?")

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
    continuous_training_date = models.DateField(blank=True, null=True)
    diploma_file = models.FileField()
    continuous_training_file = models.FileField


class QuestionTemplate(models.Model):
    text = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.text}'


class QuestionCandidate(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    question = models.CharField(max_length=200)
    text = models.TextField()
