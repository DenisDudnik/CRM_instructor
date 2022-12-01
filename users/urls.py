from django.urls import path

import users.views as users

app_name = 'users'

urlpatterns = [
    path('login/', users.login, name='login'),
    path('logout/', users.logout, name='logout'),
    path('edit-profile/', users.profile_edit, name='edit_profile'),
]
