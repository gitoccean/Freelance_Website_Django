# Generated by Django 4.2.7 on 2024-01-06 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('System', '0006_document'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='title',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='document',
            name='description',
            field=models.CharField(blank=True, max_length=445),
        ),
        migrations.AlterField(
            model_name='document',
            name='document',
            field=models.FileField(upload_to='docum        ents/'),
        ),
    ]