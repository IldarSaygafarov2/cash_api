# Generated by Django 4.2.6 on 2023-10-26 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_category_icon'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='type',
            field=models.CharField(blank=True, default='expense', max_length=15, null=True, verbose_name='Тип'),
        ),
        migrations.AddField(
            model_name='income',
            name='type',
            field=models.CharField(blank=True, default='income', max_length=15, null=True, verbose_name='Тип'),
        ),
    ]
