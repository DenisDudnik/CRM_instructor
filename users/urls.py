from django.urls import path

import users.views as users

app_name = 'users'

urlpatterns = [
    path('login/', users.login, name='login'),
    path('logout/', users.logout, name='logout'),
    path('edit-profile/', users.profile_edit, name='edit_profile'),
    path('create-user/<str:role>/', users.create_user, name='create_user'),
    path('detail-user/<uuid:pk>/',
         users.UserDetailView.as_view(), name='detail_user'),
    path('edit-user/<uuid:pk>/', users.UserEditView.as_view(), name='user_edit'),
    path('change-password/', users.UserPasswordEditView.as_view(success_url='/'), name='change_password'),
]
