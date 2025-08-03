
from django.urls import path, include


from app_organization.mod_backlog import views_backlog
from app_organization.mod_backlog import views_story_map
from app_organization.mod_backlog import views_project_tree


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
    # same as get_iterations but without release_id as parameter
    path('ajax_get_release_iterations/', views_backlog.ajax_get_release_iterations, name='ajax_get_release_iterations'),
    path('ajax_fetch_persona_activities/', views_backlog.ajax_fetch_persona_activities, name='ajax_fetch_persona_activities'),    
    path('ajax_recieve_story_mapped_details/', views_backlog.ajax_recieve_story_mapped_details, name='ajax_recieve_story_mapped_details'),
    path('ajax_story_back_to_list/', views_backlog.ajax_story_back_to_list, name='ajax_story_back_to_list'),
    
    
    # new feature
    path('create_story_map/<int:org_id>/', views_story_map.create_story_map, name='create_story_map'),
    path('create_story_map_from_backlog/<int:pro_id>/', views_story_map.create_story_map_from_backlog, name='create_story_map_from_backlog'),
    path('create_backlog_from_story_map/<int:pro_id>/<int:persona_id>/', views_story_map.create_backlog_from_story_map, name='create_backlog_from_story_map'),
    path('ajax_storymap_right_pane_content/', views_story_map.ajax_storymap_right_pane_content, name='ajax_storymap_right_pane_content'),
    path('ajax_storymap_refresh_steps_row/', views_story_map.ajax_storymap_refresh_steps_row, name='ajax_storymap_refresh_steps_row'),
    path('ajax_storymap_refresh_details_row/', views_story_map.ajax_storymap_refresh_details_row, name='ajax_storymap_refresh_details_row'),
    path('ajax_refresh_release_rows/', views_story_map.ajax_refresh_release_rows, name='ajax_refresh_release_rows'),
    path('ajax_update_backlog_release/', views_story_map.ajax_update_backlog_release, name='ajax_update_backlog_release'),    
    path('ajax_storymap_group_steps/', views_story_map.ajax_storymap_group_steps, name='ajax_storymap_group_steps'),
    path('ajax_map_steps_to_activity/', views_story_map.ajax_map_steps_to_activity, name='ajax_map_steps_to_activity'),
    path('ajax_unmap_steps_from_activity/', views_story_map.ajax_unmap_steps_from_activity, name='ajax_unmap_steps_from_activity'),
    path('storymap_group_steps/<int:pro_id>/<int:persona_id>/', views_story_map.storymap_group_steps, name='storymap_group_steps'),
    
    # backlog
    path('project_backlog_decide/<int:pro_id>/', views_backlog.project_backlog_decide, name='project_backlog_decide'),
    path('view_flat_backlog/<int:pro_id>/<int:parent_id>/', views_backlog.view_flat_backlog, name='view_flat_backlog'),
    
    path('view_project_tree_backlog/<int:pro_id>/', views_project_tree.view_project_tree_backlog, name='view_project_tree_backlog'),
    path('edit_project_tree_backlog_item/<int:pro_id>/<int:backlog_item_id>/', views_project_tree.edit_project_tree_backlog_item, name='edit_project_tree_backlog_item'),
    
    path('ajax_project_tree_sorted/', views_project_tree.ajax_project_tree_sorted, name='ajax_project_tree_sorted'),
    
    # added
    path('create_project_story_map/<int:org_id>/<int:project_id>/', views_story_map.create_project_story_map, name='create_project_story_map'),
    
    # added nearest current/next iteration

    # MVP2: Feb 15th 2025
    # Kanban and other features
    path('project_tree_board_settings/<int:pro_id>/', views_project_tree.project_tree_board_settings, name='project_tree_board_settings'),
    
    # MVP3: Aug 2nd 2025
    # Drag and drop functionality

    path('ajax/update-activity-position/', 
         views_story_map.ajax_update_activity_position, 
         name='ajax_update_activity_position'),
    
    path('ajax/update-step-position/', 
         views_story_map.ajax_update_step_position, 
         name='ajax_update_step_position'),
    
    path('ajax/update-activity-name/', 
         views_story_map.ajax_update_activity_name, 
         name='ajax_update_activity_name'),
    
    path('ajax/move-step-to-activity/', 
         views_story_map.ajax_move_step_to_activity, 
         name='ajax_move_step_to_activity'),

    path('ajax/add-activity/', 
         views_story_map.ajax_add_activity, 
         name='ajax_add_activity'),
    
    path('ajax/add-step/', 
         views_story_map.ajax_add_step, 
         name='ajax_add_step'),

    path('ajax/delete-activity/', views_story_map.ajax_delete_activity, name='ajax_delete_activity'),
    path('ajax/delete-step/', views_story_map.ajax_delete_step, name='ajax_delete_step'),


    # Restore functionality URLs
    path('ajax/get-deleted-activities/', views_story_map.ajax_get_deleted_activities, name='ajax_get_deleted_activities'),
    path('ajax/get-deleted-steps/', views_story_map.ajax_get_deleted_steps, name='ajax_get_deleted_steps'),
    path('ajax/restore-activities/', views_story_map.ajax_restore_activities, name='ajax_restore_activities'),
    path('ajax/restore-steps/', views_story_map.ajax_restore_steps, name='ajax_restore_steps'),
    
    # Optional: Permanent delete (for admin use)
    path('ajax/permanent-delete-activity/', views_story_map.ajax_permanent_delete_activity, name='ajax_permanent_delete_activity'),
    path('ajax/permanent-delete-step/', views_story_map.ajax_permanent_delete_step, name='ajax_permanent_delete_step'),

    path('ajax/create-persona/', views_story_map.ajax_create_persona, name='ajax_create_persona'),
    path('ajax/save-to-persona/', views_story_map.ajax_save_to_persona, name='ajax_save_to_persona'),
    path('ajax/refresh-mapped-items/', views_story_map.ajax_refresh_mapped_items, name='ajax_refresh_mapped_items'),

    path('ajax_update_step_name/', views_story_map.ajax_update_step_name, name='ajax_update_step_name'),

    # list the project personas if empty user creates one to start
    path('project_personas/<int:org_id>/<int:project_id>/', views_story_map.project_personas, name='project_personas'),
]
