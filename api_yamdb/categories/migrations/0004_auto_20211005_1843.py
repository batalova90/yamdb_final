# Generated by Django 2.2.16 on 2021-10-05 18:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0003_auto_20211005_1304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='titles',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='categories', to='categories.Categories'),
        ),
    ]
