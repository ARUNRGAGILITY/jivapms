
from app_organization.mod_app.all_view_imports import *
from app_organization.mod_org_board.models_org_board import *
from app_organization.mod_org_board.forms_org_board import *

from app_organization.mod_organization.models_organization import *
from app_organization.mod_project.models_project import *
from app_organization.mod_backlog.models_backlog import *
from app_organization.mod_backlog_super_type.models_backlog_super_type import *
from app_organization.mod_backlog_type.models_backlog_type import *
from app_organization.mod_project_board_swimlane.models_project_board_swimlane import *
from app_common.mod_common.models_common import *

from app_common.mod_app.all_view_imports import *
from app_jivapms.mod_app.all_view_imports import *
from app_jivapms.mod_web.views_web import *
from django.views.decorators.http import require_POST, require_GET

app_name = 'app_organization'
app_version = 'v1'

module_name = 'org_boards'
module_path = f'mod_org_board'

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
def list_org_boards(request, org_id):
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
        tobjects = OrgBoard.objects.filter(name__icontains=search_query, 
                                            org_id=org_id, **viewable_dict).order_by('position')
    else:
        tobjects = OrgBoard.objects.filter(active=True, org_id=org_id).order_by('position')
        deleted = OrgBoard.objects.filter(active=False, deleted=False,
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
                    object = get_object_or_404(OrgBoard, pk=item, active=True, **viewable_dict)
                    object.active = False
                    object.save()
                    
                elif bulk_operation == 'bulk_done':
                    object = get_object_or_404(OrgBoard, pk=item, active=True, **viewable_dict)
                    object.done = True
                    object.save()
                    
                elif bulk_operation == 'bulk_not_done':
                    object = get_object_or_404(OrgBoard, pk=item, active=True, **viewable_dict)
                    object.done = False
                    object.save()
                    
                elif bulk_operation == 'bulk_blocked':  # Correct the operation check here
                    object = get_object_or_404(OrgBoard, pk=item, active=True, **viewable_dict)
                    object.blocked = True
                    object.save()
                    
                else:
                    redirect('list_org_boards', org_id=org_id)
            return redirect('list_org_boards', org_id=org_id)
    
    # send outputs info, template,
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'list_org_boards',
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
        'page_title': f'Org_board List',
    }       
    template_file = f"{app_name}/{module_path}/list_org_boards.html"
    return render(request, template_file, context)


# ===================== POLICIES AJAX API (dev_env) ===================== #
@login_required
@require_GET
def ajax_list_policies(request):
    """Return all policies for a board grouped by column_key and general list."""
    try:
        board_id = int(request.GET.get('board_id'))
    except (TypeError, ValueError):
        return JsonResponse({"error": "board_id required"}, status=400)

    # Column policies grouped by column_key
    column_policies_qs = ProjectBoardColumnPolicy.objects.filter(board_id=board_id, active=True).order_by('position', 'id')
    grouped = {}
    for p in column_policies_qs:
        key = p.column_key or ''
        grouped.setdefault(key, []).append({
            'id': p.id,
            'text': p.text or '',
            'position': p.position,
        })

    # General policies
    general_qs = ProjectBoardGeneralPolicy.objects.filter(board_id=board_id, active=True).order_by('position', 'id')
    general = [{'id': gp.id, 'text': gp.text or '', 'position': gp.position} for gp in general_qs]

    return JsonResponse({
        'success': True,
        'columns': grouped,
        'general': general,
    })


@login_required
@require_POST
def ajax_create_column_policy(request):
    data = json.loads(request.body or '{}')
    board_id = data.get('board_id')
    column_key = data.get('column_key')
    text = (data.get('text') or '').strip()
    if not board_id or not column_key or not text:
        return JsonResponse({"error": "board_id, column_key and text required"}, status=400)

    policy = ProjectBoardColumnPolicy.objects.create(
        board_id=board_id,
        column_key=column_key,
        text=text,
        author=request.user,
    )
    return JsonResponse({'success': True, 'id': policy.id, 'text': policy.text})


@login_required
@require_POST
def ajax_update_column_policy(request):
    data = json.loads(request.body or '{}')
    policy_id = data.get('id')
    text = (data.get('text') or '').strip()
    if not policy_id or text is None:
        return JsonResponse({"error": "id and text required"}, status=400)
    try:
        policy = ProjectBoardColumnPolicy.objects.get(id=policy_id, active=True)
    except ProjectBoardColumnPolicy.DoesNotExist:
        return JsonResponse({"error": "Not found"}, status=404)
    policy.text = text
    policy.save()
    return JsonResponse({'success': True})


@login_required
@require_POST
def ajax_delete_column_policy(request):
    data = json.loads(request.body or '{}')
    policy_id = data.get('id')
    if not policy_id:
        return JsonResponse({"error": "id required"}, status=400)
    updated = ProjectBoardColumnPolicy.objects.filter(id=policy_id).update(active=False, deleted=True)
    if not updated:
        return JsonResponse({"error": "Not found"}, status=404)
    return JsonResponse({'success': True})


@login_required
@require_POST
def ajax_reorder_column_policies(request):
    """Update positions in bulk for a given column_key.
    Payload: { board_id, column_key, order: [ {id, position}, ... ] }
    """
    data = json.loads(request.body or '{}')
    order = data.get('order') or []
    for item in order:
        pid = item.get('id')
        pos = item.get('position', 1000)
        if pid:
            ProjectBoardColumnPolicy.objects.filter(id=pid).update(position=pos)
    return JsonResponse({'success': True})


@login_required
@require_POST
def ajax_create_general_policy(request):
    data = json.loads(request.body or '{}')
    board_id = data.get('board_id')
    text = (data.get('text') or '').strip()
    if not board_id or not text:
        return JsonResponse({"error": "board_id and text required"}, status=400)
    gp = ProjectBoardGeneralPolicy.objects.create(board_id=board_id, text=text, author=request.user)
    return JsonResponse({'success': True, 'id': gp.id, 'text': gp.text})


@login_required
@require_POST
def ajax_update_general_policy(request):
    data = json.loads(request.body or '{}')
    policy_id = data.get('id')
    text = (data.get('text') or '').strip()
    if not policy_id or text is None:
        return JsonResponse({"error": "id and text required"}, status=400)
    try:
        gp = ProjectBoardGeneralPolicy.objects.get(id=policy_id, active=True)
    except ProjectBoardGeneralPolicy.DoesNotExist:
        return JsonResponse({"error": "Not found"}, status=404)
    gp.text = text
    gp.save()
    return JsonResponse({'success': True})


@login_required
@require_POST
def ajax_delete_general_policy(request):
    data = json.loads(request.body or '{}')
    policy_id = data.get('id')
    if not policy_id:
        return JsonResponse({"error": "id required"}, status=400)
    updated = ProjectBoardGeneralPolicy.objects.filter(id=policy_id).update(active=False, deleted=True)
    if not updated:
        return JsonResponse({"error": "Not found"}, status=404)
    return JsonResponse({'success': True})





# ============================================================= #
@login_required
def list_deleted_org_boards(request, org_id):
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
        tobjects = OrgBoard.objects.filter(name__icontains=search_query, 
                                            active=False, deleted=False,
                                            org_id=org_id, **viewable_dict).order_by('position')
    else:
        tobjects = OrgBoard.objects.filter(active=False, deleted=False, org_id=org_id,
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
                        object = get_object_or_404(OrgBoard, pk=item, active=False, **viewable_dict)
                        object.active = True
                        object.save()         
                    elif bulk_operation == 'bulk_erase':
                        object = get_object_or_404(OrgBoard, pk=item, active=False, **viewable_dict)
                        object.active = False  
                        object.deleted = True             
                        object.save()    
                    else:
                        redirect('list_org_boards', org_id=org_id)
                redirect('list_org_boards', org_id=org_id)
    
    # send outputs info, template,
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'list_deleted_org_boards',
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
        'page_title': f'Org_board List',
    }       
    template_file = f"{app_name}/{module_path}/list_deleted_org_boards.html"
    return render(request, template_file, context)



