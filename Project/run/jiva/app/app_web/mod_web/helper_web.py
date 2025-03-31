from jiva.app.app_web.mod_app.all_view_imports import *


app_name = "app_web"
version = "v1"
module_dirname = "mod_web"
def tutorials(request):

    
    context = {
        'parent_page': 'learn',
        'page': 'tutorials',
        'page_title': 'Tutorials Page',
    }
    template_url = f"app_common/common_files/learn/tutorials.html"
    return render(request, template_url, context)   

def courses(request):

    
    context = {
        'parent_page': 'learn',
        'page': 'courses',
        'page_title': 'Courses Page',
    }
    template_url = f"app_common/common_files/learn/courses.html"
    return render(request, template_url, context)   

def quiz(request):

    
    context = {
        'parent_page': 'learn',
        'page': 'quiz',
        'page_title': 'Quiz Page',
    }
    template_url = f"app_common/common_files/learn/quiz.html"
    return render(request, template_url, context)   

def assessment(request):

    
    context = {
        'parent_page': 'learn',
        'page': 'assessment',
        'page_title': 'Assessment Page',
    }
    template_url = f"app_common/common_files/learn/assessment.html"
    return render(request, template_url, context)   

def source_code(request):

    
    context = {
        'parent_page': 'learn',
        'page': 'source_code',
        'page_title': 'Source Code Page',
    }
    template_url = f"app_common/common_files/learn/source_code.html"
    return render(request, template_url, context)   