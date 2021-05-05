# Generated by Django 3.2 on 2021-04-16 16:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('catalogos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Productos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('precio', models.FloatField(default=0.0)),
                ('marca', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogos.marca')),
                ('presentacion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogos.presentacion')),
            ],
        ),
    ]
