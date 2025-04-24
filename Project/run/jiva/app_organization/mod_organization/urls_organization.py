
from django.urls import path, include

from app_organization.mod_organization import views_organization

urlpatterns = [
    # app_organization/organizations: DB/Model: Organization
    
    path('org_homepage/<int:org_id>/', views_organization.org_homepage, name='org_homepage'),
    path('list_organizations/', views_organization.list_organizations, name='list_organizations'),
    path('list_deleted_organizations/', views_organization.list_deleted_organizations, name='list_deleted_organizations'),
    path('create_organization/', views_organization.create_organization, name='create_organization'),
    path('edit_organization/<int:organization_id>/', views_organization.edit_organization, name='edit_organization'),
    path('delete_organization/<int:organization_id>/', views_organization.delete_organization, name='delete_organization'),
    path('permanent_deletion_organization/<int:organization_id>/', views_organization.permanent_deletion_organization, name='permanent_deletion_organization'),
    path('restore_organization/<int:organization_id>/', views_organization.restore_organization, name='restore_organization'),
    path('view_organization/<int:organization_id>/', views_organization.view_organization, name='view_organization'),
    path('dashboard_organizations/', views_organization.dashboard_organizations, name='dashboard_organizations'),
]
