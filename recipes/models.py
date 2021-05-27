from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator as MinValue
from django.db import models
from django.urls import reverse

User = get_user_model()


class Tag(models.Model):
    name = models.CharField('Название тега', max_length=100, unique=True)
    slug = models.SlugField('Слаг', max_length=100, unique=True)
    style = models.CharField('Текст CSS стиля', max_length=255)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class RecipeManager(models.Manager):

    def all_with_tags_and_authors(self):
        qs = self.get_queryset()
        return qs.select_related('author').prefetch_related('tag')


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='recipes', verbose_name='Автор', )
    name = models.CharField('Название', max_length=255)
    image = models.ImageField('Изображение', upload_to='recipes/%Y/%m/%d/', )
    description = models.TextField('Описание', )
    ingredients = models.ManyToManyField('Ingredient',
                                         through='IngredientForRecipe', )
    tag = models.ManyToManyField(Tag, verbose_name='Тег')
    cook_time = models.PositiveIntegerField(
        validators=[MinValue(0, 'Время приготвления не может быть  0'), ],
        verbose_name='Время приготовления')
    created = models.DateTimeField('Дата добавления', auto_now_add=True)

    objects = RecipeManager()

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-created',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('recipes:recipe_detail', kwargs={'pk': self.pk})


class Ingredient(models.Model):
    title = models.CharField('Название', max_length=255, unique=True)
    dimension = models.CharField('Еденица измерения', max_length=20,
                                 default='шт.')
    draft = models.BooleanField('Черновик', default=True)

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ('title',)

    def __str__(self):
        return self.title


class IngredientForRecipe(models.Model):
    recipe = models.ForeignKey(Recipe, verbose_name='Рецепт',
                               on_delete=models.CASCADE,
                               related_name='get_ingredients')
    ingredient = models.ForeignKey(Ingredient, verbose_name='Ингредиент',
                                   on_delete=models.CASCADE, )
    count = models.PositiveIntegerField(
        validators=[MinValue(0, 'Время приготвления не может быть  0'), ],
        verbose_name='Количество')

    class Meta:
        verbose_name = 'Ингредиент для рецетов'
        verbose_name_plural = 'Ингредиенты для рецетов'
        constraints = [
            models.UniqueConstraint(fields=['ingredient', 'recipe'],
                                    name='unique_ingredient'),
        ]

    def __str__(self):
        return f"{self.recipe.name} {self.ingredient.title}"


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='Пользователь',
                             )
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               verbose_name='Рецепт')

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique_favorites'),
        ]

    def __str__(self):
        return f"{self.user} | {self.recipe}"


class ShoppingList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='Пользователь')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               verbose_name='Рецепт')

    class Meta:
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = [
            models.UniqueConstraint(fields=['user', 'recipe'],
                                    name='unique_recipe'),
        ]

    def __str__(self):
        return f"{self.user} | {self.recipe}"
