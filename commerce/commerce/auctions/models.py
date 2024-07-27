from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name
    
class Bid(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, blank = True, null = True, related_name = "bid_user")
    value = models.FloatField(default=0)

    def __str__(self):
        return f"({self.value})"
    
class Listing(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=500)
    image = models.CharField(max_length=1000)
    price = models.ForeignKey(Bid,on_delete = models.CASCADE, blank = True, null = True, related_name = "bid_price")
    isActive = models.BooleanField(default = True)
    owner = models.ForeignKey(User, on_delete = models.CASCADE, blank = True, null = True, related_name = "user")
    category = models.ForeignKey(Category, on_delete = models.CASCADE, blank = True, null = True, related_name = "category")
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="watchlist")

    def __str__(self):
        return self.title



class Comments(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE, blank = True, null = True, related_name = "comment_user")
    listing = models.ForeignKey(Listing, on_delete = models.CASCADE, blank = True, null = True, related_name = "comment_listing")
    text = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.user} comment on {self.listing}"