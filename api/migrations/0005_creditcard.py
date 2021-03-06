# Generated by Django 3.1.1 on 2020-11-11 16:26

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_auto_20201111_1905'),
    ]

    operations = [
        migrations.CreateModel(
            name='CreditCard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(max_length=200)),
                ('number', models.CharField(max_length=16, validators=[django.core.validators.RegexValidator('(?:[0-9]{4}){3}[0-9]{4}|[0-9]{16}')])),
                ('name_on_card', models.CharField(max_length=200)),
                ('expiry_date', models.DateField()),
                ('cvv', models.CharField(max_length=3, validators=[django.core.validators.RegexValidator('^[0-9]{3}$')])),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
