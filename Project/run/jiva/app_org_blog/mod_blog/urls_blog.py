
from django.urls import path, include

from app_org_blog.mod_blog import views_blog

app_name = "app_org_blog"
urlpatterns = [
    # Administration URLs
    path('list_blogs/<int:organization_id>/', views_blog.list_blogs, name='list_blogs'),
    path('list_deleted_blogs/<int:organization_id>/', views_blog.list_deleted_blogs, name='list_deleted_blogs'),
    path('create_blog/<int:organization_id>/', views_blog.create_blog, name='create_blog'),
    path('edit_blog/<int:organization_id>/<int:blog_id>/', views_blog.edit_blog, name='edit_blog'),
    path('delete_blog/<int:organization_id>/<int:blog_id>/', views_blog.delete_blog, name='delete_blog'),
    path('permanent_deletion_blog/<int:organization_id>/<int:blog_id>/', views_blog.permanent_deletion_blog, name='permanent_deletion_blog'),
    path('restore_blog/<int:organization_id>/<int:blog_id>/', views_blog.restore_blog, name='restore_blog'),
    path('view_blog/<int:organization_id>/<int:blog_id>/', views_blog.view_blog, name='view_blog'),
    
    # Dashboard and management URLs
    path('dashboard/<int:organization_id>/', views_blog.blog_dashboard, name='blog_dashboard'),
    path('members/<int:organization_id>/', views_blog.manage_blog_members, name='manage_blog_members'),
    path('members/<int:organization_id>/blog/<int:blog_id>/', views_blog.manage_blog_members, name='manage_blog_members_for_blog'),
    path('members/<int:organization_id>/remove/<int:member_id>/', views_blog.remove_blog_member, name='remove_blog_member'),
    
    # Public blog URLs
    path('public/<int:organization_id>/', views_blog.public_blog_list, name='public_blog_list'),
    path('public/<int:organization_id>/post/<int:blog_id>/', views_blog.public_blog_detail, name='public_blog_detail'),
    path('public/<int:organization_id>/post/<slug:slug>/', views_blog.public_blog_detail, name='public_blog_detail_slug'),
]
