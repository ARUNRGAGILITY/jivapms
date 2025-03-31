from django.urls import include, path

urlpatterns = [
    path('postnote/', include('app_postnote.mod_postnote.urls_postnote')),
    path('project/', include('app_postnote.mod_project.urls_project')),
]
