"""
Template Python file definitions for CRUD_TOP_LEVEL
Contains all Python template strings for models, forms, views, and urls
"""

# Models template
models_template = """
from ___APPNAME___.mod_app.all_model_imports import *
from app_common.mod_common.models_common import *

class ___MODELNAME___(BaseModelImpl):
    #org = models.ForeignKey('', on_delete=models.CASCADE, related_name="org_")
    
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="author____MODELNAME___")
    
    # Additional fields
    status = models.CharField(max_length=50, default='new', choices=[
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('on_hold', 'On Hold'),
    ])
    
    # Dates
    due_date = models.DateField(null=True, blank=True)
    
    # Metadata
    tags = models.CharField(max_length=200, null=True, blank=True, 
                           help_text="Comma separated tags")
    priority = models.IntegerField(default=0, 
                                 help_text="Priority (0-100, higher = more important)")
        
    def __str__(self):
        return self.name
"""

# Forms template
forms_template = """
from ___APPNAME___.mod_app.all_form_imports import *
from ___APPNAME___.mod____singularmodname___.models____singularmodname___ import *

class ___MODELNAME___Form(forms.ModelForm):
    class Meta:
        model = ___MODELNAME___
        fields = ['name', 'description', 'status', 'due_date', 'priority', 'tags']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'tags': forms.TextInput(attrs={'placeholder': 'tag1, tag2, tag3'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }
        
    def __init__(self, *args, **kwargs):
        super(___MODELNAME___Form, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
"""

# Views templates
views_header = """
from ___APPNAME___.mod_app.all_view_imports import *
from ___APPNAME___.mod____singularmodname___.models____singularmodname___ import *
from ___APPNAME___.mod____singularmodname___.forms____singularmodname___ import *

app_name = '___APPNAME___'
app_version = '___appversion___'

module_name = '___pluralmodname___'
module_path = f'___modulepath___'

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
"""

list_objects_view = """
# ============================================================= #
@login_required
def list____pluralmodname___(request):
    # take inputs
    # process inputs
    user = request.user       
    objects_count = 0    
    show_all = request.GET.get('all', '25')
    objects_per_page = int(show_all) if show_all != 'all' else 25
    pagination_options = [5, 10, 15, 25, 50, 100, 'all']
    selected_bulk_operations = None
    search_query = request.GET.get('search', '')
    deleted_count = 0
    
    if search_query:
        tobjects = ___MODELNAME___.objects.filter(name__icontains=search_query, 
                                        active=True,deleted=False, **viewable_dict ).order_by('position')
        deleted = ___MODELNAME___.objects.filter(active=False, deleted=False,**viewable_dict).order_by('position')
        deleted_count = deleted.count()
    else:
        tobjects = ___MODELNAME___.objects.filter(active=True).order_by('position')
        deleted = ___MODELNAME___.objects.filter(active=False, deleted=False,**viewable_dict).order_by('position')
        deleted_count = deleted.count()
    
    if show_all == 'all':
        # No pagination, show all records
        page_obj = tobjects
        objects_per_page = tobjects.count()
    else:
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
                    object = get_object_or_404(___MODELNAME___, pk=item, active=True, **viewable_dict)
                    object.active = False
                    object.save()
                    
                elif bulk_operation == 'bulk_done':
                    object = get_object_or_404(___MODELNAME___, pk=item, active=True, **viewable_dict)
                    object.done = True
                    object.save()
                    
                elif bulk_operation == 'bulk_not_done':
                    object = get_object_or_404(___MODELNAME___, pk=item, active=True, **viewable_dict)
                    object.done = False
                    object.save()
                    
                elif bulk_operation == 'bulk_blocked':  # Correct the operation check here
                    object = get_object_or_404(___MODELNAME___, pk=item, active=True, **viewable_dict)
                    object.blocked = True
                    object.save()
                    
                else:
                    redirect('list____pluralmodname___')
            return redirect('list____pluralmodname___')
    
    
    # send outputs info, template,
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'list____pluralmodname___',
        
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

        'page_title': f'___MODNAME___ List',
    }       
    template_file = f"{app_name}/{module_path}/list____pluralmodname___.html"
    return render(request, template_file, context)
"""

