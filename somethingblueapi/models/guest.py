from django.db import models
from django.core.validators import MinValueValidator
from .wedding import Wedding

class Guest(models.Model):
    """Guest Model"""
    wedding = models.ForeignKey("Wedding", on_delete=models.CASCADE)
    guest_first_name = models.CharField(max_length=75)
    guest_last_name = models.CharField(max_length=75)
    address = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=75)
    number_of_guests_in_party = models.IntegerField(validators=[MinValueValidator(0)])
    rsvp_status = models.CharField(max_length=75)
