# Generated by Django 5.1.2 on 2024-11-02 22:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("habits", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="habit",
            name="execution_interval_hour",
        ),
    ]