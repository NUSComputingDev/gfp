from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        if not self.user.first_name and not self.user.last_name:
            return '%s' % (self.user.username)
        return '%s %s' % (self.user.first_name, self.user.last_name)
