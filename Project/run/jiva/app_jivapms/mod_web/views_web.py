from app_web.mod_app.all_view_imports import *
from app_memberprofilerole.mod_app.all_model_imports import *
from app_memberprofilerole.mod_member.models_member import *

from app_common.mod_app.all_view_imports import *
from app_jivapms.mod_app.all_view_imports import *
from app_organization.mod_projectmembership.models_projectmembership import *

from app_organization.mod_framework.models_framework import *
from app_organization.mod_org_image_map.models_org_image_map import *

app_name = "app_jivapms"
version = "v1"
module_dirname = "mod_web"

from app_jivapms.mod_web.helper_web import *
from app_jivapms.mod_web.views_ajax_web import *


def index(request):
    user = request.user
    organization = Organization.objects.filter(active=True)
    framework = Framework.objects.filter(active=True)
    public_frameworks = Framework.objects.filter(public_framework=True, active=True)
    # Get the related Organization objects for those Frameworks
    org_ids = public_frameworks.values_list('organization__id', flat=True).distinct()
    organizations = Organization.objects.filter(id__in=org_ids)
    context = {
        'parent_page': 'home',
        'page': 'index',
        'page_title': 'Home Page',
        'user': user,
        'roles': [],
        'members': [],
        'super_user': user.is_superuser,
        'multiple_roles': False,
        'no_of_roles': 0,
        'user_roles_data': [],
        'anonymous': not user.is_authenticated,
        'role': COMMON_ROLE_CONFIG["NO_ROLE"]["name"],  # Default role
        'project_details': [],
        'organizations': organizations,
        'public_frameworks': public_frameworks,
    }

    if user.is_authenticated:
        logger.debug(f"User authenticated: {user.id}")
        if user.is_superuser:
            context['role'] = COMMON_ROLE_CONFIG["SUPER_USER"]["name"]
        else:
            # Fetch all active member instances for this user
            members = Member.objects.prefetch_related('member_roles__role', 'member_roles__org').filter(user=user)
            if members.exists():
                for member in members:
                    roles = member.member_roles.filter(active=True)
                    user_data = {
                        'member_id': member.id,
                        'username': user.username,
                        'roles': []
                    }

                    for role in roles:
                        role_data = {
                            'org_id': role.org.id if role.org else None,
                            'role_id': role.role.id if role.role else None,
                            'role_name': role.role.name if role.role else 'No Role',
                            'org_name': role.org.name if role.org else 'No Org',
                            'lc_role_name': role.role.name.lower().replace(' ', '_') if role.role else 'no_page',
                        }
                        user_data['roles'].append(role_data)
                        context['roles'].append(role)  # Aggregate all roles
                    # Fetch project memberships
                    project_memberships = Projectmembership.objects.filter(member=member)
                    project_info = [{'org': pm.project.org, 'project_id': pm.project.id ,'project_name': pm.project.name, 'role': pm.project_role.role_type} for pm in project_memberships]
                    user_data['projects'] = project_info
                    context['project_details'].extend(project_info)
                    context['user_roles_data'].append(user_data)
                    context['members'].append(member)
                context['multiple_roles'] = len(context['roles']) > 1
                context['no_of_roles'] = len(context['roles'])
                context['role'] = context['roles'][0].role.name if context['roles'] else COMMON_ROLE_CONFIG["NO_ROLE"]["name"]
            else:
                logger.error(f"Active member not found for user: {user.id}")
    else:
        logger.debug("Anonymous user access")

    # Assign template based on role
    template_url = get_template_for_role(context)

    try:
        get_template(template_url)
        return render(request, template_url, context)
    except TemplateDoesNotExist:
        logger.error(f"Template not found: {template_url}")
        template_url = f"{app_name}/{module_dirname}/general_homepage/general_homepage.html"
        return render(request, template_url, context)

