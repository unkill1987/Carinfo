from django.db import models

# Create your models here.

class Manufacture(models.Model):
    company = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    licenceNum = models.CharField(max_length=100)
    user_id = models.CharField(max_length=20, primary_key=True)
    passwd = models.CharField(max_length=20)
    charge = models.CharField(max_length=20)

    def __str__(self):
        return self.user_id


class Government(models.Model):
    government = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    user_id = models.CharField(max_length=20, primary_key=True)
    passwd = models.CharField(max_length=20)
    charge = models.CharField(max_length=20)

    def __str__(self):
        return self.user_id

class Repairshop(models.Model):
    repairshop = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    licenceNum = models.CharField(max_length=100)
    user_id = models.CharField(max_length=20, primary_key=True)
    passwd = models.CharField(max_length=20)
    charge = models.CharField(max_length=20)

    def __str__(self):
        return self.user_id


class Insurance(models.Model):
    insurance = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    licenceNum = models.CharField(max_length=100)
    user_id = models.CharField(max_length=20, primary_key=True)
    passwd = models.CharField(max_length=20)
    charge = models.CharField(max_length=20)

    def __str__(self):
        return self.user_id

