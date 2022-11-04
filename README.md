[![CI](https://github.com/Peshkov-Matvei/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg)](https://github.com/Peshkov-Matvei/foodgram-project-react/actions/workflows/foodgram_workflow.yml)
# Проект Foodgram
### Описание
Foodgram - API и онлайн-сервис для создания на котором можно публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.
### Возможости сайта
- api/docs/ - получение информации о сайте
- api/users/ - получение информации о пользователях.
- api/users/{id}/ - Получение информации о пользователе по id.
- api/users/{id}/subscribe/ - Подписаться на пользователя с соответствующим id.
- api/tags/ - Получение информации о тегах.
- api/tags/{id} - Получение информации о теге по id.
- api/ingredients/ - Получение информации о ингредиентах.
- api/ingredients/{id}/ - Получение информации о игредиенте по id.
- api/recipes/ - Получение информации о рецептах.
- api/recipes/{id} - Получение информации о нгредиенте по id.
- api/recipes/{id}/shopping_cart/ - Добавление рецепта по id в список покупок.
- api/recipes/download_shopping_cart/ - Установка списка покупок.
- api/recipes/{id}/favorite/ - Добавление рецепта по id в список избранного.
### Команды для запуска проекта
- Склонируйте репозитрий 
```
git clone https://github.com/Peshkov-Matvei/foodgram-project-react.git
```
- Войдите в папку infra/
- Создайте файл .env и заполнети его
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
DB_HOST=db
DB_PORT=5432
SECRET_KEY='Secret key'
```
- соберите образ docker-compoce
```
docker-compose up -d --build
```
- Запустите миграции
```
docker-compose exec backend python manage.py migrate
```
- Запустите статику
```
docker-compose exec backend python manage.py collectstatic --no-input
```
- Создайте суперюзера
```
docker-compose exec backend python manage.py createsuperuser
```
### Автор проекта
Пешков Матвей студент ЯндексПрактикума
