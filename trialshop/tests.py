from django.test import TestCase
from django.contrib import admin
from trialshop.models import Product,catagory,Cart
from django.contrib.auth.models import User
from model_mommy import mommy
# Create your tests here.
pro=mommy.make('Product')
cat=mommy.make('catagory')
car=mommy.make('Cart')

