# Generated by Django 4.2.7 on 2024-01-19 07:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('System', '0010_author_jobs_author'),
    ]

    operations = [
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
            ],
        ),
        migrations.AddField(
            model_name='jobs',
            name='skill',
            field=models.ManyToManyField(to='System.skill'),
        ),
    ]
