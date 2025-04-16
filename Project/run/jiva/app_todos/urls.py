from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'todo_app'

urlpatterns = [
    # MyTodos views
    path('lists/', views.my_todos_list, name='my_todos_list'),
    path('list/<int:list_id>/', views.my_todos_detail, name='my_todos_detail'),
    path('list/create/', views.my_todos_create, name='my_todos_create'),
    path('list/<int:pk>/edit/', views.my_todos_edit, name='my_todos_edit'),
    path('list/<int:pk>/delete/', views.my_todos_delete, name='my_todos_delete'),
    path('list/<int:pk>/restore/', views.my_todos_restore, name='my_todos_restore'),
    path('list/trash/', views.my_todos_trash, name='my_todos_trash'),
    path('list/<int:pk>/permanent-delete/', views.my_todos_permanent_delete, name='my_todos_permanent_delete'),
    path('list/reorder/', views.my_todos_reorder, name='my_todos_reorder'),
    path('lists/search/', views.search_lists, name='search_lists'),
    path('search/', views.global_search, name='global_search'),

    # list level trash
    path('list/<int:list_id>/trash/', views.list_trash_view, name='list_trash_view'),
    path('list/<int:list_id>/trash/bulk-restore/', views.list_bulk_restore, name='list_bulk_restore'),
    path('list/<int:list_id>/trash/bulk-delete/', views.list_bulk_permanent_delete, name='list_bulk_permanent_delete'),
    # Base views
    path('', views.todo_list, name='todo_list'),
    
    # Todo CRUD operations
    path('todo/create/', views.todo_create, name='todo_create'),
    path('todo/<int:pk>/view/', views.todo_view, name='todo_view'),
    path('todo/<int:pk>/edit/', views.todo_edit, name='todo_edit'),
    path('todo/<int:pk>/delete/', views.todo_delete, name='todo_delete'),
    path('todo/<int:pk>/copy/', views.todo_copy, name='todo_copy'),
    path('todo/<int:pk>/mark-done/', views.todo_mark_done, name='todo_mark_done'),
    path('todo/<int:pk>/toggle-blocked/', views.todo_toggle_blocked, name='todo_toggle_blocked'),
    path('todo/get-children/', views.get_children, name='get_children'),

    # View type routes
    path('view/table/', views.table_view, name='table_view'),
    path('view/kanban/', views.kanban_view, name='kanban_view'),
    path('view/canvas/', views.canvas_view, name='canvas_view'),
    path('view/calendar/', views.calendar_view, name='calendar_view'),
    
    # Kanban operations
    path('kanban/column/create/', views.kanban_column_create, name='kanban_column_create'),
    path('kanban/column/<int:pk>/edit/', views.kanban_column_edit, name='kanban_column_edit'),
    path('kanban/column/<int:pk>/delete/', views.kanban_column_delete, name='kanban_column_delete'),
    path('todo/<int:pk>/move-to-column/<int:column_id>/', views.move_todo_to_column, name='move_todo_to_column'),
    path('trash/', views.trash_view, name='trash_view'),
    path('trash/restore/', views.todo_restore, name='todo_restore'),
    path('trash/permanent-delete/', views.todo_permanent_delete, name='todo_permanent_delete'),
    path('trash/empty/', views.empty_trash, name='empty_trash'),
    path('trash/bulk-restore/', views.bulk_restore, name='bulk_restore'),
    path('trash/bulk-permanent-delete/', views.bulk_permanent_delete, name='bulk_permanent_delete'),
    
    # Canvas operations
    path('canvas/update-position/<int:pk>/', views.update_canvas_position, name='update_canvas_position'),
    
    # AJAX routes
    path('api/todos/', views.api_todos, name='api_todos'),
    path('api/todo/quick-add/', views.api_quick_add, name='api_quick_add'),
    path('api/todo/reorder/', views.api_reorder_todos, name='api_reorder_todos'),
    path('api/stats/', views.api_get_stats, name='api_get_stats'),
    path('api/kanban/reorder-columns/', views.api_reorder_columns, name='api_reorder_columns'),

    # my todos
    path('my-todos/bulk-delete/', views.my_todos_bulk_delete, name='my_todos_bulk_delete'),
    path('my-todos/bulk-restore/', views.my_todos_bulk_restore, name='my_todos_bulk_restore'),
    path('my-todos/bulk-permanent-delete/', views.my_todos_bulk_permanent_delete, name='my_todos_bulk_permanent_delete'),
    path('my-todos/empty-trash/', views.my_todos_empty_trash, name='my_todos_empty_trash'),
    path('my-todos/copy/<int:pk>/', views.my_todos_copy, name='my_todos_copy'),

    # insights
    path('insights/', views.insights_view, name='insights'),

    path('accounts/login/', auth_views.LoginView.as_view(template_name='app_todos/login.html'), name='login'),
    #path('accounts/logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('accounts/account_profile/', views.account_profile, name='account_profile'),
    path('accounts/logout/', views.custom_logout, name='logout'),
    path('accounts/password_change/', auth_views.PasswordChangeView.as_view(template_name='app_todos/password_change.html'), name='password_change'),
    path('accounts/password_change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='app_todos/password_change_done.html'), name='password_change_done'),
    path('user-stats/', views.user_stats, name='user_stats'),
    
    path('shared-with-me/', views.shared_with_me, name='shared_with_me'),
    path('my-todos/<int:pk>/toggle-public/', views.toggle_public, name='toggle_public'),
    path('my-todos/<int:pk>/share/', views.share_todo_list, name='share_todo_list'),
    path('my-todos/<int:pk>/share/remove/<int:user_id>/', views.remove_share, name='remove_share'),
]
