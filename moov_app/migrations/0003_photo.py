# Generated by Django 3.2.4 on 2021-07-22 06:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('moov_app', '0002_auto_20210722_0243'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=200)),
                ('floorplan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='moov_app.floorplan')),
            ],
        ),
    ]