# Create View
@login_required
def create_org_board(request, org_id):
    user = request.user
    organization = Organization.objects.get(id=org_id, active=True, 
                                                **first_viewable_dict)
    
    if request.method == 'POST':
        form = OrgBoardForm(request.POST)
        if form.is_valid():
            form.instance.author = user
            form.instance.org_id = org_id
            form.save()
        else:
            print(f">>> === form.errors: {form.errors} === <<<")
        return redirect('list_org_boards', org_id=org_id)
    else:
        form = OrgBoardForm()

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'create_org_board',
        'organization': organization,
        'org_id': org_id,
        
        'module_path': module_path,
        'form': form,
        'page_title': f'Create Org Board',
    }
    template_file = f"{app_name}/{module_path}/create_org_board.html"
    return render(request, template_file, context)




# Edit
@login_required
def edit_org_board(request, org_id, org_board_id):
    user = request.user
    organization = Organization.objects.get(id=org_id, active=True, 
                                                **first_viewable_dict)
    
    object = get_object_or_404(OrgBoard, pk=org_board_id, active=True,**viewable_dict)
    if request.method == 'POST':
        form = OrgBoardForm(request.POST, instance=object)
        if form.is_valid():
            form.instance.author = user
            form.instance.org_id = org_id
            form.save()
        else:
            print(f">>> === form.errors: {form.errors} === <<<")
        return redirect('list_org_boards', org_id=org_id)
    else:
        form = OrgBoardForm(instance=object)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'edit_org_board',
        'organization': organization,
        'org_id': org_id,
        
        'module_path': module_path,
        'form': form,
        'object': object,
        'page_title': f'Edit Org Board',
    }
    template_file = f"{app_name}/{module_path}/edit_org_board.html"
    return render(request, template_file, context)



@login_required
def delete_org_board(request, org_id, org_board_id):
    user = request.user
    organization = Organization.objects.get(id=org_id, active=True, 
                                                **first_viewable_dict)
    
    object = get_object_or_404(OrgBoard, pk=org_board_id, active=True,**viewable_dict)
    if request.method == 'POST':
        object.active = False
        object.save()
        return redirect('list_org_boards', org_id=org_id)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'delete_org_board',
        'organization': organization,
        'org_id': org_id,
        
        'module_path': module_path,        
        'object': object,
        'page_title': f'Delete Org Board',
    }
    template_file = f"{app_name}/{module_path}/delete_org_board.html"
    return render(request, template_file, context)


@login_required
def permanent_deletion_org_board(request, org_id, org_board_id):
    user = request.user
    organization = Organization.objects.get(id=org_id, active=True, 
                                                **first_viewable_dict)
    
    object = get_object_or_404(OrgBoard, pk=org_board_id, active=False, deleted=False, **viewable_dict)
    if request.method == 'POST':
        object.active = False
        object.deleted = True
        object.save()
        return redirect('list_org_boards', org_id=org_id)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'permanent_deletion_org_board',
        'organization': organization,
        'org_id': org_id,
        
        'module_path': module_path,        
        'object': object,
        'page_title': f'Permanent Deletion Org Board',
    }
    template_file = f"{app_name}/{module_path}/permanent_deletion_org_board.html"
    return render(request, template_file, context)


@login_required
def restore_org_board(request,  org_id, org_board_id):
    user = request.user
    object = get_object_or_404(OrgBoard, pk=org_board_id, active=False,**viewable_dict)
    object.active = True
    object.save()
    return redirect('list_org_boards', org_id=org_id)
   


@login_required
def view_org_board(request, org_id, org_board_id):
    user = request.user
    organization = Organization.objects.get(id=org_id, active=True, 
                                                **first_viewable_dict)
    
    object = get_object_or_404(OrgBoard, pk=org_board_id, active=True,**viewable_dict)    

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'view_org_board',
        'organization': organization,
        'org_id': org_id,
        
        'module_path': module_path,
        'object': object,
        'page_title': f'View Org Board',
    }
    template_file = f"{app_name}/{module_path}/view_org_board.html"
    return render(request, template_file, context)




@login_required
def view_project_board(request, project_id):
    user = request.user
    project = Project.objects.get(id=project_id, active=True)
    org_id = project.org.id
    organization = project.org
    # Backlog collections
    flat_backlog_root = Backlog.objects.filter(pro=project, name=FLAT_BACKLOG_ROOT_NAME).first()
    flat_backlog_collection_type = BacklogType.objects.filter(name='Collection').first() 
    backlog_collections = Backlog.objects.filter(pro=project, type=flat_backlog_collection_type, parent=flat_backlog_root, active=True)
    # send the backlog details of the project
    backlog_types = BacklogType.objects.filter(
        active=True, 
        name__in=FLAT_BACKLOG_TYPES.values(), 
    ).select_related('type')
    filters = {}
    # Get or create the default project board
    DEFAULT_BOARD_NAME = 'Default Board'
    project_board, created = ProjectBoard.objects.get_or_create(
        project=project,
        name=DEFAULT_BOARD_NAME,
        defaults={'author': user}
    )
    
    board_name = ProjectBoard.objects.get(project=project, active=True, name=DEFAULT_BOARD_NAME)

    # Ensure the default columns exist or create them
    DEFAULT_BOARD_COLUMNS = ['To Do', 'WIP', 'Done']
    #ProjectBoardState.objects.all().delete()
    backlog_state = None  # To store the "Backlog" state reference
    for position, column_name in enumerate(DEFAULT_BOARD_COLUMNS):
        state, _ = ProjectBoardState.objects.get_or_create(
            board=project_board,
            name=column_name,
            defaults={'author': user, 'wip_limit': 0}
        )
        if column_name == 'Backlog':
            backlog_state = state

    actual_project_backlog_items = Backlog.objects.filter(
        pro_id=project.id,
        type__in=backlog_types,
        active=True
    ).exclude(
        id__in=ProjectBoardCard.objects.filter(
            board=project_board,
            state__isnull=False  # Exclude items where state.id is NOT NULL (moved to other states)
        ).values_list('backlog_id', flat=True)
    ).order_by('position', '-created_at')    
   
    # Get the project board states
    project_board_states = ProjectBoardState.objects.filter(board=project_board)
    
    # Fetch the project backlog items state
    state_items = {state.name: [] for state in project_board.board_states.filter(active=True)}
   
    # Get the card / backlog item from the ProjectBoardStateTransition
    for state in project_board_states:
        state_items[state.name] = ProjectBoardCard.objects.filter(
            board=project_board,
            state=state,
            active=True,
            backlog__active=True  # Exclude cards linked to soft-deleted Backlog items
        ).select_related('backlog').order_by('position', '-created_at')

    context = {
        'organization': organization,
        'org_id': org_id,
        'project': project,
        'pro_id': project.id,
        'project_board': project_board,
        'project_board_states': project_board_states,
        'backlog_items': actual_project_backlog_items,
        'todo_items': state_items.get('To Do', []),
        'in_progress_items': state_items.get('In Progress', []),
        'blocked_items': state_items.get('Blocked', []),
        'done_items': state_items.get('Done', []),
        'page_title': f'Project Board: {project.name}',
        
        #'chart_data': chart_data,
    }

    template_file = f"{app_name}/{module_path}/project/view_project_board.html"
    return render(request, template_file, context)

