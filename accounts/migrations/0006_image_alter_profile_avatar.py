# Generated by Django 4.0.5 on 2022-06-28 20:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='')),
            ],
        ),
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='accounts.image'),
        ),
    ]
