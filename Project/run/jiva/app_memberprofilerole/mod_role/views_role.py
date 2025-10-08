
from app_memberprofilerole.mod_app.all_view_imports import *
from app_memberprofilerole.mod_role.models_role import *
from app_memberprofilerole.mod_role.forms_role import *
from app_memberprofilerole.mod_member.models_member import *

from app_organization.mod_organization.models_organization import *

from app_common.mod_common.models_common import *

app_name = 'app_memberprofilerole'
app_version = 'v1'

module_name = 'roles'
module_path = f'mod_role'

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
@login_required
def list_roles(request, org_id):
    # take inputs
    # process inputs
    user = request.user       
    objects_count = 0    
    show_all = request.GET.get('all', '25')
    objects_per_page = int(show_all) if show_all != 'all' else 25
    pagination_options = [5, 10, 15, 25, 50, 100, 'all']
    selected_bulk_operations = None
    deleted_count = 0
    organization = Organization.objects.get(id=org_id, active=True, 
                                                **first_viewable_dict)
    
    search_query = request.GET.get('search', '')
    if search_query:
        tobjects = Role.objects.filter(name__icontains=search_query, 
                                            org_id=org_id, **viewable_dict).order_by('position')
    else:
        tobjects = Role.objects.filter(active=True, org_id=org_id, author=user).order_by('position')
        deleted = Role.objects.filter(active=False, deleted=False,
                                org_id=org_id,
                               **viewable_dict).order_by('position')
        deleted_count = deleted.count()
    
    if show_all == 'all':
        # No pagination, show all records
        page_obj = tobjects
        objects_per_page = tobjects.count()
    else:
        objects_per_page = int(show_all)     
        paginator = Paginator(tobjects, objects_per_page)  
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    
    objects_count = tobjects.count()
    
    
    ## processing the POST
    if request.method == 'POST':
        selected_bulk_operations = request.POST.getlist('bulk_operations')
        bulk_operation = str(selected_bulk_operations[0].strip()) if selected_bulk_operations else None
             
        if 'selected_item' in request.POST:  # Correct the typo here
            selected_items = request.POST.getlist('selected_item')  # Use getlist to ensure all are captured
            for item_id in selected_items:
                item = int(item_id)  # Ensure item_id is converted to int if necessary
                if bulk_operation == 'bulk_delete':
                    object = get_object_or_404(Role, pk=item, active=True, **viewable_dict)
                    object.active = False
                    object.save()
                    
                elif bulk_operation == 'bulk_done':
                    object = get_object_or_404(Role, pk=item, active=True, **viewable_dict)
                    object.done = True
                    object.save()
                    
                elif bulk_operation == 'bulk_not_done':
                    object = get_object_or_404(Role, pk=item, active=True, **viewable_dict)
                    object.done = False
                    object.save()
                    
                elif bulk_operation == 'bulk_blocked':  # Correct the operation check here
                    object = get_object_or_404(Role, pk=item, active=True, **viewable_dict)
                    object.blocked = True
                    object.save()
                    
                else:
                    redirect('list_roles', org_id=org_id)
            return redirect('list_roles', org_id=org_id)
    
    # send outputs info, template,
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'list_roles',
        'organization': organization,
        'org_id': org_id,
        
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
        'page_title': f'Role List',
    }       
    template_file = f"{app_name}/{module_path}/list_roles.html"
    return render(request, template_file, context)





