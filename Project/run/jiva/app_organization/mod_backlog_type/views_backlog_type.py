from app_organization.mod_app.all_view_imports import *

from app_organization.mod_project.models_project import *

from app_organization.mod_backlog_type.models_backlog_type import *
from app_organization.mod_backlog_type.forms_backlog_type import *

app_name = 'app_organization'
app_version = 'v1'

module_name = 'backlog_type'
module_path = f'mod_backlog_type'

# viewable flag
first_viewable_flag = '__ALL__'  # 'all' or '__OWN__'
viewable_flag = '__ALL__'  # 'all' or '__OWN__'
# Setup dictionaries based on flags
# viewable_dict = {} if viewable_flag == '__ALL__' else {'author': user}
# first_viewable_dict = {} if first_viewable_flag == '__ALL__' else {'author': user}

def get_viewable_dicts(user, viewable_flag, first_viewable_flag):
    viewable_dict = {} if viewable_flag == '__ALL__' else {'author': user}
    first_viewable_dict = {} if first_viewable_flag == '__ALL__' else {'author': user}
    return viewable_dict, first_viewable_dict
# ============================================================= #
@login_required
def list_backlog_types(request, pro_id, parent_id):
    # take inputs
    ref_parent_id = parent_id
    parent_id = None if parent_id == 0 else parent_id
    viewable_dict, first_viewable_dict = get_viewable_dicts(request.user, 
                                viewable_flag, first_viewable_flag)
     # connect with connect id
    pro = get_object_or_404(Project, pk=pro_id, **viewable_dict)
    # process inputs
    user = request.user       
    objects_count = 0    
    show_all = request.GET.get('all', '25')
    objects_per_page = int(show_all) if show_all != 'all' else 25
    pagination_options = [5, 10, 15, 25, 50, 100, 'all']
    selected_bulk_operations = None
    search_query = request.GET.get('search', '')
    deleted_count = 0
    
    # breadcrumbs 
    # Get the current content object if not at root
    current_content = None
    breadcrumbs = []
    if parent_id:
        current_content = get_object_or_404(BacklogType, pk=parent_id)
        breadcrumbs = list(current_content.get_ancestors(include_self=True))
        
    if search_query:
        tobjects = BacklogType.objects.filter(name__icontains=search_query, 
                                            parent_id=parent_id,
                                            pro_id=pro_id,
                                            active=True,deleted=False, **viewable_dict ).order_by('position')
        deleted = BacklogType.objects.filter(active=False, deleted=False,
                                               pro_id=pro_id,
                                               **viewable_dict).order_by('position')
        deleted_count = deleted.count()
    else:
        tobjects = BacklogType.objects.filter(active=True, parent_id=parent_id,
                                                pro_id=pro_id,
                                                **viewable_dict).order_by('position')
        deleted = BacklogType.objects.filter(active=False,  parent_id=parent_id, deleted=False,**viewable_dict).order_by('position')
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
                    object = get_object_or_404(BacklogType, pk=item, active=True, **viewable_dict)
                    object.active = False
                    object.save()
                    
                elif bulk_operation == 'bulk_done':
                    object = get_object_or_404(BacklogType, pk=item, active=True, **viewable_dict)
                    object.done = True
                    object.save()
                    
                elif bulk_operation == 'bulk_not_done':
                    object = get_object_or_404(BacklogType, pk=item, active=True, **viewable_dict)
                    object.done = False
                    object.save()
                    
                elif bulk_operation == 'bulk_blocked':  # Correct the operation check here
                    object = get_object_or_404(BacklogType, pk=item, active=True, **viewable_dict)
                    object.blocked = True
                    object.save()
                    
                else:
                    return redirect('list_backlog_types',  pro_id=pro_id, parent_id=ref_parent_id)
            return redirect('list_backlog_types',  pro_id=pro_id, parent_id=ref_parent_id)
    
    
    # send outputs info, template,
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'list_backlog_types',
        'ref_parent_id': ref_parent_id,  
        'parent_id': parent_id,  
        'pro': pro,  # '_pro_'
        'pro_id': pro_id,  # '_pro_id_'
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
        'breadcrumbs': breadcrumbs,
        'page_title': f'Backlog Type List',
    }       
    template_file = f"{app_name}/{module_path}/list__backlog_types.html"
    return render(request, template_file, context)



