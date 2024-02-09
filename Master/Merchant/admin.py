from django.contrib import admin

from Merchant.models import Merchant, Warehouse


# Register your models here.
class MerchantAdmin(admin.ModelAdmin):
    list_display = ("name", "gst_number")


class WarehouseAdmin(admin.ModelAdmin):
    list_display = ("name", "gst_number", "merchant")


admin.site.register(Merchant, MerchantAdmin)
admin.site.register(Warehouse, WarehouseAdmin)
