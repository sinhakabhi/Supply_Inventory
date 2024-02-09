from django.contrib import admin

from Inventory.models import Brand, SKUCatalogue

# Register your models here.
class SKUCatalogueAdmin(admin.ModelAdmin):
    list_display = (
        "sku_name",
        "hsn_code",
        "ean_code",
        "mrp",
        "unit_price",
        "brand",
    )

class BrandAdmin(admin.ModelAdmin):
    pass


admin.site.register(SKUCatalogue, SKUCatalogueAdmin)
admin.site.register(Brand, BrandAdmin)