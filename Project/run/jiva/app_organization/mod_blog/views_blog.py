
from app_organization.mod_app.all_view_imports import *
from app_organization.mod_blog.models_blog import *
from app_organization.mod_blog.forms_blog import *

from app_organization.mod_organization.models_organization import *
from app_organization.mod_org_image_map.models_org_image_map import *
from app_common.mod_common.models_common import *

app_name = 'app_organization'
app_version = 'v1'

module_name = 'blogs'
module_path = f'mod_blog'

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
def list_blogs(request, organization_id):
    # take inputs
    # process inputs
    user = request.user       
    objects_count = 0    
    show_all = request.GET.get('all', '25')
    objects_per_page = int(show_all) if show_all != 'all' else 25
    pagination_options = [5, 10, 15, 25, 50, 100, 'all']
    selected_bulk_operations = None
    deleted_count = 0
    organization = Organization.objects.get(id=organization_id, active=True, 
                                                **first_viewable_dict)
    
    search_query = request.GET.get('search', '')
    if search_query:
        tobjects = Blog.objects.filter(name__icontains=search_query, 
                                            organization_id=organization_id, **viewable_dict).order_by('position')
    else:
        tobjects = Blog.objects.filter(active=True, organization_id=organization_id).order_by('position')
        deleted = Blog.objects.filter(active=False, deleted=False,
                                organization_id=organization_id,
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
                    object = get_object_or_404(Blog, pk=item, active=True, **viewable_dict)
                    object.active = False
                    object.save()
                    
                elif bulk_operation == 'bulk_done':
                    object = get_object_or_404(Blog, pk=item, active=True, **viewable_dict)
                    object.done = True
                    object.save()
                    
                elif bulk_operation == 'bulk_not_done':
                    object = get_object_or_404(Blog, pk=item, active=True, **viewable_dict)
                    object.done = False
                    object.save()
                    
                elif bulk_operation == 'bulk_blocked':  # Correct the operation check here
                    object = get_object_or_404(Blog, pk=item, active=True, **viewable_dict)
                    object.blocked = True
                    object.save()
                    
                else:
                    redirect('list_blogs', organization_id=organization_id)
            return redirect('list_blogs', organization_id=organization_id)
    
    # send outputs info, template,
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'list_blogs',
        'organization': organization,
        'organization_id': organization_id,
        'org_id': organization_id,
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
        'page_title': f'Blog List',
    }       
    template_file = f"{app_name}/{module_path}/list_blogs.html"
    return render(request, template_file, context)





# ============================================================= #
@login_required
def list_deleted_blogs(request, organization_id):
    # take inputs
    # process inputs
    user = request.user       
    objects_count = 0    
    show_all = request.GET.get('all', '25')
    objects_per_page = int(show_all) if show_all != 'all' else 25
    pagination_options = [5, 10, 15, 25, 50, 100, 'all']
    selected_bulk_operations = None
    organization = Organization.objects.get(id=organization_id, active=True, 
                                                **first_viewable_dict)
    
    search_query = request.GET.get('search', '')
    if search_query:
        tobjects = Blog.objects.filter(name__icontains=search_query, 
                                            active=False, deleted=False,
                                            organization_id=organization_id, **viewable_dict).order_by('position')
    else:
        tobjects = Blog.objects.filter(active=False, deleted=False, organization_id=organization_id,
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
                        object = get_object_or_404(Blog, pk=item, active=False, **viewable_dict)
                        object.active = True
                        object.save()         
                    elif bulk_operation == 'bulk_erase':
                        object = get_object_or_404(Blog, pk=item, active=False, **viewable_dict)
                        object.active = False  
                        object.deleted = True             
                        object.save()    
                    else:
                        redirect('list_blogs', organization_id=organization_id)
                redirect('list_blogs', organization_id=organization_id)
    
    # send outputs info, template,
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'list_deleted_blogs',
        'organization': organization,
        'organization_id': organization_id,
        'org_id': organization_id,
        'module_path': module_path,
        'user': user,
        'tobjects': tobjects,
        'page_obj': page_obj,
        'objects_count': objects_count,
        'objects_per_page': objects_per_page,
        'show_all': show_all,
        'pagination_options': pagination_options,
        'selected_bulk_operations': selected_bulk_operations,
        'page_title': f'Blog List',
    }       
    template_file = f"{app_name}/{module_path}/list_deleted_blogs.html"
    return render(request, template_file, context)



