from django.contrib import admin
from django.urls import path, include

from app_jivapms.mod_web import views_web as web

urlpatterns = [
    path('', web.index, name='index'), 
    path('about/', web.about, name='about'),
    path('about_the_project/', web.about_the_project, name='about_the_project'),
    path('blogs/', web.blogs, name='blogs'),
    
    path('tutorials/', web.tutorials, name='tutorials'),
    path('courses/', web.courses, name='courses'),
    path('quiz/', web.quiz, name='quiz'),
    path('assessment/', web.assessment, name='assessment'),
    path('source_code/', web.source_code, name='source_code'),

    path('role_homepage/<str:role_name>/', web.role_homepage, name='role_homepage'),
]
