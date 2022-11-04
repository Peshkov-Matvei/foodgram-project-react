from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username',
        'first_name',
        'last_name',
    ]
    email = models.EmailField(
        verbose_name='email',
        max_length=128,
        unique=True,
        help_text='Введите пароль',
    )

    def __str__(self):
        return self.username

    class Meta():
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользоватили'
        ordering = ('username',)


class Subscribe(models.Model):

    user = models.ForeignKey(
        User,
        related_name='subscriber',
        verbose_name='Подписчик',
        help_text='Выберите пользователя',
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        User,
        related_name='subscribing',
        verbose_name='Автор',
        help_text='Выберите автора',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'Пользователь {self.user} подписан на {self.author}'

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = (models.UniqueConstraint(
            fields=['user', 'author'], name='unique_follow'
        ),)
