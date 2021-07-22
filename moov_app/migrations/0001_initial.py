# Generated by Django 3.2.5 on 2021-07-22 02:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Furniture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=25)),
                ('length', models.IntegerField()),
                ('width', models.IntegerField()),
                ('color', models.CharField(max_length=12)),
                ('user_id', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='FloorPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('length', models.IntegerField()),
                ('width', models.IntegerField()),
                ('user_id', models.IntegerField()),
                ('comment', models.CharField(max_length=50)),
                ('furnitures', models.ManyToManyField(to='moov_app.Furniture')),
            ],
        ),
    ]