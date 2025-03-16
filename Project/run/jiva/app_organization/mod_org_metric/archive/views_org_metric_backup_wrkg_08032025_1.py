
from app_organization.mod_app.all_view_imports import *
from app_organization.mod_org_metric.models_org_metric import *
from app_organization.mod_org_metric.forms_org_metric import *

from app_organization.mod_organization.models_organization import *
from app_organization.mod_project.models_project import *

from app_common.mod_app.all_view_imports import *
from app_common.mod_common.models_common import *

from app_jivapms.mod_web.views_web import *
from app_common.mod_app.all_view_imports import *

app_name = 'app_organization'
app_version = 'v1'

module_name = 'org_metrics'
module_path = f'mod_org_metric'

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
def list_org_metrics(request, org_id):
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
    project = None
    project_id = None
    if 'project_id' in request.GET:
        project_id = request.GET.get('project_id')
        project = get_object_or_404(Project, pk=project_id, active=True, **viewable_dict)
    search_query = request.GET.get('search', '')
    if search_query:
        tobjects = OrgMetric.objects.filter(name__icontains=search_query, 
                                            org_id=org_id, **viewable_dict).order_by('position')
    else:
        tobjects = OrgMetric.objects.filter(active=True, org_id=org_id).order_by('position')
        deleted = OrgMetric.objects.filter(active=False, deleted=False,
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
                    object = get_object_or_404(OrgMetric, pk=item, active=True, **viewable_dict)
                    object.active = False
                    object.save()
                    
                elif bulk_operation == 'bulk_done':
                    object = get_object_or_404(OrgMetric, pk=item, active=True, **viewable_dict)
                    object.done = True
                    object.save()
                    
                elif bulk_operation == 'bulk_not_done':
                    object = get_object_or_404(OrgMetric, pk=item, active=True, **viewable_dict)
                    object.done = False
                    object.save()
                    
                elif bulk_operation == 'bulk_blocked':  # Correct the operation check here
                    object = get_object_or_404(OrgMetric, pk=item, active=True, **viewable_dict)
                    object.blocked = True
                    object.save()
                    
                else:
                    redirect('list_org_metrics', org_id=org_id)
            return redirect('list_org_metrics', org_id=org_id)
    
    # send outputs info, template,
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'list_org_metrics',
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
        'page_title': f'Org_metric List',
        
        'project': project,
        'project_id': project_id,
        'pro_id': project_id,
    }       
    template_file = f"{app_name}/{module_path}/list_org_metrics.html"
    return render(request, template_file, context)





# ============================================================= #
@login_required
def list_deleted_org_metrics(request, org_id):
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
    project = None
    project_id = None
    if 'project_id' in request.GET:
        project_id = request.GET.get('project_id')
        project = get_object_or_404(Project, pk=project_id, active=True, **viewable_dict)
    search_query = request.GET.get('search', '')
    if search_query:
        tobjects = OrgMetric.objects.filter(name__icontains=search_query, 
                                            active=False, deleted=False,
                                            org_id=org_id, **viewable_dict).order_by('position')
    else:
        tobjects = OrgMetric.objects.filter(active=False, deleted=False, org_id=org_id,
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
                        object = get_object_or_404(OrgMetric, pk=item, active=False, **viewable_dict)
                        object.active = True
                        object.save()         
                    elif bulk_operation == 'bulk_erase':
                        object = get_object_or_404(OrgMetric, pk=item, active=False, **viewable_dict)
                        object.active = False  
                        object.deleted = True             
                        object.save()    
                    else:
                        redirect('list_org_metrics', org_id=org_id)
                redirect('list_org_metrics', org_id=org_id)
    
    # send outputs info, template,
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'list_deleted_org_metrics',
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
        'page_title': f'Org_metric List',
        
        'project': project,
        'project_id': project_id,
        'pro_id': project_id,
    }       
    template_file = f"{app_name}/{module_path}/list_deleted_org_metrics.html"
    return render(request, template_file, context)



# Create View
@login_required
def create_org_metric(request, org_id):
    user = request.user
    organization = Organization.objects.get(id=org_id, active=True, 
                                                **first_viewable_dict)
    project = None
    project_id = None
    if 'project_id' in request.GET:
        project_id = request.GET.get('project_id')
        project = get_object_or_404(Project, pk=project_id, active=True, **viewable_dict)
    if request.method == 'POST':
        form = OrgMetricForm(request.POST)
        if form.is_valid():
            form.instance.author = user
            form.instance.org_id = org_id
            form.save()
        else:
            print(f">>> === form.errors: {form.errors} === <<<")
        return redirect('list_org_metrics', org_id=org_id)
    else:
        form = OrgMetricForm()

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'create_org_metric',
        'organization': organization,
        'org_id': org_id,
        
        'module_path': module_path,
        'form': form,
        'page_title': f'Create Org Metric',
        
        'project': project,
        'project_id': project_id,
        'pro_id': project_id,
    }
    template_file = f"{app_name}/{module_path}/create_org_metric.html"
    return render(request, template_file, context)




