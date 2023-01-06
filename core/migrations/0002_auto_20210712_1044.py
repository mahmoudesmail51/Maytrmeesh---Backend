# Generated by Django 3.2.2 on 2021-07-12 10:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='orderPackage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.order')),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.package')),
            ],
        ),
        migrations.CreateModel(
            name='orderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.item')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.order')),
            ],
                ),
        migrations.RemoveField(
            model_name='order',
            name='items',
        ),
        migrations.AddField(
                model_name='order',
                name='items',
                field=models.ManyToManyField(blank=True, through='core.orderItem', to='core.Item'),
        ),
        migrations.RemoveField(
            model_name='order',
            name='packages',
            
        ),
        migrations.AddField(
            model_name='order',
            name='packages',
            field=models.ManyToManyField(blank=True, through='core.orderPackage', to='core.Package'),
            
        ),
    ]

