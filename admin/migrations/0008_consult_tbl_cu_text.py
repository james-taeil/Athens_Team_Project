# Generated by Django 3.1.2 on 2020-11-20 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin', '0007_auto_20201119_1005'),
    ]

    operations = [
        migrations.AddField(
            model_name='consult_tbl',
            name='cu_text',
            field=models.TextField(blank=True, null=True),
        ),
    ]
