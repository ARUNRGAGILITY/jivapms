from django.urls import include, path

urlpatterns = [
    path('backlog/', include('app_organization.mod_backlog.urls_backlog')),
    path('backlog_super_type/', include('app_organization.mod_backlog_super_type.urls_backlog_super_type')),
    path('backlog_type/', include('app_organization.mod_backlog_type.urls_backlog_type')),
    path('memberrole/', include('app_organization.mod_memberrole.urls_memberrole')),
    path('organization/', include('app_organization.mod_organization.urls_organization')),
    path('project/', include('app_organization.mod_project.urls_project')),
    path('projectmembership/', include('app_organization.mod_projectmembership.urls_projectmembership')),
    path('team/', include('app_organization.mod_team.urls_team')),
    path('teammember/', include('app_organization.mod_teammember.urls_teammember')),
    path('work/', include('app_organization.mod_work.urls_work')),
]