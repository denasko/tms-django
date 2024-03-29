# Generated by Django 5.0 on 2024-01-05 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_question_publication'),
    ]

    operations = [
        migrations.CreateModel(
            name='Engineer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('language', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Manager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('project', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='question',
            name='pub_date',
            field=models.DateTimeField(db_index=True, verbose_name='date published'),
        ),
    ]
