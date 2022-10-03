from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (FavoriteViewSet, SubscriptionViewSet, IngredientViewSet,
                    RecipeViewSet, ShoppingCardViewSet, TagsViewSet,
                    UserViewSet)

app_name = 'api'

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet, basename='users')
router_v1.register('tags', TagsViewSet, basename='tags')
router_v1.register('ingredient', IngredientViewSet, basename='ingredient')
router_v1.register('recipe', RecipeViewSet, basename='recipe')
router_v1.register(
    r'users/(?P<user_id>\d+)/follow', SubscriptionViewSet,
    basename='follow')
router_v1.register(
    r'recipes/(?P<recipe_id>\d+)/favorite', FavoriteViewSet,
    basename='favorite')
router_v1.register(
    r'recipes/(?P<recipe_id>\d+)/shopping_card', ShoppingCardViewSet,
    basename='shoppingcard')


urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
