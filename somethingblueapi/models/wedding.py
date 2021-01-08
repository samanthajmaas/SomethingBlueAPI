from django.db import models
from django.core.validators import MinValueValidator
from .bride import Bride

class Wedding(models.Model):
    """Wedding Model"""
    bride = models.ForeignKey("Bride", on_delete=models.CASCADE)
    location = models.CharField(max_length=75, null=True)
    event_date = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    budget = models.IntegerField(null=True, validators=[MinValueValidator(0)],)

    @property
    def countdown(self):
        return self.__countdown

    @countdown.setter
    def countdown(self, value):
        self.__countdown = value