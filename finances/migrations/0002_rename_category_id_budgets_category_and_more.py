# Generated by Django 5.1.3 on 2024-12-02 01:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finances', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='budgets',
            old_name='category_id',
            new_name='category',
        ),
        migrations.RenameField(
            model_name='transaction',
            old_name='account_id',
            new_name='account',
        ),
        migrations.RenameField(
            model_name='transaction',
            old_name='category_id',
            new_name='category',
        ),
    ]