# list the deleted objects
# ============================================================= #
@login_required
def list_deleted_backlog_types(request, pro_id, parent_id):
    # take inputs
    ref_parent_id = parent_id
    parent_id = None if parent_id == 0 else parent_id
    viewable_dict, first_viewable_dict = get_viewable_dicts(request.user, 
                                viewable_flag, first_viewable_flag)
     # connect with connect id
    pro = get_object_or_404(Project, pk=pro_id, **viewable_dict)
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
    
    # breadcrumbs 
    # Get the current content object if not at root
    current_content = None
    breadcrumbs = []
    if parent_id:
        current_content = get_object_or_404(BacklogType, pk=parent_id)
        breadcrumbs = list(current_content.get_ancestors(include_self=True))
    
    if search_query:
        tobjects = BacklogType.objects.filter(name__icontains=search_query, 
                                                pro_id=pro_id,
                                            parent_id=parent_id,
                                            **viewable_dict, active=False, deleted=False).order_by('position')
    else:
        tobjects = BacklogType.objects.filter(parent_id=parent_id, active=False, 
                                                pro_id=pro_id,
                                                deleted=False, **viewable_dict).order_by('position')
    
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
                        object = get_object_or_404(BacklogType, pk=item, active=False, **viewable_dict)
                        object.active = True               
                        object.save()
                    elif bulk_operation == 'bulk_erase':
                        object = get_object_or_404(BacklogType, pk=item, active=False, **viewable_dict)
                        object.active = False  
                        object.deleted = True             
                        object.save()
                    else:
                        return redirect('list_deleted_backlog_types',  pro_id=pro_id, parent_id=ref_parent_id)
                return redirect('list_deleted_backlog_types',  pro_id=pro_id, parent_id=ref_parent_id)
    
    
    # send outputs info, template,
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'list_deleted_backlog_types',
        'ref_parent_id': ref_parent_id,  
        'parent_id': parent_id,  
        'pro': pro,  # '_pro_'
        'pro_id': pro_id,  # '_pro_id_'
        'module_path': module_path,
        'user': user,
        'tobjects': tobjects,
        'page_obj': page_obj,
        'objects_count': objects_count,
        'objects_per_page': objects_per_page,
        'show_all': show_all,
        'pagination_options': pagination_options,
        'selected_bulk_operations': selected_bulk_operations,
        'breadcrumbs': breadcrumbs,
        'page_title': f'Backlog Type Deleted List',
    }       
    template_file = f"{app_name}/{module_path}/list_deleted__backlog_types.html"
    return render(request, template_file, context)



# Create View
@login_required
def create_backlog_type(request, pro_id,parent_id):
    user = request.user
    ref_parent_id = parent_id
    parent_id = None if parent_id == 0 else parent_id
    viewable_dict, first_viewable_dict = get_viewable_dicts(request.user, 
                                viewable_flag, first_viewable_flag)
     # connect with connect id
    pro = get_object_or_404(Project, pk=pro_id, **viewable_dict)
    if request.method == 'POST':
        form = BacklogTypeForm(request.POST)
        if form.is_valid():
            form.instance.parent_id = parent_id
            form.instance.pro_id = pro_id
            form.instance.author = user
            form.save()
        else:
            print(f">>> === form.errors: {form.errors} === <<<")
        return redirect('list_backlog_types', pro_id=pro_id, parent_id=ref_parent_id)
    else:
        form = BacklogTypeForm()

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'create_backlog_type',
        'ref_parent_id': ref_parent_id,  
        'pro': pro,  # '_pro_'
        'pro_id': pro_id,  # '_pro_id_'
        'parent_id': parent_id,  
        'module_path': module_path,
        'form': form,
        'page_title': f'Create Backlog Type',
    }
    template_file = f"{app_name}/{module_path}/create__backlog_type.html"
    return render(request, template_file, context)
    


# Edit
@login_required
def edit_backlog_type(request, pro_id,parent_id,  content_type_id):
    user = request.user
    ref_parent_id = parent_id
    parent_id = None if parent_id == 0 else parent_id
    viewable_dict, first_viewable_dict = get_viewable_dicts(request.user, 
                                viewable_flag, first_viewable_flag)
     # connect with connect id
    pro = get_object_or_404(Project, pk=pro_id, **viewable_dict)
    object = get_object_or_404(BacklogType, pk=content_type_id, active=True, **viewable_dict)
    if request.method == 'POST':
        form = BacklogTypeForm(request.POST, instance=object)
        if form.is_valid():
            form.instance.parent_id = parent_id
            form.instance.pro_id = pro_id
            form.instance.author = user
            form.save()
        else:
            print(f">>> === form.errors: {form.errors} === <<<")
        return redirect('list_backlog_types', pro_id=pro_id, parent_id=ref_parent_id)
    else:
        form = BacklogTypeForm(instance=object)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'edit_backlog_type',
        'ref_parent_id': ref_parent_id,  
        'pro': pro,  # '_pro_'
        'pro_id': pro_id,  # '_pro_id_'
        'parent_id': parent_id,  
        'module_path': module_path,
        'form': form,
        'object': object,
        'page_title': f'Edit Backlog Type',
    }
    template_file = f"{app_name}/{module_path}/edit__backlog_type.html"
    return render(request, template_file, context)



