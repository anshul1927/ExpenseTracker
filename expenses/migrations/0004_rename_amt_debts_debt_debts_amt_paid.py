# Generated by Django 4.0.3 on 2022-03-08 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0003_debts_is_paid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='debts',
            old_name='amt',
            new_name='debt',
        ),
        migrations.AddField(
            model_name='debts',
            name='amt_paid',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
