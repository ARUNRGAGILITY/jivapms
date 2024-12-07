
from django.urls import path, include


from app_organization.mod_backlog import views_backlog
from app_organization.mod_backlog import views_story_map


urlpatterns = [
    # app_automate/contents: DB/Model: Content
    path('list_backlogs/<int:pro_id>/<int:parent_id>/', views_backlog.list_backlogs, name='list_backlogs'),
    path('list_deleted_backlogs/<int:pro_id>/<int:parent_id>/', views_backlog.list_deleted_backlogs, name='list_deleted_backlogs'),
    path('create_backlog/<int:pro_id>/<int:parent_id>/', views_backlog.create_backlog, name='create_backlog'),
    path('edit_backlog/<int:pro_id>/<int:parent_id>/<int:content_id>/', views_backlog.edit_backlog, name='edit_backlog'),
    path('copy_backlog/<int:pro_id>/<int:parent_id>/<int:content_id>/', views_backlog.copy_backlog, name='copy_backlog'),
    path('delete_backlog/<int:pro_id>/<int:parent_id>/<int:content_id>/', views_backlog.delete_backlog, name='delete_backlog'),
    path('permanent_deletion_backlog/<int:pro_id>/<int:parent_id>/<int:content_id>/', views_backlog.permanent_deletion_backlog, name='permanent_deletion_backlog'),
    path('restore_backlog/<int:pro_id>/<int:parent_id>/<int:content_id>/', views_backlog.restore_backlog, name='restore_backlog'),
    path('view_backlog/<int:pro_id>/<int:parent_id>/<int:content_id>/', views_backlog.view_backlog, name='view_backlog'),
    path('view_tree__backlog/<int:pro_id>/<int:parent_id>/', views_backlog.view_tree__backlog, name='view_tree__backlog'),
    
    path('iterate__backlog/<int:pro_id>/<int:parent_id>/', views_backlog.iterate__backlog, name='iterate__backlog'), 
    path('story_mapping_backlog/<int:pro_id>/<int:parent_id>/', views_backlog.story_mapping_backlog, name='story_mapping_backlog'),
    # ajax updates
    path('ajax_get_iterations/<int:release_id>/', views_backlog.ajax_get_iterations, name='ajax_get_iterations'),
    path('ajax_fetch_persona_activities/', views_backlog.ajax_fetch_persona_activities, name='ajax_fetch_persona_activities'),    
    path('ajax_recieve_story_mapped_details/', views_backlog.ajax_recieve_story_mapped_details, name='ajax_recieve_story_mapped_details'),
    path('ajax_story_back_to_list/', views_backlog.ajax_story_back_to_list, name='ajax_story_back_to_list'),
    
    # new feature
    path('create_story_map/<int:org_id>/', views_story_map.create_story_map, name='create_story_map'),
    path('create_story_map_from_backlog/<int:pro_id>/', views_story_map.create_story_map_from_backlog, name='create_story_map_from_backlog'),
    path('create_backlog_from_story_map/<int:pro_id>/', views_story_map.create_backlog_from_story_map, name='create_backlog_from_story_map'),
    
]