from app_organization.mod_backlog.views_project_tree import create_or_update_tree_from_config, get_tree_name_id
@login_required
def view_project_tree_board(request, project_id):
    user = request.user
    project = Project.objects.get(id=project_id, active=True)
    org_id = project.org.id
    organization = project.org
    # Backlog types
    pbst_name = f"{project.id}_PROJECT_TREE"
    project_backlog_type, created = BacklogType.objects.get_or_create(pro=project, name=pbst_name)
    config = PROJECT_WBS_TREE_CONFIG
    backlog_type_node = create_or_update_tree_from_config(config, model_name="app_organization.BacklogType", parent=project_backlog_type, project=project)
    bt_tree_name_and_id = get_tree_name_id(backlog_type_node)
    epic_type_id = bt_tree_name_and_id.get("Epic")
    epic_type_node = BacklogType.objects.get(id=epic_type_id)
    epic_type_children = epic_type_node.get_active_children()
    backlog_types = epic_type_children
    backlog_types_count = backlog_types.count()
    
    bug_type_id = bt_tree_name_and_id.get("Bug")
    story_type_id = bt_tree_name_and_id.get("User Story")
    tech_task_type_id = bt_tree_name_and_id.get("Technical Task")
    
    feature_type_id = bt_tree_name_and_id.get("Feature")
    component_type_id = bt_tree_name_and_id.get("Component")
    capability_type_id = bt_tree_name_and_id.get("Capability")
    
    include_types = [bug_type_id, story_type_id, tech_task_type_id]
    efcc_include_types = [epic_type_id, feature_type_id, component_type_id, capability_type_id] # meaning Epic, Feature, Component, Capability
    efcc_backlog_items = Backlog.objects.filter(pro_id=project.id, type__in=efcc_include_types, active=True)
    efcc_backlog_items_swimlane = Backlog.objects.filter(pro_id=project.id, active=True)
    get_swimlane_id = request.GET.get('swimlane_id')  if request.GET.get('swimlane_id') else '-1'
    swimlane_flag = True
    project_iteration_flag = False
    project_release_iteration_board = None
    logger.debug(f">>> === CHECK: {efcc_include_types} === <<<")
    logger.debug(f">>> === get_swimlane_id: {get_swimlane_id} === <<<" )
    efcc_backlog_with_no_epic = None 
    
    # 1. There is no swimlane_id provided, like initial page
    # 2. There is a swimlane_id provided, like when a swimlane is clicked
    # 3. All Swimlanes to be listed
    USE_DEFAULT_PROJECT_BOARD_FLAG = True
    current_datetime = now().replace(microsecond=0)
    current_release = None
    current_iteration = None
    if get_swimlane_id == '-1':  # Check if swimlane_id is provided
        # No swimlane
        project_iteration = project.project_iteration
        project_release = project.project_release
        project_iteration_flag = True
        if project.project_release and project.project_iteration:
            details = get_project_release_and_iteration_details(project.id)
            current_release = details.get('current_release')
            current_iteration = details.get('current_iteration')
            next_iteration = details.get('next_iteration')
            # Check the Project Release_Iteration Board exists, if not create it
            project_release_iteration_board, created = ProjectBoard.objects.get_or_create(
                project=project,
                name=f"{project.name} Release_Iteration Board",
                org_release=current_release,
                org_iteration=current_iteration,
                defaults={'author': user}
            )
            USE_DEFAULT_PROJECT_BOARD_FLAG = False
            BOARD_NAME = project_release_iteration_board.name
            BOARD_ID = project_release_iteration_board.id
            message = ""
            if created:
                message="Project Release_Iteration Board created successfully"
            logger.debug(f">>> === project_release_iteration_board: {project_release_iteration_board} === <<<")
            logger.debug(f">>> === current_release: {current_release} === <<<")
            logger.debug(f">>> === current_iteration: {current_iteration} === <<<")
            logger.debug(f">>> === project_iteration: {project_iteration} === <<<")
            logger.debug(f">>> === project_release: {project_release} === <<<")
            logger.debug(f">>> === current_datetime: {current_datetime} === <<<")
            logger.debug(f">>> === project: {project} {message}=== <<<")
            efcc_backlog_items_swimlane = Backlog.objects.filter(
                pro_id=project.id,
                type__in=efcc_include_types,
                active=True,            
            )
        else:
            logger.debug(f">>> === ***ALERT*** PROJECT RELEASE AND ITERATION NOT MAPPED YET === <<<")
    elif get_swimlane_id == '0':  # Check if swimlane_id is provided   
        # If no swimlane_id is provided, get all Backlog items
        efcc_backlog_items_swimlane = Backlog.objects.filter(
            pro_id=project.id,
            type__in=efcc_include_types,
            active=True
        )
        efcc_backlog_with_no_epic = Backlog.objects.filter(
            pro_id=project.id,
            active=True
        ).exclude(type__in=efcc_include_types)
        logger.debug(f">>> === efcc_backlog_items (else): {efcc_backlog_items} === <<<")
        
    else:    
        # Filter Backlog items based on swimlane_id
        efcc_backlog_items_swimlane = Backlog.objects.filter(
            pro_id=project.id,            
            id=get_swimlane_id,
            active=True
        )
        swimlane_flag = True
        
    logger.debug(f">>> === efcc_backlog_items_swimlane: {efcc_backlog_items_swimlane} === <<<")
    filters = {}
    
    #
    if USE_DEFAULT_PROJECT_BOARD_FLAG:
        # Get or create the default project board
        DEFAULT_BOARD_NAME = 'Default Board'
        project_board, created = ProjectBoard.objects.get_or_create(
            project=project,
            name=DEFAULT_BOARD_NAME,
            defaults={'author': user}
        )
        
        board_name = ProjectBoard.objects.get(project=project, active=True, name=DEFAULT_BOARD_NAME)

        # Ensure the default columns exist or create them
        DEFAULT_BOARD_COLUMNS = ['ToDo', 'WIP', 'Done']
        #ProjectBoardState.objects.all().delete()
        backlog_state = None  # To store the "Backlog" state reference
        for position, column_name in enumerate(DEFAULT_BOARD_COLUMNS):
            state, _ = ProjectBoardState.objects.get_or_create(
                board=project_board,
                name=column_name,
                defaults={'author': user, 'wip_limit': 0}
            )
            if column_name == 'Backlog':
                backlog_state = state
        
        logger.debug(f">>> === current release: {current_release} {current_iteration} === <<<")
        actual_project_backlog_items = Backlog.objects.filter(
            pro_id=project.id,
            type__in=backlog_types,
            active=True,
           
        ).exclude(
            id__in=ProjectBoardCard.objects.filter(
                board=project_board,
                state__isnull=False  # Exclude items where state.id is NOT NULL (moved to other states)
            ).values_list('backlog_id', flat=True)
        ).order_by('position', '-created_at')    
        
        # Get the project board states
        project_board_states = ProjectBoardState.objects.filter(board=project_board)
        
        # Fetch the project backlog items state
        state_items = {state.name: [] for state in project_board.board_states.filter(active=True)}
        logger.debug(f">>> === state_items: {state_items} === <<<")
        # Get the card / backlog item from the ProjectBoardStateTransition
        for state in project_board_states:
            state_items[state.name] = ProjectBoardCard.objects.filter(
                board=project_board,
                state=state,
                active=True,
                backlog__type__in=backlog_types,
                backlog__active=True  # Exclude cards linked to soft-deleted Backlog items
            ).select_related('backlog').order_by('position', '-created_at')
        logger.debug(f">>> === state_items: {project_board_states} === <<<")
    else:
        # WE HAVE THE PROJECT RELEASE_ITERATION BOARD
        DEFAULT_BOARD_COLUMNS = ['ToDo', 'WIP', 'Done']
        project_board = project_release_iteration_board
        #ProjectBoardState.objects.all().delete()
        backlog_state = None  # To store the "Backlog" state reference
        for position, column_name in enumerate(DEFAULT_BOARD_COLUMNS):
            state, _ = ProjectBoardState.objects.get_or_create(
                board=project_board,
                name=column_name,
                defaults={'author': user, 'wip_limit': 0}
            )
            if column_name == 'Backlog':
                backlog_state = state
        
        logger.debug(f">>> === current release: {current_release} {current_iteration} === <<<")
        actual_project_backlog_items = Backlog.objects.filter(
            pro_id=project.id,
            type__in=backlog_types,
            active=True,
            iteration=current_iteration,
            release=current_release,
        ).exclude(
            id__in=ProjectBoardCard.objects.filter(
                board=project_board,
                state__isnull=False  # Exclude items where state.id is NOT NULL (moved to other states)
            ).values_list('backlog_id', flat=True)
        ).order_by('position', '-created_at')    
        logger.debug(f">>> === ********************** SUPER IMPORTANT actual_project_backlog_items: {actual_project_backlog_items} === <<<")
        # Get the project board states
        project_board_states = ProjectBoardState.objects.filter(board=project_board)
        
        # Fetch the project backlog items state
        state_items = {state.name: [] for state in project_board.board_states.filter(active=True)}
        #logger.debug(f">>> === state_items: {state_items} === <<<")
        # Get the card / backlog item from the ProjectBoardStateTransition
        for state in project_board_states:
            state_items[state.name] = ProjectBoardCard.objects.filter(
                board=project_board,
                state=state,
                active=True,
                backlog__type__in=backlog_types,
                backlog__active=True  # Exclude cards linked to soft-deleted Backlog items
            ).select_related('backlog').order_by('position', '-created_at')
        logger.debug(f">>> === PROJECT REL ITR BOARD state_items: {project_board} ==> {project_board_states} === <<<")
        
        check_project_board_card = ProjectBoardCard.objects.filter(
            board=project_board,
            active=True
        )   
        logger.debug(f">>> === check_project_board_card: {check_project_board_card} === <<<")
        
    context = {
        'organization': organization,
        'org_id': org_id,
        'project': project,
        'pro_id': project.id,
        'project_board': project_board,
        'project_board_states': project_board_states,
        'backlog_items': actual_project_backlog_items,
        'todo_items': state_items.get('ToDo', []),
        'in_progress_items': state_items.get('WIP', []),
        'done_items': state_items.get('Done', []),
        'page_title': f'Project Board: {project.name}',
        'efcc_backlog_items': efcc_backlog_items,
        'efcc_backlog_with_no_epic': efcc_backlog_with_no_epic,
        'swimlane_flag': swimlane_flag,
        'efcc_backlog_items_swimlane': efcc_backlog_items_swimlane,
        
        'project_iteration_flag': project_iteration_flag,
        'current_release': current_release,
        'current_iteration': current_iteration,
        
        
        #'chart_data': chart_data,
    }
    project_type = project.project_details.template.name 
    if project_type == 'Kanban':
        template_file = f"{app_name}/{module_path}/project/view_project_tree_board_kanban.html"
    else:
        template_file = f"{app_name}/{module_path}/project/view_project_tree_board.html"
    return render(request, template_file, context)


