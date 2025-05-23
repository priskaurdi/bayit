# Generated by Django 5.1.6 on 2025-03-22 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budgets', '0003_alter_budget_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='budget',
            name='service_type',
            field=models.CharField(choices=[('Manutenção', 'Manutenção'), ('Instalação', 'Instalação'), ('Limpeza', 'Limpeza'), ('Elétrica', 'Elétrica')], max_length=50),
        ),
        migrations.AlterField(
            model_name='budget',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]
