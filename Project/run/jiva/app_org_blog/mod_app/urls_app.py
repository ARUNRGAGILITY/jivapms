from django.urls import include, path

urlpatterns = [
    path('blog/', include('app_org_blog.mod_blog.urls_blog')),
]
