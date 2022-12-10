from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

from courses.models import Lesson

# Create your models here.


class User(AbstractUser):

    CLIENT = 'C'
    TEACHER = 'T'
    MANAGER = 'M'
    HEAD_MANAGER = 'H'

    ROLES = (
        (CLIENT, 'Клиент'),
        (TEACHER, 'Преподаватель'),
        (MANAGER, 'Менеджер'),
        (HEAD_MANAGER, 'Старший менеджер')
    )

    NOT_CLIENT = 'N'
    QUEUED = 'Q'
    ACTUAL = 'C'
    VIP = 'V'

    STATUSES = (
        (NOT_CLIENT, 'Возможный клиент'),
        (QUEUED, 'В очереди'),
        (ACTUAL, 'Записан на курсы'),
        (VIP, 'Постоянный клиент'),
    )

    id = models.UUIDField(primary_key=True, default=uuid4)
    role = models.CharField(
        verbose_name='роль',
        max_length=1,
        choices=ROLES,
        null=False,
        default='C'
    )
    phone = models.CharField(
        verbose_name='Номер телефона', blank=True, max_length=15
    )
    lessons = models.ManyToManyField(
        Lesson, related_name='users', blank=True)
    manager = models.ForeignKey(
        'self', verbose_name='Персональный менеджер',
        on_delete=models.SET_NULL,
        related_name='users',
        null=True,
        blank=True
    )
    salary = models.FloatField(verbose_name='ставка', null=True, blank=True)
    percent_salary = models.IntegerField(verbose_name='надбавка в процентах',
                                         null=True, blank=True)
    created_at = models.DateTimeField(verbose_name='дата регистрации',
                                      auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='последнее обновление',
                                      auto_now=True)

    comment = models.TextField(verbose_name='комментарий', blank=True)
    status = models.CharField(
        verbose_name='статус клиента',
        max_length=1,
        choices=STATUSES,
        default=NOT_CLIENT,
        null=False
    )

    class Meta:
        ordering = ["id"]

    @property
    def verbose_status(self):
        for item in self.STATUSES:
            if item[0] == self.status:
                return item[1]

    @property
    def courses(self):
        return list(set([x.course for x in self.lessons.all()]))

    def get_absolute_url(self):
        return reverse(
            'user-detail',
            # kwargs={'pk': self.pk}
        )

    def __str__(self):
        return self.get_full_name()
