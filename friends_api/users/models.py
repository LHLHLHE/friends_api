from django.contrib.auth.models import AbstractUser
from django.db import models

FRIENDSHIP_REQUEST_STATUSES = (
    ('sent', 'Заявка отправлена'),
    ('rejected', 'Заявка отклонена')
)


class User(AbstractUser):
    username = models.CharField(
        max_length=256,
        unique=True,
        verbose_name='Логин'
    )
    friends = models.ManyToManyField('User', blank=True)

    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


class FriendshipRequest(models.Model):
    from_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='from_me_requests',
        verbose_name='Отправитель'
    )
    to_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='to_me_requests',
        verbose_name='Получатель'
    )
    status = models.CharField(
        max_length=150,
        choices=FRIENDSHIP_REQUEST_STATUSES,
        blank=True,
        default='sent',
        verbose_name='Статус заявки'
    )

    class Meta:
        verbose_name = 'Заявка в друзья'
        verbose_name_plural = 'Заявки в друзья'

    def __str__(self):
        return f'{self.from_user} --- {self.to_user}: {self.status}'
