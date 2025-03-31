from django.urls import path
from app.app_postnote.mod_postnote import views_postnote as views

#app_name = 'app_postnote'  # Replace with your actual app name

urlpatterns = [
    # Main view for the project board
    path('project/<int:project_id>/board/', views.view_project_board, name='project_board'),
    
    # AJAX endpoints for post note operations
    path('api/project/<int:project_id>/postnote/create/', views.create_postnote, name='create_postnote'),
    path('api/postnote/<int:postnote_id>/position/', views.update_postnote_position, name='update_postnote_position'),
    path('api/postnote/<int:postnote_id>/content/', views.update_postnote_content, name='update_postnote_content'),
    path('api/postnote/<int:postnote_id>/delete/', views.delete_postnote, name='delete_postnote'),
    path('api/postnote/<int:postnote_id>/attributes/', views.update_postnote_attributes, name='update_postnote_attributes'),

    # Acceptance criteria endpoints
    path('api/postnote/<int:postnote_id>/criteria/', views.update_acceptance_criteria, name='update_acceptance_criteria'),
    path('api/postnote/<int:postnote_id>/criteria/get/', views.get_acceptance_criteria, name='get_acceptance_criteria'),

    # Link endpoints
    path('api/postnote/link/create/', views.create_postnote_link, name='create_postnote_link'),
    path('api/postnote/link/<int:link_id>/delete/', views.delete_postnote_link, name='delete_postnote_link'),
    path('api/project/<int:project_id>/links/', views.get_postnote_links, name='get_postnote_links'),
]