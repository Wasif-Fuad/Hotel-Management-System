# Generated by Django 2.2.5 on 2022-09-03 21:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0018_userprofiles_need_approve'),
    ]

    operations = [
        migrations.CreateModel(
            name='staff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.UserProfiles')),
            ],
        ),
        migrations.AlterField(
            model_name='stafftask',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hotel.staff'),
        ),
    ]
