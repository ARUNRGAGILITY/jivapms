
from app_scrum.mod_app.all_view_imports import *
from app_scrum.mod_deliver.models_deliver import *
from app_scrum.mod_deliver.forms_deliver import *

from app_organization.mod_organization.models_organization import *

from app_common.mod_common.models_common import *

app_name = 'app_scrum'
app_version = 'v1'

module_name = 'delivers'
module_path = f'mod_deliver'

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
def list_delivers(request, organization_id):
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
        tobjects = Deliver.objects.filter(name__icontains=search_query, 
                                            organization_id=organization_id, **viewable_dict).order_by('position')
    else:
        tobjects = Deliver.objects.filter(active=True, organization_id=organization_id).order_by('position')
        deleted = Deliver.objects.filter(active=False, deleted=False,
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
                    object = get_object_or_404(Deliver, pk=item, active=True, **viewable_dict)
                    object.active = False
                    object.save()
                    
                elif bulk_operation == 'bulk_done':
                    object = get_object_or_404(Deliver, pk=item, active=True, **viewable_dict)
                    object.done = True
                    object.save()
                    
                elif bulk_operation == 'bulk_not_done':
                    object = get_object_or_404(Deliver, pk=item, active=True, **viewable_dict)
                    object.done = False
                    object.save()
                    
                elif bulk_operation == 'bulk_blocked':  # Correct the operation check here
                    object = get_object_or_404(Deliver, pk=item, active=True, **viewable_dict)
                    object.blocked = True
                    object.save()
                    
                else:
                    redirect('list_delivers', organization_id=organization_id)
            return redirect('list_delivers', organization_id=organization_id)
    
    # send outputs info, template,
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'list_delivers',
        'organization': organization,
        'organization_id': organization_id,
        
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
        'page_title': f'Deliver List',
    }       
    template_file = f"{app_name}/{module_path}/list_delivers.html"
    return render(request, template_file, context)





# ============================================================= #
@login_required
def list_deleted_delivers(request, organization_id):
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
        tobjects = Deliver.objects.filter(name__icontains=search_query, 
                                            active=False, deleted=False,
                                            organization_id=organization_id, **viewable_dict).order_by('position')
    else:
        tobjects = Deliver.objects.filter(active=False, deleted=False, organization_id=organization_id,
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
                        object = get_object_or_404(Deliver, pk=item, active=False, **viewable_dict)
                        object.active = True
                        object.save()         
                    elif bulk_operation == 'bulk_erase':
                        object = get_object_or_404(Deliver, pk=item, active=False, **viewable_dict)
                        object.active = False  
                        object.deleted = True             
                        object.save()    
                    else:
                        redirect('list_delivers', organization_id=organization_id)
                redirect('list_delivers', organization_id=organization_id)
    
    # send outputs info, template,
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'list_deleted_delivers',
        'organization': organization,
        'organization_id': organization_id,
        
        'module_path': module_path,
        'user': user,
        'tobjects': tobjects,
        'page_obj': page_obj,
        'objects_count': objects_count,
        'objects_per_page': objects_per_page,
        'show_all': show_all,
        'pagination_options': pagination_options,
        'selected_bulk_operations': selected_bulk_operations,
        'page_title': f'Deliver List',
    }       
    template_file = f"{app_name}/{module_path}/list_deleted_delivers.html"
    return render(request, template_file, context)



# Create View
@login_required
def create_deliver(request, organization_id):
    user = request.user
    organization = Organization.objects.get(id=organization_id, active=True, 
                                                **first_viewable_dict)
    
    if request.method == 'POST':
        form = DeliverForm(request.POST)
        if form.is_valid():
            form.instance.author = user
            form.instance.organization_id = organization_id
            form.save()
        else:
            print(f">>> === form.errors: {form.errors} === <<<")
        return redirect('list_delivers', organization_id=organization_id)
    else:
        form = DeliverForm()

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'create_deliver',
        'organization': organization,
        'organization_id': organization_id,
        
        'module_path': module_path,
        'form': form,
        'page_title': f'Create Deliver',
    }
    template_file = f"{app_name}/{module_path}/create_deliver.html"
    return render(request, template_file, context)




