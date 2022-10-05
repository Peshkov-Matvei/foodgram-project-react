from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import mixins, viewsets, permissions

from recipes.models import (Favorite, Ingredient, Recipes,
                            ShoppingCard, Tags)
from users.models import Subscribe, Users

from .filters import IngredientFilter, RecipeFilter
from .pagination import CustomPagination
from .permissions import IsAuthorOrReadOnlyPermission
from .serializers import (FavoriteSerializers, IngredientSerializers,
                          RecipesSerializers, ShoppingCardSerializers,
                          SubscribeSerializers, TagsSerializers)

User = get_user_model()


class MIXINS_VIEWSET_LIST(mixins.CreateModelMixin,
                          mixins.ListModelMixin,
                          mixins.DestroyModelMixin,
                          viewsets.GenericViewSet):
    pass


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Users.objects.all()
    permission_classes = (IsAuthorOrReadOnlyPermission,)
    pagination_class = (CustomPagination,)
    permission_classes = (IsAuthorOrReadOnlyPermission,)


class SubscribeViewSet(MIXINS_VIEWSET_LIST):
    serializer_class = (SubscribeSerializers,)
    permission_classes = (IsAuthorOrReadOnlyPermission,)

    def subscribe_create(self, request, *args, **kwargs):

        user = get_object_or_404(
            User,
            id=self.kwargs.get('id_users')
        )
        Subscribe.objects.create(
            user=request.user, following=user
        )
        return Response(HTTPStatus.CREATED)

    def subscribe_delete(self, request, *args, **kwargs):

        subscribe = get_object_or_404(
            Subscribe,
            user__id=request.user.id,
            following__id=self.kwargs['users']
        )
        subscribe.delete()
        return Response(HTTPStatus.NO_CONTENT)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = (IngredientSerializers,)
    pagination_class = (CustomPagination,)
    permission_classes = (permissions.AllowAny,)
    filterset_class = (IngredientFilter,)


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = (TagsSerializers,)
    pagination_class = (CustomPagination,)
    permission_classes = (IsAuthorOrReadOnlyPermission,)


class RecipesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Recipes.objects.all()
    serializer_class = (RecipesSerializers,)
    pagination_class = (CustomPagination,)
    permission_classes = (IsAuthorOrReadOnlyPermission,)
    filterset_class = (RecipeFilter,)


class FavoriteViewSet(MIXINS_VIEWSET_LIST):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializers
    permission_classes = (IsAuthorOrReadOnlyPermission,)


class ShoppingCardViewSet(MIXINS_VIEWSET_LIST):
    queryset = ShoppingCard.objects.all()
    serializer_class = (ShoppingCardSerializers,)
    pagination_class = (CustomPagination,)

    def shoppingcard_create(self, request, *args, **kwargs):

        user = get_object_or_404(
            User,
            id=self.kwargs.get('recipes_id')
        )
        ShoppingCard.objects.create(
            user=request.user, following=user
        )
        return Response(HTTPStatus.CREATED)

    def shoppingcard_delete(self, request, *args, **kwargs):

        subscribe = get_object_or_404(
            ShoppingCard,
            user__id=request.user.id,
            following__id=self.kwargs['recipes_id']
        )
        subscribe.delete()
        return Response(HTTPStatus.NO_CONTENT)
