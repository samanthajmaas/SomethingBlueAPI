from django.db import models

class Wedding(models.Model):
    """Wedding Model"""
    bride = models.ForeignKey("Bride", on_delete=models.CASCADE)
    location = models.CharField(max_length=75)
    event_date = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
    budget = models.IntegerField(validators=[MinValueValidator(0)],)