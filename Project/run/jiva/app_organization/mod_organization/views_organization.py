
from app_organization.mod_app.all_view_imports import *
from app_organization.mod_organization.forms_organization import *
from app_organization.mod_organization.models_organization import *
from app_common.mod_common.models_common import *
from app_memberprofilerole.mod_role.models_role import *
from app_jivapms.mod_app.all_view_imports import *
from app_organization.org_decorators import *
from app_organization.mod_projectmembership.models_projectmembership import *
from app_organization.mod_organizationdetail.models_organizationdetail import *
from app_common.mod_app.all_view_imports import *

app_name = 'app_organization'
app_version = 'v1'

module_name = 'organizations'
module_path = f'mod_organization'

# viewable flag
first_viewable_flag = '__ALL__'  # 'all' or '__OWN__'
viewable_flag = '__ALL__'  # 'all' or '__OWN__'
# Setup dictionaries based on flags
viewable_dict = {} if viewable_flag == '__ALL__' else {'author': user}
first_viewable_dict = {} if first_viewable_flag == '__ALL__' else {'author': user}
def get_viewable_dicts(user, viewable_flag, first_viewable_flag):
    viewable_dict = {} if viewable_flag == '__ALL__' else {'author': user}
    first_viewable_dict = {} if first_viewable_flag == '__ALL__' else {'author': user}
    return viewable_dict, first_viewable_dict
# ============================================================= #
# Define the function to get role context
def get_role_context(user):
    """
    Determines the administrative roles of a user and returns them as a dictionary.
    
    Args:
        user: The user object to check roles for
        
    Returns:
        Dictionary with role information
    """
    # Fetch all active memberships for the user across any organization
    memberships = Member.objects.filter(user=user, active=True)
    member_roles = MemberOrganizationRole.objects.filter(member__in=memberships)
    
    # Check if user is a site admin
    is_site_admin = MemberOrganizationRole.objects.filter(
        member__in=memberships, 
        role__name=site_admin_str
    ).exists()
    
    # Default values
    is_org_admin = False
    is_project_admin = False
    non_admin_role = False
    admin_org_ids = []
    project_org_ids = []
    member_org_ids = []
    
    if not is_site_admin:
        # Check if user is an org admin
        org_admin_roles = MemberOrganizationRole.objects.filter(
            member__in=memberships,
            role__name=org_admin_str
        )
        is_org_admin = org_admin_roles.exists()
        
        if is_org_admin:
            # Extract organization IDs where user is an org admin
            admin_org_ids = list(org_admin_roles.values_list('org_id', flat=True).distinct())
        else:
            # Check if user is a project admin
            project_admin_roles = MemberOrganizationRole.objects.filter(
                member__in=memberships,
                role__name=project_admin_str
            )
            is_project_admin = project_admin_roles.exists()
            
            if is_project_admin:
                # Extract organization IDs where user is a project admin
                project_org_ids = list(project_admin_roles.values_list('org_id', flat=True).distinct())
            else:
                # User is just a regular member
                project_member_roles = MemberOrganizationRole.objects.filter(
                    member__in=memberships,
                    role__name__in=PROJECT_MEMBER_ROLES
                )
                non_admin_role = True
                
                # Extract organization IDs where user is a member
                member_org_ids = list(project_member_roles.values_list('org_id', flat=True).distinct())
    
    # Determine if user has any admin privileges (site or org)
    relevant_admin = is_site_admin or is_org_admin
    
    # Create and return role_context dictionary
    return {
        'is_site_admin': is_site_admin,
        'is_org_admin': is_org_admin,
        'is_project_admin': is_project_admin,
        'non_admin_role': non_admin_role,
        'relevant_admin': relevant_admin,
        'admin_org_ids': admin_org_ids,
        'project_org_ids': project_org_ids,
        'member_org_ids': member_org_ids,
    }

