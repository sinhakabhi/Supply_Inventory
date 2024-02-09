from django.db import models

from Inventory.models import SKUCatalogue
from Merchant.models import Warehouse


# Create your models here.
class PurchaseOrder(models.Model):
    warehouse = models.ForeignKey(
        Warehouse, on_delete=models.CASCADE, verbose_name="Warehouse"
    )
    po_date = models.DateField(verbose_name="PO Date")
    po_number = models.CharField(max_length=20, unique=True, verbose_name="PO Number")
    total_amount = models.DecimalField(
        max_digits=7, decimal_places=2, verbose_name="Total Amount"
    )

    def __str__(self):
        return self.po_number

    class Meta:
        verbose_name = "Purchase Order"
        verbose_name_plural = "Purchase Orders"


class PurchaseOrderSKU(models.Model):
    purchase_order = models.ForeignKey(
        PurchaseOrder, on_delete=models.CASCADE, verbose_name="Purchase Order"
    )
    sku_catalogue = models.ForeignKey(
        SKUCatalogue, on_delete=models.CASCADE, verbose_name="SKU Catalogue"
    )
    quantity = models.IntegerField(verbose_name="Quantity")
    cgst = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="CGST(%)")
    sgst = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="SGST(%)")
    igst = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="IGST(%)")
    unit_price = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True, verbose_name="Unit Price"
    )
    total_amount = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Total Amount",
    )
    hsn_code = models.CharField(
        max_length=10, null=True, blank=True, verbose_name="HSN Code"
    )
    ean_code = models.CharField(
        max_length=20, null=True, blank=True, verbose_name="EAN Code"
    )
    mrp = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True, verbose_name="MRP"
    )
    taxable_value = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Taxable Value",
    )
    cgst_value = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True, verbose_name="CGST Value"
    )
    sgst_value = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True, verbose_name="SGST Value"
    )
    igst_value = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True, verbose_name="IGST Value"
    )

    def __str__(self):
        return self.sku_catalogue.sku_name

    class Meta:
        verbose_name = "Purchase Order SKU"
        verbose_name_plural = "Purchase Order SKUs"
        unique_together = (
            "sku_catalogue",
            "purchase_order",
        )

    def save(self, force_insert: bool = True, force_update: bool = False):

        sku_catalogue_instance = SKUCatalogue.objects.get(sku_name=self.sku_catalogue)
        purchase_order_instance = PurchaseOrder.objects.get(
            po_number=self.purchase_order
        )
        self.unit_price = sku_catalogue_instance.unit_price
        self.total_amount = purchase_order_instance.total_amount
        self.hsn_code = sku_catalogue_instance.hsn_code
        self.ean_code = sku_catalogue_instance.ean_code
        self.mrp = sku_catalogue_instance.mrp
        self.taxable_value = sku_catalogue_instance.unit_price * self.quantity
        self.cgst_value = (self.cgst / 100) * self.taxable_value
        self.sgst_value = (self.sgst / 100) * self.taxable_value
        self.igst_value = (self.igst / 100) * self.taxable_value
        self.total_amount = self.taxable_value + self.cgst_value + self.sgst_value + self.igst_value
        return super().save(force_insert, force_update)


def pod_directory_path(instance, filename):

    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return "user_{0}/{1}".format(instance.purchase_order.id, filename)


class SupplyOrder(models.Model):
    STATUS_CHOICES = (("abc", "abc"),)
    PARTNER_CHOICES = (("def", "def"),)
    purchase_order = models.OneToOneField(
        PurchaseOrder,
        on_delete=models.CASCADE,
        unique=True,
        verbose_name="Purchase Order",
    )
    supply_date = models.DateField(verbose_name="Supply Date")
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, verbose_name="Status"
    )
    invoice_number = models.CharField(
        max_length=20, unique=True, verbose_name="Invoice Number"
    )
    courier_partner = models.CharField(
        max_length=20, choices=PARTNER_CHOICES, verbose_name="Courier Partner"
    )
    courier_poc = models.CharField(max_length=100, verbose_name="Courier POC")
    tracking_id = models.CharField(max_length=50, verbose_name="Tracking ID")
    proof_of_delivery = models.FileField(
        upload_to=pod_directory_path, max_length=100, verbose_name="Proof Of Delivery"
    )

    def __str__(self):
        return self.invoice_number

    class Meta:
        verbose_name = "Supply Order"
        verbose_name_plural = "Supply Orders"


class SupplyOrderSKU(models.Model):
    STATUS_CHOICES = (("xyz", "xyz"),)
    supply_order = models.ForeignKey(
        SupplyOrder, on_delete=models.CASCADE, verbose_name="Supply Order"
    )
    purchase_order_sku = models.ForeignKey(
        PurchaseOrderSKU, on_delete=models.CASCADE, verbose_name="Purchase Order SKU"
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, verbose_name="Status"
    )
    quantity = models.IntegerField(verbose_name="Quantity")
    cgst = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="CGST(%)")
    sgst = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="SGST(%)")
    igst = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="IGST(%)")
    unit_price = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True, verbose_name="Unit Price"
    )
    total_amount = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Total Amount",
    )
    hsn_code = models.CharField(
        max_length=10, null=True, blank=True, verbose_name="HSN Code"
    )
    ean_code = models.CharField(
        max_length=20, null=True, blank=True, verbose_name="EAN Code"
    )
    mrp = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True, verbose_name="MRP"
    )
    taxable_value = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Taxable Value",
    )
    cgst_value = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True, verbose_name="CGST Value"
    )
    sgst_value = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True, verbose_name="SGST Value"
    )
    igst_value = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True, verbose_name="IGST Value"
    )

    class Meta:
        verbose_name = "Supply Order SKU"
        verbose_name_plural = "Supply Order SKUs"
        unique_together = ("supply_order", "purchase_order_sku")

    def save(self, force_insert: bool = True, force_update: bool = False):
        sku_catalogue_instance = SKUCatalogue.objects.get(
            sku_name=self.purchase_order_sku
        )
        purchase_order_sku_instance = PurchaseOrderSKU.objects.get(
            sku_catalogue=sku_catalogue_instance.id
        )
        purchase_order_instance = PurchaseOrder.objects.get(
            po_number=purchase_order_sku_instance.purchase_order
        )
        self.unit_price = sku_catalogue_instance.unit_price
        self.total_amount = purchase_order_instance.total_amount
        self.hsn_code = sku_catalogue_instance.hsn_code
        self.ean_code = sku_catalogue_instance.ean_code
        self.mrp = sku_catalogue_instance.mrp
        self.taxable_value = sku_catalogue_instance.unit_price * self.quantity
        self.cgst_value = (self.cgst / 100) * self.taxable_value
        self.sgst_value = (self.sgst / 100) * self.taxable_value
        self.igst_value = (self.igst / 100) * self.taxable_value
        self.total_amount = self.taxable_value + self.cgst_value + self.sgst_value + self.igst_value

        return super().save(force_insert, force_update)
