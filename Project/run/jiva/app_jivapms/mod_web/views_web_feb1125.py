from app_web.mod_app.all_view_imports import *
from app_memberprofilerole.mod_app.all_model_imports import *
from app_memberprofilerole.mod_member.models_member import *

from app_common.mod_app.all_view_imports import *
from app_jivapms.mod_app.all_view_imports import *
from app_organization.mod_projectmembership.models_projectmembership import *

from app_organization.mod_framework.models_framework import *
from app_organization.mod_org_image_map.models_org_image_map import *
from app_organization.org_decorators import *

app_name = "app_jivapms"
version = "v1"
module_dirname = "mod_web"

from app_jivapms.mod_web.helper_web import *
from app_jivapms.mod_web.views_ajax_web import *


def super_user_stats(request):
    user = request.user
    organization = Organization.objects.filter(active=True)
    framework = Framework.objects.filter(active=True)
    public_frameworks = Framework.objects.filter(public_framework=True, active=True)
    # Get the related Organization objects for those Frameworks
    org_ids = public_frameworks.values_list('organization__id', flat=True).distinct()
    organizations = Organization.objects.filter(id__in=org_ids)
    all_orgs = Organization.objects.filter(active=True)
    # Check the stats
    org_count = organization.count()
    framework_count = framework.count()
    public_framework_count = public_frameworks.count()
   
    org_project_member_counts = []

    for org in all_orgs:
        project_count = org.org_projects.filter(active=True).count()
        member_count = Member.objects.filter(member_roles__org=org).count()
        org_project_member_counts.append({
            'org_id': org.id,
            'org_name': org.name,
            'project_count': project_count,
            'member_count': member_count,
        })
    logger.info(f"Total organizations: {org_count}")
    logger.info(f"Total frameworks: {framework_count}")
    logger.info(f"Total public frameworks: {public_framework_count}")
    for org_stat in org_project_member_counts:
        logger.info(f"Organization ID: {org_stat['org_id']}, Name: {org_stat['org_name']}, Projects: {org_stat['project_count']}, Members: {org_stat['member_count']}")
    
    return { 'org_count': org_count, 'framework_count': framework_count, 
            'public_framework_count': public_framework_count, 
            'org_project_member_counts': org_project_member_counts }

def index(request):
    user = request.user
    #this_member = Member.objects.get(user=user, active=True)
    this_member = None
    organization = Organization.objects.filter(active=True)
    framework = Framework.objects.filter(active=True)
    public_frameworks = Framework.objects.filter(public_framework=True, active=True)
    # Get the related Organization objects for those Frameworks
    org_ids = public_frameworks.values_list('organization__id', flat=True).distinct()
    organizations = Organization.objects.filter(id__in=org_ids)
    all_orgs = Organization.objects.filter(active=True)
     
    
    
    
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
        this_member = Member.objects.get(user=user, active=True)
        if user.is_superuser:
            context['role'] = COMMON_ROLE_CONFIG["SUPER_USER"]["name"]
            super_user_stats(request)
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
        
    this_member_project_memberships = Projectmembership.objects.filter(member=this_member, active=True)
    # Group projects by organization
    org_projects = defaultdict(list)
    for membership in this_member_project_memberships:
        org = membership.project.org  # Assuming project has an `org` attribute
        org_projects[org].append({
            'member': membership.member,          # Include member
            'project': membership.project,        # Include project
            'project_role': membership.project_role,  # Include project_role
        }) if membership.project.active == True else None
    # Assign template based on role
    template_url = get_template_for_role(context)
    context_json = context
    context['context_json'] = context_json
    context['this_member_project_memberships'] = this_member_project_memberships
    context['org_projects'] = dict(org_projects)
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


