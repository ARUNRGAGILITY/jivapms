
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

@login_required
def view_project_metrics_release_tab(request, project_id):
    # Fetch user, project, and organization details
    user = request.user
    project = get_object_or_404(Project, pk=project_id, active=True)
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
            iterations = release.org_release_org_iterations.filter(active=True)            
            # Calculate total release points BEFORE iterating
            for iteration in iterations:
                total_points = Backlog.objects.filter(pro=project, iteration=iteration, active=True).aggregate(
                    total=Sum('size')
                )['total'] or 0
                total_release_points += total_points
                
                
            for iteration in iterations:
                # Fetch total story points for all backlog items in the iteration
                check_total = Backlog.objects.filter( iteration=iteration, active=True)
                for ct in check_total:
                    logger.debug(f">>> === PROJECT : {ct.pro} == {project} == <<<")
                    
                total_points = Backlog.objects.filter(pro=project, iteration=iteration, active=True).aggregate(
                    total=Sum('size')
                )['total'] or 0
                
                # Fetch story points for "done" backlog items in the iteration
                done_points = Backlog.objects.filter(
                    pro=project,
                    iteration=iteration, active=True, status="Done"
                ).aggregate(
                    done=Sum('size')
                )['done'] or 0

                # Fetch the count of backlog items
                total_items = Backlog.objects.filter(pro=project, iteration=iteration, active=True).count()
                done_items = Backlog.objects.filter(pro=project, iteration=iteration, active=True, status="Done").count()
                total_story_points += total_points
                completed_story_points += done_points                   
                
                # Update cumulative totals
               
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
               
                #
                # Preparing the iteration burndown for each iteration
                #
                #
                normal_release = True
                burndown_data = []
                # check the current iteration length from the release
                if iteration and release:
                    check_iteration_length_in_mins = release.iteration_length_in_mins > 0
                    if check_iteration_length_in_mins:
                        normal_release = False
                        total_minutes = release.iteration_length_in_mins
                        burndown_data = generate_minute_based_burndown(iteration, project, total_minutes, total_points)
                
                # Prepare Burndown Chart Data
                if iteration and normal_release:
                    logger.debug(f">>> === BURNDOWNcurrent_iteration: {iteration} === <<<")
                    iteration_start_date = iteration.iteration_start_date
                    iteration_end_date = iteration.iteration_end_date
                    
                    # Create date range
                    days_range = (iteration_end_date - iteration_start_date).days + 1
                    
                    current_date = now().date()
                    
                    for i in range(days_range):
                        itr_date = iteration_start_date + timedelta(days=i)  # Correct usage of timedelta
                        
                        # Filter backlog items for the current iteration
                        backlog_items = Backlog.objects.filter(
                            pro=project, 
                            active=True, 
                            iteration=iteration,
                            done_at__date__lte=itr_date
                        )
                        
                        # Log each done_at value and current_date
                        for item in backlog_items:
                            logger.debug(f"CHECK Backlog ID: {item.id}, {item}, done_at: {item.done_at}, current_date: {itr_date}")
                        
                        # Calculate remaining story points for each date
                        done_story_points_till_date = backlog_items.aggregate(total=Sum('size'))['total'] or 0
                        remaining_story_points = total_points - done_story_points_till_date
                        logger.debug(f">>> === itr_date: {itr_date} {iteration} | done_story_points_till_date: {done_story_points_till_date} | remaining_story_points: {remaining_story_points} === <<<")
                        if itr_date.date() > current_date:
                            remaining_story_points = ''
                        burndown_data.append({
                        'date': itr_date.strftime('%Y-%m-%d'),
                        'remaining_story_points': remaining_story_points
                        })
               
               
                # Log the complete burndown data
                iteration.burndown_data = burndown_data              
                iteration.normal_release = normal_release
                
                # Velocity chart
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
                    "remaining_points": remaining_points,  # Remaining points after this iteration
                })
            # Calculate ideal burndown
            iterations_count = len(iterations)
            ideal_burndown = [
                total_release_points - (i * (total_release_points / iterations_count))
                for i in range(iterations_count + 1)
            ]
    # Serialize the burndown data
    logger.debug(f">>> === total_release_points: {total_release_points} === <<<")
    logger.debug(f">>> === remaining points : {remaining_points} === <<<")
    logger.debug(f">>> === release_burndown_data: {release_burndown_data} === <<<")
    
    logger.debug(f">>> === velocity chart data : {velocity_chart_data} === <<<")
    # Serialize the burndown data
    release_burndown_json = json.dumps({
        "ideal_burndown": ideal_burndown,
        "actual_burndown": release_burndown_data,
    }, cls=DjangoJSONEncoder)
                            
    # Prepare context for rendering template            

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



