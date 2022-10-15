from django_filters import rest_framework as filters

from recipes.models import Ingredient, Recipes, Tags
from users.models import User


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
        queryset=User.objects.all(),
        field_name='author__slug',
    )

    class Meta:
        model = Recipes
        fields = ('tags',)

    def get_is_favorited(self, queryset, name, value):
        user = self.request.user
        if value == 1:
            return queryset.filter(favorite__user=user)
        return Recipes.objects.all()

    def get_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if value == 1:
            return queryset.filter(cart__user=user)
        return Recipes.objects.all()
