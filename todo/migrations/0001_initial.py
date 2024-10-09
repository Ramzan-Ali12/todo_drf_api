# Generated by Django 5.1.1 on 2024-10-01 19:34

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Todo",
            fields=[
                (
                    "uuid",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("title", models.CharField(db_index=True, max_length=100)),
                ("description", models.TextField()),
                ("completed", models.BooleanField(db_index=True, default=False)),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
    ]
