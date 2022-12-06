import json

from django.core.management.base import BaseCommand
from django.utils import timezone

from courses.models import Course, CourseType
from users.models import Lesson, User


def load_from_json(file_name):
    with open(file_name, mode='r', encoding='utf-8') as infile:

        return json.load(infile)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--user", required=True)
        parser.add_argument("--password", required=True)
        parser.add_argument("--email", default="admin@example.com")

    def handle(self, *args, **options):
        course_types = load_from_json('users/fixtures/course_types.json')

        CourseType.objects.all().delete()
        for course_type in course_types:
            c_type = course_type.get('fields')
            c_type['id'] = course_type.get('pk')
            new_type = CourseType(**c_type)
            new_type.save()

        courses = load_from_json('users/fixtures/courses.json')

        Course.objects.all().delete()
        for course in courses:
            course_item = course.get('fields')
            course_type = course_item.get('kind')
            _course_type = CourseType.objects.get(id=course_type)
            course_item['kind'] = _course_type
            new_course = Course(**course_item)
            new_course.save()

        lessons = load_from_json('users/fixtures/lessons.json')

        Lesson.objects.all().delete()
        for lesson in lessons:
            lesson_item = lesson.get('fields')
            _course = Course.objects.order_by('?').first()
            lesson_item['course'] = _course
            new_lesson = Lesson(**lesson_item)
            new_lesson.date = timezone.now()
            new_lesson.save()

        users = load_from_json('users/fixtures/users.json')

        User.objects.all().delete()

        username = options["user"]
        password = options["password"]
        email = options["email"]

        User.objects.create_superuser(username=username, password=password, email=email)

        self.stdout.write(f'Local user "{username}" was created')

        for user in users:
            user_item = user.get('fields')
            new_user = User(**user_item)
            new_user.set_password(password)
            new_user.save()

        managers = User.objects.filter(role="M")

        for user in User.objects.all():
            if user.role == "C":
                user.manager = managers.order_by('?').first()
                user.save()
