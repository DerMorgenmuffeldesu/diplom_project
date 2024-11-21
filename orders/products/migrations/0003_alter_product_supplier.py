# Generated by Django 5.1.3 on 2024-11-21 12:13

import django.db.models.deletion
import products.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_product_description_product_stock_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='supplier',
            field=models.ForeignKey(default=products.models.Product.get_default_supplier, on_delete=django.db.models.deletion.SET_DEFAULT, to='products.supplier'),
        ),
    ]