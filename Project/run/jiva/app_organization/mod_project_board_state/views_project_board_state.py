
from app_organization.mod_app.all_view_imports import *
from app_organization.mod_project_board_state.models_project_board_state import *
from app_organization.mod_project_board_state.forms_project_board_state import *

from app_organization.mod_project_board.models_project_board import *

from app_common.mod_common.models_common import *

app_name = 'app_organization'
app_version = 'v1'

module_name = 'project_board_states'
module_path = f'mod_project_board_state'

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
def list_project_board_states(request, project_board_id):
    # take inputs
    # process inputs
    user = request.user       
    objects_count = 0    
    form = ProjectBoardStateForm()
    show_all = request.GET.get('all', '25')
    objects_per_page = int(show_all) if show_all != 'all' else 25
    pagination_options = [5, 10, 15, 25, 50, 100, 'all']
    selected_bulk_operations = None
    deleted_count = 0
    project_board = ProjectBoard.objects.get(id=project_board_id, active=True, 
                                                **first_viewable_dict)
    
    search_query = request.GET.get('search', '')
    if search_query:
        tobjects = ProjectBoardState.objects.filter(name__icontains=search_query, 
                                            board_id=project_board_id, **viewable_dict).order_by('position')
                                            
    else:
        tobjects = ProjectBoardState.objects.filter(active=True, board_id=project_board_id).order_by('position')
        print(f">>>>>>>>> tobjects: {tobjects}")
        deleted = ProjectBoardState.objects.filter(active=False, deleted=False,
                                board_id=project_board_id,
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
                    object = get_object_or_404(ProjectBoardState, pk=item, active=True, **viewable_dict)
                    object.active = False
                    object.save()
                    
                elif bulk_operation == 'bulk_done':
                    object = get_object_or_404(ProjectBoardState, pk=item, active=True, **viewable_dict)
                    object.done = True
                    object.save()
                    
                elif bulk_operation == 'bulk_not_done':
                    object = get_object_or_404(ProjectBoardState, pk=item, active=True, **viewable_dict)
                    object.done = False
                    object.save()
                    
                elif bulk_operation == 'bulk_blocked':  # Correct the operation check here
                    object = get_object_or_404(ProjectBoardState, pk=item, active=True, **viewable_dict)
                    object.blocked = True
                    object.save()
                    
                else:
                    redirect('list_project_board_states', project_board_id=project_board_id)
            return redirect('list_project_board_states', project_board_id=project_board_id)
    
    # send the sub column choices
    sub_column_type_choices = ProjectBoardState.SUBCOLUMN_PAIRS

    # send outputs info, template,
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'list_project_board_states',
        'project_board': project_board,
        'project_board_id': project_board_id,
        'project': project_board.project,
        'project_id': project_board.project.id,
        'org': project_board.project.org,
        'org_id': project_board.project.org.id,
        'column_type_choices': ProjectBoardState.COLUMN_TYPE_CHOICES,
        'sub_column_type_choices': sub_column_type_choices,
        'form': form,
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
        'page_title': f'Project_board_state List',
    }       
    template_file = f"{app_name}/{module_path}/list_project_board_states.html"
    return render(request, template_file, context)





# ============================================================= #
@login_required
def list_deleted_project_board_states(request, project_board_id):
    # take inputs
    # process inputs
    user = request.user       
    objects_count = 0    
    show_all = request.GET.get('all', '25')
    objects_per_page = int(show_all) if show_all != 'all' else 25
    pagination_options = [5, 10, 15, 25, 50, 100, 'all']
    selected_bulk_operations = None
    project_board = ProjectBoard.objects.get(id=project_board_id, active=True, 
                                                **first_viewable_dict)
    
    search_query = request.GET.get('search', '')
    if search_query:
        tobjects = ProjectBoardState.objects.filter(name__icontains=search_query, 
                                            active=False, deleted=False,
                                            board_id=project_board_id, **viewable_dict).order_by('position')
    else:
        tobjects = ProjectBoardState.objects.filter(active=False, deleted=False, board_id=project_board_id,
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
                        object = get_object_or_404(ProjectBoardState, pk=item, active=False, **viewable_dict)
                        object.active = True
                        object.save()         
                    elif bulk_operation == 'bulk_erase':
                        object = get_object_or_404(ProjectBoardState, pk=item, active=False, **viewable_dict)
                        object.active = False  
                        object.deleted = True             
                        object.save()    
                    else:
                        redirect('list_project_board_states', board_id=project_board_id)
                redirect('list_project_board_states', project_board_id=project_board_id)
    
    # send outputs info, template,
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'list_deleted_project_board_states',
        'project_board': project_board,
        'project_board_id': project_board_id,
        'project': project_board.project,
        'project_id': project_board.project.id,
        'org': project_board.project.org,
        'org_id': project_board.project.org.id,

        'module_path': module_path,
        'user': user,
        'tobjects': tobjects,
        'page_obj': page_obj,
        'objects_count': objects_count,
        'objects_per_page': objects_per_page,
        'show_all': show_all,
        'pagination_options': pagination_options,
        'selected_bulk_operations': selected_bulk_operations,
        'page_title': f'Project_board_state List',
    }       
    template_file = f"{app_name}/{module_path}/list_deleted_project_board_states.html"
    return render(request, template_file, context)



