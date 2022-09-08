from django.db import models

# Create your models here.


class CityModel(models.Model):
    name = models.CharField(max_length=120)
    population = models.IntegerField()
