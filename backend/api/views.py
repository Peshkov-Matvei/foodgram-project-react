from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import mixins, viewsets, permissions

from recipes.models import (Favorite, Ingredient, Recipes,
                            ShoppingCart, Tags)
from users.models import Subscribe, User

from .filters import IngredientFilter, RecipeFilter
from .pagination import CustomPagination
from .permissions import IsAuthorOrReadOnlyPermission
from .serializers import (FavoriteSerializers, IngredientSerializers,
                          RecipesSerializers, ShoppingCardSerializers,
                          SubscribeSerializers, TagsSerializers, CustomUserSerializer, CustomUserCreateSerializer)

User = get_user_model()


class MIXINS_VIEWSET_LIST(mixins.CreateModelMixin,
                          mixins.ListModelMixin,
                          mixins.DestroyModelMixin,
                          viewsets.GenericViewSet):
    pass


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    permission_classes = (IsAuthorOrReadOnlyPermission,)

    def erializer_class(self):
        if self.action == 'create':
            return CustomUserCreateSerializer

        return CustomUserSerializer

    def subscriptions(self, request):
        queryset = Subscribe.objects.filter(user=request.user)
        pages = self.paginate_queryset(queryset)
        serializer = SubscribeSerializers(
            pages,
            many=True,
            context={'request': request},
        )
        return self.get_paginated_response(serializer.data)


class SubscribeViewSet(MIXINS_VIEWSET_LIST):
    serializer_class = (SubscribeSerializers,)
    permission_classes = (IsAuthorOrReadOnlyPermission,)

    def queryset(self):
        return self.request.user.follower.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['author_id'] = self.kwargs.get('user_id')
        return context

    def create(self, request, *args, **kwargs):
        user = get_object_or_404(
            User,
            id=self.kwargs.get('id_users')
        )
        Subscribe.objects.create(
            user=request.user, following=user
        )
        return Response(HTTPStatus.CREATED)

    def delete(self, request, *args, **kwargs):
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

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class FavoriteViewSet(MIXINS_VIEWSET_LIST):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializers
    permission_classes = (IsAuthorOrReadOnlyPermission,)

    def create(self, request, *args, **kwargs):
        user = get_object_or_404(
            User,
            id=self.kwargs.get('id_users')
        )
        Subscribe.objects.create(
            user=request.user, following=user
        )
        return Response(HTTPStatus.CREATED)

    def delete(self, request, *args, **kwargs):
        subscribe = get_object_or_404(
            Subscribe,
            user__id=request.user.id,
            following__id=self.kwargs['users']
        )
        subscribe.delete()
        return Response(HTTPStatus.NO_CONTENT)


class ShoppingCartViewSet(MIXINS_VIEWSET_LIST):
    queryset = ShoppingCart.objects.all()
    serializer_class = (ShoppingCardSerializers,)
    pagination_class = (CustomPagination,)

    def get_queryset(self):
        user = self.request.user.id
        return ShoppingCart.objects.filter(user=user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['recipe_id'] = self.kwargs.get('recipe_id')
        return context

    def shoppingcard_create(self, request, *args, **kwargs):

        user = get_object_or_404(
            User,
            id=self.kwargs.get('recipes_id')
        )
        ShoppingCart.objects.create(
            user=request.user, following=user
        )
        return Response(HTTPStatus.CREATED)

    def shoppingcard_delete(self, request, *args, **kwargs):

        subscribe = get_object_or_404(
            ShoppingCart,
            user__id=request.user.id,
            following__id=self.kwargs['recipes_id']
        )
        subscribe.delete()
        return Response(HTTPStatus.NO_CONTENT)