def role_homepage(request, role_name):
    user = request.user
    member = Member.objects.get(user=user, active=True)
    roles = member.member_roles.filter(active=True)
    
    organizations = Organization.objects.filter(active=True)
    role_id = None
    org_id = None
    org = None
    role_org = None
    lc_role_name = 'no_page'
    context = {}
    context = {
        'parent_page': 'home',
        'page': 'role_homepage',
        'page_title': 'Role Home Page',
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
        'check': 'check',
    }
    if request.GET.get('org_id'):
        org_id = request.GET.get('org_id')
        org = Organization.objects.get(id=org_id)
    if request.GET.get('role_id'):
        role_id = request.GET.get('role_id')
        role_org = Role.objects.get(id=role_id)
        lc_role_name = role_org.name.lower().replace(' ', '_') if role_org else 'no_page'
        
    # quick links for the role
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
        context['role_full'] = context['roles'][0].role.name if context['roles'] else COMMON_ROLE_CONFIG["NO_ROLE"]["name"]

    context_update = {
        'role_id': role_id,
        'org_id': org_id,
        'org': org,
        'role': role_org,
        'lc_role_name': lc_role_name,
        'test': 'test',
    }
    context.update(context_update)
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



from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

@login_required
def JIVAPMS_set_project_id(request, context):
    # Get 'project_id' from GET or session
    project_id = request.GET.get('project_id') or request.session.get('project_id')
    # logger.debug(f">>> === JIVAPMS_set_project_id: project_id={project_id} === <<<")
    # If project_id exists, validate it
    if project_id:
        try:
            # Fetch the project and organization, ensuring it's active
            project = get_object_or_404(Project, id=project_id, active=True)
            org = project.org

            # Update context
            context.update({
                'project': project,
                'org': org,
                'org_id': org.id,
                'organization': org,
                'organization_id': org.id,
                'project_id': project_id,
                'pro_id': project_id
            })

            # Update session
            request.session['project_id'] = project_id
        except Project.DoesNotExist:
            # Handle invalid project_id
            context['project_id'] = None
            request.session['project_id'] = None
    else:
        # No valid project_id provided
        context['project_id'] = None
        request.session['project_id'] = None

    # Return the updated context
    return context


@login_required
def JIVAPMS_get_project_id_from_session(request):
    # Fetch project_id directly from session
    return request.session.get('project_id', None)

from app_organization.mod_org_release.models_org_release import *
from app_organization.mod_org_iteration.models_org_iteration import *
# @login_required
# def get_project_release_and_iteration_details(project_id):
   
#     try:
#         # Fetch the project
#         project = Project.objects.get(id=project_id)
#     except Project.DoesNotExist:
#         return {"error": "Invalid project ID"}

#     current_datetime = now().replace(microsecond=0)
#     details = {
#         "project_id": project_id,
#         "current_release": None,
#         "current_iteration": None,
#         "release_details": None,
#         "iteration_details": None,
#     }

#     # Get the current release from the project
#     if project.project_release:
#         # Fetch the release
#         got_release = project.project_release        
#         release = OrgRelease.objects.get(id=got_release.id)       

#         # Check if the release dates have time components
#         release_start_has_time = (
#             release.release_start_date.time() != time(0, 0, 0) if release.release_start_date else False
#         )
#         release_end_has_time = (
#             release.release_end_date.time() != time(0, 0, 0) if release.release_end_date else False
#         )

#         # Python date comparison
#         if release.release_start_date and release.release_end_date:
#             if (
#                 release.release_start_date.date() <= current_datetime.date() <= release.release_end_date.date()
#                 if not release_start_has_time or not release_end_has_time
#                 else release.release_start_date <= current_datetime <= release.release_end_date
#             ):
#                 details["current_release"] = release
#                 details["release_details"] = {
#                     "id": release.id,
#                     "name": release.name,
#                     "start_date": release.release_start_date,
#                     "end_date": release.release_end_date,
#                 }

#     # Get the current iteration
#     if project.project_iteration:
#         got_iteration = project.project_iteration
#         iteration = OrgIteration.objects.get(id=got_iteration.id)

