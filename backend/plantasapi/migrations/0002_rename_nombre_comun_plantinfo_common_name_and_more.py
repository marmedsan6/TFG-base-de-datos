# Generated by Django 5.0.2 on 2024-05-12 11:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plantasapi', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='plantinfo',
            old_name='nombre_comun',
            new_name='common_name',
        ),
        migrations.RenameField(
            model_name='plantinfo',
            old_name='url_foto',
            new_name='image_url',
        ),
        migrations.RenameField(
            model_name='plantinfo',
            old_name='luz',
            new_name='light',
        ),
        migrations.RenameField(
            model_name='plantinfo',
            old_name='ph_maximo',
            new_name='ph_maximum',
        ),
        migrations.RenameField(
            model_name='plantinfo',
            old_name='ph_minimo',
            new_name='ph_minimum',
        ),
        migrations.RenameField(
            model_name='plantinfo',
            old_name='nombre_cientifico',
            new_name='scientific_name',
        ),
    ]