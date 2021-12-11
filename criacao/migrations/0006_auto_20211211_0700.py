# Generated by Django 3.2.9 on 2021-12-11 10:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('criacao', '0005_auto_20211209_1728'),
    ]

    operations = [
        migrations.AddField(
            model_name='boi',
            name='causa_mortis',
            field=models.TextField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='boi',
            name='esta_vivo',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='boi',
            name='morte',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='cabecagado',
            name='author',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='auth.user'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cria',
            name='causa_mortis',
            field=models.TextField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='cria',
            name='esta_vivo',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='cria',
            name='morte',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='matriz',
            name='causa_mortis',
            field=models.TextField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='matriz',
            name='esta_vivo',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='matriz',
            name='morte',
            field=models.DateField(null=True),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cargo', models.CharField(max_length=16)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='perfil', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
