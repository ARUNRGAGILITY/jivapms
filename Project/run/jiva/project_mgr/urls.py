from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static 
urlpatterns = [
    # all the common items for all apps
    path('common/', include('app_common.mod_app.urls_app')),   

    path('web/', include('app_jivapms.mod_app.urls_app')),

    # default gateway / web 
    path('', include('app_jivapms.mod_app.urls_app')),
    
    # loginsystem
    path('loginsystem/', include('app_loginsystem.mod_app.urls_app')),
    
    # organization
    path('org/', include('app_organization.mod_app.urls_app')),
    
    # Analytics
    path('infos/', include('app_analytics.mod_app.urls_app')),
    
    
    # memberprofilerole
    path('mpr/', include('app_memberprofilerole.mod_app.urls_app')),
    
    # system
    #path('system/', include('app_system.mod_app.urls_app')),
    path('user/', include('app_user.urls')),
    # administration
    path('admin/', admin.site.urls),    
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)