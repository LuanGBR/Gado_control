# Generated by Django 3.2.7 on 2021-12-15 20:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('criacao', '0002_auto_20211214_1043'),
    ]

    operations = [
        migrations.AddField(
            model_name='transacao',
            name='gados',
            field=models.TextField(blank=True, max_length=1000),
        ),
    ]
