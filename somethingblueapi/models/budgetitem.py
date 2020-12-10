from django.db import models

class BudgetItem(models.Model):
    """Model for each individual budget item"""
    save_for = models.CharField(max_length=200)
    default = models.BooleanField()
