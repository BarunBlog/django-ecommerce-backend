# Generated by Django 4.2.2 on 2023-06-13 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name_plural': 'Order'},
        ),
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.CharField(choices=[('pending', 'pending'), ('confirmed', 'confirmed'), ('delivered', 'delivered'), ('canceled', 'canceled')], default='pending', max_length=100),
        ),
    ]
