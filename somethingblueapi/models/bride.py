from django.db import models
from django.contrib.auth.models import User

class Bride(models.Model):
    """Bride Model"""
    profile_image_url = models.ImageField(upload_to="profile_img/", blank='true', null='true')
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    @property
    def is_current_user(self):
        return self.__is_current_user

    @is_current_user.setter
    def is_current_user(self, value):
        self.__is_current_user = value