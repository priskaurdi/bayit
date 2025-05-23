# Generated by Django 5.1.6 on 2025-04-18 21:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgets', '0007_alter_budget_options_alter_budget_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='budget',
            name='budget_detail',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='budget',
            name='city',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='budget',
            name='equipment_btus',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='budget',
            name='neighborhood',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='budget',
            name='number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='budget',
            name='preparation_steps',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='budget',
            name='preparation_time',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='budget',
            name='preparation_time_unit',
            field=models.CharField(blank=True, max_length=65, null=True),
        ),
        migrations.AlterField(
            model_name='budget',
            name='scheduled_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='budget',
            name='scheduled_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='budget',
            name='servings',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='budget',
            name='servings_unit',
            field=models.CharField(blank=True, max_length=65, null=True),
        ),
        migrations.AlterField(
            model_name='budget',
            name='state',
            field=models.CharField(blank=True, max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='budget',
            name='street',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='budget',
            name='zipcode',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
