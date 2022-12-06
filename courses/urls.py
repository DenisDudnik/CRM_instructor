"""portal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from courses.apps import CoursesConfig
from courses.views import (CourseCreateView, CourseDeleteView,
                           CourseDetailView, CourseListView, CourseUpdateView,
                           LessonCreateView, LessonDetailView, subscribe,
                           unsubscribe)

app_name = CoursesConfig.name

urlpatterns = [
    path("", CourseListView.as_view(), name='list'),
    path("<int:pk>/", CourseDetailView.as_view(), name='detail'),
    path("<int:pk>/update/", CourseUpdateView.as_view(), name='update'),
    path("<int:pk>/delete/", CourseDeleteView.as_view(), name='delete'),
    path("create/", CourseCreateView.as_view(), name='create'),
    path("subscribe/<int:course_id>/<int:lesson_id>/<str:role>/", subscribe,
         name='subscribe'),
    path("unsubscribe/", unsubscribe, name='unsubscribe'),
    path('create_lesson/<int:pk>/', LessonCreateView.as_view(),
         name='create-lesson'),
    path('lesson_dateil/<int:pk>/', LessonDetailView.as_view(),
         name='lesson-detail')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