def get_template_for_role(context):
    app_name = "app_jivapms"
    module_dirname = "mod_web"
    
    if context['super_user']:
        return f"{app_name}/{module_dirname}/super_user/super_user_homepage.html"
    elif context['multiple_roles']:
        return f"{app_name}/{module_dirname}/multiple_roles/multiple_roles_homepage.html"
    elif context['anonymous']:
        return f"{app_name}/{module_dirname}/index.html"
    
    role_to_template_map = {
        COMMON_ROLE_CONFIG["SITE_ADMIN"]["name"]: "site_admin/site_admin_homepage.html",
        COMMON_ROLE_CONFIG["ORG_ADMIN"]["name"]: "org_admin/org_admin_homepage.html",
        COMMON_ROLE_CONFIG["PROJECT_ADMIN"]["name"]: "project_admin/project_admin_homepage.html",
    }
    
    role = context.get('role')
    if role in role_to_template_map:
        return f"{app_name}/{module_dirname}/{role_to_template_map[role]}"
    else:
        return f"{app_name}/{module_dirname}/general_homepage/general_homepage.html"

def role_homepage(request, role_name):
    user = request.user
    member = Member.objects.get(user=user, active=True)
    roles = member.member_roles.filter(active=True)
    org_id = None
    if request.GET.get('org_id'):
        org_id = request.GET.get('org_id')
        org = Organization.objects.get(id=org_id)
    context = {
        'parent_page': 'home',
        'page': 'role_homepage',
        'page_title': 'Role Home Page',
        
        'user': user,
        'roles': roles,
        'member': member,
        'org_id': org_id,
        'org': org,
    }
    template_url = f"app_jivapms/mod_web/{role_name}/{role_name}_homepage.html"

    try:
        # Try to load the template, if it exists
        get_template(template_url)
        logger.debug(f"Template found: {template_url}")
        return render(request, template_url, context)
    except TemplateDoesNotExist:
        logger.error(f"Template not found: {template_url}")
        # Fall back to the default template
        general_template_url = "app_jivapms/mod_web/general_homepage/general_homepage.html"
        return render(request, general_template_url, context)

def public_frameworks(request):
    organization = Organization.objects.filter(active=True)
    framework = Framework.objects.filter(active=True)
    public_frameworks = Framework.objects.filter(public_framework=True, active=True)
    # Get the related Organization objects for those Frameworks
    org_ids = public_frameworks.values_list('organization__id', flat=True).distinct()
    organizations = Organization.objects.filter(id__in=org_ids)
    
    context = {
        'parent_page': 'home',
        'page': 'frameworks',
        'page_title': 'Public Frameworks Page',
        
        'organizations': organizations,
        'public_frameworks': public_frameworks,
        
    }
    template_url = f"app_organization/mod_framework/public_frameworks/public_frameworks.html"
    return render(request, template_url, context)   


def ajax_display_public_framework(request, framework_id):
    try:
        # Fetch the framework
        framework = get_object_or_404(Framework, id=framework_id, public_framework=True, active=True)

        # Fetch the organization image if available
        org_image_map = OrgImageMap.objects.filter(supporting_frameworks=framework).first()
        image_url = org_image_map.thumbnail.url if org_image_map and org_image_map.thumbnail else ""
        image_original_url = org_image_map.image.url if org_image_map and org_image_map.image else ""

        return JsonResponse({
            'status': 'success',
            'name': framework.name,  # Assuming Framework has a `name` field
            'description': framework.description,  # Assuming Framework has a `description` field
            'content': framework.content,  # Assuming Framework has a `content` field
            'default_text': framework.default_text,  # Assuming Framework has a `default_text` field
            'image_url': image_url,
            'image_original_url': image_original_url,
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

def about_the_project(request):

    
    context = {
        'parent_page': 'home',
        'page': 'about_the_project',
        'page_title': 'About the Project',
    }
    template_url = f"app_jivapms/mod_web/about_the_project.html"
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


def about(request):
    # common about
    
    context = {
        'parent_page': 'home',
        'page': 'about',
        'page_title': 'About Page',
    }
    template_url = f"app_common/common_files/specific/about.html"
    return render(request, template_url, context)   
