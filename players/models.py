from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)
