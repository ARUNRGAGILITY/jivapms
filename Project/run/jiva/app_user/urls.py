from django.urls import path, include

from . import views as app_user_views

urlpatterns = [
    # user with basic login system
    path('login_page/', app_user_views.login_page, name="login_page"),
    path('logout_page/', app_user_views.logout_page, name="logout_page"),
    path('register_page/',app_user_views.register_page, name="register_page"),
    path('profile/',app_user_views.profile, name="profile"),
    path('password_change/', app_user_views.CustomPasswordChangeView.as_view(), name='password_change'),
    path('user_home/', app_user_views.user_home, name="user_home"),
    path('user_settings/', app_user_views.user_settings, name="user_settings"),


    path('users/', app_user_views.user_list, name='user_list'),
    path('admin/users/<int:user_id>/', app_user_views.user_detail, name='user_detail'),
    path('profile/update/', app_user_views.profile_update, name='profile_update'),
    
    path('dashboard', app_user_views.dashboard, name='dashboard'),

    path('admin/dashboard/', app_user_views.admin_dashboard, name='admin_dashboard'),
    path('admin/users/batch-upload/', app_user_views.batch_user_upload, name='batch_user_upload'),
    path('admin/users/create/', app_user_views.create_user, name='create_user'),
    path('admin/users/edit/<int:user_id>/', app_user_views.edit_user, name='edit_user'),
    path('admin/users/delete/<int:user_id>/', app_user_views.delete_user, name='delete_user'),
    path('admin/users/bulk-actions/', app_user_views.bulk_user_actions, name='bulk_user_actions'),
]
