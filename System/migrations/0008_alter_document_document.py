# Generated by Django 4.2.7 on 2024-01-06 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('System', '0007_document_title_alter_document_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='document',
            field=models.FileField(upload_to=''),
        ),
    ]