@login_required
def delete_backlog_type(request, pro_id, parent_id, content_type_id):
    user = request.user
    ref_parent_id = parent_id
    parent_id = None if parent_id == 0 else parent_id
    viewable_dict, first_viewable_dict = get_viewable_dicts(request.user, 
                                viewable_flag, first_viewable_flag)
     # connect with connect id
    pro = get_object_or_404(Project, pk=pro_id, **viewable_dict)
    object = get_object_or_404(BacklogType, pk=content_type_id, active=True, **viewable_dict)
    if request.method == 'POST':
        object.active = False
        object.save()
        return redirect('list_backlog_types', pro_id=pro_id, parent_id=ref_parent_id)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'delete_backlog_type',
        'ref_parent_id': ref_parent_id,  
        'pro': pro,  # '_pro_'
        'pro_id': pro_id,  # '_pro_id_'
        'parent_id': parent_id,  
        'module_path': module_path,        
        'object': object,
        'page_title': f'Delete Backlog Type',
    }
    template_file = f"{app_name}/{module_path}/delete__backlog_type.html"
    return render(request, template_file, context)


@login_required
def permanent_deletion_backlog_type(request, pro_id, parent_id, content_type_id):
    user = request.user
    ref_parent_id = parent_id
    parent_id = None if parent_id == 0 else parent_id
    viewable_dict, first_viewable_dict = get_viewable_dicts(request.user, 
                                viewable_flag, first_viewable_flag)
     # connect with connect id
    pro = get_object_or_404(Project, pk=pro_id, **viewable_dict)
    object = get_object_or_404(BacklogType, pk=content_type_id, active=False, deleted=False, **viewable_dict)
    if request.method == 'POST':
        object.active = False
        object.deleted = True
        object.save()
        return redirect('list_backlog_types', pro_id=pro_id, parent_id=ref_parent_id)
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'permanent_deletion_backlog_type',
        'ref_parent_id': ref_parent_id,  
        'pro': pro,  # '_pro_'
        
        'parent_id': parent_id,  
        'module_path': module_path,        
        'object': object,
        'page_title': f'Permanent Deletion Backlog Type',
    }
    template_file = f"{app_name}/{module_path}/permanent_deletion__backlog_type.html"
    return render(request, template_file, context)


@login_required
def restore_backlog_type(request, pro_id, parent_id, content_type_id):
    user = request.user
    ref_parent_id = parent_id
    parent_id = None if parent_id == 0 else parent_id
    viewable_dict, first_viewable_dict = get_viewable_dicts(request.user, 
                                viewable_flag, first_viewable_flag)
     # connect with connect id
    pro = get_object_or_404(Project, pk=pro_id, **viewable_dict)
    
    object = get_object_or_404(BacklogType, pro_id=pro_id,  pk=content_type_id, active=False, **viewable_dict)
    object.active = True
    object.save()
    return redirect('list_backlog_types', pro_id=pro_id, parent_id=ref_parent_id)
   


@login_required
def view_backlog_type(request, pro_id, parent_id,  content_type_id):
    user = request.user
    ref_parent_id = parent_id
    parent_id = None if parent_id == 0 else parent_id
    viewable_dict, first_viewable_dict = get_viewable_dicts(request.user, 
                                viewable_flag, first_viewable_flag)
     # connect with connect id
    pro = get_object_or_404(Project, pk=pro_id, **viewable_dict)
    object = get_object_or_404(BacklogType, pro_id = pro_id, pk=content_type_id, active=True, **viewable_dict)    

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'view_backlog_types',
        'ref_parent_id': ref_parent_id,  
        'pro': pro,  # '_pro_'
        'pro_id': pro_id,  # '_pro_id_'
        'parent_id': parent_id,  
        'module_path': module_path,
        'object': object,
        'page_title': f'View Backlog Type',
    }
    template_file = f"{app_name}/{module_path}/view__backlog_types.html"
    return render(request, template_file, context)



