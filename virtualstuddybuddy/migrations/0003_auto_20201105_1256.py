# Generated by Django 3.1.1 on 2020-11-05 17:56

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('virtualstuddybuddy', '0002_auto_20201020_2353'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='classOf',
            field=models.CharField(default='Class of X', max_length=2000, validators=[django.core.validators.MinLengthValidator(1), django.core.validators.MaxLengthValidator(2000)]),
        ),
        migrations.AddField(
            model_name='profile',
            name='coursework',
            field=models.CharField(default='Coursework X', max_length=2000, validators=[django.core.validators.MinLengthValidator(1), django.core.validators.MaxLengthValidator(2000)]),
        ),
        migrations.AlterField(
            model_name='profile',
            name='age',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='profile',
            name='description',
            field=models.CharField(default='Description X', max_length=2000, validators=[django.core.validators.MinLengthValidator(1), django.core.validators.MaxLengthValidator(2000)]),
        ),
        migrations.AlterField(
            model_name='profile',
            name='gender',
            field=models.CharField(default='Gender X', max_length=200, validators=[django.core.validators.MinLengthValidator(1), django.core.validators.MaxLengthValidator(200)]),
        ),
        migrations.AlterField(
            model_name='profile',
            name='major',
            field=models.CharField(default='Major X', max_length=200, validators=[django.core.validators.MinLengthValidator(1), django.core.validators.MaxLengthValidator(200)]),
        ),
        migrations.AlterField(
            model_name='profile',
            name='name',
            field=models.CharField(default='Name X', max_length=50, validators=[django.core.validators.MinLengthValidator(1), django.core.validators.MaxLengthValidator(50)]),
        ),
        migrations.AlterField(
            model_name='profile',
            name='picture',
            field=models.ImageField(upload_to='uploads/', validators=[django.core.validators.validate_image_file_extension]),
        ),
    ]