@login_required
def list_organizations(request):
    # take inputs
    # process inputs
    user = request.user       
    objects_count = 0    
    show_all = request.GET.get('all', '25')
    objects_per_page = int(show_all) if show_all != 'all' else 25
    pagination_options = [5, 10, 15, 25, 50, 100, 'all']
    selected_bulk_operations = None
    search_query = request.GET.get('search', '')
    deleted_count = 0
    relevant_admin = False
    is_site_admin = False
    is_org_admin = False
    is_project_admin = False
    # Fetch all active memberships for the user across any organization
    memberships = Member.objects.filter(user=user, active=True)
    member_roles = MemberOrganizationRole.objects.filter(member__in=memberships)
    is_site_admin = MemberOrganizationRole.objects.filter(member__in=memberships, role__name=site_admin_str).exists()
    
    # non-admin roles
    # user has no admin roles
    non_admin_role = False
    
    # Filter organizations based on user access
    if is_site_admin:
        # Org admins can see all active organizations in the site
        tobjects = Organization.objects.filter(active=True)        
        logger.debug(f">>> === SiteAdmin: all: Organizations:{tobjects} === <<<")
    else:
        # Fetch all orgs where user is an org admin through any of their memberships
        logger.debug(f">>> === OrgAdmin: memberships:{memberships} === <<<")
        org_admin_roles = MemberOrganizationRole.objects.filter(
            member__in=memberships,
            role__name=org_admin_str
        )
        logger.debug(f">>> === OrgAdmin: org_admin_roles:{org_admin_roles} === <<<")
        is_org_admin = org_admin_roles.exists()
        
        
        # Check for project admin privileges if not an org admin
        if is_org_admin:
            # Extract organization IDs where user is an org admin
            org_ids = org_admin_roles.values_list('org_id', flat=True).distinct()
            logger.debug(f">>> === OrgAdmin: is_org_admin: {is_org_admin}, org_ids:{org_ids} === <<<")
            logger.debug(f">>> ===  org_ids:{org_ids} === <<<")
            # Filter  organizations where the user has specific site membership (Viewer, Editor, Admin)
            # Fetch organizations based on the org admin role
            tobjects = Organization.objects.filter(id__in=org_ids, active=True).order_by('position')
            logger.debug(f">>> === OrgAdmin Limited Access: Organizations:{tobjects} === <<<")
        else:            
            project_admin_roles = MemberOrganizationRole.objects.filter(
                member__in=memberships,
                role__name=project_admin_str
            )
            is_project_admin = project_admin_roles.exists()
            project_org_ids = project_admin_roles.values_list('org_id', flat=True).distinct()
            
            if is_project_admin:
                # Fetch organizations based on the project admin role
                tobjects = Organization.objects.filter(id__in=project_org_ids, active=True)
                logger.debug(f">>> === ProjectAdmin Limited Access: Organizations:{project_org_ids} === <<<")
            else:
                # If the user is a non-admin
                project_member_roles = MemberOrganizationRole.objects.filter(
                    member__in=memberships,
                    role__name__in=PROJECT_MEMBER_ROLES
                )
                tobjects = []
                non_admin_role = True
                is_project_member = project_member_roles.exists()
                project_org_ids = project_member_roles.values_list('org_id', flat=True).distinct()
                tobjects = Organization.objects.filter(id__in=project_org_ids, active=True)
                logger.debug(f">>> === LIST_ORGANIZATIONS: MEMBER {member_roles} === <<<")
                logger.debug(">>> === User has no admin privileges in any organization === <<<")
    
    
    relevant_admin = is_site_admin or is_org_admin
    
    if search_query:
        tobjects = Organization.objects.filter(name__icontains=search_query, 
                                            active=True,deleted=False ).order_by('position')
        deleted = Organization.objects.filter(active=False, deleted=False).order_by('position')
        deleted_count = deleted.count()
    else:
        tobjects = Organization.objects.filter(active=True).order_by('position')
        deleted = Organization.objects.filter(active=False, deleted=False).order_by('position')
        deleted_count = deleted.count()
    
    if show_all == 'all':
        # No pagination, show all records
        page_obj = tobjects
        objects_per_page = tobjects.count()
    else:
        print(f">>> === show_all: {show_all} === <<<")   
        objects_per_page = int(show_all)     
        paginator = Paginator(tobjects, objects_per_page)  # Show 10 tobjects per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    
    if tobjects:
        objects_count = tobjects.count()
    
    ## processing the POST
    if request.method == 'POST':
        selected_bulk_operations = request.POST.getlist('bulk_operations')
        bulk_operation = str(selected_bulk_operations[0].strip()) if selected_bulk_operations else None
            
        if 'selected_item' in request.POST:  
            selected_items = request.POST.getlist('selected_item')  # Use getlist to ensure all are captured
            for item_id in selected_items:
                item = int(item_id)  
                if bulk_operation == 'bulk_delete':
                    object = get_object_or_404(Organization, pk=item, active=True, **viewable_dict)
                    object.active = False
                    object.save()
                    
                elif bulk_operation == 'bulk_done':
                    object = get_object_or_404(Organization, pk=item, active=True, **viewable_dict)
                    object.done = True
                    object.save()
                    
                elif bulk_operation == 'bulk_not_done':
                    object = get_object_or_404(Organization, pk=item, active=True, **viewable_dict)
                    object.done = False
                    object.save()
                    
                elif bulk_operation == 'bulk_blocked':  # Correct the operation check here
                    object = get_object_or_404(Organization, pk=item, active=True, **viewable_dict)
                    object.blocked = True
                    object.save()
                    
                else:
                    return redirect('list_organizations')
            return redirect('list_organizations')
    
    
    # send outputs info, template,
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'list_organizations',
        
        'module_path': module_path,
        'user': user,
        'tobjects': tobjects,
        'page_obj': page_obj,
        'objects_count': objects_count,
        'objects_per_page': objects_per_page,
        'deleted_count': deleted_count,
        'show_all': show_all,
        'pagination_options': pagination_options,
        'selected_bulk_operations': selected_bulk_operations,

        'page_title': f'Organization List',
        'relevant_admin': relevant_admin,
        'is_project_admin': is_project_admin,
        'is_org_admin': is_org_admin,
        'is_site_admin': is_site_admin,
    }       
    template_file = f"{app_name}/{module_path}/list_organizations.html"
    return render(request, template_file, context)



