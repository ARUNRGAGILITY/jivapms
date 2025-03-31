from django.urls import path 
from . import views as app_web_views
urlpatterns = [
    path('', app_web_views.welcome, name='welcome'),
]

# cba