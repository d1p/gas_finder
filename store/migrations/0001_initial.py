# Generated by Django 2.1.7 on 2019-03-15 16:07

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import store.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
                ('name_in_ar', models.CharField(max_length=128, unique=True)),
                ('welcome_message_in_english', models.CharField(blank=True, max_length=120, null=True)),
                ('welcome_message_in_arabic', models.CharField(blank=True, max_length=120, null=True)),
                ('name_in_google', models.CharField(blank=True, help_text='City name from google API.', max_length=220, null=True, unique=True)),
                ('cover_picture', models.ImageField(blank=True, null=True, upload_to=store.models.RandomFileName('city/cover/'))),
                ('lat', models.FloatField()),
                ('lng', models.FloatField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'City',
                'verbose_name_plural': 'Cities',
            },
        ),
        migrations.CreateModel(
            name='Config',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(db_index=True, max_length=120, unique=True)),
                ('value', models.CharField(max_length=120)),
            ],
            options={
                'verbose_name': 'Default Text',
                'verbose_name_plural': 'Default Texts',
            },
        ),
        migrations.CreateModel(
            name='DefaultImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(db_index=True, max_length=120, unique=True)),
                ('value', models.ImageField(upload_to=store.models.RandomFileName('city/cover/'))),
            ],
        ),
        migrations.CreateModel(
            name='PhotoGallery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.ImageField(upload_to=store.models.RandomFileName('store/photo/'))),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('rating', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(1)])),
                ('comment', models.TextField(max_length=10000)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('approved', models.BooleanField(db_index=True, default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('distributor_name', models.CharField(help_text='Distributor name in English', max_length=250)),
                ('distributor_name_in_ar', models.CharField(help_text='Distributor name in Arabic', max_length=250)),
                ('cover_photo', models.ImageField(blank=True, null=True, upload_to=store.models.RandomFileName('store/cover/'))),
                ('phone_number', models.CharField(max_length=15)),
                ('address_in_en', models.TextField(max_length=1000, verbose_name='Address in English')),
                ('address_in_ar', models.TextField(max_length=1000, verbose_name='Address in Arabic')),
                ('lat', models.FloatField()),
                ('lng', models.FloatField()),
                ('city', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.City')),
            ],
        ),
        migrations.CreateModel(
            name='VisitorCity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=200, unique=True)),
                ('visitors', models.BigIntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='review',
            name='store',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.Store'),
        ),
        migrations.AddField(
            model_name='photogallery',
            name='store',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='store.Store'),
        ),
    ]
