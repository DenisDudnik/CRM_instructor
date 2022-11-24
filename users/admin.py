from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Course, CourseType, Lesson, User

# Register your models here.

admin.site.register(User, UserAdmin)
admin.site.register(Lesson)
admin.site.register(Course)
admin.site.register(CourseType)
