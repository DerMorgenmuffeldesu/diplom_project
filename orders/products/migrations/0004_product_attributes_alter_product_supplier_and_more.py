# Generated by Django 5.1.3 on 2024-11-26 05:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_supplier_contact_info_alter_product_stock_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='attributes',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='supplier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='products.supplier'),
        ),
        migrations.AlterField(
            model_name='productattribute',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_attributes', to='products.product'),
        ),
    ]