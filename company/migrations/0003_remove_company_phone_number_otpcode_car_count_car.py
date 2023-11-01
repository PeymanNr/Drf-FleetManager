# Generated by Django 4.2 on 2023-10-16 22:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0002_otpcode'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='phone_number',
        ),
        migrations.AddField(
            model_name='otpcode',
            name='car_count',
            field=models.PositiveIntegerField(default=0, verbose_name='car count'),
        ),
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='company.company', verbose_name='user')),
            ],
        ),
    ]
