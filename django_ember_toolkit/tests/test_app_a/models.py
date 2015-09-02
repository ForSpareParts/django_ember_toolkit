from django.db import models

class Foo(models.Model):
    name = models.CharField(max_length=128)

class Bar(models.Model):
    name = models.CharField(max_length=128)
    created_on = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField()
