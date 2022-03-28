# Generated by Django 3.1.4 on 2021-07-23 19:35

import book.models
from django.db import migrations, models
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('stores', '__first__'),
        ('users', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300, null=True)),
                ('price', models.FloatField(null=True)),
                ('code', models.IntegerField(null=True, unique=True)),
                ('image', models.ImageField(null=True, upload_to=book.models.rename_image)),
                ('description', models.TextField(max_length=400, null=True)),
                ('slug_book', models.SlugField(blank=True, null=True)),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='stores.category')),
                ('subcategory', smart_selects.db_fields.ChainedForeignKey(blank=True, chained_field='category', chained_model_field='category', null=True, on_delete=django.db.models.deletion.CASCADE, to='stores.subcategory')),
            ],
        ),
        migrations.CreateModel(
            name='DiscountForBook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discountrate', models.FloatField(blank=True, null=True)),
                ('discountforbook', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='book.book')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('totalprice', models.FloatField(blank=True, null=True)),
                ('discount', models.FloatField(blank=True, null=True)),
                ('Book', models.ManyToManyField(blank=True, to='book.Book')),
                ('discountbookfororder', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='book.discountforbook')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='users.myuser')),
            ],
        ),
    ]
