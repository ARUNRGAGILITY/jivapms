
from django.urls import path, include

from app_scrum.mod_deliver import views_deliver


urlpatterns = [
    # app_scrum/delivers: DB/Model: Deliver
    path('list_delivers/<int:organization_id>/', views_deliver.list_delivers, name='list_delivers'),
    path('list_deleted_delivers/<int:organization_id>/', views_deliver.list_deleted_delivers, name='list_deleted_delivers'),
    path('create_deliver/<int:organization_id>/', views_deliver.create_deliver, name='create_deliver'),
    path('edit_deliver/<int:organization_id>/<int:deliver_id>/', views_deliver.edit_deliver, name='edit_deliver'),
    path('delete_deliver/<int:organization_id>/<int:deliver_id>/', views_deliver.delete_deliver, name='delete_deliver'),
    path('permanent_deletion_deliver/<int:organization_id>/<int:deliver_id>/', views_deliver.permanent_deletion_deliver, name='permanent_deletion_deliver'),
    path('restore_deliver/<int:organization_id>/<int:deliver_id>/', views_deliver.restore_deliver, name='restore_deliver'),
    path('view_deliver/<int:organization_id>/<int:deliver_id>/', views_deliver.view_deliver, name='view_deliver'),
    path('dashboard_deliver/<int:organization_id>/', views_deliver.deliver_dashboard, name='deliver_dashboard'),
    path('settings_deliver/<int:organization_id>/', views_deliver.deliver_settings, name='deliver_settings'),
]
