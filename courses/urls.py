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
                           CourseDetailView, CourseListView,
                           CourseTypeCreateView, CourseTypeDeleteView,
                           CourseTypeDetailView, CourseTypeListView,
                           CourseTypeUpdateView, CourseUpdateView,
                           LessonCreateView, LessonDeleteView,
                           LessonDetailView, LessonEditView, subscribe,
                           unsubscribe)

app_name = CoursesConfig.name

urlpatterns = [
    path("", CourseListView.as_view(), name='list'),
    path("<int:pk>/", CourseDetailView.as_view(), name='detail'),
    path("<int:pk>/update/", CourseUpdateView.as_view(), name='update'),
    path("<int:pk>/delete/", CourseDeleteView.as_view(), name='delete'),
    path("create/", CourseCreateView.as_view(), name='create'),

    path("type_list/", CourseTypeListView.as_view(), name='type_list'),
    path("<int:pk>/", CourseTypeDetailView.as_view(), name='type_detail'),
    path("<int:pk>/update_type/", CourseTypeUpdateView.as_view(), name='update_type'),
    path("<int:pk>/delete_type/", CourseTypeDeleteView.as_view(), name='delete_type'),
    path("create_type/", CourseTypeCreateView.as_view(), name='create_type'),

    path("subscribe/<int:course_id>/<int:lesson_id>/<str:role>/", subscribe, name='subscribe'),
    path("subscribe/<int:course_id>/<int:lesson_id>/<str:role>/", subscribe,
         name='subscribe'),
    path("unsubscribe/", unsubscribe, name='unsubscribe'),
    path('create_lesson/<int:pk>/', LessonCreateView.as_view(),
         name='create-lesson'),
    path('lesson_detail/<int:pk>/', LessonDetailView.as_view(),
         name='lesson-detail'),
    path('lesson_delete/<int:pk>/', LessonDeleteView.as_view(),
         name='lesson-delete'),
    path('lesson_edit/<int:pk>/', LessonEditView.as_view(),
         name='lesson-edit'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
