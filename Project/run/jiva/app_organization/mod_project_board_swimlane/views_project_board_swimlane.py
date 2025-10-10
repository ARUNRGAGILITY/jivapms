
from app_organization.mod_app.all_view_imports import *
from app_organization.mod_project_board_swimlane.models_project_board_swimlane import *
from app_organization.mod_project_board_swimlane.forms_project_board_swimlane import *

from app_organization.mod_project.models_project import *

from app_common.mod_common.models_common import *

app_name = 'app_organization'
app_version = 'v1'

module_name = 'project_board_swimlanes'
module_path = f'mod_project_board_swimlane'

# viewable flag
first_viewable_flag = '__ALL__'  # 'all' or '__OWN__'
viewable_flag = '__ALL__'  # 'all' or '__OWN__'
# Setup dictionaries based on flags (no request.user at import time)
viewable_dict = {}
first_viewable_dict = {}
def get_viewable_dicts(user, viewable_flag, first_viewable_flag):
    viewable_dict = {} if viewable_flag == '__ALL__' else {'author': user}
    first_viewable_dict = {} if first_viewable_flag == '__ALL__' else {'author': user}
    return viewable_dict, first_viewable_dict
# ============================================================= #
@login_required
def list_project_board_swimlanes(request, project_id):
    # take inputs
    # process inputs
    user = request.user       
    objects_count = 0    
    show_all = request.GET.get('all', '25')
    objects_per_page = int(show_all) if show_all != 'all' else 25
    pagination_options = [5, 10, 15, 25, 50, 100, 'all']
    selected_bulk_operations = None
    deleted_count = 0
    project = Project.objects.get(id=project_id, active=True, 
                                                **first_viewable_dict)
    # Determine the selected/default board for this project
    DEFAULT_BOARD_NAME = 'Default Board'
    selected_board = ProjectBoard.objects.filter(project=project, default_board=True, active=True).first()
    if not selected_board:
        selected_board, _ = ProjectBoard.objects.get_or_create(
            project=project,
            name=DEFAULT_BOARD_NAME,
            defaults={'author': user}
        )
    
    search_query = request.GET.get('search', '')
    if search_query:
        tobjects = ProjectBoardSwimLane.objects.filter(name__icontains=search_query, 
                                            board=selected_board, **viewable_dict).order_by('position')
    else:
        tobjects = ProjectBoardSwimLane.objects.filter(active=True, board=selected_board).order_by('position')
        deleted = ProjectBoardSwimLane.objects.filter(active=False, deleted=False,
                                board=selected_board,
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
                    object = get_object_or_404(ProjectBoardSwimLane, pk=item, active=True, **viewable_dict)
                    object.active = False
                    object.save()
                    
                elif bulk_operation == 'bulk_done':
                    object = get_object_or_404(ProjectBoardSwimLane, pk=item, active=True, **viewable_dict)
                    object.done = True
                    object.save()
                    
                elif bulk_operation == 'bulk_not_done':
                    object = get_object_or_404(ProjectBoardSwimLane, pk=item, active=True, **viewable_dict)
                    object.done = False
                    object.save()
                    
                elif bulk_operation == 'bulk_blocked':  # Correct the operation check here
                    object = get_object_or_404(ProjectBoardSwimLane, pk=item, active=True, **viewable_dict)
                    object.blocked = True
                    object.save()
                    
                else:
                    redirect('list_project_board_swimlanes', project_id=project_id)
            return redirect('list_project_board_swimlanes', project_id=project_id)
    
    # send outputs info, template,
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'list_project_board_swimlanes',
    'project': project,
    'organization': project.org,
        'project_id': project_id,
    'org_id': project.org.id,
    'board': selected_board,
        
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
        'page_title': f'Project_board_swimlane List',
    }       
    template_file = f"{app_name}/{module_path}/list_project_board_swimlanes.html"
    return render(request, template_file, context)





