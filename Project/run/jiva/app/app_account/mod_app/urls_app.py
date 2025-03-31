from django.urls import include, path

urlpatterns = [
    path('user/', include('app_account.mod_user.urls_user')),
    path('user_admin/', include('app_account.mod_user_admin.urls_user_admin')),
]
