# Generated by Django 3.1.4 on 2020-12-15 11:12

import branch.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название Отрасли')),
                ('image', models.ImageField(upload_to='branch')),
                ('slug', models.SlugField(blank=True, max_length=250, null=True, unique=True)),
            ],
            options={
                'verbose_name': 'Отрасль',
                'verbose_name_plural': 'Отрасли',
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Краткое название компании')),
                ('logo', models.ImageField(null=True, upload_to='company', verbose_name='Логотип')),
                ('slug', models.SlugField(max_length=250, unique=True)),
                ('full_name', models.CharField(max_length=100, verbose_name='Полное название компании')),
                ('description', models.TextField(verbose_name='Описание')),
                ('branch', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='branch.branch', verbose_name='Отрасль')),
            ],
            options={
                'verbose_name': 'Организация',
                'verbose_name_plural': 'Организации',
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500, verbose_name='Название продукта')),
                ('price', models.CharField(default=0, max_length=500, verbose_name='Цена')),
                ('description', models.TextField(verbose_name='Описание продукта')),
                ('organisation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='branch.company', verbose_name='Производитель')),
            ],
            options={
                'verbose_name': 'Продукт',
                'verbose_name_plural': 'Продукция',
            },
        ),
        migrations.CreateModel(
            name='ProductPhoto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=branch.models.get_path_upload_image, verbose_name='Фото продукции')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='branch.product', verbose_name='Продукция')),
            ],
            options={
                'verbose_name': 'Фотографии к продукции',
                'verbose_name_plural': 'Фотографии к продукции',
            },
        ),
    ]
