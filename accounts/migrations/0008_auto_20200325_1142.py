# Generated by Django 2.2 on 2020-03-25 06:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20200323_0043'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extendeduser',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='extendedUser', to=settings.AUTH_USER_MODEL),
        ),
    ]