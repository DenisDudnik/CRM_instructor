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
    path('password-reset/', users.UserPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', users.UserPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         users.UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset-complete/', users.UserPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
