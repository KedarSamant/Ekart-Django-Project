from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=30,unique=True,verbose_name='category name')
   
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name=models.CharField(max_length=30,verbose_name='product name')
    price=models.IntegerField(default=0,verbose_name='product price')
    description=models.TextField(max_length=300,default='',null=True,blank=True)
    big_description=models.TextField(max_length=1000,default='',null=True,blank=True)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,default=1)
    is_active=models.BooleanField(default=True,verbose_name='Available')
    image=models.ImageField(upload_to='image')

    class Meta:
        db_table='product'
        ordering=['name']

class Cart(models.Model):
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column='uid')
    pid=models.ForeignKey(Product,on_delete=models.CASCADE,db_column='pid')
    qty=models.IntegerField(default=1)
    
class Order(models.Model):
    order_id=models.CharField(max_length=100)
    uid=models.ForeignKey(User,on_delete=models.CASCADE,db_column='uid')
    pid=models.ForeignKey(Product,on_delete=models.CASCADE,db_column='pid')
    qty=models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)