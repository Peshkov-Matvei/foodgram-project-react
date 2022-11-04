from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Ingredient(models.Model):

    name = models.CharField(
        max_length=128,
        verbose_name='Название ингридиента',
        help_text='Введите название ингридиента',
    )
    measurement_unit = models.CharField(
        max_length=32,
        verbose_name='Еденица измерения',
        help_text='Введите еденицу измерения',
    )

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'

    class Meta():
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'
        ordering = ('id',)


class Tags(models.Model):

    name = models.CharField(
        verbose_name='Название тега',
        max_length=128,
        unique=True,
    )
    color = models.CharField(
        verbose_name='Цветовой HEX-код',
        max_length=7,
        default='#FF0000',
        null=True,
        blank=True,
        unique=True,
    )
    slug = models.SlugField(
        verbose_name='Slug тега',
        max_length=64,
        unique=True,
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('name',)

    def __str__(self):
        return self.name


class Recipes(models.Model):

    author = models.ForeignKey(
        User,
        max_length=128,
        help_text='Введите автора рецепта',
        verbose_name='Имя автора',
        on_delete=models.SET_NULL,
        null=True,
        related_name='recipes',
    )
    name = models.CharField(
        max_length=128,
        help_text='Введите название рецепта',
        verbose_name='Название рецепта',
    )
    image = models.ImageField(
        help_text='Вставте изображение',
        verbose_name='Изображение',
        upload_to='recipes/images/',
    )
    text = models.TextField(
        max_length=256,
        help_text='Введите текст',
        verbose_name='Текст',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientInRecipe',
        related_name='recipes',
        verbose_name='Ингредиенты'
    )
    tags = models.ManyToManyField(
        Tags,
        related_name='recipes',
        help_text='Введите тег',
        verbose_name='Теги',
    )
    cooking_time = models.IntegerField(
        verbose_name='Время приготовления',
        help_text='Введите время приготовления',
    )

    class Meta:
        ordering = ['-id']
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class ShoppingCart(models.Model):

    user = models.ForeignKey(
        User,
        verbose_name='Список покупок',
        related_name='shopping_cart',
        help_text='Добавте ингридиенты в список покупок',
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipes,
        verbose_name='Рецепт',
        related_name='shopping_cart',
        help_text='Добавте рецепты в список покупок',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'В корзине {self.user} находятся {self.recipe}'

    class Meta():
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = (models.UniqueConstraint(
            fields=['user', 'recipe'], name='unique_shoppingCard'),
        )


class Favourite(models.Model):

    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        related_name='favorites',
        help_text='Добавте пользователя в изранное',
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipes,
        verbose_name='Рецепт',
        related_name='favorites',
        help_text='Добавте рецепты в изранное',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'Пользователю {self.user} понравился {self.recipe}'

    class Meta():
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        constraints = (models.UniqueConstraint(
            fields=['user', 'recipe'], name='unique_favorite'),
        )


class IngredientInRecipe(models.Model):

    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        related_name='ingredient_list',
        verbose_name='Рецепт',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
    )
    amount = models.IntegerField(
        verbose_name='Количество',
        help_text='Укажите количство продуктов',
    )

    class Meta:
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецептах'

    def __str__(self):
        return f'{self.ingredient}, {self.recipe}, {self.amount}'
