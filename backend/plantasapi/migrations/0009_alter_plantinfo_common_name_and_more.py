# Generated by Django 5.0.2 on 2024-05-16 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plantasapi', '0008_alter_plantinfo_common_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plantinfo',
            name='common_name',
            field=models.CharField(default='Desconocido', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='plantinfo',
            name='image_url',
            field=models.CharField(default='https://upload.wikimedia.org/wikipedia/commons/a/a3/Image-not-found.png', max_length=255, null=True),
        ),
    ]