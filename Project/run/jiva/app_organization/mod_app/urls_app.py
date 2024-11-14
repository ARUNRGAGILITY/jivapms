from django.urls import include, path

urlpatterns = [
    path('backlog/', include('app_organization.mod_backlog.urls_backlog')),
    path('backlog_super_type/', include('app_organization.mod_backlog_super_type.urls_backlog_super_type')),
    path('backlog_type/', include('app_organization.mod_backlog_type.urls_backlog_type')),
    path('dev_value_stream/', include('app_organization.mod_dev_value_stream.urls_dev_value_stream')),
    path('dev_value_stream_step/', include('app_organization.mod_dev_value_stream_step.urls_dev_value_stream_step')),
    path('memberrole/', include('app_organization.mod_memberrole.urls_memberrole')),
    path('ops_value_stream/', include('app_organization.mod_ops_value_stream.urls_ops_value_stream')),
    path('organization/', include('app_organization.mod_organization.urls_organization')),
    path('organizationdetail/', include('app_organization.mod_organizationdetail.urls_organizationdetail')),
    path('project/', include('app_organization.mod_project.urls_project')),
    path('projectmembership/', include('app_organization.mod_projectmembership.urls_projectmembership')),
    path('project_detail/', include('app_organization.mod_project_detail.urls_project_detail')),
    path('project_roadmap/', include('app_organization.mod_project_roadmap.urls_project_roadmap')),
    path('project_template/', include('app_organization.mod_project_template.urls_project_template')),
    path('roadmapitem/', include('app_organization.mod_roadmapitem.urls_roadmapitem')),
    path('team/', include('app_organization.mod_team.urls_team')),
    path('teammember/', include('app_organization.mod_teammember.urls_teammember')),
    path('work/', include('app_organization.mod_work.urls_work')),
]
