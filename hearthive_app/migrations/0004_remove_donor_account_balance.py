# Generated by Django 5.1.1 on 2024-10-06 12:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hearthive_app', '0003_donation_stripe_payment_intent_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='donor',
            name='account_balance',
        ),
    ]