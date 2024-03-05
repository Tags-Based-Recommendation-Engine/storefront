from django.db import models
from storefront.models import Seller, Listing, User

class CartItem(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Listing, on_delete=models.CASCADE)



class Review(models.Model):
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, related_name='reviews', on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(null=False, blank=False, default=2.5)
    title = models.CharField(max_length=100)
    text = models.TextField()

    def __str__(self):
        return f"{self.listing} {self.reviewer}"






# Create your models here.
