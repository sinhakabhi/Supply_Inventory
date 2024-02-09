from django.db import models

# Create your models here.


class Brand(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Brand"
        verbose_name_plural = "Brands"


class SKUCatalogue(models.Model):
    sku_name = models.CharField(max_length=100, verbose_name="SKU Name")
    hsn_code = models.CharField(max_length=10, verbose_name="HSN Code")
    ean_code = models.CharField(max_length=20, verbose_name="EAN Code")
    mrp = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="MRP")
    unit_price = models.DecimalField(
        max_digits=7, decimal_places=2, verbose_name="Unit Price"
    )
    brand = models.ForeignKey(Brand, verbose_name="Brand", on_delete=models.CASCADE)

    def __str__(self):
        return self.sku_name

    class Meta:
        verbose_name = "SKU Catalogue"
        verbose_name_plural = "SKU Catalogues"
