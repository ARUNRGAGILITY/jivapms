from django.urls import path, include

urlpatterns = [
    path('', include('jiva.app.app_web.mod_web.urls_web')),
   
]
