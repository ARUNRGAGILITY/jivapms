from django.urls import path
from . import views

urlpatterns = [

    path('', views.user_management, name='user_management'),


    path('add_user/', views.add_user, name='add_user'),
    path('modify_user/<int:user_id>/', views.modify_user, name='modify_user'),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('bulk_add_users/', views.bulk_add_users, name='bulk_add_users'),
    path('bulk_delete_users/', views.bulk_delete_users, name='bulk_delete_users'),
    path('bulk_undelete_users/', views.bulk_undelete_users, name='bulk_undelete_users'),
    path('bulk_modify_users/', views.bulk_modify_users, name='bulk_modify_users'),    
    path('bulk_add_users_from_csv/', views.bulk_add_users_from_csv, name='bulk_add_users_from_csv'),

    path('export-users/', views.export_users, name='export_users'),
    path('export-selected-users/', views.export_selected_users, name='export_selected_users'),
]