#         # Check if the iteration dates have time components
#         iteration_start_has_time = (
#             iteration.iteration_start_date.time() != time(0, 0, 0) if iteration.iteration_start_date else False
#         )
#         iteration_end_has_time = (
#             iteration.iteration_end_date.time() != time(0, 0, 0) if iteration.iteration_end_date else False
#         )

#         # Python date comparison
#         if iteration.iteration_start_date and iteration.iteration_end_date:
#             if (
#                 iteration.iteration_start_date.date() <= current_datetime.date() <= iteration.iteration_end_date.date()
#                 if not iteration_start_has_time or not iteration_end_has_time
#                 else iteration.iteration_start_date <= current_datetime <= iteration.iteration_end_date
#             ):
#                 details["current_iteration"] = iteration
#                 details["iteration_details"] = {
#                     "id": iteration.id,
#                     "name": iteration.name,
#                     "start_date": iteration.iteration_start_date,
#                     "end_date": iteration.iteration_end_date,
#                 }

#     return details



from django.utils.timezone import now
from datetime import time
from django.shortcuts import get_object_or_404

def get_project_release_and_iteration_details(project_id):
    logger.debug(f">>> === get_project_release_and_iteration_details: project_id={project_id} === <<<")
    project = None
    try:
        # Fetch the project
        project = Project.objects.get(id=project_id)
    except Project.DoesNotExist:
        return {"error": "Invalid project ID"}
    
    details = { "project_id": project_id }
    current_iteration = None
    next_iteration = None
    # Add results to the details dictionary
    details["current_release"] = None
    details["current_iteration"] = current_iteration
    details["next_iteration"] = next_iteration
    check_release_exists = OrgRelease.objects.filter(id=project.project_release.id, active=True).exists()
    logger.debug(f">>> === Check release exists: {check_release_exists} === <<<")
    if not check_release_exists:
        return details    
    
    ### BEGIN THE PROCESSING FOR RELEASE AND ITERATION ###

    current_datetime = now().replace(microsecond=0)
    details = {
        "project_id": project_id,
        "current_release": None,
        "current_iteration": None,
        "next_iteration": None,
    }

    # Get the current release from the project
    if project.project_release:
        # Fetch the release
        got_release = project.project_release
        #release = OrgRelease.objects.get(id=got_release.id, active=True)
        release = get_object_or_404(OrgRelease, id=got_release.id, active=True)
      
        # Check if the release dates have time components
        release_start_has_time = (
            release.release_start_date.time() != time(0, 0, 0) if release.release_start_date else False
        )
        release_end_has_time = (
            release.release_end_date.time() != time(0, 0, 0) if release.release_end_date else False
        )
        logger.debug(f"Release start date: {release.release_start_date} ==> {release_start_has_time}")
        logger.debug(f"Release end date: {release.release_end_date} ==> {release_end_has_time}")
        # Python date comparison
        if release.release_start_date and release.release_end_date:
            if (
                release.release_start_date.date() <= current_datetime.date() <= release.release_end_date.date()
                if not release_start_has_time or not release_end_has_time
                else release.release_start_date <= current_datetime <= release.release_end_date
            ):
                details["current_release"] = release

    # Get the current and next iterations
    if project.project_release:
        # Fetch all iterations for the release
        iterations = OrgIteration.objects.filter(
            org_release=project.project_release,
            active=True,
        ).order_by("iteration_start_date")

       

        for iteration in iterations:
            # Check if iteration dates have time components
            iteration_start_has_time = (
                iteration.iteration_start_date.time() != time(0, 0, 0) if iteration.iteration_start_date else False
            )
            iteration_end_has_time = (
                iteration.iteration_end_date.time() != time(0, 0, 0) if iteration.iteration_end_date else False
            )
            logger.debug(f"Iteration start date: {iteration.iteration_start_date} ==> {iteration_start_has_time}")
            logger.debug(f"Iteration end date: {iteration.iteration_end_date} ==> {iteration_end_has_time}")
            # Python date comparison for current_iteration
            if (
                iteration.iteration_start_date.date() <= current_datetime.date() <= iteration.iteration_end_date.date()
                if not iteration_start_has_time or not iteration_end_has_time
                else iteration.iteration_start_date <= current_datetime <= iteration.iteration_end_date
            ):
                current_iteration = iteration
                
            # Identify the next_iteration
            if current_iteration and iteration.iteration_start_date >= current_iteration.iteration_end_date:
                next_iteration = iteration
                break

        # Add results to the details dictionary
        details["current_release"] = release
        details["current_iteration"] = current_iteration
        details["next_iteration"] = next_iteration
        logger.debug(f">>> === get_project_release_and_iteration_details: project_id={project_id} {details} === <<<")
    return details









