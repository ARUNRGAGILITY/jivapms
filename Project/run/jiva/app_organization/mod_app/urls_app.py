from django.urls import include, path

urlpatterns = [
    path('backlog/', include('app_organization.mod_backlog.urls_backlog')),
    path('backlog_super_type/', include('app_organization.mod_backlog_super_type.urls_backlog_super_type')),
    path('backlog_type/', include('app_organization.mod_backlog_type.urls_backlog_type')),
    path('blog/', include('app_organization.mod_blog.urls_blog')),
    path('board/', include('app_organization.mod_board.urls_board')),
    path('dev_value_stream/', include('app_organization.mod_dev_value_stream.urls_dev_value_stream')),
    path('dev_value_stream_step/', include('app_organization.mod_dev_value_stream_step.urls_dev_value_stream_step')),
    path('event/', include('app_organization.mod_event.urls_event')),
    path('framework/', include('app_organization.mod_framework.urls_framework')),
    path('impact_map/', include('app_organization.mod_impact_map.urls_impact_map')),
    path('impact_mapping/', include('app_organization.mod_impact_mapping.urls_impact_mapping')),
    path('iteration/', include('app_organization.mod_iteration.urls_iteration')),
    path('iteration_backlog/', include('app_organization.mod_iteration_backlog.urls_iteration_backlog')),
    path('memberrole/', include('app_organization.mod_memberrole.urls_memberrole')),
    path('metric/', include('app_organization.mod_metric.urls_metric')),
    path('ops_value_stream/', include('app_organization.mod_ops_value_stream.urls_ops_value_stream')),
    path('ops_value_stream_step/', include('app_organization.mod_ops_value_stream_step.urls_ops_value_stream_step')),
    path('organization/', include('app_organization.mod_organization.urls_organization')),
    path('organizationdetail/', include('app_organization.mod_organizationdetail.urls_organizationdetail')),
    path('org_board/', include('app_organization.mod_org_board.urls_org_board')),
    path('org_event/', include('app_organization.mod_org_event.urls_org_event')),
    path('org_image_map/', include('app_organization.mod_org_image_map.urls_org_image_map')),
    path('org_iteration/', include('app_organization.mod_org_iteration.urls_org_iteration')),
    path('org_metric/', include('app_organization.mod_org_metric.urls_org_metric')),
    path('org_release/', include('app_organization.mod_org_release.urls_org_release')),
    path('org_team/', include('app_organization.mod_org_team.urls_org_team')),
    path('org_work_flow/', include('app_organization.mod_org_work_flow.urls_org_work_flow')),
    path('project/', include('app_organization.mod_project.urls_project')),
    path('projectmembership/', include('app_organization.mod_projectmembership.urls_projectmembership')),
    path('project_detail/', include('app_organization.mod_project_detail.urls_project_detail')),
    path('project_roadmap/', include('app_organization.mod_project_roadmap.urls_project_roadmap')),
    path('project_template/', include('app_organization.mod_project_template.urls_project_template')),
    path('project_work_flow/', include('app_organization.mod_project_work_flow.urls_project_work_flow')),
    path('release/', include('app_organization.mod_release.urls_release')),
    path('roadmapitem/', include('app_organization.mod_roadmapitem.urls_roadmapitem')),
    path('team/', include('app_organization.mod_team.urls_team')),
    path('teammember/', include('app_organization.mod_teammember.urls_teammember')),
    path('work_flow/', include('app_organization.mod_work_flow.urls_work_flow')),
]
