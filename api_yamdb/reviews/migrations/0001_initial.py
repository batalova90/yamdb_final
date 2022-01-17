# Generated by Django 2.2.16 on 2021-10-08 17:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

# Generated by Django 2.2.16 on 2021-10-07 08:43



class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('categories', '0004_auto_20211005_1843'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('score', models.IntegerField(verbose_name='Score')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Publication date')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL, verbose_name='Author')),
                ('title', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='categories.Titles', verbose_name='Titles')),
            ],
            options={
                'verbose_name': 'Review',
                'verbose_name_plural': 'Reviews',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(verbose_name='Text')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Publication date')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL, verbose_name='Author')),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='reviews.Review', verbose_name='Review')),
            ],
            options={
                'verbose_name': 'Comment',
                'verbose_name_plural': 'Comments',
            },
        ),
        migrations.AddConstraint(
            model_name='review',
            constraint=models.UniqueConstraint(fields=('author', 'title'), name='unique review'),
        ),
    ]