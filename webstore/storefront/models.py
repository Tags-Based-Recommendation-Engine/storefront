from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):
    username = models.CharField(max_length=100, unique=True, null=True)
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    email = models.EmailField(null=True, unique=True)
    phone = models.CharField(max_length=10, null=True, blank=True)
    pfp = models.ImageField(upload_to=f'pfps/', default='user.png')


    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username']

    def  __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    store_name = models.CharField(max_length=256)
    desc = models.TextField(blank=True)
    trust_score =  models.FloatField(default=50.0)
    slug = models.SlugField(default="", null=False)

    def __str__(self):
        return f"{self.email} {self.store_name}"
    

class Product(models.Model):
    product_name =  models.CharField(max_length=256)
    brand_name = models.CharField(max_length=256)
    specs = models.TextField(help_text="Product specifications")
    desc = models.TextField()
    
    def __str__(self):
        return f"{self.listing.seller.store_name} {self.product_name}"

class Image(models.Model):
    img = models.ImageField(upload_to='products/', default='no-default')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    
class Listing(models.Model):
    inventory = models.IntegerField(default=0)
    min_price = models.DecimalField(max_digits=7, decimal_places=2)
    max_price = models.DecimalField(max_digits=7, decimal_places=2)
    strategy = models.FloatField(default=0.0)
    slug = models.SlugField(default="", null=False)



    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
# Create your models here.
