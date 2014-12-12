# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import webservice.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=20, choices=[(b'DEPOSIT', b'Deposit account'), (b'OTHER', b'Savings account'), (b'OTHER', b'Other')])),
                ('number', models.CharField(help_text=b'IBAN format, spaceless', max_length=34, validators=[webservice.models.validate_iban])),
                ('balance', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('street', models.TextField(help_text=b'Number and street')),
                ('city', models.CharField(max_length=200)),
                ('province', models.CharField(max_length=200)),
                ('zip_code', models.CharField(max_length=20)),
            ],
            options={
                'verbose_name_plural': 'addresses',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(default=None, max_length=200, null=True, blank=True)),
                ('date_of_birth', models.DateField()),
                ('address', models.ForeignKey(to='webservice.Address')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='account',
            name='client',
            field=models.ForeignKey(to='webservice.Client'),
            preserve_default=True,
        ),
    ]