# Edit
@login_required
def edit_org_metric(request, org_id, org_metric_id):
    user = request.user
    organization = Organization.objects.get(id=org_id, active=True, 
                                                **first_viewable_dict)
    project = None
    project_id = None
    if 'project_id' in request.GET:
        project_id = request.GET.get('project_id')
        project = get_object_or_404(Project, pk=project_id, active=True, **viewable_dict)
    object = get_object_or_404(OrgMetric, pk=org_metric_id, active=True,**viewable_dict)
    if request.method == 'POST':
        form = OrgMetricForm(request.POST, instance=object)
        if form.is_valid():
            form.instance.author = user
            form.instance.org_id = org_id
            form.save()
        else:
            print(f">>> === form.errors: {form.errors} === <<<")
        return redirect('list_org_metrics', org_id=org_id)
    else:
        form = OrgMetricForm(instance=object)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'edit_org_metric',
        'organization': organization,
        'org_id': org_id,
        
        'module_path': module_path,
        'form': form,
        'object': object,
        'page_title': f'Edit Org Metric',
        
        'project': project,
        'project_id': project_id,
        'pro_id': project_id,
    }
    template_file = f"{app_name}/{module_path}/edit_org_metric.html"
    return render(request, template_file, context)



@login_required
def delete_org_metric(request, org_id, org_metric_id):
    user = request.user
    organization = Organization.objects.get(id=org_id, active=True, 
                                                **first_viewable_dict)
    project = None
    project_id = None
    if 'project_id' in request.GET:
        project_id = request.GET.get('project_id')
        project = get_object_or_404(Project, pk=project_id, active=True, **viewable_dict)
    object = get_object_or_404(OrgMetric, pk=org_metric_id, active=True,**viewable_dict)
    if request.method == 'POST':
        object.active = False
        object.save()
        return redirect('list_org_metrics', org_id=org_id)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'delete_org_metric',
        'organization': organization,
        'org_id': org_id,
        
        'module_path': module_path,        
        'object': object,
        'page_title': f'Delete Org Metric',
        
        'project': project,
        'project_id': project_id,
        'pro_id': project_id,
    }
    template_file = f"{app_name}/{module_path}/delete_org_metric.html"
    return render(request, template_file, context)


@login_required
def permanent_deletion_org_metric(request, org_id, org_metric_id):
    user = request.user
    organization = Organization.objects.get(id=org_id, active=True, 
                                                **first_viewable_dict)
    project = None
    project_id = None
    if 'project_id' in request.GET:
        project_id = request.GET.get('project_id')
        project = get_object_or_404(Project, pk=project_id, active=True, **viewable_dict)
    object = get_object_or_404(OrgMetric, pk=org_metric_id, active=False, deleted=False, **viewable_dict)
    if request.method == 'POST':
        object.active = False
        object.deleted = True
        object.save()
        return redirect('list_org_metrics', org_id=org_id)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'permanent_deletion_org_metric',
        'organization': organization,
        'org_id': org_id,
        
        'module_path': module_path,        
        'object': object,
        'page_title': f'Permanent Deletion Org Metric',
        
        'project': project,
        'project_id': project_id,
        'pro_id': project_id,
    }
    template_file = f"{app_name}/{module_path}/permanent_deletion_org_metric.html"
    return render(request, template_file, context)


@login_required
def restore_org_metric(request,  org_id, org_metric_id):
    user = request.user
    object = get_object_or_404(OrgMetric, pk=org_metric_id, active=False,**viewable_dict)
    object.active = True
    object.save()
    return redirect('list_org_metrics', org_id=org_id)
   


@login_required
def view_org_metric(request, org_id, org_metric_id):
    user = request.user
    organization = Organization.objects.get(id=org_id, active=True, 
                                                **first_viewable_dict)
    project = None
    project_id = None
    if 'project_id' in request.GET:
        project_id = request.GET.get('project_id')
        project = get_object_or_404(Project, pk=project_id, active=True, **viewable_dict)
    object = get_object_or_404(OrgMetric, pk=org_metric_id, active=True,**viewable_dict)    

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'view_org_metric',
        'organization': organization,
        'org_id': org_id,
        
        'module_path': module_path,
        'object': object,
        'page_title': f'View Org Metric',
        
        'project': project,
        'project_id': project_id,
        'pro_id': project_id,
    }
    template_file = f"{app_name}/{module_path}/view_org_metric.html"
    return render(request, template_file, context)


from app_organization.mod_backlog.models_backlog import *
from app_organization.mod_backlog.views_project_tree import jivapms_mod_backlog_helper_get_backlog_details
from django.db.models.functions import TruncDate
from app_organization.mod_org_board.models_org_board import *


@login_required
def view_project_metrics(request, project_id):
    from datetime import timedelta, date
    import random
    project = get_object_or_404(Project, pk=project_id, active=True)
    organization = project.org
    org_id = organization.id
    
    # Prepare context for rendering template
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'view_project_metrics',
        'organization': project.org,
        'org_id': org_id,
        'project': project,
        'project_id': project_id,
        'pro_id': project_id,

        'selected_tab': 'project_metrics',
    }

    # Render template
    template_file = f"{app_name}/{module_path}/project_metrics/view_project_metrics.html"
    return render(request, template_file, context)




