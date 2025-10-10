from django.urls import path
from app_organization.mod_project_board_cos import views_project_board_cos

urlpatterns = [
    path('list/<int:project_id>/', views_project_board_cos.list_project_board_cos, name='list_project_board_cos'),
    path('deleted/<int:project_id>/', views_project_board_cos.list_deleted_project_board_cos, name='list_deleted_project_board_cos'),
    path('create/<int:project_id>/', views_project_board_cos.create_project_board_cos, name='create_project_board_cos'),
    path('edit/<int:project_id>/<int:cos_id>/', views_project_board_cos.edit_project_board_cos, name='edit_project_board_cos'),
    path('delete/<int:project_id>/<int:cos_id>/', views_project_board_cos.delete_project_board_cos, name='delete_project_board_cos'),
    path('permadelete/<int:project_id>/<int:cos_id>/', views_project_board_cos.permanent_deletion_project_board_cos, name='permanent_deletion_project_board_cos'),
    path('view/<int:project_id>/<int:cos_id>/', views_project_board_cos.view_project_board_cos, name='view_project_board_cos'),
]
