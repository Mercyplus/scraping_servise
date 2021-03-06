# Generated by Django 3.1.3 on 2021-01-26 14:46

from django.db import migrations, models
import scraping.models


class Migration(migrations.Migration):

    dependencies = [
        ('scraping', '0002_url'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='vacancy',
            options={'ordering': ['-timestamp'], 'verbose_name': 'Вакансия', 'verbose_name_plural': 'Вакансии'},
        ),
        migrations.AlterField(
            model_name='url',
            name='url_data',
            field=models.JSONField(default=scraping.models.default_urls),
        ),
    ]