@login_required
def view_project_metrics_backlog_tab(request, project_id):
    from datetime import timedelta, date
    import random
    project = get_object_or_404(Project, pk=project_id, active=True)
    organization = project.org
    org_id = organization.id
    
    # Prepare context for rendering template
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'view_project_metrics_backlog_tab',
        'organization': project.org,
        'org_id': org_id,
        'project': project,
        'project_id': project_id,
        'pro_id': project_id,

        'selected_tab': 'backlog',
    }

    # Render template
    template_file = f"{app_name}/{module_path}/project_metrics/view_project_metrics_backlog_tab.html"
    return render(request, template_file, context)
####################################################################################
#
# Generate Burndown Chart Data
#
#
####################################################################################
def generate_minute_based_burndown(current_iteration, project, total_minutes, total_story_points):
    burndown_data = []
    current_datetime = now()

    # Ensure the iteration start datetime is localized to Asia/Kolkata
    tz = pytz.timezone('Asia/Kolkata')
    iteration_start_datetime = current_iteration.iteration_start_date.astimezone(tz)

    for minute_offset in range(total_minutes + 1):  # Include the last minute
        itr_datetime = iteration_start_datetime + timedelta(minutes=minute_offset)
        # Total backlog items size - datewise 
        datewise_backlog_items = Backlog.objects.filter(
            pro=project, 
            active=True, 
            iteration=current_iteration,
        )
        datewise_backlog_items_total = datewise_backlog_items.aggregate(total=Sum('size'))['total'] or 0
        # Normalize `done_at` field to the same timezone as `itr_datetime`
        backlog_items = Backlog.objects.filter(
            pro=project,
            active=True,
            iteration=current_iteration,
            done_at__lte=itr_datetime.astimezone(pytz.UTC)  # Convert `itr_datetime` to UTC
        )
        backlog_count = backlog_items.count()
        for bi in backlog_items:
            logger.debug(
                f">>> === backlog_item: {bi} DONE: {bi.done_at.astimezone(tz)} | "
                f"ITR: {itr_datetime} === <<<"
            )

        # Calculate remaining story points
        done_story_points_till_now = backlog_items.aggregate(total=Sum('size'))['total'] or 0
        remaining_story_points = total_story_points - done_story_points_till_now

        logger.debug(
            f">>> === MINUTE-BREAKDOWN: itr_datetime: {itr_datetime} | "
            f"TOTAL STORY POINTS: {total_story_points} | "
            f"DONE POINTS: {done_story_points_till_now} | "
            f"Remaining: {remaining_story_points} === <<<"
        )

        # Handle future datetime
        if itr_datetime > current_datetime:
            remaining_story_points = ''

        # Format datetime without timezone
        formatted_datetime = itr_datetime.strftime('%Y-%m-%dT%H:%M:%S')
        burndown_data.append({
            'datetime': formatted_datetime,
            'remaining_story_points': remaining_story_points,
            'backlog_count': backlog_count,
            'datewise_backlog_items_total': datewise_backlog_items_total,
        })
        logger.debug(f">>> === MINUTE BREAKDOWN: burndown_data: {burndown_data} === <<<")
    return burndown_data


