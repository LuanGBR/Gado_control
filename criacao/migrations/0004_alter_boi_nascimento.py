# Generated by Django 3.2.9 on 2021-12-09 20:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('criacao', '0003_auto_20211209_1723'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boi',
            name='nascimento',
            field=models.DateField(null=True),
        ),
    ]