@login_required
def view_project_metrics_flow_tab(request, project_id):
    # Fetch user, project, and organization details
    user = request.user
    project = get_object_or_404(Project, pk=project_id, active=True)
    organization = project.org
    org_id = organization.id
    logger.debug(f">>> === PROJECT METRICS: ****flow TAB**** === <<<")
    
    # Variables
    iteration_data = []
    total_story_points = 0
    completed_story_points = 0
    cumulative_total_points = 0
    cumulative_done_points = 0
    backlog_counts = 0
    
    tz = pytz.timezone('Asia/Kolkata')
    
    # Release and Iteration
    current_release = None
    current_iteration = None
    next_iteration = None
    normal_release = True
    release = None
    # Create a dictionary to store cumulative counts
    cumulative_counts = {
        'dates': [],
        'backlog_counts': [],
        'todo_counts': [],
        'wip_counts': [],
        'done_counts': []
    }

    if project.project_release:
        current_datetime = now().replace(microsecond=0)
        details = get_project_release_and_iteration_details(project.id)
        current_release = details['current_release']
        current_iteration = details['current_iteration']
        next_iteration = details['next_iteration']       
    
        
        release = project.project_release
        iterations = release.org_release_org_iterations.filter(active=True)   
    
        # Fetch total story points for all backlog items in the iteration
        backlog_items_check = Backlog.objects.filter(pro=project, iteration=current_iteration, active=True)
        backlog_counts = backlog_items_check.count()
        
        release_backlog_items_check = Backlog.objects.filter(pro=project, release=current_release, active=True)
        release_backlog_counts = release_backlog_items_check.count()

        def cfd_backlog_counts(project, current_release):
            release_backlog_items_check = Backlog.objects.filter(pro=project, release=current_release, active=True)
            rel_backlog_counts = release_backlog_items_check.count()
            return rel_backlog_counts

        # Calculate the sum of the sizes of the items
        total_size = release_backlog_items_check.aggregate(total_size=Sum('size'))['total_size']

        # Log the results
        logger.debug(f">>> === release_backlog_counts: {release_backlog_counts} === <<<")
        logger.debug(f">>> === total_size of items: {total_size} === <<<")
        for iteration in iterations:    
            
            
            # Check the short or normal iterations
            check_iteration_length_in_mins = release.iteration_length_in_mins > 0
            if check_iteration_length_in_mins:
                normal_release = False
            else:
                normal_release = True
                
            total_points = Backlog.objects.filter(pro=project, iteration=iteration, active=True).aggregate(
                total=Sum('size')
            )['total'] or 0
            
            # Fetch story points for "done" backlog items in the iteration
            done_points = Backlog.objects.filter(
                pro=project,
                iteration=iteration, active=True, status="Done"
            ).aggregate(
                done=Sum('size')
            )['done'] or 0

            # Fetch the count of backlog items
            total_items = Backlog.objects.filter(pro=project, iteration=iteration, active=True).count()
            done_items = Backlog.objects.filter(pro=project, iteration=iteration, active=True, status="Done").count()
            total_story_points += total_points
            completed_story_points += done_points                   
            
            # Update cumulative totals
            
            # Attach additional data to the iteration object
            iteration.total_story_points = total_points
            iteration.total_done_points = done_points              
            
            iteration_data.append(iteration)
               
            # Calculate ideal burndown
            iterations_count = len(iterations)
    
    
        # prepare the release cfd
        # Fetch all transitions within the date range
        transitions = ProjectBoardStateTransition.objects.filter(
            card__pro_id=project_id,
            transition_time__date__gte=release.release_start_date,
            transition_time__date__lte=release.release_end_date
        ).annotate(
            date=TruncDate('transition_time')  # Group by truncated date
        )
        logger.debug(f">>> === TRANSITIONS: {transitions} === <<<")
        # Get the last transition per card per day
        latest_transitions = (
            transitions.values('card_id', 'date')  # Group by card and date
            .annotate(latest_time=Max('transition_time'))  # Get the latest transition time for each card per day
        )

        # Use the latest transitions to filter the main queryset
        latest_transitions_ids = ProjectBoardStateTransition.objects.filter(
            transition_time__in=[entry['latest_time'] for entry in latest_transitions]
        )

       
        # Iterate over each date in the range
        current_date = release.release_start_date
    
        cumulative_todo = 0
        cumulative_wip = 0
        cumulative_done = 0


    if current_release and release.release_length_in_mins > 0:
        logger.debug(f">>> === SHORT-TERM RELEASE {release.release_start_date}=== <<<")
        total_minutes = release.release_length_in_mins
        tz = pytz.timezone('Asia/Kolkata')
        release_start_datetime = current_release.release_start_date.astimezone(tz)
        release_end_datetime = current_release.release_end_date.astimezone(tz)
        for minute_offset in range(total_minutes + 1):  # Include the last minute
            rel_datetime = release.release_start_date + timedelta(minutes=minute_offset)
          
            daily_transitions = latest_transitions_ids.filter(
                transition_time__gte=release_start_datetime,
                # transition_time__lte=release_end_datetime,
            )
            daily_transitions_count = daily_transitions.count()
            logger.debug(f">>> === DAILY TRANSITIONS COUNT: {daily_transitions_count} === <<<")
            # Filter transitions for the specific datetime
            todo_count = 0 
            wip_count = 0
            done_count = 0
            counter = 1
            for dt in daily_transitions:                
                formatted_transition_time = dt.transition_time.astimezone(tz).strftime('%Y-%m-%dT%H:%M:%S')
                formatted_rel_datetime = rel_datetime.astimezone(tz).strftime('%Y-%m-%dT%H:%M:%S')
                if dt.active:
                    #logger.debug(f">>> === DAILY TRANSITIONS: {dt.transition_time} {formatted_transition_time} {formatted_rel_datetime}=== <<<")
                    dt_transition_time_tz = dt.transition_time.astimezone(tz)
                    rel_datetime_tz = rel_datetime.astimezone(tz)
                    #logger.debug(f">>> === TESTING: DT TT: {dt_transition_time_tz} REL DT: {rel_datetime_tz} === <<<")
                    #logger.debug(f">>> === {formatted_transition_time} {formatted_rel_datetime} === <<<")
                    if dt.to_state.name == 'ToDo' and dt_transition_time_tz <= rel_datetime_tz :
                        todo_count += 1
                    if dt.to_state.name == 'WIP' and dt_transition_time_tz <= rel_datetime_tz: 
                        wip_count += 1
                    if dt.to_state.name == 'Done'and dt_transition_time_tz <= rel_datetime_tz   :
                        done_count += 1
                    counter += 1
            logger.debug(f">>> === COUNTER: {counter} === <<<")
            # Update cumulative counts
            cumulative_todo += todo_count
            cumulative_wip += wip_count
            cumulative_done = done_count
            logger.debug(f">>> === CUMULATIVE COUNTS: {todo_count} {wip_count} {done_count} === <<<")
            logger.debug(f">>> === CUMULATIVE COUNTS: {cumulative_todo} {cumulative_wip} {cumulative_done} === <<<")

            # check the release backlog counts for cfd in each iteration
            release_backlog_counts_cfd = cfd_backlog_counts(project, current_release)

            # Append to cumulative counts dictionary
            current_date_for_cfd = release_start_datetime.strftime('%Y-%m-%dT%H:%M:%S')
            cumulative_counts['dates'].append(current_date_for_cfd)
            cumulative_counts['backlog_counts'].append(release_backlog_counts_cfd)
            cumulative_counts['todo_counts'].append(cumulative_todo)
            cumulative_counts['wip_counts'].append(cumulative_wip)
            cumulative_counts['done_counts'].append(cumulative_done)
            # Create a random number and append to backlog counts
            # cumulative_counts['backlog_counts'].append(2)
            # cumulative_counts['todo_counts'].append(5)
            # cumulative_counts['wip_counts'].append(4)
            # cumulative_counts['done_counts'].append(10)
            logger.debug(f">>> === LOG: {cumulative_counts['backlog_counts']} === <<<")
    else:
        logger.debug(f">>> === NORMAL RELEASE === <<<")
        if release:
            while current_date <= release.release_end_date:
                # Filter latest transitions up to the current date
                daily_transitions = latest_transitions_ids.filter(
                    transition_time__date__lte=current_date
                )

                # # Aggregate counts for each state
                # todo_count = daily_transitions.filter(to_state__name='ToDo').count()
                # wip_count = daily_transitions.filter(to_state__name='WIP').count()
                # done_count = daily_transitions.filter(to_state__name='Done').count()
                # Filter transitions for the specific date
                todo_count = daily_transitions.filter(
                    transition_time__date=current_date,
                    to_state__name='ToDo'
                ).count()

                wip_count = daily_transitions.filter(
                    transition_time__date=current_date,
                    to_state__name='WIP'
                ).count()

                done_count = daily_transitions.filter(
                    transition_time__date=current_date,
                    to_state__name='Done'
                ).count()

                # Update cumulative counts
                cumulative_todo += todo_count
                cumulative_wip += wip_count
                cumulative_done += done_count

                # Append to cumulative counts dictionary
                if current_release:
                    release_start_datetime = current_release.release_start_date.astimezone(tz)
                    release_end_datetime = current_release.release_end_date.astimezone(tz)
                current_date_for_cfd = release_start_datetime.strftime('%Y-%m-%dT%H:%M:%S')
                cumulative_counts['dates'].append(current_date_for_cfd)
                cumulative_counts['backlog_counts'].append(backlog_counts)
                cumulative_counts['todo_counts'].append(cumulative_todo)
                cumulative_counts['wip_counts'].append(cumulative_wip)
                cumulative_counts['done_counts'].append(cumulative_done)

                # Move to the next date
                current_date += timedelta(days=1)

            #logger.debug(f">>> === CUMULATIVE COUNTS: {cumulative_counts} === <<<")
            
    cfd_data = cumulative_counts
    # Prepare context for rendering template
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'view_project_metrics_flow_tab',
        'organization': organization,
        'org_id': org_id,
        'project': project,
        'project_id': project_id,
        'pro_id': project_id,
        
        'selected_tab': 'flow',
        
        'current_release': current_release,
        'current_iteration': current_iteration,
        'next_iteration': next_iteration,
        
        'iteration_data': iteration_data,
        'dates': cfd_data['dates'],
        'backlog_counts': cfd_data['backlog_counts'],
        'todo_counts': cfd_data['todo_counts'],
        'wip_counts': cfd_data['wip_counts'],
        'done_counts': cfd_data['done_counts'],

    }
    logger.debug(f">>> === BACKLOG COUNTS: {cfd_data['backlog_counts']} === <<<")
    # Render template
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