@login_required
def view_project_metrics_iteration_tab(request, project_id):
    # Fetch user, project, and organization details
    user = request.user
    project = get_object_or_404(Project, pk=project_id, active=True)
    organization = project.org
    org_id = organization.id
    iteration_backlog_items = None
    logger.debug(f">>> === project: {project} {project.project_release} === <<<")
 
    
    # Project Release and Iteration
    current_release = None
    current_iteration = None
    current_datetime = now().replace(microsecond=0)
    release_mismatch_flag = False
    iteration_mismatch_flag = False
    # Step 1: Check Project Release
    if project.project_release:
       # Filter by date and time separately
        current_release = OrgRelease.objects.filter(
            id=project.project_release.id,
            release_start_date__lte=current_datetime,
            release_end_date__gte=current_datetime,            
        ).order_by("-release_start_date").first()      
        if current_release:
            logger.debug(f">>> === current_release: {current_release} {current_release.release_start_date} === <<<")
        else:
            release_mismatch_flag = True
    # Step 2: Check Project Iteration
    total_story_points = 0
    todo_story_points = 0
    wip_story_points = 0
    done_story_points = 0
    if project.project_iteration:
        # Use datetime comparison for both start and end dates
        current_datetime = now().replace(microsecond=0)
        details = get_project_release_and_iteration_details(project.id)
        current_release = details['current_release']
        current_iteration = details['current_iteration']
        next_iteration = details['next_iteration']       
        

        if current_iteration:
            logger.debug(f">>> === current_iteration: {current_iteration} {current_iteration.iteration_start_date} === <<<")

            # Filter backlog items for the current iteration
            iteration_backlog_items = Backlog.objects.filter(
                pro=project, 
                active=True, 
                deleted=False, 
                iteration=current_iteration
            )
            logger.debug(f">>> === iteration_backlog_items: {iteration_backlog_items} === <<<")

            # Calculate total story points
            total_story_points = iteration_backlog_items.aggregate(total=Sum('size'))['total'] or 0
            # CHECK THE PROJECT BOARD CARD details MODEL
            project_board = ProjectBoard.objects.filter(project=project, org_release=current_release, org_iteration=current_iteration, active=True).first()
            logger.debug(f">>> === project_board: {project_board} === <<<")
            
            
            # # Calculate story points by status
            # todo_story_points = iteration_backlog_items.filter(status="ToDo").aggregate(total=Sum('size'))['total'] or 0
            # wip_story_points = iteration_backlog_items.filter(status="WIP").aggregate(total=Sum('size'))['total'] or 0
            # done_story_points = iteration_backlog_items.filter(status="Done").aggregate(total=Sum('size'))['total'] or 0
            # Fetch the states for each status from ProjectBoardCardState
            # Fetch the states for ToDo, WIP, and Done from ProjectBoardState
           
            # Fetch states by their names
            todo_states = ProjectBoardState.objects.filter(name="ToDo", active=True).values_list('id', flat=True)
            wip_states = ProjectBoardState.objects.filter(name="WIP", active=True).values_list('id', flat=True)
            done_states = ProjectBoardState.objects.filter(name="Done", active=True).values_list('id', flat=True)

            logger.debug(f"ToDo States: {list(todo_states)}")
            logger.debug(f"WIP States: {list(wip_states)}")
            logger.debug(f"Done States: {list(done_states)}")

            # Fetch ProjectBoardCards linked to these states
            todo_cards_objects = ProjectBoardCard.objects.filter(board=project_board, state_id__in=todo_states, active=True)
            wip_cards_objects = ProjectBoardCard.objects.filter(board=project_board, state_id__in=wip_states, active=True)
            done_cards_objects = ProjectBoardCard.objects.filter(board=project_board, state_id__in=done_states, active=True)

            # Log card counts and details
            logger.debug(f"ToDo Cards Count: {todo_cards_objects.count()}")
            logger.debug(f"WIP Cards Count: {wip_cards_objects.count()}")
            logger.debug(f"Done Cards Count: {done_cards_objects.count()}")

            # Extract backlog IDs from cards
            todo_cards = todo_cards_objects.values_list('backlog_id', flat=True)
            wip_cards = wip_cards_objects.values_list('backlog_id', flat=True)
            done_cards = done_cards_objects.values_list('backlog_id', flat=True)

            logger.debug(f"ToDo Backlog IDs: {list(todo_cards)}")
            logger.debug(f"WIP Backlog IDs: {list(wip_cards)}")
            logger.debug(f"Done Backlog IDs: {list(done_cards)}")

            # Verify matching backlog items
            todo_items = iteration_backlog_items.filter(id__in=todo_cards)
            wip_items = iteration_backlog_items.filter(id__in=wip_cards)
            done_items = iteration_backlog_items.filter(id__in=done_cards)

            logger.debug(f"ToDo Items Count: {todo_items.count()}")
            logger.debug(f"WIP Items Count: {wip_items.count()}")
            logger.debug(f"Done Items Count: {done_items.count()}")

            # Helper function to calculate numeric story points
            def get_numeric_story_points(backlog_items):
                total_points = 0
                for item in backlog_items:
                    size = item.size
                    # Check if size is numeric or a valid integer-like string
                    if isinstance(size, (int, float)):
                        total_points += size
                    elif isinstance(size, str):
                        size = size.strip()
                        if size.isdigit():
                            total_points += int(size)
                        else:
                            logger.warning(f"Invalid size value: {size}")
                    else:
                        logger.warning(f"Unsupported size type: {type(size)}")
                return total_points

            # Calculate story points using the helper function
            todo_story_points = get_numeric_story_points(todo_items)
            wip_story_points = get_numeric_story_points(wip_items)
            done_story_points = get_numeric_story_points(done_items)

            logger.debug(f"ToDo Story Points: {todo_story_points}")
            logger.debug(f"WIP Story Points: {wip_story_points}")
            logger.debug(f"Done Story Points: {done_story_points}")

        
            # Log the results
            logger.debug(f"Total Story Points: {total_story_points}")
            logger.debug(f"ToDo Story Points: {todo_story_points}")
            logger.debug(f"WIP Story Points: {wip_story_points}")
            logger.debug(f"Done Story Points: {done_story_points}")
            
            
           
            
        else:
            iteration_mismatch_flag = True

    # Set the Iteration backlog items count
    iteration_backlog_items_count = iteration_backlog_items.count() if iteration_backlog_items else 0
    
    
    ##
    ##
    ## BURNDOWN CHART
    ##
    ##

    
    normal_release = True
    burndown_data = []
    # check the current iteration length from the release
    if current_iteration and current_release:
        check_iteration_length_in_mins = current_release.iteration_length_in_mins > 0
        if check_iteration_length_in_mins:
            normal_release = False
            total_minutes = current_release.iteration_length_in_mins
            burndown_data = generate_minute_based_burndown(current_iteration, project, total_minutes, total_story_points)
    
    # Prepare Burndown Chart Data
    if current_iteration and normal_release:
        logger.debug(f">>> === BURNDOWNcurrent_iteration: {current_iteration} === <<<")
        iteration_start_date = current_iteration.iteration_start_date
        iteration_end_date = current_iteration.iteration_end_date
        
        # Create date range
        days_range = (iteration_end_date - iteration_start_date).days + 1
        
        current_date = now().date()
        
        for i in range(days_range):
            itr_date = iteration_start_date + timedelta(days=i)  # Correct usage of timedelta
            
            # Total backlog items size - datewise 
            datewise_backlog_items = Backlog.objects.filter(
                pro=project, 
                active=True, 
                iteration=current_iteration,
            )
            datewise_backlog_items_total = datewise_backlog_items.aggregate(total=Sum('size'))['total'] or 0
            # Filter backlog items for the current iteration
            backlog_items = Backlog.objects.filter(
                pro=project, 
                active=True, 
                iteration=current_iteration,
                done_at__date__lte=itr_date
            )
            backlog_count = backlog_items.count()
            # Log each done_at value and current_date
            for item in backlog_items:
                logger.debug(f"CHECK Backlog ID: {item.id}, {item}, done_at: {item.done_at}, current_date: {itr_date}")
            
            # Calculate remaining story points for each date
            done_story_points_till_date = backlog_items.aggregate(total=Sum('size'))['total'] or 0
            remaining_story_points = total_story_points - done_story_points_till_date
            logger.debug(f">>> === itr_date: {itr_date} | done_story_points_till_date: {done_story_points_till_date} | remaining_story_points: {remaining_story_points} === <<<")
            if itr_date.date() > current_date:
                remaining_story_points = ''
            burndown_data.append({
            'date': itr_date.strftime('%Y-%m-%d'),
            'remaining_story_points': remaining_story_points,
            'backlog_count': backlog_count,
            'datewise_backlog_items_total': datewise_backlog_items_total,
            })
            
    # Log the complete burndown data
    logger.debug(f">>> === NORMAL RELEASE: {normal_release} burndown_data: {burndown_data} === <<<")

           
    
    # Prepare context for rendering template
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'view_project_metrics_iteration_tab',
        'organization': organization,
        'org_id': org_id,
        'project': project,
        'project_id': project_id,
        'pro_id': project_id,
        'current_release': current_release,
        'current_iteration': current_iteration,
        'release_mismatch_flag': release_mismatch_flag,
        'iteration_mismatch_flag': iteration_mismatch_flag,
        'iteration_backlog_items': iteration_backlog_items,
        'iteration_backlog_items_count': iteration_backlog_items_count,
        'total_story_points': total_story_points,
        'todo_story_points': todo_story_points,
        'wip_story_points': wip_story_points,
        'done_story_points': done_story_points,
        
        'burndown_data': burndown_data,
        'normal_release': normal_release,
        
        'selected_tab': 'iteration',
    }

    # Render template
    template_file = f"{app_name}/{module_path}/project_metrics/view_project_metrics_iteration_tab.html"
    return render(request, template_file, context)
