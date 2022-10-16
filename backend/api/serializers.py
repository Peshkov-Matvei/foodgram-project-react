from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
from recipes.models import Favorite, Ingredient, Recipes, ShoppingCart, Tags
from rest_framework import serializers
from users.models import Subscribe, User

User = get_user_model()


class CustomUserCreateSerializer(UserCreateSerializer):

    class Meta:
        model = User
        fields = '__all__'


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        fields = '__all__'
        model = User

    def is_subscribed(self, obj):
        return (self.context.get('request').user.is_authenticated
                and Subscribe.objects.filter(
                    user=self.context.get('request').user,
                    author=obj).exists()
                )


class TagsSerializers(serializers.ModelSerializer):

    class Meta:
        model = Tags
        fields = '__all__'


class FavoriteSerializers(serializers.ModelSerializer):
    id = serializers.IntegerField(source='id_favorite',)
    cooking_time = serializers.IntegerField(source='cooking_time_favorite',)
    image = Base64ImageField(source='image_favorite',)
    name = serializers.CharField(
        source='name_favorite',
        max_length=128,
        allow_blank=False,
    )

    class Meta:
        model = Favorite
        fields = '__all__'


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

    class Meta:
        model = ShoppingCart
        fields = '__all__'


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
        fields = '__all__'
        model = Ingredient


class IngredientsRedactSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='id_ingridientredact',)
    amount = serializers.IntegerField(source='id_ingridientredact',)

    class Meta:
        fields = '__all__'
        model = Ingredient


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


class SubscribeRecipeSerializers(serializers.ModelSerializer):

    class Meta:
        model = Subscribe
        fields = '__all__'


class RecipesSerializers(serializers.ModelSerializer):
    author = serializers.CharField(
        max_length=128,
        read_only=True,
        allow_blank=False,
    )
    ingredients = serializers.CharField(
        max_length=128,
        allow_blank=False,
    )
    tags = serializers.CharField(max_length=128)
    image = Base64ImageField()

    class Meta:
        model = Recipes
        fields = '__all__'
