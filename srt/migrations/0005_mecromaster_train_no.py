# Generated by Django 5.0.4 on 2024-07-07 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('srt', '0004_rename_user_mecromaster_client'),
    ]

    operations = [
        migrations.AddField(
            model_name='mecromaster',
            name='train_no',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
