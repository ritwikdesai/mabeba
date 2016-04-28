from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Account(models.Model):
    user_id = models.CharField(max_length=50,primary_key= True)
    password = models.CharField(max_length=1500)
    secret = models.CharField(max_length=1500)
    otp_salt = models.CharField(max_length=16)
    passwd_salt = models.CharField(max_length=50)
    f_name = models.CharField(max_length=20)
    l_name = models.CharField(max_length=20)
    email_address = models.EmailField()

    def __unicode__(self):
        return unicode(self.user_id)


class SessionData(models.Model):
    user_id = models.CharField(max_length=50)
    random_nonce = models.CharField(max_length=20)
    expiry_time = models.CharField(max_length=20)
    other_data = models.TextField(null=True)
    session_id = models.CharField(max_length=50,primary_key=True)

class RequestQR(models.Model):
    request_id = models.CharField(max_length=50,primary_key=True)
    email_address = models.EmailField()
    expiry_time = models.CharField(max_length=20)
    reset = models.BooleanField(default=False)
