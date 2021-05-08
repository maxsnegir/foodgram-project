from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError


class User(AbstractUser):
    email = models.EmailField(unique=True, )

    class Meta(AbstractUser.Meta):
        ordering = ['username']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='follower', )
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='following', )

    def clean(self):
        if self.user == self.author:
            raise ValidationError(
                'Пользователь не может подписываться на самого себя')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'author'],
                                    name='unique_followers'),
        ]
