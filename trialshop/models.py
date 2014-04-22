from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
import datetime
from django import forms
from django.forms import ModelForm

# Create your models here.
class catagory(models.Model):
	product_catg = models.CharField(max_length=15)

	def __unicode__(self):
		return self.product_catg

class Product(models.Model):
	product_type = models.ForeignKey(catagory)
	product_name = models.CharField(max_length=15)
	product_brand = models.CharField(max_length=15)
	product_price = models.IntegerField(default=0)
	pub_date = models.DateTimeField(default=datetime.datetime.now)
	
	product_pic=models.ImageField("product_pic",upload_to="trialshop/static/media/%Y/%m/%d",blank=True,null=True)
	
	product_detail=models.TextField(max_length=50)
	list_display = ["product_name", "product_brand", "product_price", "pub_date", "cart_value","thumbnail"]
	
	def __unicode__(self):
		return self.product_name

class Cart(models.Model):
	user=models.ForeignKey(User)
	product_id=models.ForeignKey(Product)
	pid=models.IntegerField(default=0)
	quantity=models.IntegerField(default=1)
	price=models.IntegerField(default=0)
	total_val=models.IntegerField(default=0)
	def __unicode__(self):
		return self.product_brand
