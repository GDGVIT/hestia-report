# Generated by Django 3.0.4 on 2020-03-31 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_createshoprecommendation_item'),
    ]

    operations = [
        migrations.AlterField(
            model_name='createshoprecommendation',
            name='description_of_shop',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='createshoprecommendation',
            name='extra_instruction',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='createshoprecommendation',
            name='item',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='createshoprecommendation',
            name='landmark',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='createshoprecommendation',
            name='recommended_for',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='createshoprecommendation',
            name='user_id',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='reportuser',
            name='reason',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='reportuser',
            name='reported_by',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='reportuser',
            name='user_id',
            field=models.CharField(max_length=250),
        ),
    ]
