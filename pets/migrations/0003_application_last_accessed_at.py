# Generated by Django 4.2.2 on 2023-11-24 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pets', '0002_remove_pet_adoptedby'),
    ]

    operations = [
        migrations.AddField(
            model_name='application',
            name='last_accessed_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
