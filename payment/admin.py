from django.contrib import admin

from .models import Payment,PaymentOrder,PaymentVendor

admin.site.register(Payment)
admin.site.register(PaymentOrder)
admin.site.register(PaymentVendor)

