from django.db import models

# Create your models here.
class loginform(models.Model):
    Email=models.CharField(max_length=50)
    password=models.CharField(max_length=50)

class signform(models.Model):
    Name=models.CharField(max_length=50)
    Email=models.CharField(max_length=50)
    password=models.CharField(max_length=50)
    cpassword=models.CharField(max_length=50)
    Address=models.CharField(max_length=50)
    country=models.CharField(max_length=50)
    City=models.CharField(max_length=50)
    code=models.IntegerField(max_length=50)
    number=models.IntegerField(max_length=50)

class adminreg(models.Model):
    aname=models.CharField(max_length=255)
    aemail=models.CharField(max_length=50)
    apassword=models.CharField(max_length=50)
    capassword=models.CharField(max_length=50)


class product_tab(models.Model):
	productname=models.CharField(max_length=255)
	oldprice=models.CharField(max_length=255)
	newprice=models.CharField(max_length=255)
	pdescription=models.CharField(max_length=255)
	image=models.ImageField(upload_to="product/")
	catagory=models.CharField(max_length=255)
    

class cart(models.Model):
    pid=models.ForeignKey(product_tab,on_delete=models.CASCADE)
    uid=models.ForeignKey(signform, on_delete=models.CASCADE)
    quantity=models.CharField(max_length=250)
    total=models.CharField(max_length=250)
    status=models.CharField(max_length=250,default="pending")


class contform(models.Model):
    name=models.CharField(max_length=50)
    email=models.CharField(max_length=50)
    subject=models.CharField(max_length=50)
    message=models.CharField(max_length=100)
