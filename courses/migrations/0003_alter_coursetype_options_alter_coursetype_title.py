# Generated by Django 4.1.3 on 2022-12-09 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_alter_course_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='coursetype',
            options={'ordering': ['id']},
        ),
        migrations.AlterField(
            model_name='coursetype',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Направление курса'),
        ),
    ]
