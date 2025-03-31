
from app_memberprofilerole.mod_app.all_view_imports import *
from app_memberprofilerole.mod_profile.models_profile import *
from app_memberprofilerole.mod_profile.forms_profile import *

from app_organization.mod_organization.models_organization import *

from app_common.mod_common.models_common import *

app_name = 'app_memberprofilerole'
app_version = 'v1'

module_name = 'profiles'
module_path = f'mod_profile'

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
def list_profiles(request, org_id):
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
        tobjects = Profile.objects.filter(name__icontains=search_query, 
                                            org_id=org_id, **viewable_dict).order_by('position')
    else:
        tobjects = Profile.objects.filter(active=True, org_id=org_id, **viewable_dict).order_by('position')
        deleted = Profile.objects.filter(active=False, deleted=False,
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
                    object = get_object_or_404(Profile, pk=item, active=True, **viewable_dict)
                    object.active = False
                    object.save()
                    
                elif bulk_operation == 'bulk_done':
                    object = get_object_or_404(Profile, pk=item, active=True, **viewable_dict)
                    object.done = True
                    object.save()
                    
                elif bulk_operation == 'bulk_not_done':
                    object = get_object_or_404(Profile, pk=item, active=True, **viewable_dict)
                    object.done = False
                    object.save()
                    
                elif bulk_operation == 'bulk_blocked':  # Correct the operation check here
                    object = get_object_or_404(Profile, pk=item, active=True, **viewable_dict)
                    object.blocked = True
                    object.save()
                    
                else:
                    redirect('list_profiles', org_id=org_id)
            return redirect('list_profiles', org_id=org_id)
    
    # send outputs info, template,
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'list_profiles',
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
        'page_title': f'Profile List',
    }       
    template_file = f"{app_name}/{module_path}/list_profiles.html"
    return render(request, template_file, context)





# ============================================================= #
@login_required
def list_deleted_profiles(request, org_id):
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
        tobjects = Profile.objects.filter(name__icontains=search_query, 
                                            active=False,
                                            org_id=org_id, **viewable_dict).order_by('position')
    else:
        tobjects = Profile.objects.filter(active=False, org_id=org_id,
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
                        object = get_object_or_404(Profile, pk=item, active=False, **viewable_dict)
                        object.active = True
                        object.save()         
                    elif bulk_operation == 'bulk_erase':
                        object = get_object_or_404(Profile, pk=item, active=False, **viewable_dict)
                        object.active = False  
                        object.deleted = True             
                        object.save()    
                    else:
                        redirect('list_profiles', org_id=org_id)
                redirect('list_profiles', org_id=org_id)
    
    # send outputs info, template,
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'list_deleted_profiles',
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
        'page_title': f'Profile List',
    }       
    template_file = f"{app_name}/{module_path}/list_deleted_profiles.html"
    return render(request, template_file, context)



# Create View
@login_required
def create_profile(request, org_id):
    user = request.user
    organization = Organization.objects.get(id=org_id, active=True, 
                                                **first_viewable_dict)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            form.instance.author = user
            form.instance.org_id = org_id
            form.save()
        else:
            print(f">>> === form.errors: {form.errors} === <<<")
        return redirect('list_profiles', org_id=org_id)
    else:
        form = ProfileForm()

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'create_profile',
        'organization': organization,
        'org_id': org_id,
        
        'module_path': module_path,
        'form': form,
        'page_title': f'Create Profile',
    }
    template_file = f"{app_name}/{module_path}/create_profile.html"
    return render(request, template_file, context)




# Edit
@login_required
def edit_profile(request, org_id, profile_id):
    user = request.user
    organization = Organization.objects.get(id=org_id, active=True, 
                                                **first_viewable_dict)
    
    object = get_object_or_404(Profile, pk=profile_id, active=True,**viewable_dict)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=object)
        if form.is_valid():
            form.instance.author = user
            form.instance.org_id = org_id
            form.save()
        else:
            print(f">>> === form.errors: {form.errors} === <<<")
        return redirect('list_profiles', org_id=org_id)
    else:
        form = ProfileForm(instance=object)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'edit_profile',
        'organization': organization,
        'org_id': org_id,
        
        'module_path': module_path,
        'form': form,
        'object': object,
        'page_title': f'Edit Profile',
    }
    template_file = f"{app_name}/{module_path}/edit_profile.html"
    return render(request, template_file, context)



