# Generated by Django 5.0.2 on 2024-05-16 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plantasapi', '0006_alter_plantinfo_common_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plantinfo',
            name='image_url',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
