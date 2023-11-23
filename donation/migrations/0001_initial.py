# Generated by Django 4.2.2 on 2023-11-23 04:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import donation.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Donation',
            fields=[
                ('donationId', models.CharField(default=donation.models.generate_donation_key, max_length=15, primary_key=True, serialize=False, unique=True)),
                ('donationAmount', models.DecimalField(decimal_places=2, max_digits=8)),
            ],
        ),
        migrations.CreateModel(
            name='FundraisingCampaign',
            fields=[
                ('campaignId', models.CharField(default=donation.models.generate_campaign_key, max_length=20, primary_key=True, serialize=False, unique=True)),
                ('campaignName', models.CharField(max_length=50, unique=True)),
                ('campaignDescription', models.TextField(blank=True, max_length=800, null=True)),
                ('campaignGoal', models.DecimalField(decimal_places=2, max_digits=8)),
                ('campaignPurpose', models.TextField(default='', max_length=200)),
                ('campaignImage', models.ImageField(upload_to='static/image/campaign_img')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('checkout_session_id', models.CharField(max_length=150, primary_key=True, serialize=False, unique=True)),
                ('checkout_url', models.URLField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=8)),
                ('processed', models.BooleanField(default=False)),
                ('donation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='donation.donation')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(max_length=250)),
                ('for_campaign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='donation.fundraisingcampaign')),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='donation',
            name='campaign',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='donation.fundraisingcampaign'),
        ),
        migrations.AddField(
            model_name='donation',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]