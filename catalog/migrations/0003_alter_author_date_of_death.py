# Generated by Django 5.1.2 on 2024-10-25 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_language_book_language'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='date_of_death',
            field=models.DateField(blank=True, default='', null=True, verbose_name='Died'),
        ),
    ]
