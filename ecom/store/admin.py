from django.contrib import admin
from .models import *


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'ordered']


admin.site.register(Product)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct)
admin.site.register(Payment)
