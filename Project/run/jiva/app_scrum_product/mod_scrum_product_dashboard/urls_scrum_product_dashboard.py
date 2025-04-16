from django.urls import path
from app_scrum_product.mod_scrum_product_dashboard import views_scrum_product_dashboard

urlpatterns = [
    # Main dashboard view for all products
    path('', views_scrum_product_dashboard.scrum_products_dashboard, name='scrum_products_dashboard'),
    
    # Analytics view
    path('analytics/', views_scrum_product_dashboard.scrum_dashboard_analytics, name='scrum_dashboard_analytics'),
]