def update_project_board_state_transition(board_id, card, from_state_id, to_state_id):
    with transaction.atomic():
        if to_state_id == 0:
            # Move to backlog
            to_state_id = None
        if from_state_id == 0:
            # Move from backlog
            from_state_id = None
        # Log the transition
        created_st_entry = ProjectBoardStateTransition.objects.create(
            board_id = board_id,
            card=card.backlog,
            from_state_id=from_state_id,
            to_state_id=to_state_id,
            transition_time=now(),
        )
        created_st_entry.save()
        
        # need to update the completed details / done details
        print(f">>>>>>>> TOSTATE: {to_state_id} FROMSTATE: {from_state_id}") 
        to_state_details = ProjectBoardState.objects.filter(id=to_state_id).first()
        from_state_details = ProjectBoardState.objects.filter(id=from_state_id).first()
        if to_state_details and to_state_details.name == "Done":
            card.backlog.done = True
            card.backlog.done_at = now()
            card.backlog.save()
            logger.debug(f">>> === DONE FOR CARD {card.backlog} {card.backlog.done} {card.backlog.done_at} === <<<")
        if from_state_details and from_state_details.name == "Done":
            card.backlog.done = False
            card.backlog.done_at = None
            card.backlog.save()
            logger.debug(f">>> === UNDONE FOR CARD {card.backlog} {card.backlog.done} {card.backlog.done_at} === <<<")
        
        print(f">>> === Created State Transition: {created_st_entry} === <<<")
    return created_st_entry
                


def column_to_column_update(positions, board_id, card_id, from_column, from_state_id, dest_column, to_state_id):    
    try:
        # Get the specific ProjectBoardCard being moved
        pbc = ProjectBoardCard.objects.filter(id=card_id, active=True).first()
        logger.debug(f">>> === Moving card: {pbc} from {from_state_id} to {to_state_id} === <<<")
        
        if not pbc:
            logger.error(f">>> === ProjectBoardCard with id {card_id} not found === <<<")
            return JsonResponse({"success": False, "error": "Card not found"})

        # Update positions for all cards in the destination column
        for pos in positions:
            pos_card_id = pos.get('card_id')
            position = pos.get('position')    
            
            # Update the card's position and state
            ProjectBoardCard.objects.filter(
                id=pos_card_id,
                active=True
            ).update(position=position, state_id=to_state_id, board_id=board_id)

        # Create audit trail entry (this SHOULD create a new transition record)
        update_project_board_state_transition(board_id, pbc, from_state_id, to_state_id)
        return JsonResponse({"success": True})
        
    except Exception as e:
        logger.error(f">>> === Error in column_to_column_update: {str(e)} === <<<")
        return JsonResponse({"success": False, "error": str(e)})




def column_to_backlog_update(positions, board_id, this_card_id, from_column, from_state_id, dest_column, to_state_id):  
    try:
        # Get the ProjectBoardCard being moved back to backlog
        card = ProjectBoardCard.objects.filter(id=this_card_id, active=True).first()
        
        if not card:
            logger.error(f">>> === ProjectBoardCard with id {this_card_id} not found === <<<")
            return JsonResponse({"success": False, "error": "Card not found"})
            
        # Move card back to backlog (set state to None)
        card.state = None
        card.position = 0
        card.save()
        
        logger.debug(f">>> === Card {card.id} moved back to backlog === <<<")
        
        # Update backlog item positions
        for pos in positions:
            backlog_card_id = pos.get('card_id')
            position = pos.get('position')
            
            if backlog_card_id == card.backlog.id:
                # Update position of the backlog item that was moved
                Backlog.objects.filter(id=card.backlog.id, active=True).update(position=position)
            else:
                # Update positions of other backlog items
                Backlog.objects.filter(id=backlog_card_id, active=True).update(position=position)

        # Create audit trail entry (this SHOULD create a new transition record)
        update_project_board_state_transition(board_id, card, from_state_id, to_state_id)
        return JsonResponse({"success": True})

    except Exception as e:
        logger.error(f">>> === Error in column_to_backlog_update: {str(e)} === <<<")
        return JsonResponse({"success": False, "error": str(e)})


def backlog_to_column_update(positions, board_id, this_card_id, from_column, from_state_id, dest_column, to_state_id):
    logger.debug(f">>> === BACKLOG_TO_COLUMN: {positions} {board_id} {this_card_id} {from_column} {from_state_id} {dest_column} {to_state_id}=== <<<") 
    try:
        # Look for existing ProjectBoardCard for this backlog item on this board
        # regardless of current state - we want only ONE card per backlog item per board
        card = ProjectBoardCard.objects.filter(
            board_id=board_id,
            backlog_id=this_card_id,
            active=True
        ).first()
        
        if card:
            # Update existing card to new state
            card.state_id = to_state_id
            card.position = 0
            card.save()
            logger.debug(f">>> === Updated existing card to new state: {card} === <<<")
        else:
            # Create new card only if none exists for this backlog item on this board
            card = ProjectBoardCard.objects.create(
                board_id=board_id,
                backlog_id=this_card_id,
                state_id=to_state_id,
                position=0
            )
            logger.debug(f">>> === Created new card: {card} === <<<")

        # Update positions for all cards in the destination column
        for pos in positions:
            card_id = pos.get('card_id')
            position = pos.get('position')            
            if card_id == this_card_id:
                # Update the moved card (by backlog_id since it came from backlog)
                ProjectBoardCard.objects.filter(
                    backlog_id=this_card_id, 
                    board_id=board_id,
                    active=True
                ).update(position=position, state_id=to_state_id)
            else:
                # Update other cards in the column (by card ID)
                ProjectBoardCard.objects.filter(
                    id=card_id,
                    active=True
                ).update(position=position)
                
        # Create audit trail entry (this SHOULD create multiple entries)
        update_project_board_state_transition(board_id, card, from_state_id, to_state_id)
        return JsonResponse({"success": True})

    except Exception as e:
        logger.error(f">>> === Error in backlog_to_column_update: {str(e)} === <<<")
        return JsonResponse({"success": False, "error": str(e)})


def within_column_update(positions, board_id, card_id, dest_column, to_state_id):   
    pbc = ProjectBoardCard.objects.get(id=card_id)    
    for pos in positions:
        card_id = pos.get('card_id')
        position = pos.get('position')     
        check_card = ProjectBoardCard.objects.filter(id=card_id)
        print(f">>> === CHECK CARD: {check_card} === <<<")
        ProjectBoardCard.objects.filter(id=card_id).update(position=position, board_id=board_id)       
    return JsonResponse({"success": True})

def within_backlog_update(positions, board_id, card_id):  
    bi = Backlog.objects.get(id=card_id)    
    for pos in positions:
        card_id = pos.get('card_id')
        position = pos.get('position')       
        Backlog.objects.filter(id=card_id).update(position=position)        
    return JsonResponse({"success": True})

def update_backlog_text_status(card_id, to_state):
    try:
        backlog = Backlog.objects.get(id=card_id)
        backlog.status = to_state
        backlog.save()
        return JsonResponse({"success": True})
    except Exception as e:
        return JsonResponse({"error": str(e)})  
    
