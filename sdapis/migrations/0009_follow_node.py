# Generated by Django 3.2.8 on 2021-10-19 03:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sdapis', '0008_auto_20211018_2136'),
    ]

    operations = [
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author1', models.CharField(max_length=50)),
                ('author2', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('host', models.CharField(max_length=150)),
            ],
        ),
    ]