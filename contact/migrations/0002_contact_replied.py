# Generated by Django 4.2.3 on 2023-08-23 13:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("contact", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="contact",
            name="replied",
            field=models.BooleanField(default=False),
        ),
    ]