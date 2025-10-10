
from django.urls import path, include

from app_organization.mod_org_board import views_org_board


urlpatterns = [
    # app_organization/org_boards: DB/Model: OrgBoard
    path('list_org_boards/<int:org_id>/', views_org_board.list_org_boards, name='list_org_boards'),
    path('list_deleted_org_boards/<int:org_id>/', views_org_board.list_deleted_org_boards, name='list_deleted_org_boards'),
    path('create_org_board/<int:org_id>/', views_org_board.create_org_board, name='create_org_board'),
    path('edit_org_board/<int:org_id>/<int:org_board_id>/', views_org_board.edit_org_board, name='edit_org_board'),
    path('delete_org_board/<int:org_id>/<int:org_board_id>/', views_org_board.delete_org_board, name='delete_org_board'),
    path('permanent_deletion_org_board/<int:org_id>/<int:org_board_id>/', views_org_board.permanent_deletion_org_board, name='permanent_deletion_org_board'),
    path('restore_org_board/<int:org_id>/<int:org_board_id>/', views_org_board.restore_org_board, name='restore_org_board'),
    path('view_org_board/<int:org_id>/<int:org_board_id>/', views_org_board.view_org_board, name='view_org_board'),
    
    
    path('view_project_board/<int:project_id>/', views_org_board.view_project_board, name='view_project_board'),
    path('view_project_tree_board/<int:project_id>/', views_org_board.view_project_tree_board, name='view_project_tree_board'),
    path('ajax_update_project_board_card_state/', views_org_board.ajax_update_project_board_card_state, name='ajax_update_project_board_card_state'),    
    path('ajax_update_project_board_card_order/', views_org_board.ajax_update_project_board_card_order, name='ajax_update_project_board_card_order'),

    path('view_project_tree_board_custom/<int:project_id>/', views_org_board.view_project_tree_board_custom, name='view_project_tree_board_custom'),
    path('view_project_tree_board_smart_kanban/<int:project_id>/', views_org_board.view_project_tree_board_smart_kanban, name='view_project_tree_board_smart_kanban'),

    # Policies AJAX (dev_env)
    path('ajax_policies/list/', views_org_board.ajax_list_policies, name='ajax_list_policies'),
    path('ajax_policies/column/create/', views_org_board.ajax_create_column_policy, name='ajax_create_column_policy'),
    path('ajax_policies/column/update/', views_org_board.ajax_update_column_policy, name='ajax_update_column_policy'),
    path('ajax_policies/column/delete/', views_org_board.ajax_delete_column_policy, name='ajax_delete_column_policy'),
    path('ajax_policies/column/reorder/', views_org_board.ajax_reorder_column_policies, name='ajax_reorder_column_policies'),
    path('ajax_policies/general/create/', views_org_board.ajax_create_general_policy, name='ajax_create_general_policy'),
    path('ajax_policies/general/update/', views_org_board.ajax_update_general_policy, name='ajax_update_general_policy'),
    path('ajax_policies/general/delete/', views_org_board.ajax_delete_general_policy, name='ajax_delete_general_policy'),
]
