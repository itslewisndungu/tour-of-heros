from django.db import models

from cities.models import CityModel

# Create your models here.


class HeroModel(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField()

    city = models.ForeignKey(
        CityModel, on_delete=models.SET_NULL, blank=True, null=True
    )
