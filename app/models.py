from django.db import models

# Create your models here.


class Notice(models.Model):
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=1000)
    c_date = models.DateTimeField(null=True)


class Sellcar(models.Model):
    serialnumber = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    modelname = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    volume = models.CharField(max_length=100)
    fuel = models.CharField(max_length=100)
    owner = models.CharField(max_length=100)
    plate = models.CharField(max_length=100)
    whentobuy = models.CharField(max_length=100)
    sellprice = models.CharField(max_length=100)
    details = models.CharField(max_length=500)


class Market(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    residentnum = models.CharField(max_length=100)
    user_id = models.CharField(max_length=20, primary_key=True)
    passwd = models.CharField(max_length=20)
    passconfirm = models.CharField(max_length=20)
    otp = models.CharField(max_length=50)
    c_date = models.DateTimeField(null=True)

    def __str__(self):
        return self.user_id

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

