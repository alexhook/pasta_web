from django.db import models
from django.contrib.auth.models import User

class UserPersonalInfo(models.Model):
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    photo = models.ImageField(upload_to='account/userpersonalinfo/', null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'.strip()
    
    def get_short_name(self):
        return f'{self.first_name}'.strip()
    
    def __str__(self):
        return self.user.username
