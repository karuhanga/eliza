from django.db import models


# Create your models here.
class Action(models.Model):
    name = models.CharField(max_length=100)
    completed_step_number = models.IntegerField(default=1)


class App(models.Model):
    name = models.CharField(max_length=100)
    command = models.CharField(max_length=100)


class File(models.Model):
    path = models.CharField(max_length=10000, unique=True)
    name = models.CharField(max_length=1000)
