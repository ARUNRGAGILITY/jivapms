from django.urls import path
from app_scrum.mod_dashboard import views_dashboard

urlpatterns = [
    # Main dashboard view
    path('', views_dashboard.scrum_dashboard, name='scrum_dashboard'),
    
    # Module-specific dashboard views
    path('project/', views_dashboard.module_dashboard, {'module_type': 'project'}, name='project_dashboard'),
    path('product/', views_dashboard.module_dashboard, {'module_type': 'product'}, name='product_dashboard'),
    path('solution/', views_dashboard.module_dashboard, {'module_type': 'solution'}, name='solution_dashboard'),
    path('consulting/', views_dashboard.module_dashboard, {'module_type': 'consulting'}, name='consulting_dashboard'),
]