# Create View
@login_required
def create_project_board_state(request, project_board_id):
    user = request.user
    project_board = ProjectBoard.objects.get(id=project_board_id, active=True, 
                                                **first_viewable_dict)
    
    if request.method == 'POST':
        form = ProjectBoardStateForm(request.POST)
        if form.is_valid():
            form.instance.author = user
            form.instance.board_id = project_board_id
            form.save()
        else:
            print(f">>> === form.errors: {form.errors} === <<<")
        return redirect('list_project_board_states', project_board_id=project_board_id)
    else:
        form = ProjectBoardStateForm()

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'create_project_board_state',
        'project_board': project_board,
        'project_board_id': project_board_id,
        'project': project_board.project,
        'project_id': project_board.project.id,
        'org': project_board.project.org,
        'org_id': project_board.project.org.id,

        'module_path': module_path,
        'form': form,
        'page_title': f'Create Project Board State',
    }
    template_file = f"{app_name}/{module_path}/create_project_board_state.html"
    return render(request, template_file, context)


# Add View
@login_required
def add_project_board_state(request, project_board_id):
    user = request.user
    project_board = ProjectBoard.objects.get(id=project_board_id, active=True, 
                                                **first_viewable_dict)
    
    board = ProjectBoardState.objects.create(
        author=user,
        board_id=project_board_id,
    )
    board.save()

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'create_project_board_state',
        'project_board': project_board,
        'project_board_id': project_board_id,
        'project': project_board.project,
        'project_id': project_board.project.id,
        'org': project_board.project.org,
        'org_id': project_board.project.org.id,

        'module_path': module_path,
        'page_title': f'Create Project Board State',
    }
    return redirect('list_project_board_states', project_board_id=project_board_id)


# Edit
@login_required
def edit_project_board_state(request, project_board_id, project_board_state_id):
    user = request.user
    project_board = ProjectBoard.objects.get(id=project_board_id, active=True, 
                                                **first_viewable_dict)
    
    object = get_object_or_404(ProjectBoardState, pk=project_board_state_id, active=True,**viewable_dict)
    if request.method == 'POST':
        form = ProjectBoardStateForm(request.POST, instance=object)
        if form.is_valid():
            form.instance.author = user
            form.instance.project_board_id = project_board_id
            form.save()
        else:
            print(f">>> === form.errors: {form.errors} === <<<")
        return redirect('list_project_board_states', project_board_id=project_board_id)
    else:
        form = ProjectBoardStateForm(instance=object)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'edit_project_board_state',
        'project_board': project_board,
        'project_board_id': project_board_id,
        'project': project_board.project,
        'project_id': project_board.project.id,
        'org': project_board.project.org,
        'org_id': project_board.project.org.id,

        'module_path': module_path,
        'form': form,
        'object': object,
        'page_title': f'Edit Project Board State',
    }
    template_file = f"{app_name}/{module_path}/edit_project_board_state.html"
    return render(request, template_file, context)



@login_required
def delete_project_board_state(request, project_board_id, project_board_state_id):
    user = request.user
    project_board = ProjectBoard.objects.get(id=project_board_id, active=True, 
                                                **first_viewable_dict)
    
    object = get_object_or_404(ProjectBoardState, pk=project_board_state_id, active=True,**viewable_dict)
    if request.method == 'POST':
        ## Additionally ##
        ## move all the cards from this column to Backlog
        cards_in_this_state = ProjectBoardCard.objects.filter(board_id=project_board_id, state_id=project_board_state_id, active=True)
        for card in cards_in_this_state:
            card.state = None
            card.save()

        object.active = False
        object.save()

        


        return redirect('list_project_board_states', project_board_id=project_board_id)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'delete_project_board_state',
        'project_board': project_board,
        'project_board_id': project_board_id,
        'project': project_board.project,
        'project_id': project_board.project.id,
        'org': project_board.project.org,
        'org_id': project_board.project.org.id,

        'module_path': module_path,        
        'object': object,
        'page_title': f'Delete Project Board State',
    }
    template_file = f"{app_name}/{module_path}/delete_project_board_state.html"
    return render(request, template_file, context)


@login_required
def permanent_deletion_project_board_state(request, project_board_id, project_board_state_id):
    user = request.user
    project_board = ProjectBoard.objects.get(id=project_board_id, active=True, 
                                                **first_viewable_dict)
    
    object = get_object_or_404(ProjectBoardState, pk=project_board_state_id, active=False, deleted=False, **viewable_dict)
    if request.method == 'POST':
        object.active = False
        object.deleted = True
        object.save()
        return redirect('list_project_board_states', project_board_id=project_board_id)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'permanent_deletion_project_board_state',
        'project_board': project_board,
        'project_board_id': project_board_id,
        'project': project_board.project,
        'project_id': project_board.project.id,
        'org': project_board.project.org,
        'org_id': project_board.project.org.id,

        'module_path': module_path,        
        'object': object,
        'page_title': f'Permanent Deletion Project Board State',
    }
    template_file = f"{app_name}/{module_path}/permanent_deletion_project_board_state.html"
    return render(request, template_file, context)


@login_required
def restore_project_board_state(request,  project_board_id, project_board_state_id):
    user = request.user
    object = get_object_or_404(ProjectBoardState, pk=project_board_state_id, active=False,**viewable_dict)
    object.active = True
    object.save()
    return redirect('list_project_board_states', project_board_id=project_board_id)
   


@login_required
def view_project_board_state(request, project_board_id, project_board_state_id):
    user = request.user
    project_board = ProjectBoard.objects.get(id=project_board_id, active=True, 
                                                **first_viewable_dict)
    
    object = get_object_or_404(ProjectBoardState, pk=project_board_state_id, active=True,**viewable_dict)    

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'view_project_board_state',
        'project_board': project_board,
        'project_board_id': project_board_id,
        'project': project_board.project,
        'project_id': project_board.project.id,
        'org': project_board.project.org,
        'org_id': project_board.project.org.id,

        'module_path': module_path,
        'object': object,
        'page_title': f'View Project Board State',
    }
    template_file = f"{app_name}/{module_path}/view_project_board_state.html"
    return render(request, template_file, context)