# ============================================================= #
@login_required
def list_deleted_roles(request, org_id):
    # take inputs
    # process inputs
    user = request.user       
    objects_count = 0    
    show_all = request.GET.get('all', '25')
    objects_per_page = int(show_all) if show_all != 'all' else 25
    pagination_options = [5, 10, 15, 25, 50, 100, 'all']
    selected_bulk_operations = None
    organization = Organization.objects.get(id=org_id, active=True, 
                                                **first_viewable_dict)
    
    search_query = request.GET.get('search', '')
    if search_query:
        tobjects = Role.objects.filter(name__icontains=search_query, 
                                            active=False,
                                            org_id=org_id, **viewable_dict).order_by('position')
    else:
        tobjects = Role.objects.filter(active=False, org_id=org_id,
                                            **viewable_dict).order_by('position')        
    
    if show_all == 'all':
        # No pagination, show all records
        page_obj = tobjects
        objects_per_page = tobjects.count()
    else:
        objects_per_page = int(show_all)     
        paginator = Paginator(tobjects, objects_per_page)  
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    objects_count = tobjects.count()
    
    ## processing the POST
    if request.method == 'POST':
        selected_bulk_operations = request.POST.getlist('bulk_operations')
        bulk_operation = str(selected_bulk_operations[0].strip()) if selected_bulk_operations else None
     
        if 'selected_item' in request.POST:  # Correct the typo here
                selected_items = request.POST.getlist('selected_item')  # Use getlist to ensure all are captured
                for item_id in selected_items:
                    item = int(item_id)  # Ensure item_id is converted to int if necessary
                    if bulk_operation == 'bulk_restore':
                        object = get_object_or_404(Role, pk=item, active=False, **viewable_dict)
                        object.active = True
                        object.save()         
                    elif bulk_operation == 'bulk_erase':
                        object = get_object_or_404(Role, pk=item, active=False, **viewable_dict)
                        object.active = False  
                        object.deleted = True             
                        object.save()    
                    else:
                        redirect('list_roles', org_id=org_id)
                redirect('list_roles', org_id=org_id)
    
    # send outputs info, template,
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'list_deleted_roles',
        'organization': organization,
        'org_id': org_id,
        
        'module_path': module_path,
        'user': user,
        'tobjects': tobjects,
        'page_obj': page_obj,
        'objects_count': objects_count,
        'objects_per_page': objects_per_page,
        'show_all': show_all,
        'pagination_options': pagination_options,
        'selected_bulk_operations': selected_bulk_operations,
        'page_title': f'Role List',
    }       
    template_file = f"{app_name}/{module_path}/list_deleted_roles.html"
    return render(request, template_file, context)



# Create View
@login_required
def create_role(request, org_id):
    user = request.user
    organization = Organization.objects.get(id=org_id, active=True, 
                                                **first_viewable_dict)
    
    if request.method == 'POST':
        form = RoleForm(request.POST)
        if form.is_valid():
            form.instance.author = user
            form.instance.org_id = org_id
            form.save()
        else:
            print(f">>> === form.errors: {form.errors} === <<<")
        return redirect('list_roles', org_id=org_id)
    else:
        form = RoleForm()

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'create_role',
        'organization': organization,
        'org_id': org_id,
        
        'module_path': module_path,
        'form': form,
        'page_title': f'Create Role',
    }
    template_file = f"{app_name}/{module_path}/create_role.html"
    return render(request, template_file, context)




# Edit
@login_required
def edit_role(request, org_id, role_id):
    user = request.user
    organization = Organization.objects.get(id=org_id, active=True, 
                                                **first_viewable_dict)
    
    object = get_object_or_404(Role, pk=role_id, active=True,**viewable_dict)
    if request.method == 'POST':
        form = RoleForm(request.POST, instance=object)
        if form.is_valid():
            form.instance.author = user
            form.instance.org_id = org_id
            form.save()
        else:
            print(f">>> === form.errors: {form.errors} === <<<")
        return redirect('list_roles', org_id=org_id)
    else:
        form = RoleForm(instance=object)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'edit_role',
        'organization': organization,
        'org_id': org_id,
        
        'module_path': module_path,
        'form': form,
        'object': object,
        'page_title': f'Edit Role',
    }
    template_file = f"{app_name}/{module_path}/edit_role.html"
    return render(request, template_file, context)



@login_required
def delete_role(request, org_id, role_id):
    user = request.user
    organization = Organization.objects.get(id=org_id, active=True, 
                                                **first_viewable_dict)
    
    object = get_object_or_404(Role, pk=role_id, active=True,**viewable_dict)
    if request.method == 'POST':
        object.active = False
        object.save()
        return redirect('list_roles', org_id=org_id)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'delete_role',
        'organization': organization,
        'org_id': org_id,
        
        'module_path': module_path,        
        'object': object,
        'page_title': f'Delete Role',
    }
    template_file = f"{app_name}/{module_path}/delete_role.html"
    return render(request, template_file, context)


@login_required
def permanent_deletion_role(request, org_id, role_id):
    user = request.user
    organization = Organization.objects.get(id=org_id, active=True, 
                                                **first_viewable_dict)
    
    object = get_object_or_404(Role, pk=role_id, active=False, deleted=False, **viewable_dict)
    if request.method == 'POST':
        object.active = False
        object.deleted = True
        object.save()
        return redirect('list_roles', org_id=org_id)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'permanent_deletion_role',
        'organization': organization,
        'org_id': org_id,
        
        'module_path': module_path,        
        'object': object,
        'page_title': f'Permanent Deletion Role',
    }
    template_file = f"{app_name}/{module_path}/permanent_deletion_role.html"
    return render(request, template_file, context)


@login_required
def restore_role(request,  org_id, role_id):
    user = request.user
    object = get_object_or_404(Role, pk=role_id, active=False,**viewable_dict)
    object.active = True
    object.save()
    return redirect('list_roles', org_id=org_id)
   


