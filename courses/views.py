from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from django.views.generic.list import ListView

from courses.forms import (CourseForm, CourseSubscribeForm, CourseTypeForm,
                           LessonCreateForm)
from courses.models import Course, CourseType, Lesson
from users.models import User

# Create your views here.


def unsubscribe(request):
    course_id = request.POST.get('course')
    lesson_id = request.POST.get('lesson')
    lesson = Lesson.objects.get(pk=lesson_id)
    course = Course.objects.get(pk=course_id)
    lessons = course.lessons.all()
    user = request.user
    if lesson:
        if lesson in user.lessons.all():
            user.lessons.remove(lesson)
    else:
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
            manager=request.user,
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
            if lesson_id:
                return HttpResponseRedirect(
                    reverse('courses:lesson-detail', kwargs={'pk': lesson_id})
                )
            return HttpResponseRedirect(
                reverse('courses:detail', kwargs={'pk': course_id})
            )
    form = CourseSubscribeForm(
        role=role,
        manager=request.user,
        course_item=course or None,
        lesson_item=lesson or None
    )
    context = {
        'form': form,
        'button': 'Сохранить',
        'back': reverse(
            'courses:detail', kwargs={'pk': course_id}
        )
    }
    return render(request, 'courses/form.html', context)


class CourseListView(ListView):
    model = Course
    template_name = 'courses/course_list.html'
    extra_context = {
        'title': 'список курсов',
        'kinds': CourseType.objects.all()
    }

    def get_queryset(self):
        queryset = Course.objects.all()
        filtering = self.request.GET.get('filter')
        if filtering:
            queryset = queryset.filter(kind_id=filtering)
        if self.request.user.role == User.MANAGER:
            queryset = queryset
        if self.request.user.role in [User.CLIENT, User.TEACHER]:
            ids = [x.pk for x in self.request.user.courses]
            queryset = queryset.filter(pk__in=ids)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filtering = self.request.GET.get('filter')
        if filtering:
            context.update({'filtered': int(self.request.GET.get('filter'))})
        return context


class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/course_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = Course.objects.get(pk=self.kwargs['pk'])
        lessons = course.lessons.all()
        context['clients'] = User.objects.filter(
            lessons__in=lessons, role="C"
        ).distinct()

        return context

    extra_context = {
        'title': 'детали курса',
        'back': reverse_lazy('courses:list')
    }


class CourseUpdateView(UpdateView):
    model = Course
    template_name = 'courses/form.html'
    extra_context = {
        'title': 'редактирование курса',
        'button': 'сохранить'
    }
    form_class = CourseForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # form = CourseForm(instance=self.object)
        context['back'] = reverse_lazy('courses:detail', kwargs={
            'pk': self.object.pk
        })
        # context.update({
        #     'title': 'редактирование курса',
        #     'button': 'сохранить',
        #     'form': form
        # })
        return context


class CourseCreateView(CreateView):
    model = Course
    template_name = 'courses/form.html'
    success_url = reverse_lazy('courses:list')
    extra_context = {
        'title': 'создание курса',
        'button': 'сохранить',
        'back': reverse_lazy('courses:list')
    }
    form_class = CourseForm


class CourseDeleteView(DeleteView):
    model = Course
    success_url = reverse_lazy('courses:list')
    extra_context = {
        'title': 'удаление курса',
        'button': 'удалить',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back'] = reverse_lazy('courses:detail', kwargs={
            'pk': self.kwargs['pk']
        })
        return context


class CourseTypeListView(ListView):
    model = CourseType
    template_name = 'courses/course_type_list.html'
    extra_context = {
        'title': 'список типов курсов',
    }

    def get_queryset(self):
        queryset = CourseType.objects.all()
        if self.request.user.role == User.MANAGER:
            queryset = queryset
        if self.request.user.role in [User.CLIENT, User.TEACHER]:
            ids = [x.pk for x in self.request.user.course_type]
            queryset = queryset.filter(pk__in=ids)
        return queryset


class CourseTypeCreateView(CreateView):
    model = CourseType
    template_name = 'courses/form.html'
    success_url = reverse_lazy('courses:type_list')
    extra_context = {
        'title': 'создание типа курса',
        'button': 'сохранить',
    }
    form_class = CourseTypeForm


class CourseTypeDetailView(DetailView):
    model = CourseType
    template_name = 'courses/course_type_detail.html'
    extra_context = {
        'title': 'детали типа',
    }


class CourseTypeUpdateView(UpdateView):
    model = CourseType
    template_name = 'courses/form.html'
    success_url = reverse_lazy('courses:type_list')
    extra_context = {
        'title': 'редактирование типа курса',
        'button': 'сохранить',
    }
    form_class = CourseTypeForm


class CourseTypeDeleteView(DeleteView):
    model = CourseType
    success_url = reverse_lazy('courses:type_list')
    extra_context = {
        'title': 'удаление типа курса',
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back'] = reverse('courses:detail', kwargs={
            'pk': self.kwargs['pk']
        })
        return context

    def get_form(self, form_class=None):
        form = super().get_form()
        form.set_course(Course.objects.get(pk=self.kwargs.get('pk')))
        return form


class LessonDetailView(LoginRequiredMixin, DetailView):

    model = Lesson
    template_name = 'courses/lesson_detail.html'
    extra_context = {
        'title': 'Иноформация об уроке'
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['teachers'] = [
            x for x in context['object'].users.all() if x.role == User.TEACHER
        ]
        context['clients'] = [
            x for x in context['object'].users.all() if x.role == User.CLIENT
        ]
        context['back'] = reverse_lazy('courses:detail', kwargs={
            'pk': self.object.course.pk}
        )
        return context


class LessonDeleteView(LoginRequiredMixin, DeleteView):

    model = Lesson
    extra_context = {
        'title': 'удаление урока',
        'button': 'удалить',
    }

    def get_success_url(self):
        return reverse_lazy('courses:detail', kwargs={
            'pk': self.object.course.pk}
        )

    @method_decorator(user_passes_test(lambda u: u.role in [User.MANAGER, User.HEAD_MANAGER]))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back'] = reverse_lazy('courses:lesson-detail', kwargs={
            'pk': self.kwargs['pk']
        })
        return context


class LessonEditView(LoginRequiredMixin, UpdateView):
    form_class = LessonCreateForm
    template_name = 'courses/form.html'
    extra_context = {
        'title': 'редактирование урока',
        'button': 'сохранить',
    }
    model = Lesson

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['back'] = reverse('courses:lesson-detail', kwargs={
            'pk': self.kwargs['pk']
        })
        return context