# Create View
@login_required
def create_blog(request, organization_id):
    user = request.user
    organization = Organization.objects.get(id=organization_id, active=True, 
                                                **first_viewable_dict)
    
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            form.instance.author = user
            form.instance.organization_id = organization_id
            # Use regex to replace either 4 spaces or a tab with 8 spaces
            content = form.cleaned_data['content']
            replaced_content = re.sub(r"( {3}|\t)", "        ", content)  
            # Replace 4 spaces or tab with 8 spaces
            form.instance.content = replaced_content
            
            form.save()
        else:
            print(f">>> === form.errors: {form.errors} === <<<")
        return redirect('list_blogs', organization_id=organization_id)
    else:
        form = BlogForm()

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'create_blog',
        'organization': organization,
        'organization_id': organization_id,
        'org_id': organization_id,
        'module_path': module_path,
        'form': form,
        'page_title': f'Create Blog',
    }
    template_file = f"{app_name}/{module_path}/create_blog.html"
    return render(request, template_file, context)




# Edit
@login_required
def edit_blog(request, organization_id, blog_id):
    user = request.user
    organization = Organization.objects.get(id=organization_id, active=True, 
                                                **first_viewable_dict)
    
    object = get_object_or_404(Blog, pk=blog_id, active=True,**viewable_dict)
    if request.method == 'POST':
        form = BlogForm(request.POST, instance=object)
        if form.is_valid():
            form.instance.author = user
            form.instance.organization_id = organization_id
            # Use regex to replace either 4 spaces or a tab with 8 spaces
            content = form.cleaned_data['content']
            replaced_content = re.sub(r"( {3}|\t)", "        ", content)  
            # Replace 4 spaces or tab with 8 spaces
            form.instance.content = replaced_content

            form.save()
        else:
            print(f">>> === form.errors: {form.errors} === <<<")
        return redirect('list_blogs', organization_id=organization_id)
    else:
        form = BlogForm(instance=object)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'edit_blog',
        'organization': organization,
        'organization_id': organization_id,
        'org_id': organization_id,
        'module_path': module_path,
        'form': form,
        'object': object,
        'page_title': f'Edit Blog',
    }
    template_file = f"{app_name}/{module_path}/edit_blog.html"
    return render(request, template_file, context)



@login_required
def delete_blog(request, organization_id, blog_id):
    user = request.user
    organization = Organization.objects.get(id=organization_id, active=True, 
                                                **first_viewable_dict)
    
    object = get_object_or_404(Blog, pk=blog_id, active=True,**viewable_dict)
    if request.method == 'POST':
        object.active = False
        object.save()
        return redirect('list_blogs', organization_id=organization_id)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'delete_blog',
        'organization': organization,
        'organization_id': organization_id,
        'org_id': organization_id,
        'module_path': module_path,        
        'object': object,
        'page_title': f'Delete Blog',
    }
    template_file = f"{app_name}/{module_path}/delete_blog.html"
    return render(request, template_file, context)


@login_required
def permanent_deletion_blog(request, organization_id, blog_id):
    user = request.user
    organization = Organization.objects.get(id=organization_id, active=True, 
                                                **first_viewable_dict)
    
    object = get_object_or_404(Blog, pk=blog_id, active=False, deleted=False, **viewable_dict)
    if request.method == 'POST':
        object.active = False
        object.deleted = True
        object.save()
        return redirect('list_blogs', organization_id=organization_id)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'permanent_deletion_blog',
        'organization': organization,
        'organization_id': organization_id,
        'org_id': organization_id,
        'module_path': module_path,        
        'object': object,
        'page_title': f'Permanent Deletion Blog',
    }
    template_file = f"{app_name}/{module_path}/permanent_deletion_blog.html"
    return render(request, template_file, context)


