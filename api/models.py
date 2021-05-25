from django.db import models
from django.contrib.auth.models import User
import time
import datetime
from django.shortcuts import reverse
import uuid
from urllib.parse import urljoin
from django.conf import settings

class ActivationCode(models.Model):
    expiration_timestamp = models.PositiveIntegerField(default=0)
    code = models.CharField(max_length=100, unique=True)

    def save(self, *args, **kwargs):

        if not self.expiration_timestamp:
            raise Exception("There must be an expiration timestamp")

        self.code = str(uuid.uuid4()).upper().replace("-","")

        super(__class__,self).save(*args, **kwargs)

    def check_validity(self):
        if time.time() > self.expiration_timestamp:
            return False
        else:
            return True

    def get_link(self):
        base = reverse("interface:sign_up", kwargs={"code":self.code})
        url = urljoin(settings.SITE_URL, base.lstrip("/"))
        return url
        
    def get_exp_str(self):
        dt = datetime.datetime.fromtimestamp(self.expiration_timestamp)
        return f"{dt.month}/{dt.day}/{dt.year} {dt.hour}:{dt.minute}"



    def __str__(self):
        
        return f"{self.code} Expires: {self.get_exp_str()}; Link: {self.get_link()}"


class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.__class__.objects.exclude(id=self.id).delete()
        super(SingletonModel, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        try:
            return cls.objects.get()
        except cls.DoesNotExist:
            return cls()

class Alert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='alerts')
    timestamp = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.timestamp:
            self.timestamp = int(time.time())

        super(__class__,self).save(*args, **kwargs)

    def __str__(self):
        dt = datetime.datetime.fromtimestamp(self.timestamp)
        return f"{self.user.username} | {dt.month}//{dt.day}/{dt.year} {dt.hour}:{dt.minute}"
        

class AccountConnection(SingletonModel):
    code = models.CharField(max_length=10000, blank=False, null=False)
    button_url = models.CharField(max_length=500, blank=False, null=False)

    def __str__(self):
        return f"Connection to: {self.button_url}"


class Buttons(models.Model):
    name = models.CharField(max_length=100)
    number = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.number} | {self.name}"


