# Generated by Django 5.0.2 on 2024-05-12 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plantasapi', '0002_rename_nombre_comun_plantinfo_common_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plantinfo',
            name='id',
            field=models.BigAutoField(editable=False, primary_key=True, serialize=False),
        ),
    ]
