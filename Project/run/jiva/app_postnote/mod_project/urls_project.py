
from django.urls import path, include

from app.app_postnote.mod_project import views_project

urlpatterns = [
    # app_postnote/projects: DB/Model: Project
    path('list_projects/', views_project.list_projects, name='list_projects'),
    path('list_deleted_projects/', views_project.list_deleted_projects, name='list_deleted_projects'),
    path('create_project/', views_project.create_project, name='create_project'),
    path('edit_project/<int:project_id>/', views_project.edit_project, name='edit_project'),
    path('delete_project/<int:project_id>/', views_project.delete_project, name='delete_project'),
    path('permanent_deletion_project/<int:project_id>/', views_project.permanent_deletion_project, name='permanent_deletion_project'),
    path('restore_project/<int:project_id>/', views_project.restore_project, name='restore_project'),
    path('view_project/<int:project_id>/', views_project.view_project, name='view_project'),
]