# list the deleted objects
# ============================================================= #
@login_required
def list_deleted_organizations(request):
    # take inputs
    # process inputs
    user = request.user        
    objects_count = 0    
    show_all = request.GET.get('all', '25')
    objects_per_page = int(show_all) if show_all != 'all' else 25
    pagination_options = [5, 10, 15, 25, 50, 100, 'all']
    selected_bulk_operations = None

    show_all = request.GET.get('all', '25')
    objects_per_page = int(show_all) if show_all != 'all' else 25
    
    search_query = request.GET.get('search', '')
    if search_query:
        tobjects = Organization.objects.filter(name__icontains=search_query, 
                                            **viewable_dict, active=False, deleted=False).order_by('position')
    else:
        tobjects = Organization.objects.filter(active=False, deleted=False, **viewable_dict).order_by('position')
    
    if show_all == 'all':
        # No pagination, show all records
        page_obj = tobjects
        objects_per_page = tobjects.count()
    else:
        print(f">>> === show_all: {show_all} === <<<")   
        objects_per_page = int(show_all)     
        paginator = Paginator(tobjects, objects_per_page)  # Show 10 tobjects per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    objects_count = tobjects.count()
    
    ## processing the POST
    if request.method == 'POST':
        selected_bulk_operations = request.POST.getlist('bulk_operations')
        bulk_operation = str(selected_bulk_operations[0].strip()) if selected_bulk_operations else None
            
        if 'selected_item' in request.POST:  
                selected_items = request.POST.getlist('selected_item')  # Use getlist to ensure all are captured
                for item_id in selected_items:
                    item = int(item_id)  
                    if bulk_operation == 'bulk_restore':
                        object = get_object_or_404(Organization, pk=item, active=False, **viewable_dict)
                        object.active = True               
                        object.save()
                    elif bulk_operation == 'bulk_erase':
                        object = get_object_or_404(Organization, pk=item, active=False, **viewable_dict)
                        object.active = False  
                        object.deleted = True             
                        object.save()
                    else:
                        return redirect('list_deleted_organizations')
                return redirect('list_deleted_organizations')
    
    
    # send outputs info, template,
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'list_deleted_organizations',
        
        'module_path': module_path,
        'user': user,
        'tobjects': tobjects,
        'page_obj': page_obj,
        'objects_count': objects_count,
        'objects_per_page': objects_per_page,
        'show_all': show_all,
        'pagination_options': pagination_options,
        'selected_bulk_operations': selected_bulk_operations,

        'page_title': f'Organization List',
    }       
    template_file = f"{app_name}/{module_path}/list_deleted_organizations.html"
    return render(request, template_file, context)




