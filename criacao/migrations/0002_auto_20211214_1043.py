# Generated by Django 3.2.7 on 2021-12-14 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('criacao', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ficha_medica',
            name='pesos_timeseries',
            field=models.CharField(default='', max_length=2048, null=True),
        ),
        migrations.AlterField(
            model_name='transacao',
            name='tipo',
            field=models.CharField(choices=[('Compra', 'Compra'), ('Venda', 'Venda')], max_length=6),
        ),
    ]
