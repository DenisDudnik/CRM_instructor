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
                           subscribe, unsubscribe)

app_name = CoursesConfig.name

urlpatterns = [
    path("", CourseListView.as_view(), name='list'),
    path("<int:pk>/", CourseDetailView.as_view(), name='detail'),
    path("<int:pk>/update/", CourseUpdateView.as_view(), name='update'),
    path("<int:pk>/delete/", CourseDeleteView.as_view(), name='delete'),
    path("create/", CourseCreateView.as_view(), name='create'),
    path("subscribe/<int:course_id>/<int:lesson_id>/<str:role>/", subscribe, name='subscribe'),
    path("unsubscribe/", unsubscribe, name='unsubscribe'),
    # path("devitem/<uuid:pk>/", DevItemDetailView.as_view(), name='devitem_detail'),
    # path("devitem/<uuid:pk>/edit/",
    #      DevItemUpdateView.as_view(), name='devitem_update'),
    # path("devitem/add/<str:ip>/<str:mac>/",
    #      DevItemCreateView.as_view(), name='devitem_add'),
    # path("devitem/<uuid:pk>/delete/",
    #      DevItemDeleteView.as_view(), name='devitem_delete'),
    # path("devmodel/<uuid:pk>/", DevModelDetailView.as_view(), name='devmodel_detail'),
    # path("devmodel/add/", DevModelCreateView.as_view(), name='devmodel_add'),
    # path("devmodel/<uuid:pk>/edit/",
    #      DevModelUpdateView.as_view(), name='devmodel_update'),
    # path("devmodel/<uuid:pk>/delete/",
    #      DevModelDeleteView.as_view(), name='devmodel_delete'),
    # path("devmodel/<uuid:pk>/addphoto/",
    #      DevModelPhotoCreateView.as_view(), name='devmodelphoto_add'),
    # path("devmodel/photo/<uuid:pk>/delete/",
    #      DevModelPhotoDeleteView.as_view(), name='devmodelphoto_del'),
    # path("devmodel/<uuid:pk>/addfile/",
    #      DevModelFileCreateView.as_view(), name='devmodelfile_add'),
    #  path("devmodel/file/<uuid:pk>/delete/",
    #      DevModelFileDeleteView.as_view(), name='devmodelfile_del'),
    # path("nets/add/", NetsCreateView.as_view(), name='nets_add'),
    # path("nets/<uuid:pk>/edit/", NetsUpdateView.as_view(), name='nets_update'),
    # path("nets/<uuid:pk>/delete/", NetsDeleteView.as_view(), name='nets_delete'),
    #     path("login/", LoginPage.as_view(), {'title': 'вход'}, name='login'),
    #     path("logout/", LogoutPage.as_view(), {'title': 'выход'}, name='logout'),
    #     path("user/<pk>/", ProfilePage.as_view(), {'title': 'просмотр профиля'}, name='user-detail'),
    #     path("user/<pk>/edit/", ProfileEditPage.as_view(), {'title': 'редактирование профиля'}, name='user-edit'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
