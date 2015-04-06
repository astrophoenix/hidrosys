# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hidro_core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UmbralMedidaFisica',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('variable_fisica', models.CharField(max_length=100)),
                ('umbral', models.DecimalField(max_digits=11, decimal_places=2)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='equipo',
            name='estado',
            field=models.CharField(default=b'A', max_length=1),
        ),
    ]
