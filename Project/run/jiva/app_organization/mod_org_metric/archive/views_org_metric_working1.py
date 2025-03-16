
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
@login_required
def view_project_metrics(request, project_id):
    user = request.user
    project = get_object_or_404(Project, pk=project_id, active=True, **viewable_dict)
    organization = project.org
    org_id = organization.id
    
    # get the backlog details
    backlog_details = jivapms_mod_backlog_helper_get_backlog_details(request, project_id)
    include_types = backlog_details['include_types']
    
    end_date = now()
    start_date = end_date - timedelta(days=90)  # Last 3 months

    # Query backlog data
    backlog_check = Backlog.objects.filter(pro=project, active=True, deleted=False, type__in=include_types)
    backlog_count = backlog_check.count()
    logger.debug(f">>> === backlog_count: {backlog_count} === <<<")
    backlog_data = (
        Backlog.objects
        .filter(pro=project, created_at__range=(start_date, end_date), active=True, deleted=False, type__in=include_types)
        .extra({'created_date': "date(created_at)"})
        .values('created_date', 'status')
        .annotate(count=models.Count('id'))
        .order_by('created_date')
    )

    # Prepare data for Chart.js
    labels = [item['created_date'] for item in backlog_data]
    daily_counts = [item['count'] for item in backlog_data]

    # Compute cumulative counts
    cumulative_counts = []
    total = 0
    for count in daily_counts:
        total += count
        cumulative_counts.append(total)

    # Prepare data for Chart.js
    labels = []
    daily_counts = []
    cumulative_counts = []
    to_do_counts = []
    in_progress_counts = []
    done_counts = []
    backlog_counts = []
    
    total_count = 0
    to_do_total = 0
    in_progress_total = 0
    done_total = 0
    backlog_total = 0

    for item in backlog_data:
        labels.append(item['created_date'])
        daily_counts.append(item['count'])

        # Calculate cumulative counts
        total_count += item['count']
        cumulative_counts.append(total_count)

        # Calculate cumulative counts for each status
        if item['status'] == 'To Do':
            to_do_total += item['count']
        elif item['status'] == 'In Progress':
            in_progress_total += item['count']
        elif item['status'] == 'Done':
            done_total += item['count']

        # Calculate the total backlog count as the sum of all statuses
        backlog_total = to_do_total + in_progress_total + done_total
        
        logger.debug(f">>> === backlog_total: {backlog_total} === <<<")
        logger.debug(f">>> === to_do_total: {to_do_total} === <<<")
        logger.debug(f">>> === in_progress_total: {in_progress_total} === <<<")
        logger.debug(f">>> === done_total: {done_total} === <<<")
        

        # Append CFD data
        backlog_counts.append(backlog_total)
        to_do_counts.append(to_do_total)
        in_progress_counts.append(in_progress_total)
        done_counts.append(done_total)

       


    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'view_project_metrics',
        'organization': organization,
        'org_id': org_id,
        
        'module_path': module_path,
        
        'page_title': f'View Project Metrics',
        'labels': labels,
        'data': daily_counts,
        'cumulative_data': cumulative_counts,
        'to_do_data': to_do_counts,          # To Do status counts
        'in_progress_data': in_progress_counts,  # In Progress status counts
        'done_data': done_counts,          # Done status counts
        'backlog_data': backlog_counts,    # Backlog status counts
        'project': project,
        'project_id': project_id,
        'pro_id': project_id,
    }
    
    template_file = f"{app_name}/{module_path}/project_metrics/view_project_metrics.html"
    return render(request, template_file, context)



# @login_required
# def view_project_metrics(request, project_id):
#     user = request.user
#     project = get_object_or_404(Project, pk=project_id, active=True)
#     organization = project.org
#     org_id = organization.id

#     # Get backlog details
#     backlog_details = jivapms_mod_backlog_helper_get_backlog_details(request, project_id)
#     include_types = backlog_details['include_types']

#     # Date range (last 3 months)
#     end_date = now().date()  # Today's date
#     start_date = end_date - timedelta(days=90)

#     # Generate all dates in the range
#     date_range = [(start_date + timedelta(days=i)).strftime('%Y-%m-%d') for i in range((end_date - start_date).days + 1)]

#     # Query backlog data grouped by date and status
#     backlog_data = (
#         Backlog.objects
#         .filter(
#             pro=project,
#             created_at__range=(start_date, end_date),
#             active=True,
#             deleted=False,
#             type__in=include_types
#         )
#         .extra({'created_date': "date(created_at)"})
#         .values('created_date', 'status')
#         .annotate(count=models.Count('id'))
#         .order_by('created_date')
#     )

#     # Prepare data for Chart.js
#     labels = date_range
#     daily_counts = []           # Total items added per day
#     cumulative_counts = []      # Total cumulative items over time
#     to_do_counts = []           # To Do cumulative counts
#     in_progress_counts = []     # In Progress cumulative counts
#     done_counts = []            # Done cumulative counts
#     backlog_counts = []         # Total Backlog cumulative counts

#     # Initialize counters
#     to_do_total = 0
#     in_progress_total = 0
#     done_total = 0
#     daily_total = 0
#     cumulative_total = 0

#     # Map data by date and status
#     data_map = {date: {'To Do': 0, 'In Progress': 0, 'Done': 0} for date in labels}
#     for item in backlog_data:
#         date = item['created_date']
#         status = item['status']
#         count = item['count']
#         if date in data_map and status in data_map[date]:
#             data_map[date][status] += count

#     # Compute counts for each date
#     for date in labels:
#         # Daily count for that date
#         daily_count = sum(data_map[date].values())
#         daily_total += daily_count
#         daily_counts.append(daily_count)

#         # Cumulative count
#         cumulative_total += daily_count
#         cumulative_counts.append(cumulative_total)

#         # Status-specific cumulative counts
#         to_do_total += data_map[date]['To Do']
#         in_progress_total += data_map[date]['In Progress']
#         done_total += data_map[date]['Done']

#         # Total backlog count as sum of all statuses
#         backlog_total = to_do_total + in_progress_total + done_total

#         # Append data for charts
#         backlog_counts.append(backlog_total)
#         to_do_counts.append(to_do_total)
#         in_progress_counts.append(in_progress_total)
#         done_counts.append(done_total)

#         # Debug logs
#         logger.debug(f"Date: {date} | Backlog: {backlog_total}, To Do: {to_do_total}, In Progress: {in_progress_total}, Done: {done_total}")

#     # Context for rendering
#     context = {
#         'parent_page': '___PARENTPAGE___',
#         'page': 'view_project_metrics',
#         'organization': organization,
#         'org_id': org_id,
#         'page_title': 'View Project Metrics',
#         'labels': labels,                       # Date labels
#         'data': daily_counts,                   # Daily counts
#         'cumulative_data': cumulative_counts,   # Cumulative counts
#         'to_do_data': to_do_counts,             # To Do counts
#         'in_progress_data': in_progress_counts, # In Progress counts
#         'done_data': done_counts,               # Done counts
#         'backlog_data': backlog_counts,         # Backlog counts
#         'project': project,
#         'project_id': project_id,
#     }

#     template_file = f"{app_name}/{module_path}/project_metrics/view_project_metrics.html"
#     return render(request, template_file, context)
