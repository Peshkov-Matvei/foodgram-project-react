from django.contrib.auth import get_user_model
from rest_framework import serializers

from recipes.models import Ingredient, Recipes, Tags
from users.models import Subscribe

User = get_user_model()


class UserListSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        fields = '__all__'
        model = User

    def is_subscribed(self, obj):
        return (self.context.get('request').user.is_authenticated
                and Subscribe.objects.filter(
                    user=self.context.get('request').user,
                    author=obj
        ).exists())


class TagsSerializers(serializers.ModelSerializer):
    class Meta():
        fields = '__all__'
        model = Tags


class FavoriteSerializers(serializers.ModelSerializer):
    id = serializers.IntegerField(source='id_favorite',)
    cooking_time = serializers.IntegerField(source='cooking_time_favorite',)
    name = serializers.CharField(
        source='name_favorite',
        max_length=128,
        allow_blank=False,
    )


class ShoppingCardSerializers(serializers.ModelSerializer):
    id = serializers.IntegerField(source='id_shopping_card',)
    cooking_time = serializers.IntegerField(
        source='cooking_time_shopping_card',
        read_only=True,
    )
    name = serializers.CharField(
        source='name_shopping_card',
        max_length=128,
        allow_blank=False,
    )


class IngredientSerializers(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='id_ingridient',)
    name = serializers.CharField(
        source='name_ingridient',
        max_length=128,
        allow_blank=False,
    )
    measurement_unit = serializers.ReadOnlyField(
        source='measurement_unit_ingridient'
    )

    class Meta():
        model = Ingredient
        fields = '__all__'


class SubscribeSerializers(serializers.ModelSerializer):
    email = serializers.EmailField(
        source='email_subscribe',
        read_only=True,
        allow_blank=False,
    )
    id = serializers.IntegerField(source='id_subscribe',)
    username = serializers.CharField(
        source='username_subscribe',
        max_length=128,
        read_only=True,
        allow_blank=False,
    )
    first_name = serializers.CharField(
        source='first_name_subscribe',
        max_length=128,
        read_only=True,
        allow_blank=False,
    )
    last_name = serializers.CharField(
        source='last_name_subscribe',
        max_length=128,
        read_only=True,
        allow_blank=False,
    )
    recipes = serializers.SerializerMethodField(source='recipes_subscription',)
    is_subscribed = serializers.SerializerMethodField(
        source='is_subscribed_subscription',
    )
    recipes_count = serializers.CharField(
        source='recipes_count_subscription',
        max_length=128,
        allow_blank=False,
    )

    class Meta:
        model = Subscribe
        fields = '__all__'


class RecipesSerializers(serializers.ModelSerializer):
    author = serializers.CharField(
        source='author_recipes',
        max_length=128,
        read_only=True,
        allow_blank=False,
    )
    ingredients = serializers.CharField(
        source='ingredients_recipes',
        max_length=128,
        allow_blank=False,
    )
    shopping_list = serializers.CharField(
        source='shopping_list_recipes',
        max_length=128,
        allow_blank=False,
    )
    tags = serializers.CharField(source='tags_recipes', max_length=128)
    ingredients = serializers.CharField(
        source='ingredients_recipes',
        max_length=128,
        allow_blank=False,
    )

    class Meta:
        model = Recipes
        fields = '__all__'
