# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-09-17 14:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Consume',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('price', models.PositiveIntegerField()),
                ('quantity', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('date', models.DateTimeField()),
                ('cleared', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Participation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cleared', models.BooleanField(default=False)),
                ('meeting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dutchpay.Meeting')),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('nickname', models.CharField(blank=True, max_length=10)),
                ('note', models.CharField(blank=True, max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('meeting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dutchpay.Meeting')),
            ],
        ),
        migrations.AddField(
            model_name='participation',
            name='person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dutchpay.Person'),
        ),
        migrations.AddField(
            model_name='meeting',
            name='people',
            field=models.ManyToManyField(through='dutchpay.Participation', to='dutchpay.Person'),
        ),
        migrations.AddField(
            model_name='item',
            name='participation',
            field=models.ManyToManyField(through='dutchpay.Consume', to='dutchpay.Participation'),
        ),
        migrations.AddField(
            model_name='item',
            name='place',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dutchpay.Place'),
        ),
        migrations.AddField(
            model_name='consume',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dutchpay.Item'),
        ),
        migrations.AddField(
            model_name='consume',
            name='participation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dutchpay.Participation'),
        ),
    ]