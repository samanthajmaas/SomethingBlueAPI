from django.db import models

class ChecklistItem(models.Model):
    """Model for each individual checklist item"""
    toDo = models.CharField(max_length=200)
    default = models.BooleanField()
