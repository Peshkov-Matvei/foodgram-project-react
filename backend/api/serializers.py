from recipes.models import (Favorite, Ingredient, RecipeIngredient, Recipes,
                            RecipeTags, ShoppingCard, Tags)
from rest_framework import serializers
from users.models import Subscription


class TagsSerializers(serializers.ModelSerializer):
    class Meta():
        fields = '__all__'
        model = Tags


class FavoriteSerializers(serializers.ModelSerializer):
    id = serializers.IntegerField()
    cooking_time = serializers.IntegerField()
    name = serializers.CharField()


class ShoppingCardSerializers(serializers.ModelSerializer):
    id = serializers.IntegerField()
    cooking_time = serializers.IntegerField()
    name = serializers.CharField()


class IngredientSerializers(serializers.ModelSerializer):
    id = serializers.IntegerField()
    name = serializers.ReadOnlyField()
    measurement_unit = serializers.ReadOnlyField()

    class Meta():
        model = Ingredient
        fields = '__all__'


class SubscriptionSerializers(serializers.ModelSerializer):
    email = serializers.CharField()
    id = serializers.IntegerField()
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    recipes = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()
    recipes_count = serializers.ReadOnlyField()

    class Meta:
        model = Subscription
        fields = '__all__'


class RecipesSerializers(serializers.ModelSerializer):
    author = serializers.CharField()
    ingredients = serializers.CharField()
    shopping_list = serializers.SerializerMethodField()
    tags = serializers.CharField()
    ingredients = serializers.CharField()

    class Meta:
        model = Recipes
        fields = '__all__'
