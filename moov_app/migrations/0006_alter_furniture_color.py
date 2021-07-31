# Generated by Django 3.2.5 on 2021-07-31 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moov_app', '0005_alter_furniture_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='furniture',
            name='color',
            field=models.CharField(choices=[('Orange', 'Orange'), ('Red', 'Red'), ('Brown', 'Brown'), ('Purple', 'Purple'), ('Blue', 'Blue'), ('Green', 'Green'), ('Black', 'Black'), ('Gray', 'Gray')], default='Orange', max_length=10),
        ),
    ]