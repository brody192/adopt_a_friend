# Generated by Django 4.2.2 on 2023-11-25 05:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pets', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='interview',
            name='interviewedBy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='idpicture',
            name='applicationId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pets.application'),
        ),
        migrations.AddField(
            model_name='housepicture',
            name='applicationId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pets.application'),
        ),
        migrations.AddField(
            model_name='condoagreement',
            name='applicationId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pets.application'),
        ),
        migrations.AddField(
            model_name='completionform',
            name='applicationId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pets.application'),
        ),
        migrations.AddField(
            model_name='completionform',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='application',
            name='pet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pets.pet'),
        ),
        migrations.AddField(
            model_name='application',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='adoptedanimals',
            name='pet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pets.pet'),
        ),
        migrations.AddField(
            model_name='adoptedanimals',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]