from django.db.models import Sum, Prefetch
from django.utils.timezone import now
from django.shortcuts import render, get_object_or_404
from django.core.serializers.json import DjangoJSONEncoder
import json
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)

@login_required
def view_project_metrics_release_tab(request, project_id):
    # Fetch user, project, and organization details
    user = request.user
    project = get_object_or_404(Project.objects.select_related("org"), pk=project_id, active=True)
    organization = project.org
    org_id = organization.id
    
    current_iteration = None
    current_release = None
    next_iteration = None
    iteration_data = []
    total_story_points = 0
    completed_story_points = 0
    cumulative_total_points = 0
    cumulative_done_points = 0
    iteration_data_serialized = []
    current_datetime = now().replace(microsecond=0)
    total_release_points = 0  # Total story points for the release
    release_burndown_data = []  # List to store iteration-wise burndown data
    cumulative_done_points = 0  # Tracks cumulative points completed across iterations
    ideal_burndown = []  # Ideal burndown data
    actual_burndown = []  # Actual burndown data
    velocity_chart_data = []  # Velocity chart data
    remaining_points = 0  # Remaining points after each iteration
    
    # Prepare context for rendering template
    if project.project_iteration:
        # Use datetime comparison for both start and end dates
        current_datetime = now().replace(microsecond=0)
        details = get_project_release_and_iteration_details(project.id)
        current_release = details['current_release']
        current_iteration = details['current_iteration']
        next_iteration = details['next_iteration']       

        if project.project_release:
            release = project.project_release

            # Prefetch backlog items for all iterations in one go
            iterations = release.org_release_org_iterations.filter(active=True).prefetch_related(
                Prefetch(
                    "backlog_iteration",
                    queryset=Backlog.objects.filter(pro=project, active=True).only("size", "status", "done_at"),
                    to_attr="prefetched_backlogs"
                )
            )

            # Calculate total release points BEFORE iterating
            for iteration in iterations:
                total_points = sum(int(item.size) for item in iteration.prefetched_backlogs)
                total_release_points += total_points

            for iteration in iterations:
                backlog_items = iteration.prefetched_backlogs
                
                total_points = sum(int(item.size)for item in backlog_items)
                done_points = sum(int(item.size) for item in backlog_items if item.status == "Done")
                total_items = len(backlog_items)
                done_items = sum(1 for item in backlog_items if item.status == "Done")

                total_story_points += total_points
                completed_story_points += done_points                   
                
                # Attach additional data to the iteration object
                iteration.total_story_points = total_points
                iteration.total_done_points = done_points

                velocity_chart_data.append({
                    'name': iteration.name,
                    "id": iteration.id,
                    'total_points': total_points,
                    'done_points': done_points,
                    'total_items': total_items,
                    'done_items': done_items,
                })

                # Preparing the iteration burndown for each iteration
                normal_release = True
                burndown_data = []

                if iteration and release:
                    check_iteration_length_in_mins = release.iteration_length_in_mins > 0
                    if check_iteration_length_in_mins:
                        normal_release = False
                        total_minutes = release.iteration_length_in_mins
                        burndown_data = generate_minute_based_burndown(iteration, project, total_minutes, total_points)

                # Prepare Burndown Chart Data
                if iteration and normal_release:
                    iteration_start_date = iteration.iteration_start_date
                    iteration_end_date = iteration.iteration_end_date
                    
                    # Create date range
                    days_range = (iteration_end_date - iteration_start_date).days + 1
                    current_date = now().date()

                    for i in range(days_range):
                        itr_date = iteration_start_date + timedelta(days=i)
                        
                        # Filter backlog items for the current iteration
                        done_story_points_till_date = sum(
                            int(item.size) for item in backlog_items if item.done_at and item.done_at.date() <= itr_date.date()
                        )
                        remaining_story_points = total_points - done_story_points_till_date

                        if itr_date.date() > current_date:
                            remaining_story_points = ''
                        burndown_data.append({
                            'date': itr_date.strftime('%Y-%m-%d'),
                            'remaining_story_points': remaining_story_points
                        })

                # Attach burndown data to iteration
                iteration.burndown_data = burndown_data              
                iteration.normal_release = normal_release
                iteration.velocity_chart_data = velocity_chart_data

                iteration_data.append(iteration)

                # Add data for this iteration
                cumulative_done_points += done_points
                remaining_points = total_release_points - cumulative_done_points
                actual_burndown.append(cumulative_done_points)
                release_burndown_data.append({
                    "name": iteration.name,
                    "iteration_id": iteration.id,
                    "iteration_start_date": iteration.iteration_start_date.isoformat(),
                    "iteration_end_date": iteration.iteration_end_date.isoformat(),
                    "remaining_points": remaining_points,
                })

            # Calculate ideal burndown
            iterations_count = len(iterations)
            ideal_burndown = [
                total_release_points - (i * (total_release_points / iterations_count))
                for i in range(iterations_count + 1)
            ]

    # Serialize the burndown data
    release_burndown_json = json.dumps({
        "ideal_burndown": ideal_burndown,
        "actual_burndown": release_burndown_data,
    }, cls=DjangoJSONEncoder)

    iteration_data_json = json.dumps(
        list(iteration_data_serialized),  # Convert QuerySet or list of objects to list of dictionaries
        cls=DjangoJSONEncoder
    )

    # Prepare context for rendering template
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'view_project_metrics_release_tab',
        'organization': organization,
        'org_id': org_id,
        'project': project,
        'project_id': project_id,
        'pro_id': project_id,
        
        # Release details
        'current_release': current_release,
        'current_iteration': current_iteration,
        'next_iteration': next_iteration,
        'current_datetime': current_datetime,
        'iteration_data': iteration_data,
        'iteration_data_json': iteration_data_json,
        'release_burndown_json': release_burndown_json,
        'selected_tab': 'release',
    }

    logger.debug(f"Release Burndown JSON: {release_burndown_json}")

    # Render template
    template_file = f"{app_name}/{module_path}/project_metrics/view_project_metrics_release_tab.html"
    return render(request, template_file, context)





