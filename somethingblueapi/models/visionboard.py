from django.db import models
from .wedding import Wedding

class VisionBoard(models.Model):
    """Model for each vision board images"""
    wedding = models.ForeignKey("Wedding", on_delete=models.CASCADE)
    vb_img = models.ImageField(upload_to="visionboard/", null = False)