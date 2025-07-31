from django.urls import include, path

urlpatterns = [
    path('authz/', include('app_authz.mod_authz.urls_authz')),
]
