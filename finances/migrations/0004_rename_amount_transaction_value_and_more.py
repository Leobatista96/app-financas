# Generated by Django 5.1.3 on 2024-12-02 02:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finances', '0003_delete_budgets'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='amount',
            new_name='value',
        ),
        migrations.RemoveField(
            model_name='transaction',
            name='transaction_name',
        ),
    ]
