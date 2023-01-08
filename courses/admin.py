from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from courses.models import Course, CourseType, Lesson

# Register your models here.


admin.site.register(Lesson)
admin.site.register(Course)
admin.site.register(CourseType)
