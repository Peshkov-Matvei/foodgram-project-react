from django_filters import rest_framework as filters

from recipes.models import Ingredient, Recipes, Tags
from users.models import Users


class IngredientFilter(filters.FilterSet):

    name = filters.CharFilter(
        queryset=Ingredient.objects.all(),
        field_name='name__name',
    )

    class Meta:
        model = Ingredient
        fields = '__all__'


class RecipeFilter(filters.FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        queryset=Tags.objects.all(),
        field_name='tags__slug',
    )
    author = filters.ModelChoiceFilter(
        queryset=Users.objects.all(),
        field_name='author__slug',
    )

    class Meta:
        model = Recipes
        fields = ('tags',)
