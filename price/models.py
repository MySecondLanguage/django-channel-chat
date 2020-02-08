from django.db import models

class Price(models.Model):
    price = models.CharField(max_length=200)
