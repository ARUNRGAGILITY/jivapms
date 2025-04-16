from app_scrum_product.mod_app.all_view_imports import *

# Import models from other modules to display their data
# These imports will need to be updated once those modules are implemented
try:
    from app_scrum_product.mod_scrum_product.models_scrum_product import ScrumProduct
    from app_scrum_product.mod_scrum_product_sprint.models_scrum_product_sprint import ScrumProductSprint
    from app_scrum_product.mod_scrum_product_release.models_scrum_product_release import ScrumProductRelease
    from app_scrum_product.mod_scrum_product_team.models_scrum_product_team import ScrumProductTeam
    from app_scrum_product.mod_scrum_event.models_scrum_event import ScrumEvent
except ImportError:
    # Define placeholder models for development
    ScrumProduct = None
    ScrumProductSprint = None
    ScrumProductRelease = None
    ScrumProductTeam = None
    ScrumEvent = None

@login_required
def scrum_products_dashboard(request):
    """
    Main dashboard view for all Scrum Products.
    Displays overview of all products, active sprints, upcoming releases, and events.
    """
    # Get the user
    user = request.user
    
    # Sample data - replace with actual data when models are implemented
    all_products = []
    active_sprints = []
    upcoming_releases = []
    upcoming_events = []
    team_members = []
    
    try:
        if ScrumProduct:
            all_products = ScrumProduct.objects.filter(active=True).order_by('-created_at')
        if ScrumProductSprint:
            active_sprints = ScrumProductSprint.objects.filter(active=True, status='in_progress').order_by('end_date')[:5]
        if ScrumProductRelease:
            upcoming_releases = ScrumProductRelease.objects.filter(active=True, status='planned').order_by('release_date')[:5]
        if ScrumProductTeam:
            team_members = ScrumProductTeam.objects.filter(active=True).order_by('name')[:10]
        if ScrumEvent:
            upcoming_events = ScrumEvent.objects.filter(active=True, date__gte=timezone.now()).order_by('date')[:5]
    except Exception as e:
        # Handle any errors when the models aren't fully implemented
        logger.error(f"Error fetching data for scrum products dashboard: {e}")
    
    # If models aren't implemented yet, use sample data for development
    if not all_products:
        all_products = [
            {'id': 1, 'name': 'Customer Portal', 'description': 'Web application for customer self-service', 'progress': 65, 'status': 'Active', 'sprints_completed': 23, 'team_size': 8},
            {'id': 2, 'name': 'Mobile App', 'description': 'iOS and Android mobile application', 'progress': 42, 'status': 'Active', 'sprints_completed': 7, 'team_size': 6},
            {'id': 3, 'name': 'API Gateway', 'description': 'Centralized API management system', 'progress': 78, 'status': 'Active', 'sprints_completed': 15, 'team_size': 5},
            {'id': 4, 'name': 'Admin Dashboard', 'description': 'Internal administration tool', 'progress': 31, 'status': 'Active', 'sprints_completed': 6, 'team_size': 4},
            {'id': 5, 'name': 'Data Analytics Platform', 'description': 'Business intelligence platform', 'progress': 90, 'status': 'Maintenance', 'sprints_completed': 35, 'team_size': 3},
            {'id': 6, 'name': 'Legacy System Integration', 'description': 'Integration with legacy systems', 'progress': 100, 'status': 'Completed', 'sprints_completed': 18, 'team_size': 0},
        ]
    
    if not active_sprints:
        active_sprints = [
            {'id': 1, 'name': 'Sprint 24', 'product': 'Customer Portal', 'start_date': '2025-04-01', 'end_date': '2025-04-14', 'progress': 50},
            {'id': 2, 'name': 'Sprint 8', 'product': 'Mobile App', 'start_date': '2025-04-03', 'end_date': '2025-04-17', 'progress': 30},
            {'id': 3, 'name': 'Sprint 16', 'product': 'API Gateway', 'start_date': '2025-03-28', 'end_date': '2025-04-11', 'progress': 75},
            {'id': 4, 'name': 'Sprint 7', 'product': 'Admin Dashboard', 'start_date': '2025-04-05', 'end_date': '2025-04-19', 'progress': 20},
        ]
    
    if not upcoming_releases:
        upcoming_releases = [
            {'id': 1, 'name': 'v2.5.0', 'product': 'Customer Portal', 'release_date': '2025-05-15', 'status': 'Planned'},
            {'id': 2, 'name': 'v1.2.0', 'product': 'Mobile App', 'release_date': '2025-04-30', 'status': 'In Development'},
            {'id': 3, 'name': 'v3.0.0', 'product': 'API Gateway', 'release_date': '2025-06-10', 'status': 'Planned'},
            {'id': 4, 'name': 'v1.0.0', 'product': 'Admin Dashboard', 'release_date': '2025-05-20', 'status': 'In Development'},
        ]
    
    if not upcoming_events:
        upcoming_events = [
            {'id': 1, 'name': 'Sprint Planning', 'date': '2025-04-15', 'time': '10:00 AM', 'product': 'Customer Portal', 'type': 'Sprint Event'},
            {'id': 2, 'name': 'Product Demo', 'date': '2025-04-14', 'time': '2:00 PM', 'product': 'Mobile App', 'type': 'Demo'},
            {'id': 3, 'name': 'Retrospective', 'date': '2025-04-12', 'time': '11:00 AM', 'product': 'API Gateway', 'type': 'Sprint Event'},
            {'id': 4, 'name': 'Stakeholder Meeting', 'date': '2025-04-18', 'time': '9:00 AM', 'product': 'All Products', 'type': 'Business'},
        ]
    
    if not team_members:
        team_members = [
            {'id': 1, 'name': 'John Doe', 'role': 'Product Owner', 'product': 'Customer Portal', 'assignments': 1},
            {'id': 2, 'name': 'Jane Smith', 'role': 'Scrum Master', 'product': 'Customer Portal', 'assignments': 2},
            {'id': 3, 'name': 'Bob Johnson', 'role': 'Developer', 'product': 'Mobile App', 'assignments': 1},
            {'id': 4, 'name': 'Alice Williams', 'role': 'Product Owner', 'product': 'Mobile App', 'assignments': 1},
            {'id': 5, 'name': 'Charlie Brown', 'role': 'QA Engineer', 'product': 'API Gateway', 'assignments': 1},
        ]
    
    # Count statistics
    product_counts = {
        'total': len(all_products),
        'active': len([p for p in all_products if p['status'] == 'Active']),
        'maintenance': len([p for p in all_products if p['status'] == 'Maintenance']),
        'completed': len([p for p in all_products if p['status'] == 'Completed']),
    }
    
    # Prepare data for product status chart
    product_status_chart = {
        'labels': ['Active', 'Maintenance', 'Completed'],
        'data': [product_counts['active'], product_counts['maintenance'], product_counts['completed']]
    }
    
    # Prepare data for team allocation chart
    team_allocation_data = {}
    for member in team_members:
        product = member['product']
        if product in team_allocation_data:
            team_allocation_data[product] += 1
        else:
            team_allocation_data[product] = 1
    
    team_allocation_chart = {
        'labels': list(team_allocation_data.keys()),
        'data': list(team_allocation_data.values())
    }
    
    # Prepare activity data (monthly product progress)
    monthly_progress = [
        {'month': 'Jan', 'completed': 12, 'planned': 15},
        {'month': 'Feb', 'completed': 18, 'planned': 20},
        {'month': 'Mar', 'completed': 22, 'planned': 25},
        {'month': 'Apr', 'completed': 10, 'planned': 30},  # Current month (in progress)
    ]
    
    activity_chart = {
        'labels': [item['month'] for item in monthly_progress],
        'completed': [item['completed'] for item in monthly_progress],
        'planned': [item['planned'] for item in monthly_progress],
    }
    
    context = {
        'user': user,
        'page_title': 'Scrum Products Dashboard',
        'all_products': all_products,
        'active_sprints': active_sprints,
        'upcoming_releases': upcoming_releases,
        'upcoming_events': upcoming_events,
        'team_members': team_members,
        'product_counts': product_counts,
        'product_status_chart': product_status_chart,
        'team_allocation_chart': team_allocation_chart,
        'activity_chart': activity_chart,
    }
    
    template_file = 'app_scrum_product/mod_scrum_product_dashboard/scrum_products_dashboard.html'
    return render(request, template_file, context)

