# Generated by Django 5.1.3 on 2024-12-04 23:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finances', '0014_remove_categories_type_alter_transaction_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categories',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='categories',
            name='name',
        ),
    ]