def update_movement(project_id, board_id, card_id, from_state_id, to_state_id, from_column, to_column, positions):
    project = Project.objects.filter(id=project_id).first()
    project_board = ProjectBoard.objects.filter(id=board_id).first()
    card = ProjectBoardCard.objects.filter(id=card_id).first()
    from_column = ProjectBoardState.objects.filter(id=from_state_id).first()
    to_column = ProjectBoardState.objects.filter(id=to_state_id).first()




# Utility function to find and fix duplicate ProjectBoardCard entries
def find_and_fix_duplicate_board_cards(board_id=None):
    """
    Find and fix duplicate ProjectBoardCard entries.
    Keep the most recent card for each backlog item on each board.
    NOTE: This does NOT touch ProjectBoardStateTransition - those are audit trails and should remain.
    """
    try:
        from django.db.models import Count
        
        query = ProjectBoardCard.objects.filter(active=True)
        if board_id:
            query = query.filter(board_id=board_id)
            
        # Find backlog items that have multiple active cards on the same board
        duplicates = query.values('board_id', 'backlog_id').annotate(
            count=Count('id')
        ).filter(count__gt=1)
        
        fixed_count = 0
        
        for duplicate in duplicates:
            board_id = duplicate['board_id']
            backlog_id = duplicate['backlog_id']
            
            # Get all cards for this backlog item on this board, ordered by creation time
            cards = ProjectBoardCard.objects.filter(
                board_id=board_id,
                backlog_id=backlog_id,
                active=True
            ).order_by('-created_at')  # Most recent first
            
            # Keep the first (most recent) card, deactivate the rest
            cards_to_deactivate = cards[1:]  # Skip the first one
            for card in cards_to_deactivate:
                card.active = False
                card.save()
                logger.debug(f">>> === Deactivated duplicate ProjectBoardCard: {card.id} === <<<")
                fixed_count += 1
                
        logger.info(f">>> === Fixed {fixed_count} duplicate ProjectBoardCard entries === <<<")
        return fixed_count
        
    except Exception as e:
        logger.error(f">>> === Error fixing duplicates: {str(e)} === <<<")
        return 0


@login_required
def ajax_update_project_board_card_state(request):
    if request.method == "POST":
        data = json.loads(request.body)
        #data = request.POST
        card_id = data.get('card_id')
        board_id = data.get('board_id')
        from_state_id = data.get('from_state_id')
        to_state_id = data.get('to_state_id')

        # position 
        positions = data.get('positions')
        from_column = data.get('from_column').strip()
        dest_column = data.get('dest_column').strip()
        project_id = data.get('project_id')
        # just to set 
        to_column = dest_column
        is_new_card = data.get('is_new_card')
        card_text = data.get('title')
        card_priority = data.get('priority')
        card_substate = data.get('substate')

        #ProjectBoardStateTransition.objects.filter(board_id=board_id).delete()
        print(f">>> === positions: {positions} === <<<")
        print(f">>> === from_state_id: {from_state_id} === <<<")
        print(f">>> === to_state_id: {to_state_id} === <<<")
        print(f">>> === from_column: {from_column} === <<<")
        print(f">>> === dest_column: {dest_column} === <<<")
        print(f">>> === project_id: {project_id} === <<<")
        print(f">>> === board_id: {board_id} === <<<")
        print(f">>> === card_id: {card_id} === <<<")
        print(f">>> === is_new_card: {is_new_card} === <<<")
        print(f">>> === card_text: {card_text} === <<<")
        print(f">>> === card_priority: {card_priority} === <<<")
        print(f">>> === card_substate: {card_substate} === <<<")
       

        if from_state_id != None:
            from_state_id = int(from_state_id)

        if to_state_id != None:
            to_state_id = int(to_state_id)



        if is_new_card:
            # If it's a new card, create it and set its state
            context = _GET_BACKLOG_TYPES(request, project_id)
            story_type_id = context.get('story_type_id')
            project_backlog_root_node = context.get('project_backlog_root_node')
            print(f">>> === project_backlog_root_node: {story_type_id}  {story_type_id} === <<<")
            backlog_item = Backlog.objects.create(name=card_text, pro_id=project_id, type_id=story_type_id, priority=card_priority,
                                                  parent=project_backlog_root_node, author=request.user, status="Backlog")
            from_state_id = 0
            if to_state_id == 0: 
                to_state_id = None
            card = ProjectBoardCard.objects.create(
                backlog=backlog_item,
                board_id=board_id,
                state_id=to_state_id,
                position=0,  # Set the initial position
            )
            update_project_board_state_transition(board_id, card, from_state_id, to_state_id)
            return JsonResponse({"success": True})
        else:
            if from_state_id == 0  and to_state_id == 0:
                logger.debug(f">>> === Backlogx: Within column movement === <<<")
                within_backlog_update(positions, board_id, card_id)
            elif from_column != 'Backlog' and from_state_id !=0 and to_state_id != 0 and from_state_id == to_state_id:
                logger.debug(f">>> === {dest_column}: Within column movement  === <<<")
                within_column_update(positions, board_id, card_id, dest_column, to_state_id)
            elif from_column != 'Backlog' and from_state_id !=0 and to_state_id != 0 and from_state_id != to_state_id:
                logger.debug(f">>> === FSID{from_state_id},TSID{to_state_id} {from_column} to {dest_column}: Between column movement  === <<<")
                column_to_column_update(positions, board_id, card_id, from_column, from_state_id, dest_column, to_state_id)
                actual_card = ProjectBoardCard.objects.filter(id=card_id).first()
                actual_card_id = actual_card.backlog.id
                update_backlog_text_status(actual_card_id, dest_column)
            elif from_column == 'Backlog' and to_state_id != 0:
                logger.debug(f">>> ===  FSID{from_state_id},TSID{to_state_id} {from_column} to {dest_column}: Between column movement (from Backlog) === <<<")
                backlog_to_column_update(positions, board_id, card_id, from_column, from_state_id, dest_column, to_state_id)
                update_backlog_text_status(card_id, dest_column)
            elif to_state_id == 0 and from_state_id != 0:
                logger.debug(f">>> ===   {from_column} to {dest_column}: Between Column Movement (to Backlog)   === <<<")
                column_to_backlog_update(positions, board_id, card_id, from_column, from_state_id, dest_column, to_state_id)
                update_backlog_text_status(card_id, dest_column)

            # Update Movement: project_id, board_id, card_id, from_state_id, to_state_id, from_column, dest_column, positions
            update_movement(project_id, board_id, card_id, from_state_id, to_state_id, from_column, to_column, positions)

            return JsonResponse({"success": True})

    return JsonResponse({"error": "Invalid request method"}, status=405)


def get_cumulative_flow_data(board_id):
    # Fetch all transitions for the board
    # Get the project board instance
    project_board = ProjectBoard.objects.get(id=board_id)

    # Fetch transitions for cards on the board
    transitions = ProjectBoardStateTransition.objects.filter(
        card__board_cards__board=project_board  # Access ProjectBoardCard through Backlog and filter by board
    ).values(
        'card__id',  # Backlog ID
        'from_state__name', 
        'to_state__name', 
        'transition_time'
    )

    # Fetch the min and max dates for transitions
    min_date = transitions.aggregate(Min('transition_time'))['transition_time__min'].date()
    max_date = transitions.aggregate(Max('transition_time'))['transition_time__max'].date()

    # Prepare a mapping of states to daily counts
    states = ProjectBoardState.objects.filter(board=project_board).values_list('name', flat=True)
    state_data = {state: [0] * ((max_date - min_date).days + 1) for state in states}

    # Create a mapping of dates for the range
    date_index = {min_date + timedelta(days=i): i for i in range((max_date - min_date).days + 1)}

    # Process transitions to populate state data
    for transition in transitions:
        card_id = transition['card__id']
        from_state = transition['from_state__name']
        to_state = transition['to_state__name']
        transition_time = transition['transition_time'].date()

        # Increment the state on the respective day
        if to_state in state_data:
            state_data[to_state][date_index[transition_time]] += 1
#{{item.backlog.id}}
    # Cumulatively sum the counts for each state
    for state, counts in state_data.items():
        for i in range(1, len(counts)):
            counts[i] += counts[i - 1]

    # Prepare data for Chart.js
    chart_data = {
        "labels": [str(min_date + timedelta(days=i)) for i in range((max_date - min_date).days + 1)],
        "datasets": [
            {
                "label": state,
                "data": counts,
                "fill": "origin"
            } for state, counts in state_data.items()
        ]
    }
    print(f">>> === chart_data: {chart_data} === <<<")
    return chart_data

