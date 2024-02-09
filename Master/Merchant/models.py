from django.db import models

# Create your models here.
class Merchant(models.Model):
    name = models.CharField(max_length=100, verbose_name='Name')
    gst_number = models.CharField(max_length=20, unique=True, verbose_name='GST Number')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Merchant'
        verbose_name_plural = 'Merchants'




class Warehouse(models.Model):
    name = models.CharField(max_length=100, verbose_name='Name')
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE, verbose_name='Merchant')
    gst_number = models.CharField(max_length=20, unique=True, verbose_name='GST Number')

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Warehouse'
        verbose_name_plural = 'Warehouses'