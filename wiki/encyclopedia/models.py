from django.db import models

class ModeloTest(models.Model):
    Nome = models.CharField(max_length=30)
    Idade = models.IntegerField()
