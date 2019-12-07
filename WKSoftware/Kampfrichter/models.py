from django.db import models


class Competition(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateField()
    token = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class Run(models.Model):
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)
    name = models.CharField(max_length=12)
    sex = models.CharField(max_length=1, default=None)
    age = models.CharField(max_length=10, default=None)
    number = models.IntegerField(default=None)
    violation = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Relay(models.Model):
    run = models.OneToOneField(Run, on_delete=models.CASCADE, primary_key=True)
    handoff_ready = models.BooleanField(default=False)
    relay_violation = models.BooleanField(default=False)

    def __str__(self):
        return self.run.name
