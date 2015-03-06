# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Equipo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=100)),
                ('estado', models.CharField(max_length=1)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_modificacion', models.DateTimeField(auto_now=True)),
                ('usuario', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EquipoMedicion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('temperatura', models.DecimalField(max_digits=11, decimal_places=2)),
                ('humedad', models.DecimalField(max_digits=11, decimal_places=2)),
                ('intensidad_luz', models.DecimalField(max_digits=11, decimal_places=2)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('equipo', models.ForeignKey(to='hidro_core.Equipo')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
