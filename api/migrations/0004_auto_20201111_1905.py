# Generated by Django 3.1.1 on 2020-11-11 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20201111_1816'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan',
            name='title',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]