@login_required
def restore_blog(request,  organization_id, blog_id):
    user = request.user
    object = get_object_or_404(Blog, pk=blog_id, active=False,**viewable_dict)
    object.active = True
    object.save()
    return redirect('list_blogs', organization_id=organization_id)
   
import markdown

@login_required
def view_blog(request, organization_id, blog_id):
    user = request.user
    organization = Organization.objects.get(id=organization_id, active=True, 
                                                **first_viewable_dict)
    
    object = get_object_or_404(Blog, pk=blog_id, active=True,**viewable_dict)    

    # Replace all occurrences of 4 spaces with 8 spaces
    formatted_content = object.content.replace("    ", "        ")
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'view_blog',
        'organization': organization,
        'organization_id': organization_id,
        'org_id': organization_id,
        'formatted_content': formatted_content,
        'module_path': module_path,
        'object': object,
        'page_title': f'View Blog',
    }
    template_file = f"{app_name}/{module_path}/view_blog.html"
    return render(request, template_file, context)

#@login_required
# MODIFIED FOR GA
def display_blog(request, organization_id, blog_id):
    user = request.user
    organization = Organization.objects.get(id=organization_id, active=True, 
                                                **first_viewable_dict)
    
    object = get_object_or_404(Blog, pk=blog_id, active=True,**viewable_dict)    
    # Retrieve query parameters
    org_image_map_id = request.GET.get('org_image_map_id')  # Image map ID
    area_id = request.GET.get('area_id')  # Area ID
    area_name = request.GET.get('area_name')  # Area name
    link_ref = request.GET.get('link_ref')  # Link reference
    current_url = request.GET.get('current_url')  # Current URL
    print(f">>> === current_url: {current_url} === <<<")
    selected_area = request.GET.get('selected_area')  # Custom detail

    # Optional: Validate or use the parameters as needed
    # For example, fetch related objects or log information
    if org_image_map_id:
        org_image_map = OrgImageMap.objects.filter(id=org_image_map_id, active=True).first()
    else:
        org_image_map = None
        
    area = org_image_map.areas.filter(id=area_id).first() if area_id and org_image_map else None

    # Split the coordinates into x, y, width, height
    coords = list(map(float, area.coords.split(','))) if area and area.coords else [0, 0, 0, 0]
     # Dynamically generate cropped image
    cropped_image = org_image_map.generate_cropped_image(coords) if org_image_map and coords != [0, 0, 0, 0] else None

    if cropped_image:
        # Save cropped image temporarily for use in the template
        cropped_image_url = f"/media/temp/{cropped_image.name}"
        with open(f"{settings.MEDIA_ROOT}/temp/{cropped_image.name}", "wb") as f:
            f.write(cropped_image.read())
    else:
        cropped_image_url = None

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'display_blog',
        'organization': organization,
        'organization_id': organization_id,
        'org_id': organization_id,
        'module_path': module_path,
        'object': object,
        'org_image_map': org_image_map,  # Pass the image map if found
        'org_image_map_id': org_image_map_id,
        'area_coords': coords,  
        'cropped_image_url': cropped_image_url, 
        'area_id': area_id,
        'area_name': area_name,
        'link_ref': link_ref,
        'current_url': current_url,
        'selected_area': selected_area,
        
        'page_title': f'Display Blog',
    }
    template_file = f"{app_name}/{module_path}/display_blog.html"
    return render(request, template_file, context)

@login_required
def big_picture_blog_view(request, organization_id, slug):
    user = request.user
    organization = Organization.objects.get(id=organization_id, active=True, 
                                                **first_viewable_dict)
    
    object = get_object_or_404(Blog, slug=slug, active=True,**viewable_dict)    

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'big_picture_blog_view',
        'organization': organization,
        'organization_id': organization_id,
        'org_id': organization_id,
        'module_path': module_path,
        'object': object,
        'page_title': f'Big Picture Blog View',
    }
    template_file = f"{app_name}/{module_path}/big_picture_blog_view.html"
    return render(request, template_file, context)