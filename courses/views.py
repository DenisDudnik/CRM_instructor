from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from django.views.generic.list import ListView

from courses.forms import CourseForm, CourseSubscribeForm, LessonCreateForm
from courses.models import Course, Lesson
from users.models import User

# Create your views here.


def unsubscribe(request):
    course_id = request.POST.get('course')
    course = Course.objects.get(pk=course_id)
    lessons = course.lessons.all()
    user = request.user
    for lesson in lessons:
        if lesson in user.lessons.all():
            user.lessons.remove(lesson)
    user.save()
    return HttpResponseRedirect(reverse('courses:list'))


def subscribe(request, course_id=None, lesson_id=None, role: str = None):
    course = None
    lesson = None
    if course_id:
        course = Course.objects.get(pk=course_id)
    if lesson_id:
        lesson = Lesson.objects.get(pk=lesson_id)
    if request.method == 'POST':
        form = CourseSubscribeForm(
            request.POST,
            role=role,
            manager=request.user.pk,
            course_item=course,
            lesson_item=lesson
        )
        if form.is_valid():
            user_id = form.data.get('user')
            user = User.objects.get(pk=user_id)
            lesson_id = form.data.get('lesson')
            if lesson_id:
                lesson = Lesson.objects.get(pk=int(lesson_id))
            course = Course.objects.get(pk=int(form.data.get('course')))
            if lesson:
                user.lessons.add(lesson)
            else:
                for lesson in course.lessons.all():
                    user.lessons.add(lesson)
            user.save()
            return HttpResponseRedirect(
                reverse('auth:detail_user', kwargs={'pk': user.pk})
            )
    form = CourseSubscribeForm(
        role=role,
        manager=request.user.pk,
        course_item=course or None,
        lesson_item=lesson or None
    )
    return render(request, 'courses/form.html',
                  {'form': form, 'button': 'Сохранить'})


class CourseListView(ListView):
    model = Course
    template_name = 'courses/course_list.html'
    extra_context = {
        'title': 'список курсов',
    }

    def get_queryset(self):
        queryset = Course.objects.all()
        if self.request.user.role == User.MANAGER:
            queryset = queryset
        if self.request.user.role in [User.CLIENT, User.TEACHER]:
            ids = [x.pk for x in self.request.user.courses]
            queryset = queryset.filter(pk__in=ids)
        return queryset


class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course_detail.html'
    extra_context = {
        'title': 'детали курса',
    }


class CourseUpdateView(UpdateView):
    model = Course
    template_name = 'courses/form.html'
    extra_context = {
        'title': 'редактирование курса',
        'button': 'сохранить',
    }
    form_class = CourseForm


class CourseCreateView(CreateView):
    model = Course
    template_name = 'courses/form.html'
    extra_context = {
        'title': 'создание курса',
        'button': 'сохранить',
    }
    form_class = CourseForm


class CourseDeleteView(DeleteView):
    model = Course
    success_url = reverse_lazy('courses:list')
    extra_context = {
        'title': 'удаление курса',
        'button': 'удалить',
    }


class LessonCreateView(LoginRequiredMixin, CreateView):

    model = Lesson
    template_name = 'courses/form.html'
    extra_context = {
        'title': 'Создание урока',
        'button': 'Сохранить'
    }
    form_class = LessonCreateForm

    @method_decorator(user_passes_test(
        lambda user: user.role in [User.MANAGER, User.HEAD_MANAGER]
    ))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class LessonDetailView(LoginRequiredMixin, DetailView):

    model = Lesson
    template_name = 'courses/lesson_detail.html'
    extra_context = {
        'title': 'Иноформация об уроке'
    }