list_deleted_objects_view = """
# list the deleted objects
# ============================================================= #
@login_required
def list_deleted____pluralmodname___(request):
    # take inputs
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
    if search_query:
        tobjects = ___MODELNAME___.objects.filter(name__icontains=search_query, 
                                        **viewable_dict, active=False, deleted=False).order_by('position')
    else:
        tobjects = ___MODELNAME___.objects.filter(active=False, deleted=False, **viewable_dict).order_by('position')
    
    if show_all == 'all':
        # No pagination, show all records
        page_obj = tobjects
        objects_per_page = tobjects.count()
    else: 
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
                        object = get_object_or_404(___MODELNAME___, pk=item, active=False, **viewable_dict)
                        object.active = True               
                        object.save()
                    elif bulk_operation == 'bulk_erase':
                        object = get_object_or_404(___MODELNAME___, pk=item, active=False, **viewable_dict)
                        object.active = False  
                        object.deleted = True             
                        object.save()
                    else:
                        redirect('list_deleted____pluralmodname___')
                return redirect('list_deleted____pluralmodname___')
    
    
    # send outputs info, template,
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'list_deleted____pluralmodname___',
        
        'module_path': module_path,
        'user': user,
        'tobjects': tobjects,
        'page_obj': page_obj,
        'objects_count': objects_count,
        'objects_per_page': objects_per_page,
        'show_all': show_all,
        'pagination_options': pagination_options,
        'selected_bulk_operations': selected_bulk_operations,

        'page_title': f'___MODNAME___ List',
    }       
    template_file = f"{app_name}/{module_path}/list_deleted____pluralmodname___.html"
    return render(request, template_file, context)
"""

create_object_view = """
# Create View
@login_required
def create____singularmodname___(request):
    user = request.user
    
    if request.method == 'POST':
        form = ___MODELNAME___Form(request.POST)
        if form.is_valid():
            form.instance.author = user
            form.save()
        else:
            print(f">>> === form.errors: {form.errors} === <<<")
        return redirect('list____pluralmodname___')
    else:
        form = ___MODELNAME___Form()

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'create____singularmodname___',
        
        'module_path': module_path,
        'form': form,
        'page_title': f'Create ___DISPMODNAMESINGULAR___',
    }
    template_file = f"{app_name}/{module_path}/create____singularmodname___.html"
    return render(request, template_file, context)
"""

view_object_view = """
@login_required
def view____singularmodname___(request,  ___directid___):
    user = request.user
    
    object = get_object_or_404(___MODELNAME___, pk=___directid___, active=True, **viewable_dict)    

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'view____singularmodname___',
        
        'module_path': module_path,
        'object': object,
        'page_title': f'View ___DISPMODNAMESINGULAR___',
    }
    template_file = f"{app_name}/{module_path}/view____singularmodname___.html"
    return render(request, template_file, context)
"""

edit_object_view = """
# Edit
@login_required
def edit____singularmodname___(request, ___directid___):
    user = request.user
    
    object = get_object_or_404(___MODELNAME___, pk=___directid___, active=True, **viewable_dict)
    if request.method == 'POST':
        form = ___MODELNAME___Form(request.POST, instance=object)
        if form.is_valid():
            form.instance.author = user
            form.save()
        else:
            print(f">>> === form.errors: {form.errors} === <<<")
        return redirect('list____pluralmodname___')
    else:
        form = ___MODELNAME___Form(instance=object)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'edit____singularmodname___',
        
        'module_path': module_path,
        'form': form,
        'object': object,
        'page_title': f'Edit ___DISPMODNAMESINGULAR___',
    }
    template_file = f"{app_name}/{module_path}/edit____singularmodname___.html"
    return render(request, template_file, context)
"""

delete_object_view = """
@login_required
def delete____singularmodname___(request, ___directid___):
    user = request.user
    
    object = get_object_or_404(___MODELNAME___, pk=___directid___, active=True, **viewable_dict)
    if request.method == 'POST':
        object.active = False
        object.save()
        return redirect('list____pluralmodname___')

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'delete____singularmodname___',
        
        'module_path': module_path,        
        'object': object,
        'page_title': f'Delete ___DISPMODNAMESINGULAR___',
    }
    template_file = f"{app_name}/{module_path}/delete____singularmodname___.html"
    return render(request, template_file, context)
"""

restore_object_view = """
@login_required
def restore____singularmodname___(request, ___directid___):
    user = request.user
    object = get_object_or_404(___MODELNAME___, pk=___directid___, active=False, **viewable_dict)
    object.active = True
    object.save()
    return redirect('list____pluralmodname___')
"""

permanent_deletion_object_view = """
@login_required
def permanent_deletion____singularmodname___(request, ___directid___):
    user = request.user
    
    object = get_object_or_404(___MODELNAME___, pk=___directid___, active=False, deleted=False, **viewable_dict)
    if request.method == 'POST':
        object.active = False
        object.deleted = True
        object.save()
        return redirect('list____pluralmodname___')

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'permanent_deletion____singularmodname___',
        
        'module_path': module_path,        
        'object': object,
        'page_title': f'Permanent Deletion ___DISPMODNAMESINGULAR___',
    }
    template_file = f"{app_name}/{module_path}/permanent_deletion____singularmodname___.html"
    return render(request, template_file, context)
"""

