# Generated by Django 3.2.8 on 2021-10-27 02:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sdapis', '0029_auto_20211023_2345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='visibility',
            field=models.CharField(choices=[('PUBLIC', 'public'), ('FRIEND', 'friend'), ('PRIVATE', 'private')], default='PUBLIC', max_length=7),
        ),
    ]
