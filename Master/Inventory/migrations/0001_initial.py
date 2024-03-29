# Generated by Django 5.0.2 on 2024-02-09 10:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Brand',
                'verbose_name_plural': 'Brands',
            },
        ),
        migrations.CreateModel(
            name='SKUCatalogue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sku_name', models.CharField(max_length=100, verbose_name='SKU Name')),
                ('hsn_code', models.CharField(max_length=10, unique=True, verbose_name='HSN Code')),
                ('ean_code', models.CharField(max_length=20, unique=True, verbose_name='EAN Code')),
                ('mrp', models.DecimalField(decimal_places=2, max_digits=7, verbose_name='MRP')),
                ('unit_price', models.DecimalField(decimal_places=2, max_digits=7, verbose_name='Unit Price')),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Inventory.brand', verbose_name='Brand')),
            ],
            options={
                'verbose_name': 'SKU Catalogue',
                'verbose_name_plural': 'SKU Catalogues',
            },
        ),
    ]