# Create View
@login_required
def create_organization(request):
    user = request.user
    logger.debug(f">>> === TEST1: CREATE ORGANIZATION === <<<")
    
    if request.method == 'POST':
        form = OrganizationForm(request.POST)
        if form.is_valid():
            form.instance.author = user
            organization = form.save()

            org_admin_roles = Role.objects.filter(name=org_admin_str, org=organization).values_list('id', flat=True)
            member = Member.objects.filter(user=user, active=True).first()
            member_create, created = MemberOrganizationRole.objects.get_or_create(
                member=member, 
                org=organization, 
                role_id__in=org_admin_roles
            )
            logger.debug(f">>> === member_create: {member_create} === <<<")
            
            # Check if it's an AJAX request
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'organization_id': organization.id,
                    'organization_name': organization.name,
                    'message': 'Organization created successfully!'
                })
            
            # For regular form submission
            return redirect('list_organizations')
        else:
            print(f">>> === form.errors: {form.errors} === <<<")
            
            # Return form errors for AJAX requests
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': 'Form validation failed',
                    'errors': form.errors.as_json()
                }, status=400)
    else:
        form = OrganizationForm()
    
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'create_organization',
        'module_path': module_path,
        'form': form,
        'page_title': f'Create Organization',
    }
    template_file = f"{app_name}/{module_path}/create_organization.html"
    return render(request, template_file, context)


# Edit View
@login_required
def edit_organization(request, organization_id):
    user = request.user
    
    object = get_object_or_404(Organization, pk=organization_id, active=True, **viewable_dict)
    if request.method == 'POST':
        form = OrganizationForm(request.POST, instance=object)
        if form.is_valid():
            form.instance.author = user
            organization = form.save()
            
            # Check if it's an AJAX request
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'organization_id': organization.id,
                    'organization_name': organization.name,
                    'message': 'Organization updated successfully!'
                })
            
            return redirect('list_organizations')
        else:
            print(f">>> === form.errors: {form.errors} === <<<")
            
            # Return form errors for AJAX requests
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': 'Form validation failed',
                    'errors': form.errors.as_json()
                }, status=400)
    else:
        form = OrganizationForm(instance=object)
    
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'edit_organization',
        
        'module_path': module_path,
        'form': form,
        'object': object,
        'page_title': f'Edit Organization',
    }
    template_file = f"{app_name}/{module_path}/edit_organization.html"
    return render(request, template_file, context)  

@login_required
def delete_organization(request, organization_id):
    user = request.user
    
    object = get_object_or_404(Organization, pk=organization_id, active=True, **viewable_dict)
    if request.method == 'POST':
        object.active = False
        object.save()
        return redirect('list_organizations')

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'delete_organization',
        
        'module_path': module_path,        
        'object': object,
        'page_title': f'Delete Organization',
    }
    template_file = f"{app_name}/{module_path}/delete_organization.html"
    return render(request, template_file, context)


@login_required
def permanent_deletion_organization(request, organization_id):
    user = request.user
    
    object = get_object_or_404(Organization, pk=organization_id, active=False, deleted=False, **viewable_dict)
    if request.method == 'POST':
        object.active = False
        object.deleted = True
        object.save()
        return redirect('list_organizations')

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'permanent_deletion_organization',
        
        'module_path': module_path,        
        'object': object,
        'page_title': f'Permanent Deletion Organization',
    }
    template_file = f"{app_name}/{module_path}/permanent_deletion_organization.html"
    return render(request, template_file, context)


@login_required
def restore_organization(request, organization_id):
    user = request.user
    object = get_object_or_404(Organization, pk=organization_id, active=False, **viewable_dict)
    object.active = True
    object.save()
    return redirect('list_organizations')
   


@login_required
def view_organization(request,  organization_id):
    user = request.user
    
    object = get_object_or_404(Organization, pk=organization_id, active=True, **viewable_dict)    

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'view_organization',
        
        'module_path': module_path,
        'object': object,
        'page_title': f'View Organization',
    }
    template_file = f"{app_name}/{module_path}/view_organization.html"
    return render(request, template_file, context)



