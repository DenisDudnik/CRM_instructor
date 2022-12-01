import datetime
from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

# Create your models here.


class CourseType(models.Model):
    """Направление обучения (лыжи, сноуборд, кройка и шитье, что угодно...)"""
    title = models.CharField(
        verbose_name='Направление', max_length=255, null=False
    )


class Course(models.Model):
    """Курс обучения"""
    kind = models.ForeignKey(
        CourseType, related_name='courses', on_delete=models.CASCADE
    )
    title = models.CharField(
        verbose_name='Название', max_length=255, null=False
    )
    description = models.TextField(
        blank=True, verbose_name='Описание', null=True)

    @property
    def cost(self):
        return sum(x.cost for x in self.lessons.all())

    @property
    def duration(self) -> int:
        if not len(self.lessons.all()):
            return 0
        if len(self.lessons.all()) == 1:
            return self.lessons[0].duration
        lessons = list(self.lessons.all())
        return (
            (lessons[-1].date + datetime.timedelta(
                minutes=lessons[-1].duration
            )).timestamp() - lessons[0].date.timestamp()
        ) / 60


class Lesson(models.Model):
    """Отдельный урок"""
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='lessons', null=True
    )
    description = models.TextField(blank=True, null=True,
                                   verbose_name='Описание')
    address = models.CharField(
        max_length=255, verbose_name='Место проведения', blank=False
    )
    date = models.DateTimeField(verbose_name='Дата начала', blank=False)
    duration = models.IntegerField(
        verbose_name='Продолжительность занятия в минутах', default=0
    )
    cost = models.FloatField(verbose_name='Стоимость участия', null=False)


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

    class Meta:
        ordering = ["id"]

    @property
    def courses(self):
        return list(set([x.course for x in self.lessons.all()]))

    def get_absolute_url(self):
        return reverse(
            'user-detail',
            # kwargs={'pk': self.pk}
        )
