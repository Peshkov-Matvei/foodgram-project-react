from django.db.models import F
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import exceptions, fields, relations, serializers

from recipes.models import Ingredient, IngredientInRecipe, Recipe, Tag
from users.models import Subscribe

User = get_user_model()


class CustomUserCreateSerializer(UserCreateSerializer):

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username',
            'first_name', 'last_name', 'password'
        )


class CustomUserSerializer(UserSerializer):
    is_subscribed = fields.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username',
            'first_name', 'last_name', 'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Subscribe.objects.filter(user=user, author=obj).exists()


class IngredientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ingredient
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


class SubscribeSerializer(CustomUserSerializer):
    recipes = fields.SerializerMethodField()
    recipes_count = fields.SerializerMethodField()

    class Meta(CustomUserSerializer.Meta):
        fields = (
            'recipes', 'recipes_count'
        )

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def get_recipes(self, obj):
        recipes = obj.recipes.all()
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        if limit:
            recipes = recipes.all()[:int(limit)]
        context = {'request': request}
        return SmallRecipeSerializer(
            recipes,
            context=context,
            read_only=True,
            many=True
        ).data


class SmallRecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'name',
            'image', 'cooking_time'
        )


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = fields.IntegerField()

    class Meta:
        model = IngredientInRecipe
        fields = (
            'id', 'amount'
        )


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    image = Base64ImageField()
    author = CustomUserSerializer()
    ingredients = fields.SerializerMethodField()
    is_favorited = fields.SerializerMethodField()
    is_in_shopping_cart = fields.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients',
            'is_favorited', 'is_in_shopping_cart',
            'name', 'image', 'text', 'cooking_time',
        )

    def get_ingredients(self, obj):
        recipe = obj
        ingredients = recipe.ingredients.values(
            'id', 'name', 'measurement_unit',
            amount=F('ingredientinrecipe__amount')
        )
        return ingredients

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.favorites.filter(recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.shopping_cart.filter(recipe=obj).exists()


class RecipeCreateSerializer(serializers.ModelSerializer):
    tags = relations.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    image = Base64ImageField()
    author = CustomUserSerializer(read_only=True)
    ingredients = RecipeIngredientSerializer(many=True)

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'author', 'ingredients',
            'name', 'image', 'text', 'cooking_time'
        )

    def validate_ingredients(self, value):
        ingredients = []
        if not value:
            raise exceptions.ValidationError(
                'Нельзя создать рецепт без ингредиентов'
            )
        for product in value:
            ingredient = get_object_or_404(Ingredient, id=product['id'])
            if ingredient in ingredients:
                raise exceptions.ValidationError(
                    'Ингредиент уже существует'
                )
            ingredients.append(ingredient)
        return value

    def validate_tags(self, value):
        if not value:
            raise exceptions.ValidationError(
                'Нельзя создать рецепт без тегов'
            )
        return value

    def ingredient_in_recipe(self, recipe, ingredients):
        IngredientInRecipe.objects.bulk_create(
            [IngredientInRecipe(
                ingredient=get_object_or_404(Ingredient, id=ingredient['id']),
                recipe=recipe, amount=ingredient['amount']
            ) for ingredient in ingredients]
        )

    def create(self, data):
        tags = data.pop('tags')
        ingredients = data.pop('ingredients')
        recipe = Recipe.objects.create(**data)
        recipe.tags.set(tags)
        self.ingredient_in_recipe(
            recipe=recipe,
            ingredients=ingredients
        )
        return recipe

    def update(self, recipe, data):
        tags = data.pop('tags')
        recipe.tags.clear()
        recipe.tags.set(tags)
        ingredients = data.pop('ingredients')
        recipe = super().update(recipe, data)
        recipe.ingredients.clear()
        self.ingredient_in_recipe(
            recipe=recipe,
            ingredients=ingredients
        )
        return recipe

    def to_representation(self, recipe):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeSerializer(recipe, context=context).data
