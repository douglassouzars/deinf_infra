# Generated by Django 4.1.7 on 2023-07-04 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mapeamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subchefe', models.BooleanField(default=False)),
                ('cn', models.CharField(max_length=100, null=True)),
            ],
        ),
    ]