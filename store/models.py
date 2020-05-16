from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=225, null=True)
    email = models.CharField(max_length=224, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    SEX = (
        ('MALE', 'MALE'),
        ('FEMALE', 'FEMALE'),
        ('UNISEX', 'UNISEX')
    )
    name = models.CharField(max_length=255)
    price = models.FloatField()
    digital = models.BooleanField(default=False, null=True, blank=False)
    image = models.ImageField(null=True, blank=True)
    imageF = models.ImageField(null=True, blank=True)
    imageS = models.ImageField(null=True, blank=True)
    imageT = models.ImageField(null=True, blank=True)
    sex_for = models.CharField(max_length=225, choices=SEX, blank=True, null=True)
    description = models.TextField(max_length=100000, null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = '.'
        return url


    @property
    def imageSURL(self):
        try:
            url = self.imageS.url
        except:
            url = '.'
        return url

    @property
    def imageTURL(self):
        try:
            url = self.imageT.url
        except:
            url = '.'
        return url

    @property
    def imageFtURL(self):
        try:
            url = self.imageFt.url
        except:
            url = '.'
        return url


# class prodImage(models.Model):
#     product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
#     imageF = models.ImageField(null=True, blank=True)
#     imageS = models.ImageField(null=True, blank=True)
#     imageT = models.ImageField(null=True, blank=True)
#     imageFt = models.ImageField(null=True, blank=True)
#
#     def __str__(self):
#         return self.product.name


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=True)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if not i.product.digital:
                shipping = True
        return shipping


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=255, null=False)
    city = models.CharField(max_length=225, null=False)
    state = models.CharField(max_length=225, null=False)
    zipcode = models.CharField(max_length=225, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