@login_required
@site_admin_this_org_admin_or_member_of_org
def org_homepage(request,  org_id):
    user = request.user
    role_context = get_role_context(user)
    organization = get_object_or_404(Organization, pk=org_id, 
                               active=True, **viewable_dict)    
    org_detail = organization.org_details.filter(active=True).first()
    logger.debug(f">>> === org_detail: {organization.org_details} === <<<")
    
    projects = organization.org_projects.filter(active=True)
    # if it is a project admin 
    memberships = Member.objects.filter(user=user, active=True)
    role_ids = ProjectRole.objects.filter(active=True).values_list('id', flat=True)
    
    
    # Fetch projects the user has access to, along with their roles
    project_roles = Projectmembership.objects.filter(
        member__in=memberships,
        project_role_id__in=role_ids,
        active=True,
        project__org_id=org_id,
        project__active=True
    ).values('project_id', 'project_role__role_type')  # Adjust field names as necessary
    
    
    # Group roles by project
    project_roles_dict = defaultdict(list)
    for entry in project_roles:
        project_roles_dict[entry['project_id']].append(entry['project_role__role_type'])

    # Fetch the projects (distinct and ordered)
    projects = Project.objects.filter(
        id__in=project_roles_dict.keys()
    ).distinct().order_by('position')
    logger.debug(f">>> === |||||||Projects: {projects} with Roles: {dict(project_roles_dict)} === <<<")
    
    # To check roles for a specific project
    for project in projects:
        logger.debug(f"Project: {project.name}, Roles: {project_roles_dict.get(project.id, [])}")
    
  
    # Prepare context with projects and their roles
    projects_with_roles = []
    for project in projects:
        projects_with_roles.append({
            'id': project.id,
            'name': project.name,
            'description': project.description,
            'roles': ', '.join(project_roles_dict.get(project.id, []))  # Join roles as a string
        })

    # check the organization role
    org_admin_role = MemberOrganizationRole.objects.filter(
                member__in=memberships,
                role__name=org_admin_str
            )
    is_org_admin = org_admin_role.exists()
    logger.debug(f">>> === USER: {user} is an ORG ADMIN {is_org_admin} === <<<")
    if is_org_admin:
        projects = Project.objects.filter(org_id=org_id, active=True)
    #roadmap_items = organization.roadmap_items.all().delete()
    roadmap_items = organization.roadmap_items.order_by('start_date').filter(active=True)
    logger.debug(f">>> === roadmap_items: {roadmap_items} === <<<")
    
    # Show all active records
    active_items = organization.roadmap_items.filter(active=True)
    print(active_items.values('id', 'active'))

    # Show all inactive records
    inactive_items = organization.roadmap_items.filter(active=False)
    print(inactive_items.values('id', 'active'))

    # Create a dynamic Gantt chart string for Mermaid.js
    roadmap_str = "gantt\n    title Organizational Roadmap\n    dateFormat  YYYY-MM-DD\n"
    
    current_section = ""
    
    for item in roadmap_items:

        if item.section != current_section:
            roadmap_str += f"    section {item.section}\n"
            current_section = item.section
        
        roadmap_str += f"    {item.task_name} :{item.status}, {item.start_date}, {item.end_date}\n"

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'view_organization',
        
        'module_path': module_path,
        'user': user,
        'organization': organization,
        'org_detail': org_detail,
        'projects': projects,
        'project_roles_dict': dict(project_roles_dict),
        'projects_with_roles': projects_with_roles,
        'roadmap': roadmap_str,
        'page_title': f'Organization Homepage',
    }
    context.update(role_context)
    editable = request.editable
    if editable:
        template_file = f"{app_name}/{module_path}/organization_homepage.html"
    else:
        template_file = f"{app_name}/{module_path}/viewer_organization_homepage.html"
    return render(request, template_file, context)

