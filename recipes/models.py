from django.contrib.auth import get_user_model
from django.db import models
from multiselectfield import MultiSelectField

User = get_user_model()


class Recipe(models.Model):
    BREAKFAST = 'Завтрак'
    LUNCH = 'Обед'
    DINNER = 'Ужин'

    TAG_CHOICES = (
        ('BF', BREAKFAST),
        ('LH', LUNCH),
        ('DR', DINNER)
    )

    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='recipes', verbose_name='Автор', )
    name = models.CharField('Название', max_length=255)
    slug = models.SlugField('Слаг', unique=True)
    image = models.ImageField('Изображение', upload_to='recipes/%Y/%m/%d/', )
    description = models.TextField('Описание', )
    ingredients = models.ManyToManyField('Ingredient',
                                         through='IngredientForRecipe',)
    tag = MultiSelectField(choices=TAG_CHOICES, max_choices=3,
                           verbose_name='Тег')
    cook_time = models.PositiveIntegerField('Время приготовления', )
    created = models.DateTimeField('Дата добавления', auto_now_add=True)

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-created',)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField('Название', max_length=255)

    class Meta:
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'
        ordering = ('name',)

    def __str__(self):
        return self.name


class IngredientForRecipe(models.Model):
    ingredient = models.ForeignKey(Ingredient, verbose_name='Ингридиент',
                                   on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, verbose_name='Рецепт',
                               on_delete=models.CASCADE)
    count = models.PositiveIntegerField('Количество')
    unit = models.CharField('Еденица измерения', max_length=10)

    class Meta:
        verbose_name = 'Ингридиент для рецетов'
        verbose_name_plural = 'Ингридиенты для рецетов'
        constraints = [
            models.UniqueConstraint(fields=['ingredient', 'recipe'],
                                    name='unique_ingredient'),
        ]

    def __str__(self):
        return f"{self.recipe.name} {self.ingredient.name}"
