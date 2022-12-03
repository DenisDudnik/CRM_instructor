import datetime

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