from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Ingredient(models.Model):

    name = models.CharField(
        max_length=128,
        verbose_name='Название ингридиента',
        help_text='Введите название ингридиента',
    )
    unit_measurement = models.CharField(
        max_length=32,
        verbose_name='Еденица измерения',
        help_text='Введите еденицу измерения',
    )

    def __str__(self):
        return self.name

    class Meta():
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'
        ordering = ('id',)


class Tags(models.Model):

    name = models.CharField(
        max_length=128,
        verbose_name='Название тега',
        help_text='Введите имя тега',
        unique=True,
    )
    color = models.CharField(
        max_length=32,
        verbose_name='Цвет кода',
        help_text='Введите цвет кода',
        unique=True,
    )
    slug = models.SlugField(
        max_length=256,
        verbose_name='Слаг',
        help_text='Введите слаг',
        unique=True,
    )

    def __str__(self):
        return self.name

    class Meta():
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('name',)


class Recipes(models.Model):

    author = models.ForeignKey(
        User,
        max_length=128,
        help_text='Введите автора рецепта',
        verbose_name='Имя автора',
        on_delete=models.CASCADE,
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
        upload_to='recipes/image/',
    )
    text = models.TextField(
        max_length=256,
        help_text='Введите текст',
        verbose_name='Текст',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        verbose_name='Ингридиенты',
        help_text='Введите игридиенты',
    )
    tags = models.ManyToManyField(
        Tags,
        through='RecipeTags',
        verbose_name='Теги',
        help_text='Введите тег',
    )
    time_cooking = models.IntegerField(
        verbose_name='Время приготовления',
        help_text='Введите время приготовления',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата создания',
        help_text='Дата создания',
    )

    def __str__(self):
        return self.name

    class Meta():
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('pub_date',)


class ShoppingCart(models.Model):

    user = models.ForeignKey(
        User,
        verbose_name='Список покупок',
        help_text='Добавте ингридиенты в список покупок',
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipes,
        verbose_name='Рецепт',
        help_text='Добавте рецепты в список покупок',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.user, self.recipe

    class Meta():
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'
        constraints = (models.UniqueConstraint(
            fields=['user', 'recipe'], name='unique_shoppingCard'
        ),)


class Favorite(models.Model):

    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        help_text='Добавте пользователя в изранное',
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipes,
        verbose_name='Рецепт',
        help_text='Добавте рецепты в изранное',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.user, self.recipe

    class Meta():
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        constraints = (models.UniqueConstraint(
            fields=['user', 'recipe'], name='unique_favorite'
        ),)


class RecipeTags(models.Model):

    tags = models.ForeignKey(
        Tags,
        verbose_name='Название тега',
        help_text='Введите имя тега',
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipes,
        verbose_name='Рецепт',
        help_text='Добавте рецепты',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.tags, self.recipe

    class Meta():
        verbose_name = 'Тег в рецепте'
        verbose_name_plural = 'Теги в рецептах'


class RecipeIngredient(models.Model):

    ingredient = models.ForeignKey(
        Ingredient,
        verbose_name='Продукты в рецепте',
        help_text='Добавте ингридиенты',
        on_delete=models.CASCADE,
    )
    recipe = models.ForeignKey(
        Recipes,
        verbose_name='Рецепт',
        help_text='Выберите рецепт',
        on_delete=models.CASCADE,
    )
    amount = models.IntegerField(
        verbose_name='Количество',
        help_text='Укажите количство продуктов',
    )

    def __str__(self):
        return self.ingredient, self.recipe

    class Meta():
        verbose_name = 'Ингридиент в рецепте'
        verbose_name_plural = 'Ингридиенти в рецептах'