# ============================================================= #
@login_required
def list_deleted_project_board_swimlanes(request, project_id):
    # take inputs
    # process inputs
    user = request.user       
    objects_count = 0    
    show_all = request.GET.get('all', '25')
    objects_per_page = int(show_all) if show_all != 'all' else 25
    pagination_options = [5, 10, 15, 25, 50, 100, 'all']
    selected_bulk_operations = None
    project = Project.objects.get(id=project_id, active=True, 
                                                **first_viewable_dict)
    DEFAULT_BOARD_NAME = 'Default Board'
    selected_board = ProjectBoard.objects.filter(project=project, default_board=True, active=True).first()
    if not selected_board:
        selected_board, _ = ProjectBoard.objects.get_or_create(
            project=project,
            name=DEFAULT_BOARD_NAME,
            defaults={'author': user}
        )
    
    search_query = request.GET.get('search', '')
    if search_query:
        tobjects = ProjectBoardSwimLane.objects.filter(name__icontains=search_query, 
                                            active=False, deleted=False,
                                            board=selected_board, **viewable_dict).order_by('position')
    else:
        tobjects = ProjectBoardSwimLane.objects.filter(active=False, deleted=False, board=selected_board,
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
                        object = get_object_or_404(ProjectBoardSwimLane, pk=item, active=False, **viewable_dict)
                        object.active = True
                        object.save()         
                    elif bulk_operation == 'bulk_erase':
                        object = get_object_or_404(ProjectBoardSwimLane, pk=item, active=False, **viewable_dict)
                        object.active = False  
                        object.deleted = True             
                        object.save()    
                    else:
                        redirect('list_project_board_swimlanes', project_id=project_id)
                redirect('list_project_board_swimlanes', project_id=project_id)
    
    # send outputs info, template,
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'list_deleted_project_board_swimlanes',
    'project': project,
    'organization': project.org,
        'project_id': project_id,
    'org_id': project.org.id,
    'board': selected_board,
        
        'module_path': module_path,
        'user': user,
        'tobjects': tobjects,
        'page_obj': page_obj,
        'objects_count': objects_count,
        'objects_per_page': objects_per_page,
        'show_all': show_all,
        'pagination_options': pagination_options,
        'selected_bulk_operations': selected_bulk_operations,
        'page_title': f'Project_board_swimlane List',
    }       
    template_file = f"{app_name}/{module_path}/list_deleted_project_board_swimlanes.html"
    return render(request, template_file, context)



# Create View
@login_required
def create_project_board_swimlane(request, project_id):
    user = request.user
    project = Project.objects.get(id=project_id, active=True, 
                                                **first_viewable_dict)
    # resolve board
    DEFAULT_BOARD_NAME = 'Default Board'
    selected_board = ProjectBoard.objects.filter(project=project, default_board=True, active=True).first()
    if not selected_board:
        selected_board, _ = ProjectBoard.objects.get_or_create(
            project=project,
            name=DEFAULT_BOARD_NAME,
            defaults={'author': user}
        )
    
    if request.method == 'POST':
        form = ProjectBoardSwimlaneForm(request.POST)
        if form.is_valid():
            form.instance.author = user
            form.instance.board = selected_board
            form.save()
        else:
            print(f">>> === form.errors: {form.errors} === <<<")
        return redirect('list_project_board_swimlanes', project_id=project_id)
    else:
        form = ProjectBoardSwimlaneForm()

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'create_project_board_swimlane',
    'project': project,
    'organization': project.org,
        'project_id': project_id,
    'org_id': project.org.id,
    'board': selected_board,
        
        'module_path': module_path,
        'form': form,
        'page_title': f'Create Project Board Swimlane',
    }
    template_file = f"{app_name}/{module_path}/create_project_board_swimlane.html"
    return render(request, template_file, context)




