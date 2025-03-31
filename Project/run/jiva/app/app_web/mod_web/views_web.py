from app_web.mod_app.all_view_imports import *
from app_memberprofilerole.mod_app.all_model_imports import *
from app_memberprofilerole.mod_member.models_member import *

app_name = "app_web"
version = "v1"
module_dirname = "mod_web"

from app_web.mod_web.helper_web import *
# Create your views here.
def index(request):
    user = request.user
    roles = []
    member = None
    superadmin = False
    multiple_roles = False
    no_of_roles = 0
    # user's home page
    if user.is_authenticated:
        print(f">>> === User is authenticated: {user} === <<<")
        print(f">>> === User is authenticated: {user.id} === <<<")
        if user.is_superuser:
            print(f">>> === User is superuser: {user} === <<<")
        else:
            print(f">>> === User is normal user: {user} === <<<")
            member = Member.objects.get(user__id=user.id)
            print(f">>> === Member is normal user: {member} === <<<")
            roles = member.member_roles.filter(active=True)
            no_of_roles = roles.count()
            if roles.count() > 1:
                multiple_roles = True

            print(f">>> === Roles: {roles} === <<<")
    context = {
        'parent_page': 'home',
        'page': 'index',
        'page_title': 'Home Page',

        'user': user,
        'roles': roles,
        'member': member,
        'superadmin': superadmin,
        'multiple_roles': multiple_roles,
        'no_of_roles': no_of_roles,
        
    }
    template_url = f"{app_name}/{module_dirname}/index.html"
    return render(request, template_url, context)   


def about(request):

    
    context = {
        'parent_page': 'home',
        'page': 'about',
        'page_title': 'About Page',
    }
    template_url = f"app_common/common_files/specific/about.html"
    return render(request, template_url, context)   

def blogs(request):

    
    context = {
        'parent_page': 'home',
        'page': 'blogs',
        'page_title': 'Blogs Page',
    }
    template_url = f"app_common/common_files/specific/blogs.html"
    return render(request, template_url, context)   



def learn(request):

    
    context = {
        'parent_page': 'home',
        'page': 'learn',
        'page_title': 'Learning Page',
    }
    template_url = f"app_common/common_files/specific/learn.html"
    return render(request, template_url, context)   