@login_required
def ajax_update_project_board_card_order(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            card_order = data.get("card_order", [])

            # Update positions in the database
            for item in card_order:
                card_id = item.get("card_id")
                position = item.get("position")
                if card_id is not None and position is not None:
                    ProjectBoardCard.objects.filter(id=card_id).update(position=position)

            return JsonResponse({"success": True, "message": "Card positions updated successfully."})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=405)


from app_organization.mod_backlog.views_project_tree import create_or_update_tree_from_config, get_tree_name_id

@login_required
def _GET_BACKLOG_TYPES(request, project_id):
    user = request.user
    project = Project.objects.get(id=project_id, active=True)
    org_id = project.org.id
    organization = project.org
    # Backlog types
    pbst_name = f"{project.id}_PROJECT_TREE"
    project_backlog_root_node = Backlog.objects.get(pro=project, name=pbst_name)
    project_backlog_type, created = BacklogType.objects.get_or_create(pro=project, name=pbst_name)
    config = PROJECT_WBS_TREE_CONFIG
    backlog_type_node = create_or_update_tree_from_config(config, model_name="app_organization.BacklogType", parent=project_backlog_type, project=project)
    bt_tree_name_and_id = get_tree_name_id(backlog_type_node)
    epic_type_id = bt_tree_name_and_id.get("Epic")
    epic_type_node = BacklogType.objects.get(id=epic_type_id)
    epic_type_children = epic_type_node.get_active_children()
    backlog_types = epic_type_children
    backlog_types_count = backlog_types.count()
    
    bug_type_id = bt_tree_name_and_id.get("Bug")
    story_type_id = bt_tree_name_and_id.get("User Story")
    tech_task_type_id = bt_tree_name_and_id.get("Technical Task")
    
    feature_type_id = bt_tree_name_and_id.get("Feature")
    component_type_id = bt_tree_name_and_id.get("Component")
    capability_type_id = bt_tree_name_and_id.get("Capability")
    
    include_types = [bug_type_id, story_type_id, tech_task_type_id]
    efcc_include_types = [epic_type_id, feature_type_id, component_type_id, capability_type_id] # meaning Epic, Feature, Component, Capability
    efcc_backlog_items = Backlog.objects.filter(pro_id=project.id, type__in=efcc_include_types, active=True)

    return {
        'organization': organization,
        'org_id': org_id,
        'project': project,
        'pro_id': project.id,
        'backlog_types': backlog_types,
        'backlog_types_count': backlog_types_count,
        'include_types': include_types,
        'efcc_include_types': efcc_include_types,
        'efcc_backlog_items': efcc_backlog_items,
        'story_type_id': story_type_id,
        'bug_type_id': bug_type_id,
        'tech_task_type_id': tech_task_type_id,
        'feature_type_id': feature_type_id,
        'component_type_id': component_type_id,
        'capability_type_id': capability_type_id,
        'epic_type_id': epic_type_id,
        'project_backlog_root_node': project_backlog_root_node,
    }

