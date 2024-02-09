from typing import Any
from django import forms
from django.contrib import admin
from django.shortcuts import redirect

from OrderManagement.models import PurchaseOrder, PurchaseOrderSKU, SupplyOrder, SupplyOrderSKU



# Register your models here.



class SKUCatalogueAdmin(admin.ModelAdmin):
    list_display = (
        "sku_name",
        "hsn_code",
        "ean_code",
        "mrp",
        "unit_price",
        "brand_name",
    )
    list_filter = ('brand_name',)

class PurchaseOrderSKUInline(admin.TabularInline):
    model = PurchaseOrderSKU
    extra = 1
    fields = ("purchase_order", "sku_catalogue", "quantity", "cgst", "sgst", "igst")


class PurchaseOrderAdmin(admin.ModelAdmin):
    inlines = [PurchaseOrderSKUInline]
    list_display = ("po_number", "po_date", "get_merchant_name", "warehouse", "total_amount")
    list_filter = ('po_date',)

    def get_merchant_name(self, obj):
        return obj.warehouse.merchant.name
    
    get_merchant_name.short_description = 'Merchant'

    def add_view(self, request, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_add_another'] = False  # Show "Save and add another" button
        extra_context['show_save'] = False  # Hide "Save" button
        return super().add_view(request, form_url, extra_context=extra_context)


    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_add_another'] = False  # Show "Save and add another" button
        extra_context['show_save'] = False  # Hide "Save" button
        return super().change_view(request, object_id, form_url, extra_context=extra_context)
        


class PurchaseOrderSKUAdmin(admin.ModelAdmin):
    fields = ("purchase_order", "sku_catalogue", "quantity", "cgst", "sgst", "igst")
    list_display = (
        "purchase_order",
        "sku_catalogue",
        "quantity",
        "cgst",
        "sgst",
        "igst",
        "unit_price",
        "hsn_code",
        "ean_code",
        "mrp",
        "taxable_value",
        "cgst_value",
        "sgst_value",
        "igst_value",
        "total_amount"
    )
    list_filter = ('purchase_order', 'sku_catalogue')



class SupplyOrderSKUInline(admin.TabularInline):
    model = SupplyOrderSKU
    extra = 1
    fields = ("supply_order", "purchase_order_sku", "status", "quantity", "cgst", "sgst", "igst")

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        field = super(SupplyOrderSKUInline, self).formfield_for_foreignkey(db_field, request, **kwargs)

        if db_field.name == 'purchase_order_sku':
            if request._obj_ is not None:
                purchase_order = SupplyOrder.objects.get(invoice_number=request._obj_).purchase_order
                field.queryset = field.queryset.filter(purchase_order_id = purchase_order)  
            else:
                field.queryset = field.queryset.none()

        return field
    
    def save_model(self, request, obj, form, change):
        obj.save()


# class SupplyOrderForm(forms.ModelForm):
#     # upload_proof_of_delivery = forms.FileField(required=True)



class SupplyOrderAdmin(admin.ModelAdmin):
    # forms = SupplyOrderForm
    inlines = [SupplyOrderSKUInline]

    fieldsets = (
        (None, {
            "fields": (
                "purchase_order",
                "supply_date",
                "status",
                "invoice_number",
                "courier_partner",
                "courier_poc",
                "tracking_id",
                "proof_of_delivery",
            ),
        }),
    )
    
    list_display = (
        "purchase_order",
        "supply_date",
        "status",
        "invoice_number",
        "courier_partner",
        "courier_poc",
        "tracking_id",
        "proof_of_delivery",
    )
    list_filter=('supply_date', 'status')

    def get_form(self, request, obj=None, **kwargs):
        # just save obj reference for future processing in Inline
        request._obj_ = obj
        return super(SupplyOrderAdmin, self).get_form(request, obj, **kwargs)

    def add_view(self, request, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_add_another'] = False  # Show "Save and add another" button
        extra_context['show_save'] = False  # Hide "Save" button
        return super().add_view(request, form_url, extra_context=extra_context)


    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_add_another'] = False  # Show "Save and add another" button
        extra_context['show_save'] = False  # Hide "Save" button
        return super().change_view(request, object_id, form_url, extra_context=extra_context)


class SupplyOrderSKUAdmin(admin.ModelAdmin):
    fields = ("supply_order", "purchase_order_sku", "status", "quantity", "cgst", "sgst", "igst")
    list_display = (
        "supply_order",
        "purchase_order_sku",
        "status",
        "quantity",
        "cgst",
        "sgst",
        "igst",
        "unit_price",
        "hsn_code",
        "ean_code",
        "mrp",
        "taxable_value",
        "cgst_value",
        "sgst_value",
        "igst_value",
        "total_amount"
    )
    list_filter =('supply_order', 'purchase_order_sku', 'status')



admin.site.register(PurchaseOrder, PurchaseOrderAdmin)
admin.site.register(PurchaseOrderSKU, PurchaseOrderSKUAdmin)
admin.site.register(SupplyOrder, SupplyOrderAdmin)
admin.site.register(SupplyOrderSKU, SupplyOrderSKUAdmin)
