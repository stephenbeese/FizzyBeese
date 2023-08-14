# Generated by Django 4.2.3 on 2023-08-14 09:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("checkout", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="county",
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name="order",
            name="country",
            field=models.CharField(default="United Kingdom", max_length=40),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="order",
            name="postcode",
            field=models.CharField(max_length=20),
        ),
    ]
