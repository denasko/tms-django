# Generated by Django 5.0 on 2024-02-11 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_alter_profile_shopping_cart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderentry',
            name='count',
            field=models.IntegerField(default=1),
        ),
    ]
