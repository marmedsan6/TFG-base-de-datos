# Generated by Django 5.0.2 on 2024-05-03 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plantasapi', '0003_historial_fecha_riego'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historial',
            name='fecha_riego',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