@login_required
def _COMMON_for_kanban(request, project_id):
    user = request.user
    project = Project.objects.get(id=project_id, active=True)
    org_id = project.org.id
    organization = project.org
    # Backlog types
    pbst_name = f"{project.id}_PROJECT_TREE"
    project_backlog_type, created = BacklogType.objects.get_or_create(pro=project, name=pbst_name)
    config = PROJECT_WBS_TREE_CONFIG
    backlog_type_node = create_or_update_tree_from_config(config, model_name="app_organization.BacklogType", parent=project_backlog_type, project=project)
    bt_tree_name_and_id = get_tree_name_id(backlog_type_node)
    epic_type_id = bt_tree_name_and_id.get("Epic")
    epic_type_node = BacklogType.objects.get(id=epic_type_id)
    epic_type_children = epic_type_node.get_active_children()
    backlog_types = epic_type_children
    backlog_types_count = backlog_types.count()
    
    bug_type_id = bt_tree_name_and_id.get("Bug")
    story_type_id = bt_tree_name_and_id.get("User Story")
    tech_task_type_id = bt_tree_name_and_id.get("Technical Task")
    
    feature_type_id = bt_tree_name_and_id.get("Feature")
    component_type_id = bt_tree_name_and_id.get("Component")
    capability_type_id = bt_tree_name_and_id.get("Capability")
    
    include_types = [bug_type_id, story_type_id, tech_task_type_id]
    efcc_include_types = [epic_type_id, feature_type_id, component_type_id, capability_type_id] # meaning Epic, Feature, Component, Capability
    efcc_backlog_items = Backlog.objects.filter(pro_id=project.id, type__in=efcc_include_types, active=True)
    efcc_backlog_items_swimlane = Backlog.objects.filter(pro_id=project.id, active=True)
    get_swimlane_id = request.GET.get('swimlane_id')  if request.GET.get('swimlane_id') else '-1'
    swimlane_flag = False
    project_iteration_flag = False
    project_release_iteration_board = None
    efcc_backlog_with_no_epic = None 

    # Step1: Check whether default board is there
    # Step2: Check whether Project - Release - Iteration board is there
    # Step3: Check whether other boards are there
    # Step4: Check which one is the selected board as default board, if no selected default board as default
    # Step5: Select the Project Board
    # Step6: Select the Project Board States or columns
    # Step7: Collect the Backlog items
    # Step8: Collect the state/column items
    # Step9: Check the swimlane
    # Step10: Set the flags

    project_board = None
    default_project_board = None
    release_iteration_project_board = None
    selected_project_board = None

    # Step1: Check whether default board is there
    DEFAULT_BOARD_NAME = 'Default Board'
    PROJECT_RELEASE_ITERATION_BOARD_NAME = None
    default_project_board, created = ProjectBoard.objects.get_or_create(
        project=project,
        name=DEFAULT_BOARD_NAME,
        defaults={'author': user}
    )
    # Step2: Check whether Project - Release - Iteration board is there
    project_iteration = project.project_iteration
    project_release = project.project_release
    current_release = None
    current_iteration = None
    if project.project_release and project.project_iteration:
        project_iteration_flag = True
        details = get_project_release_and_iteration_details(project.id)
        current_release = details.get('current_release')
        current_iteration = details.get('current_iteration')
        next_iteration = details.get('next_iteration')
        # Check the Project Release_Iteration Board exists, if not create it
        PROJECT_RELEASE_ITERATION_BOARD_NAME = f"{project.name}__{project_release}__{project_iteration}__PrjRelItrBoard"
        release_iteration_project_board, created = ProjectBoard.objects.get_or_create(
            project=project,
            name=PROJECT_RELEASE_ITERATION_BOARD_NAME,
            org_release=current_release,
            org_iteration=current_iteration,
            defaults={'author': user}
        )
    # Step3: Check whether other boards are there
    all_project_boards = ProjectBoard.objects.filter(
        project=project, 
        active=True
    ).exclude(name=DEFAULT_BOARD_NAME).exclude(name=PROJECT_RELEASE_ITERATION_BOARD_NAME)
    # Step4: Check which one is the selected board as default board, if no selected default board as default
    selected_project_board = ProjectBoard.objects.filter(
        project=project, 
        default_board=True, 
        active=True
    ).first()

    if not selected_project_board:
        # If no board is marked as default, set the Default Board as the default
        default_project_board.default_board = True
        default_project_board.save()
        selected_project_board = default_project_board  # Assign default board as selected project_board
    # Step4.1: Add the default columns if there are no columns
    # Ensure the default columns exist or create them
    DEFAULT_BOARD_COLUMNS = GLOBAL_DEFAULT_BOARD_COLUMNS
    # SOMETHING LIKE THIS ['ToDo', 'WIP', 'Done']
    #ProjectBoardState.objects.all().delete()
    backlog_state = None  # To store the "Backlog" state reference
    COLUMN_TYPE_MAPPING = {
        'ToDo': 'ToDo',
        'WIP': 'WIP',
        'Done': 'Done'
    }
    existing_column_count = ProjectBoardState.objects.filter(board=selected_project_board).count()
    if existing_column_count == 0:
        for position, column_name in enumerate(DEFAULT_BOARD_COLUMNS):
            
            state, _ = ProjectBoardState.objects.get_or_create(
                board=selected_project_board,
                name=column_name,
                defaults={'author': user, 'wip_limit': 3, 'apply_wip_limit': True if column_name == 'WIP' else False, 'column_type': COLUMN_TYPE_MAPPING[column_name]}
            )
            if column_name == 'Backlog':
                backlog_state = state
    # Step5: Select the Project Board
    if selected_project_board:
        project_board = selected_project_board
    else:
        project_board = default_project_board    
    # Step6: Select the Project Board States or columns
    if project_board:
        project_board_states = ProjectBoardState.objects.filter(board=project_board, active=True)
    # Step7: Collect the Backlog items
    if project.project_details.template.name == 'Scrum':
        actual_project_backlog_items = Backlog.objects.filter(
                pro_id=project.id,
                type__in=backlog_types,
                active=True,
                iteration=current_iteration,
                release=current_release,
            ).exclude(
                id__in=ProjectBoardCard.objects.filter(
                    board=project_board,
                    state__isnull=False  # Exclude items where state.id is NOT NULL (moved to other states)
                ).values_list('backlog_id', flat=True)
            ).order_by('position', '-created_at')   
    else:
        print(f">>> === project.project_details.template.name: {project.project_details.template.name} === <<<")
        actual_project_backlog_items = Backlog.objects.filter(
                pro_id=project.id,
                type__in=backlog_types,
                active=True,
                
            ).exclude(
                id__in=ProjectBoardCard.objects.filter(
                    board=project_board,
                    state__isnull=False  # Exclude items where state.id is NOT NULL (moved to other states)
                ).values_list('backlog_id', flat=True)
            ).order_by('position', '-created_at')   
        print(f">>> === actual_project_backlog_items: {actual_project_backlog_items.count()} === <<<")
    reference_backlog_items =  Backlog.objects.filter(
            pro_id=project.id,
            type__in=backlog_types,
            active=True,       
        ).order_by('position', '-created_at')  
    # Step8: Collect the state/column items
    # Fetch the project backlog items state
    if project_board:
        find_and_fix_duplicate_board_cards(project_board.id)
    
    # Database-agnostic approach to get unique cards per state
    state_items = {}
    state_items_list = []
    
    for state in project_board.board_states.filter(active=True):
        # Get all cards for this state
        all_cards = ProjectBoardCard.objects.filter(
            board=project_board,
            state=state,
            active=True,
            backlog__type__in=backlog_types,
            backlog__active=True
        ).select_related('backlog').order_by('-created_at')
        
        # Deduplicate in Python by backlog_id (keep most recent card for each backlog item)
        seen_backlog_ids = set()
        unique_cards = []
        for card in all_cards:
            if card.backlog_id not in seen_backlog_ids:
                unique_cards.append(card)
                seen_backlog_ids.add(card.backlog_id)
        
        # Sort by position for proper display order
        unique_cards.sort(key=lambda x: (x.position or 0, -x.created_at.timestamp()))
        
        state_items[state.id] = unique_cards
        state_items_list.append((state, unique_cards))
    
    # IT HAS TO BE ITERATED -- see REFERENCE_01
    # Step9: Check the swimlane
    board_swimlanes = ProjectBoardSwimLane.objects.filter(board=project_board, active=True)
    board_swimlanes_count = board_swimlanes.count()    
    #print(f">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> BOARD SWIMLANES {board_swimlanes} {board_swimlanes_count}")
    # Step10: Set the flags
    FLAG_board_swimlane_exists = board_swimlanes_count > 0
    if FLAG_board_swimlane_exists:
        efcc_backlog_items_swimlane = Backlog.objects.filter(
            pro_id=project.id,
            type__in=efcc_include_types,
            active=True
        )
        efcc_backlog_with_no_epic = Backlog.objects.filter(
            pro_id=project.id,
            active=True
        ).exclude(type__in=efcc_include_types)

    # Step10.1: Preprocess
    # Preprocess state_items to create a backlog-to-state mapping
    # Create a mapping of backlog item ID to its state ID from ProjectBoardCard
    # Create a dictionary mapping backlog_id to a set of state_ids
    # Create a dictionary mapping backlog_id to its cards in different states
    backlog_state_mapping = {}

    # Query all active ProjectBoardCards related to the board
    board_cards = ProjectBoardCard.objects.filter(board=project_board, active=True).select_related('backlog', 'state')

    # Build the mapping
    for card in board_cards:
        if card.backlog_id not in backlog_state_mapping:
            backlog_state_mapping[card.backlog_id] = []  # Store a list of card-state pairs

        backlog_state_mapping[card.backlog_id].append({
            "state_id": card.state_id,  # State ID where this card exists
            "state_name": card.state,  # State Name
            "card_id": card.id,  # Card ID
            "card_name": str(card),  # Card Name
            "substate": card.substate,  # Substate (Doing/Done)
            "priority": card.backlog.priority if card.backlog else None,  # Priority of the backlog item
        })



    print(f"SWIMLANES>>>>>>>>>>>>>>>>>>>>>>>>>>>>exists>>>>>>>>>>>>> {efcc_backlog_items_swimlane}")

    print(f">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> BACKLOG ITEMS {actual_project_backlog_items} ")
    count_of_actual_backlog_items = actual_project_backlog_items.count()
    print(f">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> BACKLOG ITEMS COUNT {count_of_actual_backlog_items} ")
    project_type = project.project_details.template.name
    
    context = {
        'organization': organization,
        'org_id': org_id,
        'project': project,
        'pro_id': project.id,
        'project_board': selected_project_board,
        'project_board_states': project_board_states,
        'backlog_items': actual_project_backlog_items,
        'reference_backlog_items': reference_backlog_items,
        'todo_items': state_items.get('ToDo', []),
        'in_progress_items': state_items.get('WIP', []),
        'done_items': state_items.get('Done', []),
        'state_items': state_items,
        'state_items_list': state_items_list,
        'page_title': f'Project Board: {project.name}',
        'efcc_backlog_items': efcc_backlog_items,
        'efcc_backlog_with_no_epic': efcc_backlog_with_no_epic,
        'swimlane_flag': swimlane_flag,
        'efcc_backlog_items_swimlane': efcc_backlog_items_swimlane,
        'backlog_state_mapping': backlog_state_mapping,
        'project_iteration_flag': project_iteration_flag,
        'current_release': current_release,
        'current_iteration': current_iteration,
        'project_type': project_type,
        'FLAG_board_swimlane_exists': FLAG_board_swimlane_exists,
        #'chart_data': chart_data,
    }
     
    print(f">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> {project_type}")
    return context


@login_required
def view_project_tree_board_custom(request, project_id):
    context = _COMMON_for_kanban(request, project_id)
    project_type = context.get('project_type')
    context["page"] = "custom"
    if project_type == 'Kanban':
        template_file = f"{app_name}/{module_path}/project/view_project_tree_board_custom.html"
    else:
        template_file = f"{app_name}/{module_path}/project/view_project_tree_board.html"
    return render(request, template_file, context)

@login_required
def view_project_tree_board_smart_kanban(request, project_id):
    context = _COMMON_for_kanban(request, project_id)
    context["page"] = "smart"
    project_type = context.get('project_type')
    if project_type in ['Kanban', 'Scrum', 'Agile']:
        template_file = f"{app_name}/{module_path}/project/view_project_tree_board_smart_kanban.html"
    else:
        template_file = f"{app_name}/{module_path}/project/view_project_tree_board.html"
    return render(request, template_file, context)


