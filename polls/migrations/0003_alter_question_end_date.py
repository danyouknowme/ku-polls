# Generated by Django 3.2.6 on 2021-09-11 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_question_end_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='end_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='date ended'),
        ),
    ]
