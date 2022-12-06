from django import forms

from courses.models import Course, Lesson
from users.models import User


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ('kind', 'title', 'description',)
        # fields = '__all__'


class CourseSubscribeForm(forms.Form):

    role = None

    def __init__(
            self, *args,
            course_item: Course, role: str, manager: str,
            lesson_item: Lesson = None,
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        course_field = self.fields.get('course')
        course_field.queryset = Course.objects.filter(pk=course_item.pk)
        course_field.initial = course_item
        # course_field.widget.attrs['disabled'] = True
        lesson_field = self.fields.get('lesson')
        if lesson_item:
            lesson_field.queryset = Lesson.objects.filter(pk=lesson_item.pk)
            lesson_field.initial = lesson_item
        else:
            lesson_field.queryset = course_item.lessons.all()
        # lesson_field.widget.attrs['disabled'] = True

        user_field = self.fields.get('user')
        user_field.queryset = User.objects.filter(role__exact=role).filter(
            manager_id=manager
        )

    course = forms.ModelChoiceField(queryset=Course.objects.all())
    lesson = forms.ModelChoiceField(
        queryset=Lesson.objects.all(), required=False
    )
    user = forms.ModelChoiceField(
        User.objects.filter(role__exact=role)
    )
