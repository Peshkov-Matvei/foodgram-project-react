from django.db import models


class Users(models.Model):

    first_name = models.CharField(
        max_length=128,
        unique=True,
        help_text='Введите имя',
    )
    second_name = models.CharField(
        max_length=128,
        unique=True,
        help_text='Введите фамилию',
    )
    username = models.CharField(
        max_length=128,
        unique=True,
        help_text='Введите логин',
    )
    email = models.EmailField(
        max_length=128,
        unique=True,
        help_text='Введите эмейл',
    )
    password = models.CharField(
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


class Subscription(models.Model):

    user = models.ForeignKey(
        Users,
        related_name='follower',
        verbose_name='Пользователь',
        help_text='Выберите пользователя',
        on_delete=models.CASCADE,
    )
    author = models.ForeignKey(
        Users,
        related_name='following',
        verbose_name='Автор',
        help_text='Выберите автора',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.user, self.author

    class Meta():
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
