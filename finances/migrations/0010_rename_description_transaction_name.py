# Generated by Django 5.1.3 on 2024-12-02 02:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('finances', '0009_alter_categories_type'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='description',
            new_name='name',
        ),
    ]
