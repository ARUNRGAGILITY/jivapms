from django.urls import path
from django.contrib.auth import views as auth_views
from app_loginsystem.mod_auth import views_auth as auth
from django.urls import reverse_lazy
urlpatterns = [
    path('login/', auth.at_login, name="login"),
    path('register/', auth.at_register, name="register"),
    path('logout/', auth.at_logout, name="logout"),    
    path('change_password/', auth_views.PasswordChangeView.as_view(
        template_name='app_loginsystem/mod_auth/change_password.html',
        success_url=reverse_lazy('change_password_done')  # Corrected redirection
    ), name='change_password'),

    path('change_password/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='app_loginsystem/mod_auth/change_password_done.html'
    ), name='change_password_done'),
    # after the user is logged in
    path('user_logged_in/', auth.user_logged_in, name='user_logged_in'),
]