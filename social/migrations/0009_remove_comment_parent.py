# Generated by Django 3.2 on 2021-05-01 09:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0008_alter_post_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='parent',
        ),
    ]
