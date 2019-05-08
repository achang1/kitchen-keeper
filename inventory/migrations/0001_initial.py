# Generated by Django 2.2.1 on 2019-05-08 07:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('is_perishable', models.BooleanField(default=True, verbose_name='perishable food')),
            ],
        ),
        migrations.CreateModel(
            name='Fridge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('quantity', models.IntegerField(default=0, verbose_name='quantity')),
                ('purchase_date', models.DateTimeField(verbose_name='date purchased')),
                ('expiry_date', models.DateTimeField(verbose_name='expiry date')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.Category')),
                ('fridge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inventory.Fridge')),
            ],
        ),
    ]
