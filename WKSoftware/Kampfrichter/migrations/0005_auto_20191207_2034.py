# Generated by Django 2.1.5 on 2019-12-07 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Kampfrichter', '0004_auto_20190106_1448'),
    ]

    operations = [
        migrations.AlterField(
            model_name='run',
            name='age',
            field=models.CharField(default=None, max_length=10),
        ),
    ]