# Dashboard View for Organizations
@login_required
def dashboard_organizations(request):
    user = request.user       
    
    # Variables for dashboard stats
    total_organizations = 0
    active_projects = 0
    total_members = 0
    recent_activities = 0
    
    # Authorization variables
    relevant_admin = False
    is_site_admin = False
    is_org_admin = False
    is_project_admin = False
    
    # Fetch all active memberships for the user across any organization
    memberships = Member.objects.filter(user=user, active=True)
    member_roles = MemberOrganizationRole.objects.filter(member__in=memberships)
    is_site_admin = MemberOrganizationRole.objects.filter(member__in=memberships, role__name=site_admin_str).exists()
    
    # Get organizations based on user role
    if is_site_admin:
        # Make sure we're only counting active=True and deleted=False
        organizations = Organization.objects.filter(active=True, deleted=False)
        total_organizations = organizations.count()
        active_projects = Project.objects.filter(active=True, deleted=False).count()
        # Rest of the code remains the same...

    # And similarly update all other organization queries to include both active=True and deleted=False:
    else:
        # Check if user is org admin
        org_admin_roles = MemberOrganizationRole.objects.filter(
            member__in=memberships,
            role__name=org_admin_str
        )
        is_org_admin = org_admin_roles.exists()
        
        if is_org_admin:
            org_ids = org_admin_roles.values_list('org_id', flat=True).distinct()
            # Update the filter here too
            organizations = Organization.objects.filter(id__in=org_ids, active=True, deleted=False).order_by('position')
            total_organizations = Organization.objects.filter(active=True, deleted=False)
            my_organizations = organizations.count()
            active_projects = Project.objects.filter(org_id__in=org_ids, active=True).count()
            member_org_roles = MemberOrganizationRole.objects.filter(org_id__in=org_ids)
            member_ids = member_org_roles.values_list('member_id', flat=True).distinct()
            total_members = member_ids.count()
            recent_activities = MemberOrganizationRole.objects.filter(org_id__in=org_ids).order_by('-id')[:10]
        else:
            # Check if user is project admin
            project_admin_roles = MemberOrganizationRole.objects.filter(
                member__in=memberships,
                role__name=project_admin_str
            )
            is_project_admin = project_admin_roles.exists()
            
            if is_project_admin:
                project_org_ids = project_admin_roles.values_list('org_id', flat=True).distinct()
                organizations = Organization.objects.filter(id__in=project_org_ids, active=True)
                total_organizations = organizations.count()
                active_projects = Project.objects.filter(org_id__in=project_org_ids, active=True).count()
                project_memberships = Projectmembership.objects.filter(project__org_id__in=project_org_ids, active=True)
                member_ids = project_memberships.values_list('member_id', flat=True).distinct()
                total_members = member_ids.count()
                recent_activities = Projectmembership.objects.filter(project__org_id__in=project_org_ids).order_by('-id')[:10]
            else:
                # Regular member
                project_member_roles = MemberOrganizationRole.objects.filter(
                    member__in=memberships,
                    role__name__in=PROJECT_MEMBER_ROLES
                )
                project_org_ids = project_member_roles.values_list('org_id', flat=True).distinct()
                organizations = Organization.objects.filter(id__in=project_org_ids, active=True)
                total_organizations = organizations.count()
                active_projects = Project.objects.filter(
                    projectmembership__member__in=memberships, 
                    active=True
                ).distinct().count()
                member_project_ids = Projectmembership.objects.filter(
                    member__in=memberships, 
                    active=True
                ).values_list('project_id', flat=True)
                project_memberships = Projectmembership.objects.filter(
                    project_id__in=member_project_ids, 
                    active=True
                )
                member_ids = project_memberships.values_list('member_id', flat=True).distinct()
                total_members = member_ids.count()
                recent_activities = Projectmembership.objects.filter(
                    project_id__in=member_project_ids
                ).order_by('-id')[:10]
    
    # Calculate monthly organization statistics for chart
    current_year = timezone.now().year
    monthly_org_counts = []
    monthly_project_counts = []
    
    for month in range(1, 13):
        # Count organizations created in this month
        month_orgs = Organization.objects.filter(
            created_at__year=current_year,
            created_at__month=month,
            active=True
        ).count()
        monthly_org_counts.append(month_orgs)
        
        # Count projects created in this month
        month_projects = Project.objects.filter(
            created_at__year=current_year,
            created_at__month=month,
            active=True
        ).count()
        monthly_project_counts.append(month_projects)
    
    # Get authors of organizations for distribution chart
    author_stats = Organization.objects.filter(active=True).values('author__username').annotate(
        count=Count('author')
    ).order_by('-count')[:5]  # Top 5 authors
    
    # Format for chart
    author_labels = [item['author__username'] or 'Unknown' for item in author_stats]
    author_counts = [item['count'] for item in author_stats]
    
    # Get list of recent organizations
    recent_organizations = organizations.order_by('-created_at')[:5]  # Most recently created
    
    # Add project and member counts for each organization
    for org in recent_organizations:
        org.project_count = Project.objects.filter(org=org, active=True).count()
        org.member_count = MemberOrganizationRole.objects.filter(org=org).values('member').distinct().count()
    
    relevant_admin = is_site_admin or is_org_admin
    
    # send outputs info, template,
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'dashboard_organizations',
        
        'module_path': module_path,
        'user': user,
        'organizations': organizations,
        'total_organizations_count': total_organizations.count(),
        'my_organizations_count': my_organizations,
        'total_organizations': total_organizations,
        'my_organizations': organizations,
        'active_projects': active_projects,
        'total_members': total_members,
        'recent_activities': recent_activities,
        'recent_orgs': recent_organizations,
        
        # Chart data
        'monthly_org_counts': monthly_org_counts,
        'monthly_project_counts': monthly_project_counts,
        'author_labels': author_labels,
        'author_counts': author_counts,

        'page_title': 'Organizations Dashboard',
        'relevant_admin': relevant_admin,
        'is_project_admin': is_project_admin,
        'is_org_admin': is_org_admin,
        'is_site_admin': is_site_admin,
    }       
    template_file = f"{app_name}/{module_path}/dashboard_organizations.html"
    return render(request, template_file, context)