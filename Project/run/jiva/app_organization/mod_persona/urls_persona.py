
from django.urls import path, include

from app_organization.mod_persona import views_persona


urlpatterns = [
    # app_organization/personae: DB/Model: Persona
    path('list_personae/<int:organization_id>/', views_persona.list_personae, name='list_personae'),    
    path('list_deleted_personae/<int:organization_id>/', views_persona.list_deleted_personae, name='list_deleted_personae'),
    path('create_persona/<int:organization_id>/', views_persona.create_persona, name='create_persona'),
    path('edit_persona/<int:organization_id>/<int:persona_id>/', views_persona.edit_persona, name='edit_persona'),
    path('delete_persona/<int:organization_id>/<int:persona_id>/', views_persona.delete_persona, name='delete_persona'),
    path('permanent_deletion_persona/<int:organization_id>/<int:persona_id>/', views_persona.permanent_deletion_persona, name='permanent_deletion_persona'),
    path('restore_persona/<int:organization_id>/<int:persona_id>/', views_persona.restore_persona, name='restore_persona'),
    path('view_persona/<int:organization_id>/<int:persona_id>/', views_persona.view_persona, name='view_persona'),
    
    # added
    path('list_project_personae/<int:organization_id>/<int:project_id>/', views_persona.list_project_personae, name='list_project_personae'),

    path('create_persona_with_project_id/<int:organization_id>/<int:project_id>/', views_persona.create_persona_with_project_id, name='create_persona_with_project_id'),
]