@login_required
def scrum_dashboard_analytics(request):
    """
    Analytics view showing detailed metrics for all scrum products.
    """
    user = request.user
    
    # Sample metrics data - replace with actual data when models are implemented
    sprint_velocity_data = {
        'labels': ['Jan', 'Feb', 'Mar', 'Apr'],
        'datasets': [
            {
                'label': 'Customer Portal',
                'data': [45, 55, 60, 58]
            },
            {
                'label': 'Mobile App',
                'data': [25, 30, 35, 40]
            },
            {
                'label': 'API Gateway',
                'data': [50, 55, 60, 65]
            }
        ]
    }
    
    story_completion_rate = {
        'labels': ['Customer Portal', 'Mobile App', 'API Gateway', 'Admin Dashboard'],
        'planned': [120, 85, 95, 60],
        'completed': [110, 70, 90, 45]
    }
    
    defect_trends = {
        'labels': ['Jan', 'Feb', 'Mar', 'Apr'],
        'found': [35, 25, 30, 15],
        'resolved': [25, 30, 20, 10]
    }
    
    resource_allocation = {
        'labels': ['Development', 'Testing', 'Design', 'Documentation', 'Management'],
        'data': [45, 25, 15, 10, 5]
    }
    
    context = {
        'user': user,
        'page_title': 'Scrum Dashboard Analytics',
        'sprint_velocity_data': sprint_velocity_data,
        'story_completion_rate': story_completion_rate,
        'defect_trends': defect_trends,
        'resource_allocation': resource_allocation,
    }
    
    template_file = 'app_scrum_product/mod_scrum_product_dashboard/scrum_dashboard_analytics.html'
    return render(request, template_file, context)