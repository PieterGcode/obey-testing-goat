# Generated by Django 4.0.1 on 2022-02-10 10:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0004_item_list'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='list',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='lists.list'),
        ),
    ]
