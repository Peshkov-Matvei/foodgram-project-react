from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from recipes.models import (Favorite, Ingredient, RecipeIngredient, Recipes,
                            RecipeTags, ShoppingCard, Tags)
from rest_framework import mixins, viewsets
from users.models import Subscription, Users

from .pagination import CustomPagination
from .permissions import IsAuthorOrReadOnlyPermission
from .serializers import (FavoriteSerializers, SubscriptionSerializers,
                          IngredientSerializers, RecipesSerializers,
                          ShoppingCardSerializers, TagsSerializers)

User = get_user_model()

MIXINS_VIEWSET_LIST = (
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Users.objects.all()
    permission_classes = (IsAuthorOrReadOnlyPermission,)


class SubscriptionViewSet(*MIXINS_VIEWSET_LIST):
    serializer_class = (SubscriptionSerializers,)
    permission_classes = (IsAuthorOrReadOnlyPermission,)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = (IngredientSerializers,)
    pagination_class = (CustomPagination,)
    permission_classes = (IsAuthorOrReadOnlyPermission,)


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = (TagsSerializers,)
    pagination_class = (CustomPagination,)
    permission_classes = (IsAuthorOrReadOnlyPermission,)


class RecipeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Recipes.objects.all()
    serializer_class = (RecipesSerializers,)
    pagination_class = (CustomPagination,)


class FavoriteViewSet(*MIXINS_VIEWSET_LIST):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializers
    permission_classes = (IsAuthorOrReadOnlyPermission,)


class ShoppingCardViewSet(*MIXINS_VIEWSET_LIST):
    queryset = ShoppingCard.objects.all()
    serializer_class = (ShoppingCardSerializers,)
    pagination_class = (CustomPagination,)


def page_not_found(request, exception):
    return render(
        request, 'posts/404.html',
        {'path': request.path}, status=HTTPStatus.NOT_FOUND
    )
