from django.shortcuts import render
from django.views.generic.list import ListView

from courses.models import Course

# Create your views here.

class CourseListView(ListView):

    model = Course
    template_name = 'courses/courses_list.html'
    extra_context = {
        'title': 'список устройств',
    }
