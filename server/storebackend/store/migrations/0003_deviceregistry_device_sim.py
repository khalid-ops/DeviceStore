# Generated by Django 3.2.12 on 2023-07-10 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_rename_sima_brand_simregistry_sim_brand'),
    ]

    operations = [
        migrations.AddField(
            model_name='deviceregistry',
            name='device_sim',
            field=models.IntegerField(default=0),
        ),
    ]