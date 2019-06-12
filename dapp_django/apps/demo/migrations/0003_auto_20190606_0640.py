# Generated by Django 2.2.1 on 2019-06-06 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0002_auto_20190601_0616'),
    ]

    operations = [
        migrations.AddField(
            model_name='hepprofilemodel',
            name='address',
            field=models.CharField(default='', max_length=42),
        ),
        migrations.AddField(
            model_name='hepprofilemodel',
            name='avatar',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AddField(
            model_name='hepprofilemodel',
            name='country_code',
            field=models.CharField(default='', max_length=10),
        ),
        migrations.AddField(
            model_name='hepprofilemodel',
            name='invite_code',
            field=models.CharField(default='', max_length=10),
        ),
        migrations.AddField(
            model_name='hepprofilemodel',
            name='sign_type',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AddField(
            model_name='hepprofilemodel',
            name='signature',
            field=models.CharField(default='', max_length=500),
        ),
        migrations.AlterField(
            model_name='hepprofilemodel',
            name='cellphone',
            field=models.CharField(default='', max_length=128),
        ),
        migrations.AlterField(
            model_name='hepprofilemodel',
            name='name',
            field=models.CharField(default='', max_length=128),
        ),
        migrations.AlterField(
            model_name='hepprofilemodel',
            name='newid',
            field=models.CharField(default='', max_length=128),
        ),
    ]
