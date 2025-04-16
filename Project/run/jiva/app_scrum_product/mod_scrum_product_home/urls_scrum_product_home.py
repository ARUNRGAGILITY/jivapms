from django.urls import path
from app_scrum_product.mod_scrum_product_home import views_scrum_product_home

urlpatterns = [
    # Main home/dashboard view
    path('', views_scrum_product_home.scrum_product_home, name='scrum_product_home'),
    
    # Product overview view
    path('overview/', views_scrum_product_home.scrum_product_home_overview, name='scrum_product_home_overview'),
    path('overview/<int:product_id>/', views_scrum_product_home.scrum_product_home_overview, name='scrum_product_home_overview_detail'),
]