# Generated by Django 4.2.7 on 2024-09-19 05:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Mashinani', '0004_rename_account_no_bank_account'),
    ]

    operations = [
        migrations.RenameField(
            model_name='group',
            old_name='account_no',
            new_name='account',
        ),
    ]
