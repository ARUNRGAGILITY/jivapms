from django.urls import path
from . import views

app_name = 'app_authz'

urlpatterns = [
    # Member URLs
    path('org/<int:org_id>/members/', views.member_list, name='member_list'),
    path('org/<int:org_id>/members/create/', views.member_create, name='member_create'),
    path('org/<int:org_id>/members/<int:member_id>/update/', views.member_update, name='member_update'),
    path('org/<int:org_id>/members/<int:member_id>/delete/', views.member_delete, name='member_delete'),
    path('org/<int:org_id>/members/batch-upload/', views.member_batch_upload, name='member_batch_upload'),
    
    # Member Role URLs
    path('org/<int:org_id>/member-roles/', views.member_role_list, name='member_role_list'),
    path('org/<int:org_id>/member-roles/create/', views.member_role_create, name='member_role_create'),
    path('org/<int:org_id>/member-roles/<int:role_id>/update/', views.member_role_update, name='member_role_update'),
    path('org/<int:org_id>/member-roles/<int:role_id>/delete/', views.member_role_delete, name='member_role_delete'),
    path('org/<int:org_id>/member-roles/batch-upload/', views.member_role_batch_upload, name='member_role_batch_upload'),
]