# =========> working one below

# def get_project_release_and_iteration_details(project_id):  

#     try:
#         # Fetch the project
#         project = Project.objects.get(id=project_id)
#     except Project.DoesNotExist:
#         return {"error": "Invalid project ID"}

#     current_datetime = now().replace(microsecond=0)
#     details = {
#         "project_id": project_id,
#         "current_release": None,
#         "current_iteration": None,
#         "next_iteration": None,
#     }

#     # Get the current release from the project
#     if project.project_release:
#         # Fetch the release
#         got_release = project.project_release
#         #release = OrgRelease.objects.get(id=got_release.id, active=True)
#         release = get_object_or_404(OrgRelease, id=got_release.id, active=True)
#         if not release:
#             return details
#         # Check if the release dates have time components
#         release_start_has_time = (
#             release.release_start_date.time() != time(0, 0, 0) if release.release_start_date else False
#         )
#         release_end_has_time = (
#             release.release_end_date.time() != time(0, 0, 0) if release.release_end_date else False
#         )
#         logger.debug(f"Release start date: {release.release_start_date} ==> {release_start_has_time}")
#         logger.debug(f"Release end date: {release.release_end_date} ==> {release_end_has_time}")
#         # Python date comparison
#         if release.release_start_date and release.release_end_date:
#             if (
#                 release.release_start_date.date() <= current_datetime.date() <= release.release_end_date.date()
#                 if not release_start_has_time or not release_end_has_time
#                 else release.release_start_date <= current_datetime <= release.release_end_date
#             ):
#                 details["current_release"] = release

#     # Get the current and next iterations
#     if project.project_release:
#         # Fetch all iterations for the release
#         iterations = OrgIteration.objects.filter(
#             org_release=project.project_release,
#             active=True,
#         ).order_by("iteration_start_date")

       

#         for iteration in iterations:
#             # Check if iteration dates have time components
#             iteration_start_has_time = (
#                 iteration.iteration_start_date.time() != time(0, 0, 0) if iteration.iteration_start_date else False
#             )
#             iteration_end_has_time = (
#                 iteration.iteration_end_date.time() != time(0, 0, 0) if iteration.iteration_end_date else False
#             )
#             logger.debug(f"Iteration start date: {iteration.iteration_start_date} ==> {iteration_start_has_time}")
#             logger.debug(f"Iteration end date: {iteration.iteration_end_date} ==> {iteration_end_has_time}")
#             # Python date comparison for current_iteration
#             if (
#                 iteration.iteration_start_date.date() <= current_datetime.date() <= iteration.iteration_end_date.date()
#                 if not iteration_start_has_time or not iteration_end_has_time
#                 else iteration.iteration_start_date <= current_datetime <= iteration.iteration_end_date
#             ):
#                 current_iteration = iteration

#             # Identify the next_iteration
#             if current_iteration and iteration.iteration_start_date >= current_iteration.iteration_end_date:
#                 next_iteration = iteration
#                 break

#         # Add results to the details dictionary
#         details["current_iteration"] = current_iteration
#         details["next_iteration"] = next_iteration

#     return details