@login_required
def copy_backlog_type(request, pro_id , parent_id, content_type_id):
    user = request.user
    ref_parent_id = parent_id
    parent_id = None if parent_id == 0 else parent_id
    viewable_dict, first_viewable_dict = get_viewable_dicts(request.user, 
                                viewable_flag, first_viewable_flag)
    # connect with connect id
    pro = get_object_or_404(Project, pk=pro_id, **viewable_dict)
    tobject = get_object_or_404(BacklogType, id=content_type_id, 
                                pro_id = pro_id, 
                                **viewable_dict, active=True,
                                author=user)

    # clone the tree db given
    fields_to_copy = ['name', 'description', 'type', 'pro', 'position', 'author']  # Specify fields you want to copy
    cloned_treedb = clone_mptt_tree(BacklogType, tobject, fields=fields_to_copy)
    cloned_treedb.pro_id = pro_id
    cloned_treedb.parent_id = parent_id
    cloned_treedb.save()

    return redirect('list_backlog_types', pro_id=pro_id, parent_id=ref_parent_id) 


def build_serial_number_tree(node, current_path=[], serial_no=None):
    if serial_no is None:
        serial_no = defaultdict(int)  

    level = len(current_path)
    serial_no[level] += 1

    node_serial = '.'.join(map(str, current_path + [serial_no[level]]))
    result = [(node, node_serial)]   
    child_levels = list(range(level + 1, max(serial_no.keys()) + 1))
    for l in child_levels:
        serial_no[l] = 0

    children = node.get_children().order_by('position')
    for child in children:
        result.extend(build_serial_number_tree(child, current_path + [serial_no[level]], serial_no))

    return result


# Function to fetch a node by ID and generate its subtree with serial numbers
def get_serialized_subtree_from_node(request, node_id):
    user = request.user
    try:
        node = BacklogType.objects.get(id=node_id, active=True, author=user)
        return build_serial_number_tree(node)
    except BacklogType.DoesNotExist:
        return []
    


@login_required
def view_backlog_type_tree(request, pro_id, parent_id):
    # take inputs
    user = request.user
    ref_parent_id = parent_id
    parent_id = None if parent_id == 0 else parent_id
    viewable_dict, first_viewable_dict = get_viewable_dicts(request.user, 
                                viewable_flag, first_viewable_flag)
    # process inputs
    
    workspace = None
    wslist = None
    objects_per_page = 100
    objects_count = 0
    
    parent = get_object_or_404(BacklogType, id=parent_id, author=user)
    children = None 
    ancestors = None
    root = parent.get_root()
    root_workspace = None
      
    if not parent.is_leaf_node():
        children = parent.get_active_children()    
    if not children:
        ancestors = parent.get_ancestors()
        
    if children != None:
        for child in children:
            ancestors = child.get_ancestors()
            if ancestors:
                parent = ancestors[0]    

    ## Check whether an workspace item exists in treedb
    treedb = BacklogType.objects.filter(id=parent_id, 
                                          pro_id=pro_id,
                                          **viewable_dict,
                                          author=user).first()

    if treedb:
        wslist = treedb.get_active_children().order_by('position')
        objects_count = wslist.count()
        #print(f">>> === Getting Tree wslist: {wslist} === <<<")
    show_all = request.GET.get('all', 'false').lower() == 'true'
   
    if show_all:
        # No pagination, show all records
        page_obj = wslist
        serialized_nodes = get_serialized_subtree_from_node(request, pk)
    else:
        paginator = Paginator(wslist, objects_per_page)  # Show 10 topics per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        serialized_nodes = get_serialized_subtree_from_node(request, pk)
    
    
    # send outputs (info, template,
    context = {
        'parent_page': '__PARENTPAGE__',
        'page': 'view_backlog_type_tree',
        'user': user,
        'ancestors': ancestors,

        'wslist': wslist,
        'treedb': treedb,
        'root': root,

        'serialized_nodes': serialized_nodes,
    
        'page_obj': page_obj,
        'objects_count': objects_count,
        'objects_per_page': objects_per_page,
        'show_all': show_all,
        'page_title': f'Backlog Type Tree View',
    }       
    template_file = f"{app_name}/{module_path}/view__backlog_type_tree.html"
    return render(request, template_file, context)    
    
    