# Edit
@login_required
def edit_deliver(request, organization_id, deliver_id):
    user = request.user
    organization = Organization.objects.get(id=organization_id, active=True, 
                                                **first_viewable_dict)
    
    object = get_object_or_404(Deliver, pk=deliver_id, active=True,**viewable_dict)
    if request.method == 'POST':
        form = DeliverForm(request.POST, instance=object)
        if form.is_valid():
            form.instance.author = user
            form.instance.organization_id = organization_id
            form.save()
        else:
            print(f">>> === form.errors: {form.errors} === <<<")
        return redirect('list_delivers', organization_id=organization_id)
    else:
        form = DeliverForm(instance=object)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'edit_deliver',
        'organization': organization,
        'organization_id': organization_id,
        
        'module_path': module_path,
        'form': form,
        'object': object,
        'page_title': f'Edit Deliver',
    }
    template_file = f"{app_name}/{module_path}/edit_deliver.html"
    return render(request, template_file, context)



@login_required
def delete_deliver(request, organization_id, deliver_id):
    user = request.user
    organization = Organization.objects.get(id=organization_id, active=True, 
                                                **first_viewable_dict)
    
    object = get_object_or_404(Deliver, pk=deliver_id, active=True,**viewable_dict)
    if request.method == 'POST':
        object.active = False
        object.save()
        return redirect('list_delivers', organization_id=organization_id)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'delete_deliver',
        'organization': organization,
        'organization_id': organization_id,
        
        'module_path': module_path,        
        'object': object,
        'page_title': f'Delete Deliver',
    }
    template_file = f"{app_name}/{module_path}/delete_deliver.html"
    return render(request, template_file, context)


@login_required
def permanent_deletion_deliver(request, organization_id, deliver_id):
    user = request.user
    organization = Organization.objects.get(id=organization_id, active=True, 
                                                **first_viewable_dict)
    
    object = get_object_or_404(Deliver, pk=deliver_id, active=False, deleted=False, **viewable_dict)
    if request.method == 'POST':
        object.active = False
        object.deleted = True
        object.save()
        return redirect('list_delivers', organization_id=organization_id)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'permanent_deletion_deliver',
        'organization': organization,
        'organization_id': organization_id,
        
        'module_path': module_path,        
        'object': object,
        'page_title': f'Permanent Deletion Deliver',
    }
    template_file = f"{app_name}/{module_path}/permanent_deletion_deliver.html"
    return render(request, template_file, context)


@login_required
def restore_deliver(request,  organization_id, deliver_id):
    user = request.user
    object = get_object_or_404(Deliver, pk=deliver_id, active=False,**viewable_dict)
    object.active = True
    object.save()
    return redirect('list_delivers', organization_id=organization_id)
   


@login_required
def view_deliver(request, organization_id, deliver_id):
    user = request.user
    organization = Organization.objects.get(id=organization_id, active=True, 
                                                **first_viewable_dict)
    
    object = get_object_or_404(Deliver, pk=deliver_id, active=True,**viewable_dict)    

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'view_deliver',
        'organization': organization,
        'organization_id': organization_id,
        
        'module_path': module_path,
        'object': object,
        'page_title': f'View Deliver',
    }
    template_file = f"{app_name}/{module_path}/view_deliver.html"
    return render(request, template_file, context)



@login_required
def deliver_dashboard(request, organization_id):
    user = request.user
    organization = Organization.objects.get(id=organization_id, active=True, 
                                                **first_viewable_dict)
    
    
    # Get total counts
    total_count = Deliver.objects.filter(organization_id=organization_id, **viewable_dict).count()
    active_count = Deliver.objects.filter(organization_id=organization_id, active=True, **viewable_dict).count()
    archived_count = Deliver.objects.filter(organization_id=organization_id, active=False, deleted=False, **viewable_dict).count()
    
    # Get recent items (created in last 30 days)
    thirty_days_ago = timezone.now() - timezone.timedelta(days=30)
    recent_count = Deliver.objects.filter(organization_id=organization_id, 
                                           created_at__gte=thirty_days_ago,
                                           **viewable_dict).count()
    
    # Get recent items for table display
    recent_items = Deliver.objects.filter(organization_id=organization_id, active=True, 
                                           **viewable_dict).order_by('-created_at')[:10]
    
    # Prepare chart data
    # 1. Timeline data - Items created per month for the last 6 months
    six_months_ago = timezone.now() - timezone.timedelta(days=180)
    items_by_month = Deliver.objects.filter(
        organization_id=organization_id,
        created_at__gte=six_months_ago,
        **viewable_dict
    ).annotate(
        month=TruncMonth('created_at')
    ).values('month').annotate(
        count=Count('id')
    ).order_by('month')
    
    # Format for Chart.js
    months = []
    counts = []
    
    # Get all months in the last 6 months period
    current_date = timezone.now().date().replace(day=1)
    date_list = []
    for i in range(6):
        new_date = current_date - timezone.timedelta(days=30*i)
        date_list.append(new_date)
    date_list.reverse()  # Oldest first
    
    # Format months and fill in zeroes for months with no data
    month_data = {item['month'].strftime('%Y-%m'): item['count'] for item in items_by_month}
    
    for date in date_list:
        month_key = date.strftime('%Y-%m')
        months.append(date.strftime('%b %Y'))
        counts.append(month_data.get(month_key, 0))
    
    # 2. Status distribution data
    status_labels = ['Active', 'Archived', 'Deleted']
    status_data = [
        active_count,
        archived_count,
        Deliver.objects.filter(organization_id=organization_id, deleted=True, **viewable_dict).count()
    ]
    
    # Prepare stats data
    stats = {
        'total': total_count,
        'active': active_count,
        'recent': recent_count,
        'archived': archived_count
    }
    
    # Prepare chart data dictionary
    chart_data = {
        'timeline_labels': months,
        'timeline_data': counts,
        'status_labels': status_labels,
        'status_data': status_data
    }
    
    # Convert to JSON for template
    import json
    chart_data_json = {
        'timeline_labels': json.dumps(months),
        'timeline_data': json.dumps(counts),
        'status_labels': json.dumps(status_labels),
        'status_data': json.dumps(status_data)
    }
    
    # Send outputs info, template
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'deliver_dashboard',
        'organization': organization,
        'organization_id': organization_id,
        
        'module_path': module_path,
        'module_title': 'Deliver',
        'user': user,
        'stats': stats,
        'recent_items': recent_items,
        'chart_data': chart_data_json,
        'page_title': 'Deliver Dashboard',
    }
    
    template_file = f"{app_name}/{module_path}/dashboard_deliver.html"
    return render(request, template_file, context)


