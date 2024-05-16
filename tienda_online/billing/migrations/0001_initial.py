# Generated by Django 4.2.7 on 2024-05-16 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.CharField(max_length=100)),
                ('customer_email', models.EmailField(max_length=254)),
                ('pdf_file', models.FileField(upload_to='bills/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
