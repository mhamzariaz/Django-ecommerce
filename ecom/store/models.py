from django.db import models
from django.conf import settings
from django.urls import reverse


class Product(models.Model):

    retailer_sku = models.CharField(max_length=200)
    category = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    care = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    brand = models.CharField(max_length=200)
    market = models.CharField(max_length=200)
    retailer = models.CharField(max_length=200)
    gender = models.CharField(max_length=200)
    image_urls = models.CharField(max_length=200)
    price = models.FloatField()
    discount_price = models.FloatField()
    slug = models.SlugField()

    def __str__(self):
        return self.name

    def get_add_to_cart(self):
        return reverse('add-to-cart', kwargs={
            'slug': self.slug
        })

    def remove_from_cart(self):
        return reverse('remove-from-cart', kwargs={
            'slug': self.slug
        })


class OrderProduct(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

    def get_total_item_price(self):
        return self.quantity * self.product.price


class Order(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    products = models.ManyToManyField(OrderProduct)
    billing_address = models.ForeignKey('BillingAddress', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        for order_item in self.products.all():
            total += order_item.get_total_item_price()
        return total


class BillingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address1 = models.CharField(max_length=200)
    address2 = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    zip_code = models.CharField(max_length=200)

    def __str__(self):
        return self.user.username


class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()

    def __str__(self):
        return self.user.username
