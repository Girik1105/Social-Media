# Generated by Django 3.2 on 2021-08-01 11:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0015_auto_20210801_0025'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-created_on']},
        ),
        migrations.RenameField(
            model_name='post',
            old_name='shared_on',
            new_name='og_post_date',
        ),
    ]