# Edit
@login_required
def edit_project_board_swimlane(request, project_id, project_board_swimlane_id):
    user = request.user
    project = Project.objects.get(id=project_id, active=True, 
                                                **first_viewable_dict)
    DEFAULT_BOARD_NAME = 'Default Board'
    selected_board = ProjectBoard.objects.filter(project=project, default_board=True, active=True).first()
    if not selected_board:
        selected_board, _ = ProjectBoard.objects.get_or_create(
            project=project,
            name=DEFAULT_BOARD_NAME,
            defaults={'author': user}
        )
    
    object = get_object_or_404(ProjectBoardSwimLane, pk=project_board_swimlane_id, active=True,**viewable_dict)
    if request.method == 'POST':
        form = ProjectBoardSwimlaneForm(request.POST, instance=object)
        if form.is_valid():
            form.instance.author = user
            form.instance.board = selected_board
            form.save()
        else:
            print(f">>> === form.errors: {form.errors} === <<<")
        return redirect('list_project_board_swimlanes', project_id=project_id)
    else:
        form = ProjectBoardSwimlaneForm(instance=object)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'edit_project_board_swimlane',
    'project': project,
    'organization': project.org,
        'project_id': project_id,
    'org_id': project.org.id,
    'board': selected_board,
        
        'module_path': module_path,
        'form': form,
        'object': object,
        'page_title': f'Edit Project Board Swimlane',
    }
    template_file = f"{app_name}/{module_path}/edit_project_board_swimlane.html"
    return render(request, template_file, context)



@login_required
def delete_project_board_swimlane(request, project_id, project_board_swimlane_id):
    user = request.user
    project = Project.objects.get(id=project_id, active=True, 
                                                **first_viewable_dict)
    
    object = get_object_or_404(ProjectBoardSwimLane, pk=project_board_swimlane_id, active=True,**viewable_dict)
    if request.method == 'POST':
        object.active = False
        object.save()
        return redirect('list_project_board_swimlanes', project_id=project_id)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'delete_project_board_swimlane',
        'project': project,
    'organization': project.org,
        'project_id': project_id,
    'org_id': project.org.id,
        
        'module_path': module_path,        
        'object': object,
        'page_title': f'Delete Project Board Swimlane',
    }
    template_file = f"{app_name}/{module_path}/delete_project_board_swimlane.html"
    return render(request, template_file, context)


@login_required
def permanent_deletion_project_board_swimlane(request, project_id, project_board_swimlane_id):
    user = request.user
    project = Project.objects.get(id=project_id, active=True, 
                                                **first_viewable_dict)
    
    object = get_object_or_404(ProjectBoardSwimLane, pk=project_board_swimlane_id, active=False, deleted=False, **viewable_dict)
    if request.method == 'POST':
        object.active = False
        object.deleted = True
        object.save()
        return redirect('list_project_board_swimlanes', project_id=project_id)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'permanent_deletion_project_board_swimlane',
        'project': project,
    'organization': project.org,
        'project_id': project_id,
    'org_id': project.org.id,
        
        'module_path': module_path,        
        'object': object,
        'page_title': f'Permanent Deletion Project Board Swimlane',
    }
    template_file = f"{app_name}/{module_path}/permanent_deletion_project_board_swimlane.html"
    return render(request, template_file, context)


@login_required
def restore_project_board_swimlane(request,  project_id, project_board_swimlane_id):
    user = request.user
    object = get_object_or_404(ProjectBoardSwimLane, pk=project_board_swimlane_id, active=False,**viewable_dict)
    object.active = True
    object.save()
    return redirect('list_project_board_swimlanes', project_id=project_id)
   


@login_required
def view_project_board_swimlane(request, project_id, project_board_swimlane_id):
    user = request.user
    project = Project.objects.get(id=project_id, active=True, 
                                                **first_viewable_dict)
    
    object = get_object_or_404(ProjectBoardSwimLane, pk=project_board_swimlane_id, active=True,**viewable_dict)    

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'view_project_board_swimlane',
    'project': project,
    'organization': project.org,
        'project_id': project_id,
    'org_id': project.org.id,
    # board is not required for detail view context here
        
        'module_path': module_path,
        'object': object,
        'page_title': f'View Project Board Swimlane',
    }
    template_file = f"{app_name}/{module_path}/view_project_board_swimlane.html"
    return render(request, template_file, context)


