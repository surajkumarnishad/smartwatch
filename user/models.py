from django.db import models


# Create your models here.
class contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=120)
    mobile = models.CharField(max_length=20)
    message = models.CharField(max_length=500)

    def __str__(self):
        return self.email


class brand(models.Model):
    bname = models.CharField(max_length=40)
    bpic = models.ImageField(upload_to='static/brand/', default="")
    bdate = models.DateField()

    def __str__(self):
        return self.bname


class product(models.Model):
    pname = models.CharField(max_length=150)
    ppic = models.ImageField(upload_to='static/product/', default="")
    pcolor = models.CharField(max_length=12)
    category = models.CharField(max_length=20)
    tprice = models.FloatField()
    disprice = models.FloatField()
    pdes = models.TextField(max_length=500)
    brand = models.ForeignKey(brand, on_delete=models.CASCADE)
    pdate = models.DateField()


class profile(models.Model):
    Name = models.CharField(max_length=150)
    Gender = models.CharField(max_length=10)
    Dob = models.DateField()
    Mobile = models.CharField(max_length=20)
    Email = models.EmailField(max_length=100,primary_key=True)
    Password = models.CharField(max_length=20)
    Address = models.TextField(max_length=500)
    Photo = models.ImageField(upload_to='static/profile/', default="")


class order(models.Model):
    pid = models.IntegerField()
    userid = models.EmailField(max_length=100)
    remarks = models.CharField(max_length=40)
    status = models.BooleanField()
    odate = models.DateField()


class addtocart(models.Model):
    pid = models.IntegerField()
    userid = models.EmailField(max_length=100)
    status = models.BooleanField()
    cdate = models.DateField()
