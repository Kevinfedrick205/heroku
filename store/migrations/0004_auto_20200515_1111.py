# Generated by Django 2.1.5 on 2020-05-15 10:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_auto_20200515_1107'),
    ]

    operations = [
        migrations.RenameField(
            model_name='images',
            old_name='image1',
            new_name='imageF',
        ),
        migrations.RenameField(
            model_name='images',
            old_name='image2',
            new_name='imageFt',
        ),
        migrations.RenameField(
            model_name='images',
            old_name='image3',
            new_name='imageS',
        ),
        migrations.RenameField(
            model_name='images',
            old_name='image4',
            new_name='imageT',
        ),
    ]