# REFERENCE_01
# {% for state, items in state_items_list %}
#     <td class="kanban-column kanban-column-with-cards">
#         <h4>{{ state.name }}</h4> <!-- Display State Name -->
#         {% for item in items %}
#             <div class="kanban-card">
#                 {{ item }}
#             </div>
#         {% empty %}
#             <div class="kanban-card-placeholder">No Cards</div>
#         {% endfor %}
#     </td>
# {% endfor %}
@login_required
def _GET_backlog_details(request, project_id):
    user = request.user
    project = Project.objects.get(id=project_id, active=True)
    org_id = project.org.id
    organization = project.org
    # Backlog types
    pbst_name = f"{project.id}_PROJECT_TREE"
    project_backlog_type, created = BacklogType.objects.get_or_create(pro=project, name=pbst_name)
    config = PROJECT_WBS_TREE_CONFIG
    backlog_type_node = create_or_update_tree_from_config(config, model_name="app_organization.BacklogType", parent=project_backlog_type, project=project)
    bt_tree_name_and_id = get_tree_name_id(backlog_type_node)
    epic_type_id = bt_tree_name_and_id.get("Epic")
    epic_type_node = BacklogType.objects.get(id=epic_type_id)
    epic_type_children = epic_type_node.get_active_children()
    backlog_types = epic_type_children
    backlog_types_count = backlog_types.count()
    
    bug_type_id = bt_tree_name_and_id.get("Bug")
    story_type_id = bt_tree_name_and_id.get("User Story")
    tech_task_type_id = bt_tree_name_and_id.get("Technical Task")
    
    feature_type_id = bt_tree_name_and_id.get("Feature")
    component_type_id = bt_tree_name_and_id.get("Component")
    capability_type_id = bt_tree_name_and_id.get("Capability")
    
    include_types = [bug_type_id, story_type_id, tech_task_type_id]
    efcc_include_types = [epic_type_id, feature_type_id, component_type_id, capability_type_id] # meaning Epic, Feature, Component, Capability
    
    return {
        'bt_tree_name_and_id': bt_tree_name_and_id,
        'epic_type_id': epic_type_id,
        'epic_type_node': epic_type_node,
        'epic_type_children': epic_type_children,
        'backlog_types': backlog_types,
        'backlog_types_count': backlog_types_count,
        'bug_type_id': bug_type_id,
        'story_type_id': story_type_id,
        'tech_task_type_id': tech_task_type_id,
        'feature_type_id': feature_type_id,
        'component_type_id': component_type_id,
        'capability_type_id': capability_type_id,
        'include_types': include_types,
        'efcc_include_types': efcc_include_types,
    }


from app_organization.mod_backlog.views_project_tree import create_or_update_tree_from_config, get_tree_name_id
@login_required
def _UTILS_for_project_backlog(request, project_id):
    user = request.user
    project = Project.objects.get(id=project_id, active=True)
    org_id = project.org.id
    organization = project.org
    # Backlog types
    pbst_name = f"{project.id}_PROJECT_TREE"
    project_backlog_type, created = BacklogType.objects.get_or_create(pro=project, name=pbst_name)
    config = PROJECT_WBS_TREE_CONFIG
    backlog_type_node = create_or_update_tree_from_config(config, model_name="app_organization.BacklogType", parent=project_backlog_type, project=project)
    bt_tree_name_and_id = get_tree_name_id(backlog_type_node)
    epic_type_id = bt_tree_name_and_id.get("Epic")
    epic_type_node = BacklogType.objects.get(id=epic_type_id)
    epic_type_children = epic_type_node.get_active_children()
    backlog_types = epic_type_children
    backlog_types_count = backlog_types.count()
    
    bug_type_id = bt_tree_name_and_id.get("Bug")
    story_type_id = bt_tree_name_and_id.get("User Story")
    tech_task_type_id = bt_tree_name_and_id.get("Technical Task")
    
    feature_type_id = bt_tree_name_and_id.get("Feature")
    component_type_id = bt_tree_name_and_id.get("Component")
    capability_type_id = bt_tree_name_and_id.get("Capability")
    
    include_types = [bug_type_id, story_type_id, tech_task_type_id]
    efcc_include_types = [epic_type_id, feature_type_id, component_type_id, capability_type_id] # meaning Epic, Feature, Component, Capability
    efcc_backlog_items = Backlog.objects.filter(pro_id=project.id, type__in=efcc_include_types, active=True)
    efcc_backlog_items_swimlane = Backlog.objects.filter(pro_id=project.id, active=True)
    get_swimlane_id = request.GET.get('swimlane_id')  if request.GET.get('swimlane_id') else '-1'
    swimlane_flag = False
    project_iteration_flag = False
    project_release_iteration_board = None
    efcc_backlog_with_no_epic = None 

    # Step1: Check whether default board is there
    # Step2: Check whether Project - Release - Iteration board is there
    # Step3: Check whether other boards are there
    # Step4: Check which one is the selected board as default board, if no selected default board as default
    # Step5: Select the Project Board
    # Step6: Select the Project Board States or columns
    # Step7: Collect the Backlog items
    # Step8: Collect the state/column items
    # Step9: Check the swimlane
    # Step10: Set the flags

    project_board = None
    default_project_board = None
    release_iteration_project_board = None
    selected_project_board = None

    # Step1: Check whether default board is there
    DEFAULT_BOARD_NAME = 'Default Board'
    PROJECT_RELEASE_ITERATION_BOARD_NAME = None
    default_project_board, created = ProjectBoard.objects.get_or_create(
        project=project,
        name=DEFAULT_BOARD_NAME,
        defaults={'author': user}
    )
    # Step2: Check whether Project - Release - Iteration board is there
    project_iteration = project.project_iteration
    project_release = project.project_release
    current_release = None
    current_iteration = None
    if project.project_release and project.project_iteration:
        project_iteration_flag = True
        details = get_project_release_and_iteration_details(project.id)
        current_release = details.get('current_release')
        current_iteration = details.get('current_iteration')
        next_iteration = details.get('next_iteration')
        # Check the Project Release_Iteration Board exists, if not create it
        PROJECT_RELEASE_ITERATION_BOARD_NAME = f"{project.name}__{project_release}__{project_iteration}__PrjRelItrBoard"
        release_iteration_project_board, created = ProjectBoard.objects.get_or_create(
            project=project,
            name=PROJECT_RELEASE_ITERATION_BOARD_NAME,
            org_release=current_release,
            org_iteration=current_iteration,
            defaults={'author': user}
        )
    # Step3: Check whether other boards are there
    all_project_boards = ProjectBoard.objects.filter(
        project=project, 
        active=True
    ).exclude(name=DEFAULT_BOARD_NAME).exclude(name=PROJECT_RELEASE_ITERATION_BOARD_NAME)
    # Step4: Check which one is the selected board as default board, if no selected default board as default
    selected_project_board = ProjectBoard.objects.filter(
        project=project, 
        default_board=True, 
        active=True
    ).first()

    if not selected_project_board:
        # If no board is marked as default, set the Default Board as the default
        default_project_board.default_board = True
        default_project_board.save()
        selected_project_board = default_project_board  # Assign default board as selected project_board
    # Step4.1: Add the default columns if there are no columns
    # Ensure the default columns exist or create them
    DEFAULT_BOARD_COLUMNS = GLOBAL_DEFAULT_BOARD_COLUMNS
    # SOMETHING LIKE THIS ['ToDo', 'WIP', 'Done']
    #ProjectBoardState.objects.all().delete()
    backlog_state = None  # To store the "Backlog" state reference
    COLUMN_TYPE_MAPPING = GLOBAL_COLUMN_TYPE_MAPPING
    existing_column_count = ProjectBoardState.objects.filter(board=selected_project_board).count()
    if existing_column_count == 0:
        for position, column_name in enumerate(DEFAULT_BOARD_COLUMNS):
            
            state, _ = ProjectBoardState.objects.get_or_create(
                board=selected_project_board,
                name=column_name,
                defaults={'author': user, 'wip_limit': 5, 'apply_wip_limit': True if column_name == 'WIP' else False, 'column_type': COLUMN_TYPE_MAPPING[column_name]}
            )
            if column_name == 'Backlog':
                backlog_state = state
    # Step5: Select the Project Board
    if selected_project_board:
        project_board = selected_project_board
    else:
        project_board = default_project_board    
    # Step6: Select the Project Board States or columns
    if project_board:
        project_board_states = ProjectBoardState.objects.filter(board=project_board, active=True)
    # Step7: Collect the Backlog items
    actual_project_backlog_items = Backlog.objects.filter(
            pro_id=project.id,
            type__in=backlog_types,
            active=True,
            iteration=current_iteration,
            release=current_release,
        ).exclude(
            id__in=ProjectBoardCard.objects.filter(
                board=project_board,
                state__isnull=False  # Exclude items where state.id is NOT NULL (moved to other states)
            ).values_list('backlog_id', flat=True)
        ).order_by('position', '-created_at')   
    reference_backlog_items =  Backlog.objects.filter(
            pro_id=project.id,
            type__in=backlog_types,
            active=True,
        ).order_by('position', '-created_at')  
    
    return {
        'organization': organization,
        'org_id': org_id,
        'project': project,
        'pro_id': project.id,
        'project_board': selected_project_board,
        'project_board_states': project_board_states,
        'backlog_items': actual_project_backlog_items,
        'reference_backlog_items': reference_backlog_items,
        
    }