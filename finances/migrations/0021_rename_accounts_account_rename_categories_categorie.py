# Generated by Django 5.1.3 on 2025-04-02 01:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finances', '0020_alter_categories_category'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Accounts',
            new_name='Account',
        ),
        migrations.RenameModel(
            old_name='Categories',
            new_name='Categorie',
        ),
    ]