@login_required
def view_project_metrics_quality_tab(request, project_id):
    # Fetch user, project, and organization details
    user = request.user
    project = get_object_or_404(Project, pk=project_id, active=True)
    organization = project.org
    org_id = organization.id
    # Prepare context for rendering template
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'view_project_metrics_quality_tab',
        'organization': organization,
        'org_id': org_id,
        'project': project,
        'project_id': project_id,
        'pro_id': project_id,
        
        'selected_tab': 'quality',

    }

    # Render template
    template_file = f"{app_name}/{module_path}/project_metrics/view_project_metrics_quality_tab.html"
    return render(request, template_file, context)
import csv
from datetime import datetime
import pytz

@login_required
def view_project_metrics_flow_tab(request, project_id):
    user = request.user
    project = get_object_or_404(Project, pk=project_id, active=True)
    organization = project.org
    tz = pytz.timezone('Asia/Kolkata')
    ist_tz = pytz.timezone('Asia/Kolkata')
    logger.debug(f">>> === PROJECT METRICS: ****FLOW TAB**** === <<<")
    # Release and Iteration
    current_release = None
    current_iteration = None
    next_iteration = None
    release = None

    # Fetch current release details
    if project.project_release:
        current_datetime = now().replace(microsecond=0)
        details = get_project_release_and_iteration_details(project.id)
        current_release = details['current_release']
        current_iteration = details['current_iteration']
        next_iteration = details['next_iteration']
        release = project.project_release
  
    if not release:
        return HttpResponse("No active release found.", status=404)

    project_board = ProjectBoard.objects.filter(
        project=project, active=True, default_board=True
    ).first()
    
    if not project_board:
        return HttpResponse("No active board found.", status=404)

    active_columns = list(ProjectBoardState.objects.filter(
        board=project_board, active=True
    ).values_list("name", flat=True))

    cumulative_counts = {'dates': [], 'backlog_counts': []}
    for column in active_columns:
        cumulative_counts[column.lower() + '_counts'] = []
    

    # Snapshot range: by day or by minute
    CFD_BY = "DATE"
    if release.release_length_in_mins > 0:
        # Minute-based snapshots
        total_minutes = release.release_length_in_mins
        snapshot_start = release.release_start_date.astimezone(tz)

        snapshot_points = [
                (snapshot_start + timedelta(minutes=i)).strftime('%Y-%m-%dT%H:%M:%S')
                    for i in range(total_minutes + 1)
                    ]
        CFD_BY = "TIME"
    else:
        # Daily snapshots
        snapshot_start = release.release_start_date.astimezone(tz)
        snapshot_end = release.release_end_date
        total_days = (snapshot_end - snapshot_start).days

        snapshot_points = [
                    (snapshot_start + timedelta(days=i)).strftime('%Y-%m-%dT%H:%M:%S')
                    for i in range(total_days + 1)
                ]
    

    # NEW QUERY DESIGN
    movements = None
    best_cfd_data = {}
    best_cfd_counts = defaultdict(dict)
    for snapshot_time in snapshot_points:
        if CFD_BY == "DATE":
            s_date, stime = snapshot_time.split('T')
            # Initialize counts for the current date with 0 for all active columns
             # Convert s_date to the desired format (e.g., 07-03-2025)
            s_date_formatted = datetime.strptime(s_date, '%Y-%m-%d').strftime('%d-%m-%Y')
            best_cfd_counts[str(s_date_formatted)] = {col.lower(): 0 for col in active_columns}
            
            # find out movements between the dates chosen
            #ProjectBoardStateTransition.objects.all().delete()
             # Find out movements between the dates chosen
            movements = ProjectBoardStateTransition.objects.filter(
                board=project_board,
                card__pro=project,
                transition_time__date=s_date,
                active=True,
            ).order_by('card', '-transition_time')
            
            #print(f">>> === TOTAL MOVEMENTS: {movements.count()} === <<<")
            
            # Group transitions by card
            card_transitions = defaultdict(list)    
            for mov in movements:
                #print(f">>> === MOVEMENT: {mov} === <<<")
                card_transitions[mov.card].append(mov)
            
            #print(f">>> === UNIQUE CARDS WITH TRANSITIONS: {len(card_transitions)} === <<<")
            
            # Process each card's transitions
            for card, transitions in card_transitions.items():
                # print(f"Card: {card}")
                # print(f">>> === TRANSITIONS FOR CARD {card.id}:")
                # for mov in transitions:
                #     print(f"  Transition: {mov.transition_time} | From: {mov.from_state} | To: {mov.to_state} | Active: {mov.active}")
                # Collect the card id, top most transition details, to state and date and time
                which_transition = transitions[0]
                date_field = which_transition.formatted_date()
                to_state = which_transition.to_state
                
                
                # Update CFD counts for the date and state
                to_state_lc = str(to_state).lower() 
                #print(f">>> === checking important: {to_state_lc} {best_cfd_counts[s_date_formatted]} === <<<")               
                if to_state and to_state_lc in best_cfd_counts[s_date_formatted]:
                    best_cfd_counts[s_date_formatted][to_state_lc] += 1
                    


                best_cfd_data[card.id] = {
                    'card_id': card.id,
                    'from_state': which_transition.from_state,
                    'to_state': which_transition.to_state,
                    'date_field': which_transition.formatted_date(),
                    'time_field': which_transition.formatted_time(),
                }
                #print(f"  Card: {
                #    card.id} | To State: {which_transition.to_state} | Date: {which_transition.formatted_date()} | Time: {which_transition.formatted_time()}")
                
                # for mov in transitions:
                #     print(f"  Transition: {mov.transition_time} | From: {mov.from_state} | To: {mov.to_state}")
    # Print CFD counts
    print("CFD Counts:")
    for date, state_counts in best_cfd_counts.items():
        for state, count in state_counts.items():
            if (count > 0):
                print(f"Date: {date}  State: {state} | Count: {count}")
    
    # for cfd in best_cfd_data.values():
    #     print(f">>> === CFD:{cfd['date_field']}{cfd['time_field']}: {cfd['card_id']} {cfd['from_state']} {cfd['to_state']}  === <<<")
    # Print CFD data in ascending order of to_state
    # Print CFD data in ascending order of card ID
    print("CFD Data (Sorted by Card ID):")
    counter = 1
    for card_id in sorted(best_cfd_data.keys()):  # Sort by card ID
        cfd = best_cfd_data[card_id]
        print(f">>> === {counter}: CFD:{cfd['date_field']}{cfd['time_field']}: {cfd['card_id']} {cfd['from_state']} {cfd['to_state']} === <<<")
        counter +=1 
    # # Gather all transitions beforehand
    # transitions = ProjectBoardStateTransition.objects.filter(
    #     board=project_board,
    #     card__pro=project,
    #     transition_time__lte=snapshot_points[-1] if snapshot_points else snapshot_start
    # ).order_by('card', 'transition_time')
    from django.db.models import OuterRef, Subquery

    # Get the latest transition per card within the project and board
    latest_transition = (
        ProjectBoardStateTransition.objects
        .filter(
            card=OuterRef('card'),
            board=project_board,  # Ensure it is within the correct board
            card__pro=project,  # Ensure it's within the correct project
            active=True,
        )
        .order_by('-transition_time')  # Get the latest transition first
        .values('id')[:1]  # Select only one ID
    )

    # Now use this Subquery correctly in the main query
    transitions = ProjectBoardStateTransition.objects.filter(
        id__in=Subquery(latest_transition),  # Ensure we only get latest transitions
        board=project_board,  # Ensure correct filtering
        card__pro=project,
        active=True,
        transition_time__lte=snapshot_points[-1] if snapshot_points else snapshot_start
    )

    #print(f">>> === TRANSITIONS: {transitions} === <<<")
    transitions_by_card = defaultdict(list)
    for transition in transitions:
        transitions_by_card[transition.card_id].append(transition)

    for snapshot_time in snapshot_points:
        snapshot_counts = {col.lower(): 0 for col in active_columns}  # Initialize counts
        snapshot_dt = datetime.strptime(snapshot_time, '%Y-%m-%dT%H:%M:%S').replace(tzinfo=tz)

        for card_id, card_transitions in transitions_by_card.items():
            latest_trans = max(
                (t for t in card_transitions if t.transition_time.astimezone(tz) <= snapshot_dt),
                key=lambda t: t.transition_time,
                default=None
            )

            if latest_trans:
                latest_state = str(latest_trans.to_state).lower()
                #print(f"Card {card_id} | Snapshot: {snapshot_time} | Latest State: {latest_state}")  # Debug

                if latest_state in snapshot_counts:
                    snapshot_counts[latest_state] += 1

        cumulative_counts['dates'].append(snapshot_time)

        backlog_count = Backlog.objects.filter(
            pro=project,
            release=current_release,
            iteration=current_iteration,
            active=True
        ).count()

        cumulative_counts['backlog_counts'].append(backlog_count)
        
        for col_name, count in snapshot_counts.items():           
            cumulative_counts[str(col_name).lower() + '_counts'].append(count)

    #print(f">>> === SNAPSHOT POINTS {snapshot_points}=== <<<")

    # Prepare the output CSV file
    csv_filename = "cfd_snapshot_data.csv"

    # Initialize a list to hold all rows (including headers)
    csv_data = []

    # Add header row (snapshot_time + state columns)
    state_columns = [col.lower() for col in active_columns]
    header = ["snapshot_time"] + state_columns
    csv_data.append(header)

    # Iterate over snapshot points
    for snapshot_time in snapshot_points:  # Already formatted as '%Y-%m-%dT%H:%M:%S'
        snapshot_counts = {col.lower(): 0 for col in active_columns}  # Initialize counts

        # Convert snapshot_time string back to a datetime object
        snapshot_dt = datetime.strptime(snapshot_time, '%Y-%m-%dT%H:%M:%S').replace(tzinfo=tz)

        # Iterate over card transitions
        for card_transitions in transitions_by_card.values():
            latest_state = None
            for trans in card_transitions:
                trans_time = trans.transition_time.astimezone(tz)  # Convert transition time to IST

                if trans_time <= snapshot_dt:  # Compare as datetime objects
                    latest_state = str(trans.to_state).lower()
                else:
                    break  # Transitions are sorted by time, so break early
            
            # Update snapshot counts
            if latest_state and latest_state in snapshot_counts:
                snapshot_counts[latest_state] += 1

        # Prepare row with snapshot_time and corresponding state counts
        row = [snapshot_time] + [snapshot_counts[col] for col in state_columns]
        csv_data.append(row)

    # Write data to CSV
    with open(csv_filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(csv_data)

    print(f"CSV file '{csv_filename}' generated successfully!")
    
    # Prepare context for rendering template
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'view_project_metrics_flow_tab',
        'organization': organization,
        'org_id': project.org.id,
        'project': project,
        'project_id': project_id,
        'pro_id': project_id,
        'selected_tab': 'flow',
        'current_release': current_release,
        'current_iteration': current_iteration,
        'next_iteration': next_iteration,
        'dates': cumulative_counts['dates'],
        'backlog_counts': cumulative_counts['backlog_counts'],
        'column_names': active_columns,  # Send dynamic column names
        'column_data': {col.lower(): cumulative_counts[col.lower() + '_counts'] for col in active_columns},  # Send dynamic data
    }

   
    template_file = f"{app_name}/{module_path}/project_metrics/view_project_metrics_flow_tab.html"
    return render(request, template_file, context)

@login_required
def view_project_metrics_value_tab(request, project_id):
    # Fetch user, project, and organization details
    user = request.user
    project = get_object_or_404(Project, pk=project_id, active=True)
    organization = project.org
    org_id = organization.id
    logger.debug(f">>> === PROJECT METRICS: ****value TAB**** === <<<")
    # Prepare context for rendering template
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'view_project_metrics_value_tab',
        'organization': organization,
        'org_id': org_id,
        'project': project,
        'project_id': project_id,
        'pro_id': project_id,
        
        'selected_tab': 'value',

    }

    # Render template
    template_file = f"{app_name}/{module_path}/project_metrics/view_project_metrics_value_tab.html"
    return render(request, template_file, context)

