# Generated by Django 4.2.7 on 2024-09-19 05:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Mashinani', '0003_rename_lender_no_allocation_bank_no_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bank',
            old_name='account_no',
            new_name='account',
        ),
    ]
