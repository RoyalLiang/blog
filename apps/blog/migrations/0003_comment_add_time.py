# Generated by Django 2.1.2 on 2018-11-27 15:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='add_time',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='发布时间'),
        ),
    ]
