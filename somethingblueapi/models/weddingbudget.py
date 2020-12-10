from django.db import models
from .wedding import Wedding
from .budgetitem import BudgetItem

class WeddingBudget(models.Model):
    """Wedding budget Model"""
    wedding = models.ForeignKey("Wedding", on_delete=models.CASCADE)
    budget_item = models.ForeignKey("BudgetItem", on_delete=models.CASCADE)
    estimated_cost = models.FloatField()
    actual_cost = models.FloatField()
    paid = models.BooleanField()
    proof_img = models.ImageField(
        upload_to='budgetproofs/', height_field=None,
        width_field=None, max_length=None, null=True)
