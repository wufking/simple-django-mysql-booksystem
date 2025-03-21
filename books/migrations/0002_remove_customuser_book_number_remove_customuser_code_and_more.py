# Generated by Django 5.1.6 on 2025-02-21 13:32

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='book_number',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='code',
        ),
        migrations.AddField(
            model_name='customuser',
            name='borrowed_books_count',
            field=models.PositiveIntegerField(default=0, verbose_name='已借阅数量'),
        ),
        migrations.AddField(
            model_name='customuser',
            name='id_card',
            field=models.CharField(blank=True, max_length=18, null=True, unique=True, validators=[django.core.validators.MinLengthValidator(18)], verbose_name='身份证号'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='address',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='地址'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='tel',
            field=models.CharField(max_length=20, primary_key=True, serialize=False, unique=True, validators=[django.core.validators.MinLengthValidator(11)], verbose_name='手机号'),
        ),
    ]
