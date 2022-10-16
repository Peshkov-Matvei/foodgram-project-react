from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
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


class UserViewSet(UserViewSet):
    queryset = User.objects.all()
    permission_classes = (IsAuthorOrReadOnlyPermission,)

    def get_serializer_class(self):
        if self.action == 'create':
            return CustomUserCreateSerializer

        return CustomUserSerializer

    def subscriptions(self, request):
        queryset = Subscribe.objects.filter(user=request.user)
        serializer = SubscribeSerializers(
            self.paginate_queryset(queryset),
            context={'request': request},
        )
        return self.get_paginated_response(serializer.data)


class SubscribeViewSet(MIXINS_VIEWSET_LIST):
    queryset = Subscribe.objects.all()
    serializer_class = (SubscribeSerializers,)
    permission_classes = (IsAuthorOrReadOnlyPermission,)

    def create(self, request, *args, **kwargs):
        user_id = self.kwargs.get('users_id')
        user = get_object_or_404(User, id=user_id)
        Subscribe.objects.create(
            user=request.user,
            following=user
        )
        return Response(HTTPStatus.CREATED)

    def delete(self, request, *args, **kwargs):
        author_id = self.kwargs['users_id']
        user_id = request.user.id
        subscribe = get_object_or_404(
            Subscribe,
            user__id=user_id,
            following__id=author_id
        )
        subscribe.delete()
        return Response(HTTPStatus.NO_CONTENT)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = (IngredientSerializers)
    pagination_class = (CustomPagination)
    permission_classes = (permissions.AllowAny,)
    filterset_class = (IngredientFilter,)


class TagsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = (TagsSerializers)
    pagination_class = (CustomPagination)
    permission_classes = (IsAuthorOrReadOnlyPermission,)


class RecipesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Recipes.objects.all()
    serializer_class = (RecipesSerializers)
    pagination_class = (CustomPagination)
    permission_classes = (IsAuthorOrReadOnlyPermission,)
    filterset_class = (RecipeFilter,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class FavoriteViewSet(MIXINS_VIEWSET_LIST):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializers
    permission_classes = (IsAuthorOrReadOnlyPermission,)

    def create(self, request, *args, **kwargs):
        recipe_id = int(self.kwargs['recipes_id'])
        recipes = get_object_or_404(Recipes, id=recipe_id)
        self.model.objects.create(
            user=request.user,
            recipe=recipes
        )
        return Response(HTTPStatus.CREATED)

    def delete(self, request, *args, **kwargs):
        recipe_id = self.kwargs['recipes_id']
        user_id = request.user.id
        object = get_object_or_404(
            Favorite,
            user__id=user_id,
            recipe__id=recipe_id
        )
        object.delete()
        return Response(HTTPStatus.NO_CONTENT)


class ShoppingCardViewSet(MIXINS_VIEWSET_LIST):
    queryset = ShoppingCart.objects.all()
    serializer_class = (ShoppingCardSerializers,)
    pagination_class = (CustomPagination,)

    def create(self, request, *args, **kwargs):
        shoppingcard_id = int(self.kwargs['shoppingcard_id'])
        shopingcard = get_object_or_404(Recipes, id=shoppingcard_id)
        self.model.objects.create(
            user=request.user,
            recipe=shopingcard
        )
        return Response(HTTPStatus.CREATED)

    def delete(self, request, *args, **kwargs):
        shoppingcard_id = self.kwargs['shoppingcard_id']
        user_id = request.user.id
        object = get_object_or_404(
            Subscribe,
            user__id=user_id,
            shoppingcard__id=shoppingcard_id
        )
        object.delete()
        return Response(HTTPStatus.NO_CONTENT)
