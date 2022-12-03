from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy

from courses.models import Course
from courses.forms import CourseForm
from users.models import User

# Create your views here.

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
        if self.request.user.role == User.CLIENT:
            queryset = queryset.filter(title="Курс 1")
        if self.request.user.role == User.TEACHER:
            queryset = queryset.filter(title="Курс 2")
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