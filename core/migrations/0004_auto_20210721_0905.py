# Generated by Django 3.2.5 on 2021-07-21 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20210720_1345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foodvenue',
            name='image',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='package',
            name='image',
            field=models.TextField(blank=True),
        ),
    ]