@login_required
def delete_profile(request, org_id, profile_id):
    user = request.user
    organization = Organization.objects.get(id=org_id, active=True, 
                                                **first_viewable_dict)
    
    object = get_object_or_404(Profile, pk=profile_id, active=True,**viewable_dict)
    if request.method == 'POST':
        object.active = False
        object.save()
        return redirect('list_profiles', org_id=org_id)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'delete_profile',
        'organization': organization,
        'org_id': org_id,
        
        'module_path': module_path,        
        'object': object,
        'page_title': f'Delete Profile',
    }
    template_file = f"{app_name}/{module_path}/delete_profile.html"
    return render(request, template_file, context)


@login_required
def permanent_deletion_profile(request, org_id, profile_id):
    user = request.user
    organization = Organization.objects.get(id=org_id, active=True, 
                                                **first_viewable_dict)
    
    object = get_object_or_404(Profile, pk=profile_id, active=False, deleted=False, **viewable_dict)
    if request.method == 'POST':
        object.active = False
        object.deleted = True
        object.save()
        return redirect('list_profiles', org_id=org_id)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'permanent_deletion_profile',
        'organization': organization,
        'org_id': org_id,
        
        'module_path': module_path,        
        'object': object,
        'page_title': f'Permanent Deletion Profile',
    }
    template_file = f"{app_name}/{module_path}/permanent_deletion_profile.html"
    return render(request, template_file, context)


@login_required
def restore_profile(request,  org_id, profile_id):
    user = request.user
    object = get_object_or_404(Profile, pk=profile_id, active=False,**viewable_dict)
    object.active = True
    object.save()
    return redirect('list_profiles', org_id=org_id)
   


@login_required
def view_profile(request, org_id, profile_id):
    user = request.user
    if org_id == 0:
        organization = None
    else:
        organization = Organization.objects.get(id=org_id, active=True, 
                                                **first_viewable_dict)
    object = None
    ref_profile_id = None
    if profile_id == 0:
        object = Profile(name=f'{user.username}', description = 'New Profile', 
                         bio='Tell about yourself here...',
                         author=user)
        object.save()
        ref_profile_id = object.id
    else:
        object = get_object_or_404(Profile, pk=profile_id, active=True,**viewable_dict)    
    ############################################################################
    # check if user has profile or create one
    user_profile = None 
    try:
        user_profile = Profile.objects.get(user=request.user)
    except:
        print(f"UserProfile does not exists")
        user_profile = object
        user_profile.save()
    
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('user-home')
        else:
            print(f"error in the profile updation {u_form} {p_form}")

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    ############################################################################
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'view_profile',
        'organization': organization,
        'org_id': org_id,
        'profile_id': profile_id,
        'ref_profile_id': ref_profile_id,
        'u_form': u_form,
        'p_form': p_form,
        'module_path': module_path,
        'object': object,
        'page_title': f'View Profile',
    }
    template_file = f"{app_name}/{module_path}/view_profile.html"
    return render(request, template_file, context)

@login_required
def display_profile(request):
    user = request.user
    
    # Check if user has profile or create one
    user_profile, created = Profile.objects.get_or_create(
        user=user,
        defaults={
            'name': user.username,
            'description': 'New Profile',
            'bio': 'Tell about yourself here...'
        }
    )
    
    if created:
        print(f"Profile created for user {user.username}")

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been updated!')
            return redirect('display_profile')
        else:
            print(f"Error in the profile update: {u_form.errors}, {p_form.errors}")
    else:
        u_form = UserUpdateForm(instance=user)
        p_form = ProfileUpdateForm(instance=user.profile)

    context = {
        'parent_page': 'user_logged_in',
        'page': 'display_profile',      
        'u_form': u_form,
        'p_form': p_form,
        'org_id': 1,
        'object': user_profile,
        'module_path': 'module_path',  # Replace with the actual module path
        'page_title': 'Display Profile',
    }
    template_file = f"{app_name}/{module_path}/display_profile.html"
    return render(request, template_file, context)
