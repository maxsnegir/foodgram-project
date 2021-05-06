# Generated by Django 3.2 on 2021-05-04 18:05

from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Ингридиент',
                'verbose_name_plural': 'Ингридиенты',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='IngredientForRecipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.PositiveIntegerField(verbose_name='Количество')),
                ('unit', models.CharField(max_length=10, verbose_name='Еденица измерения')),
            ],
            options={
                'verbose_name': 'Ингридиент для рецетов',
                'verbose_name_plural': 'Ингридиенты для рецетов',
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('slug', models.SlugField(unique=True, verbose_name='Слаг')),
                ('image', models.ImageField(upload_to='recipes/%Y/%m/%d/', verbose_name='Изображение')),
                ('description', models.TextField(verbose_name='Описание')),
                ('tag', multiselectfield.db.fields.MultiSelectField(choices=[('BF', 'Завтрак'), ('LH', 'Обед'), ('DR', 'Ужин')], max_length=8, verbose_name='Тег')),
                ('cook_time', models.PositiveIntegerField(verbose_name='Время приготовления')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')),
            ],
            options={
                'verbose_name': 'Рецепт',
                'verbose_name_plural': 'Рецепты',
                'ordering': ('-created',),
            },
        ),
    ]