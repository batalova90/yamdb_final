# Generated by Django 2.2.16 on 2021-10-09 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0007_auto_20211008_1738'),
    ]

    operations = [
        migrations.AddField(
            model_name='titles',
            name='rating',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