# New dashboard view
dashboard_view = """
@login_required
def ___singularmodname____dashboard(request):
    user = request.user
    
    # Get total counts
    total_count = ___MODELNAME___.objects.filter(**viewable_dict).count()
    active_count = ___MODELNAME___.objects.filter(active=True, **viewable_dict).count()
    archived_count = ___MODELNAME___.objects.filter(active=False, deleted=False, **viewable_dict).count()
    
    # Get recent items (created in last 30 days)
    thirty_days_ago = timezone.now() - timezone.timedelta(days=30)
    recent_count = ___MODELNAME___.objects.filter(
                                       created_at__gte=thirty_days_ago,
                                       **viewable_dict).count()
    
    # Get recent items for table display
    recent_items = ___MODELNAME___.objects.filter(active=True, 
                                       **viewable_dict).order_by('-created_at')[:10]
    
    # Prepare chart data
    # 1. Timeline data - Items created per month for the last 6 months
    six_months_ago = timezone.now() - timezone.timedelta(days=180)
    items_by_month = ___MODELNAME___.objects.filter(
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
        ___MODELNAME___.objects.filter(deleted=True, **viewable_dict).count()
    ]
    
    # 3. Status breakdown
    status_breakdown = ___MODELNAME___.objects.filter(
        active=True, 
        **viewable_dict
    ).values('status').annotate(
        count=Count('id')
    ).order_by('status')
    
    status_breakdown_labels = []
    status_breakdown_data = []
    status_colors = []
    
    for item in status_breakdown:
        status_breakdown_labels.append(item['status'].replace('_', ' ').title())
        status_breakdown_data.append(item['count'])
    
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
        'status_data': status_data,
        'status_breakdown_labels': status_breakdown_labels,
        'status_breakdown_data': status_breakdown_data
    }
    
    # Convert to JSON for template
    import json
    chart_data_json = {
        'timeline_labels': json.dumps(months),
        'timeline_data': json.dumps(counts),
        'status_labels': json.dumps(status_labels),
        'status_data': json.dumps(status_data),
        'status_breakdown_labels': json.dumps(status_breakdown_labels),
        'status_breakdown_data': json.dumps(status_breakdown_data)
    }
    
    # Send outputs info, template
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': '___singularmodname____dashboard',
        
        'module_path': module_path,
        'module_title': '___DISPMODNAMESINGULAR___',
        'user': user,
        'stats': stats,
        'recent_items': recent_items,
        'chart_data': chart_data_json,
        'page_title': '___DISPMODNAMESINGULAR___ Dashboard',
    }
    
    template_file = f"{app_name}/{module_path}/dashboard____singularmodname___.html"
    return render(request, template_file, context)
"""

# New settings view
settings_view = """
@login_required
def ___singularmodname____settings(request):
    user = request.user
    
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
        return redirect('___singularmodname____settings')
    
    # Send outputs info, template
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': '___singularmodname____settings',
        
        'module_path': module_path,
        'module_title': '___DISPMODNAMESINGULAR___',
        'user': user,
        'settings': settings,
        'page_title': '___DISPMODNAMESINGULAR___ Settings',
    }
    
    template_file = f"{app_name}/{module_path}/settings____singularmodname___.html"
    return render(request, template_file, context)
"""

# URLs template
urls_template = """
from django.urls import path, include

from ___APPNAME___.mod____singularmodname___ import views____singularmodname___

urlpatterns = [
    # ___APPNAME___/___pluralmodname___: DB/Model: ___MODELNAME___
    # List and CRUD operations
    path('list____pluralmodname___/', views____singularmodname___.list____pluralmodname___, name='list____pluralmodname___'),
    path('list_deleted____pluralmodname___/', views____singularmodname___.list_deleted____pluralmodname___, name='list_deleted____pluralmodname___'),
    path('create____singularmodname___/', views____singularmodname___.create____singularmodname___, name='create____singularmodname___'),
    path('edit____singularmodname___/<int:___directid___>/', views____singularmodname___.edit____singularmodname___, name='edit____singularmodname___'),
    path('delete____singularmodname___/<int:___directid___>/', views____singularmodname___.delete____singularmodname___, name='delete____singularmodname___'),
    path('permanent_deletion____singularmodname___/<int:___directid___>/', views____singularmodname___.permanent_deletion____singularmodname___, name='permanent_deletion____singularmodname___'),
    path('restore____singularmodname___/<int:___directid___>/', views____singularmodname___.restore____singularmodname___, name='restore____singularmodname___'),
    path('view____singularmodname___/<int:___directid___>/', views____singularmodname___.view____singularmodname___, name='view____singularmodname___'),
    
    # Dashboard and settings
    path('___singularmodname____dashboard/', views____singularmodname___.___singularmodname____dashboard, name='___singularmodname____dashboard'),
    path('___singularmodname____settings/', views____singularmodname___.___singularmodname____settings, name='___singularmodname____settings'),
]
"""

# Export all templates
__all__ = [
    'models_template',
    'forms_template',
    'views_header',
    'list_objects_view',
    'list_deleted_objects_view',
    'create_object_view',
    'view_object_view',
    'edit_object_view',
    'delete_object_view',
    'restore_object_view',
    'permanent_deletion_object_view',
    'dashboard_view',
    'settings_view',
    'urls_template',
]