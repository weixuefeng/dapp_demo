# Generated by Django 2.2.1 on 2019-06-06 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demo', '0003_auto_20190606_0640'),
    ]

    operations = [
        migrations.CreateModel(
            name='PayModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.CharField(db_index=True, max_length=128)),
                ('txid', models.CharField(db_index=True, max_length=128)),
            ],
        ),
    ]
