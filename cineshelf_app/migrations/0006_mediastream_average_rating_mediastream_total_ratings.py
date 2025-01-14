# Generated by Django 5.1.4 on 2025-01-14 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cineshelf_app", "0005_review_reviewer"),
    ]

    operations = [
        migrations.AddField(
            model_name="mediastream",
            name="average_rating",
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name="mediastream",
            name="total_ratings",
            field=models.IntegerField(default=0),
        ),
    ]
