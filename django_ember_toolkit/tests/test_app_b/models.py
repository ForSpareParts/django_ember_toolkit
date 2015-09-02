from django.db import models

class Baz(models.Model):
    name = models.CharField(max_length=128)

class SecretModel(models.Model):
    name = models.CharField(max_length=128)