@login_required
def view_role(request, org_id, role_id):
    user = request.user
    organization = Organization.objects.get(id=org_id, active=True, 
                                                **first_viewable_dict)
    
    object = get_object_or_404(Role, pk=role_id, active=True,**viewable_dict)    

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'view_role',
        'organization': organization,
        'org_id': org_id,
        
        'module_path': module_path,
        'object': object,
        'page_title': f'View Role',
    }
    template_file = f"{app_name}/{module_path}/view_role.html"
    return render(request, template_file, context)



# @login_required
# def view_my_role(request):
#     user = request.user
#     super_user = False
#     no_of_roles = 0
#     multiple_roles = False
#     organization = None
#     user_roles_data = []
#     members = []
    
#     try:
#         # Fetch the member and their roles in a single query
#         members = Member.objects.prefetch_related('member_roles__role', 'member_roles__org').filter(user=user)
#     except Member.DoesNotExist:
#         # Handle the case where a Member does not exist for the user
#         print(f"No Member entry found for user: {user.id}")
    
#     # Populate roles data if the member exists
#     for member in members:
#         user_data = {
#             'member_id': member.id,
#             'username': member.user.username if member.user else 'Unknown User',
#             'roles': []
#         }

#         # Get active roles
#         active_roles = member.member_roles.filter(active=True, member=member)
#         for role in active_roles:
#             role_data = {
#                 'org_id': role.org.id if role.org else None,
#                 'role_id': role.role.id if role.role else None,
#                 'role_name': role.role.name if role.role else 'No Role',
#                 'org_name': role.org.name if role.org else 'No Organization',
#             }
#             user_data['roles'].append(role_data)

#         # Append the user's roles data
#         user_roles_data.append(user_data)

#     if user.is_authenticated:
#         if user.is_superuser:
#             super_user = True
#         elif members:
#             member = members.first()
#             roles = member.member_roles.filter(active=True)
#             no_of_roles = roles.count()
#             multiple_roles = no_of_roles > 1
#         else:
#             # Handle case where no roles are found for the user
#             print(f"No roles found for user: {user.id}")
    
#     # Context for rendering the page
#     context = {
#         'parent_page': '___PARENTPAGE___',
#         'page': 'view_my_role',
#         'user': user,
#         'super_user': super_user,
#         'no_of_roles': no_of_roles,
#         'multiple_roles': multiple_roles,
#         'user_roles_data': user_roles_data,
#         'page_title': 'View Role',
#     }

    # # Render the appropriate template
    # template_file = f"{app_name}/{module_path}/view_my_role.html"
    # return render(request, template_file, context)


@login_required
def view_my_role(request):
    user = request.user
    context = {
        'super_user': user.is_superuser,
        'user_roles_data': [],
        'multiple_roles': False,
        'no_of_roles': 0,
    'admin_orgs_unique': [],
    }

    if user.is_superuser:
        context.update({
            'page_title': 'Super User - Access to All',
        })
    else:
        members = Member.objects.prefetch_related('member_roles__role', 'member_roles__org').filter(user=user)
        if members.exists():
            for member in members:
                roles = member.member_roles.filter(active=True)
                user_data = {
                    'member_id': member.id,
                    'username': user.username,  # No need to check if user exists on member, it's guaranteed by the relationship
                    'roles': [{
                        'org_id': role.org.id if role.org else None,
                        'role_id': role.role.id if role.role else None,
                        'role_name': role.role.name if role.role else 'No Role',
                        'org_name': role.org.name if role.org else 'No Organization',
                        'lc_role_name': (role.role.name.lower().replace(' ', '_') if role.role else 'no_page'),
                    } for role in roles]
                }
                context['user_roles_data'].append(user_data)

            # Build a unique list of orgs where the user is Org Admin
            admin_orgs = set()
            for member_info in context['user_roles_data']:
                for role in member_info['roles']:
                    if role['role_name'] == 'Org Admin' and role['org_id']:
                        admin_orgs.add((role['org_id'], role['org_name']))

            # Convert to list of dicts for template consumption
            context['admin_orgs_unique'] = [
                {'org_id': org_id, 'org_name': org_name} for (org_id, org_name) in sorted(admin_orgs, key=lambda x: x[1] or '')
            ]

            context.update({
                'no_of_roles': sum(len(member['roles']) for member in context['user_roles_data']),
                'multiple_roles': context['no_of_roles'] > 1,
                'page_title': 'View My Roles',
            })
        else:
            context['page_title'] = 'No Roles Assigned'

    # Render the appropriate template
    template_file = f"{app_name}/{module_path}/view_my_role.html"
    return render(request, template_file, context)

