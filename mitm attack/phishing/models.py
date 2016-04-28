from django.db import models

# Create your models here.
class UserSession(models.Model):
    email = models.CharField(max_length=100)
    passwd = models.CharField(max_length= 50)
    cookies = models.TextField()
    website = models.CharField(max_length=20)

    def __unicode__(self):
        return self.email