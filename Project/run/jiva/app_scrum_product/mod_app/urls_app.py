from django.urls import include, path

urlpatterns = [
    path('scrum_event/', include('app_scrum_product.mod_scrum_event.urls_scrum_event')),
    path('scrum_product/', include('app_scrum_product.mod_scrum_product.urls_scrum_product')),
    path('scrum_product_artifact/', include('app_scrum_product.mod_scrum_product_artifact.urls_scrum_product_artifact')),
    path('scrum_product_backlog/', include('app_scrum_product.mod_scrum_product_backlog.urls_scrum_product_backlog')),
    path('scrum_product_category/', include('app_scrum_product.mod_scrum_product_category.urls_scrum_product_category')),
    path('scrum_product_dashboard/', include('app_scrum_product.mod_scrum_product_dashboard.urls_scrum_product_dashboard')),
    path('scrum_product_home/', include('app_scrum_product.mod_scrum_product_home.urls_scrum_product_home')),
    path('scrum_product_metric/', include('app_scrum_product.mod_scrum_product_metric.urls_scrum_product_metric')),
    path('scrum_product_priority/', include('app_scrum_product.mod_scrum_product_priority.urls_scrum_product_priority')),
    path('scrum_product_release/', include('app_scrum_product.mod_scrum_product_release.urls_scrum_product_release')),
    path('scrum_product_report/', include('app_scrum_product.mod_scrum_product_report.urls_scrum_product_report')),
    path('scrum_product_sprint/', include('app_scrum_product.mod_scrum_product_sprint.urls_scrum_product_sprint')),
    path('scrum_product_sub_category/', include('app_scrum_product.mod_scrum_product_sub_category.urls_scrum_product_sub_category')),
    path('scrum_product_tag/', include('app_scrum_product.mod_scrum_product_tag.urls_scrum_product_tag')),
    path('scrum_product_team/', include('app_scrum_product.mod_scrum_product_team.urls_scrum_product_team')),
    path('scrum_product_type/', include('app_scrum_product.mod_scrum_product_type.urls_scrum_product_type')),
    path('scrum_role/', include('app_scrum_product.mod_scrum_role.urls_scrum_role')),
]