@login_required
def deliver_settings(request, organization_id):
    user = request.user
    organization = Organization.objects.get(id=organization_id, active=True, 
                                                **first_viewable_dict)
    
    
    # Default settings
    default_settings = {
        'default_view': 'list',
        'items_per_page': 25,
        'enable_notifications': False,
        'date_format': 'MM/DD/YYYY',
        'theme': 'light',
        'email_integration_enabled': False,
        'api_enabled': False,
        'calendar_integration_enabled': False,
        'caching_strategy': 'normal',
        'logging_level': 'error',
        'debug_mode': False
    }
    
    # Get user settings from database or session
    # For demonstration purposes, we'll use default settings
    # In a real application, you might load these from the database
    settings = default_settings
    
    # Handle form submissions
    if request.method == 'POST':
        # Determine which form was submitted based on request data
        if 'default_view' in request.POST:
            # General settings form
            settings['default_view'] = request.POST.get('default_view')
            settings['items_per_page'] = int(request.POST.get('items_per_page', 25))
            settings['enable_notifications'] = 'enable_notifications' in request.POST
            settings['date_format'] = request.POST.get('date_format')
            messages.success(request, 'General settings updated successfully.')
            
        elif 'theme' in request.POST:
            # Display settings form
            settings['theme'] = request.POST.get('theme')
            # Handle visible columns (would be stored as a list/array)
            messages.success(request, 'Display settings updated successfully.')
            
        elif 'default_role' in request.POST:
            # Permissions settings form
            settings['default_role'] = request.POST.get('default_role')
            messages.success(request, 'Permission settings updated successfully.')
            
        elif 'email_integration_enabled' in request.POST:
            # Integration settings form
            settings['email_integration_enabled'] = 'email_integration_enabled' in request.POST
            settings['email_template'] = request.POST.get('email_template')
            settings['api_enabled'] = 'api_enabled' in request.POST
            settings['calendar_integration_enabled'] = 'calendar_integration_enabled' in request.POST
            settings['calendar_provider'] = request.POST.get('calendar_provider')
            messages.success(request, 'Integration settings updated successfully.')
            
        elif 'caching_strategy' in request.POST:
            # Advanced settings form
            settings['caching_strategy'] = request.POST.get('caching_strategy')
            settings['logging_level'] = request.POST.get('logging_level')
            settings['debug_mode'] = 'debug_mode' in request.POST
            messages.success(request, 'Advanced settings updated successfully.')
        
        # Save settings to database or session
        # In a real application, this would save to a database
        # For this example, we'll just update our settings dictionary
        
        # Redirect to avoid form resubmission
        return redirect('deliver_settings', organization_id=organization_id)
    
    # Send outputs info, template
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'deliver_settings',
        'organization': organization,
        'organization_id': organization_id,
        
        'module_path': module_path,
        'module_title': 'Deliver',
        'user': user,
        'settings': settings,
        'page_title': 'Deliver Settings',
    }
    
    template_file = f"{app_name}/{module_path}/settings_deliver.html"
    return render(request, template_file, context)

