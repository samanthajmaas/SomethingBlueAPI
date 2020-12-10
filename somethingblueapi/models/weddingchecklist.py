from django.db import models
from .wedding import Wedding
from .checlistitem import ChecklistItem

class WeddingChecklist(models.Model):
    """Wedding Checklist Model"""
    wedding = models.ForeignKey("Wedding", on_delete=models.CASCADE)
    checklist_item = models.ForeignKey("ChecklistItem", on_delete=models.CASCADE)
    completed_date = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True)
