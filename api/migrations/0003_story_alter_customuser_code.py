# Generated by Django 4.2.6 on 2023-10-21 21:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0002_customuser_code"),
    ]

    operations = [
        migrations.CreateModel(
            name="Story",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        blank=True, max_length=155, null=True, verbose_name="Название"
                    ),
                ),
                (
                    "img",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="photos/stories/",
                        verbose_name="Фото",
                    ),
                ),
            ],
            options={
                "verbose_name": "История",
                "verbose_name_plural": "Истории",
            },
        ),
        migrations.AlterField(
            model_name="customuser",
            name="code",
            field=models.CharField(
                blank=True,
                default="",
                max_length=6,
                null=True,
                verbose_name="Код авторизации",
            ),
        ),
    ]
