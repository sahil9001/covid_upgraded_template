# Generated by Django 2.2 on 2020-03-22 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='extendeduser',
            name='last_fetched',
            field=models.DateTimeField(null=True),
        ),
    ]