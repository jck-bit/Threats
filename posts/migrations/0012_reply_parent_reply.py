# Generated by Django 4.1.7 on 2023-08-30 11:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0011_reply'),
    ]

    operations = [
        migrations.AddField(
            model_name='reply',
            name='parent_reply',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='posts.reply'),
        ),
    ]
