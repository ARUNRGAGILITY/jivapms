from app_scrum_product.mod_app.all_view_imports import *

# Import models from other modules to display their data
# These imports will need to be updated once those modules are implemented
try:
    from app_scrum_product.mod_scrum_product.models_scrum_product import ScrumProduct
    from app_scrum_product.mod_scrum_product_sprint.models_scrum_product_sprint import ScrumProductSprint
    from app_scrum_product.mod_scrum_product_release.models_scrum_product_release import ScrumProductRelease
    from app_scrum_product.mod_scrum_product_team.models_scrum_product_team import ScrumProductTeam
except ImportError:
    # Define placeholder models for development
    ScrumProduct = None
    ScrumProductSprint = None
    ScrumProductRelease = None
    ScrumProductTeam = None

@login_required
def scrum_product_home(request):
    """
    Main home/dashboard view for the Scrum Product module.
    Displays overview of products, sprints, releases, and team information.
    """
    # Get the user
    user = request.user
    
    # Sample data - replace with actual data when models are implemented
    active_products = []
    active_sprints = []
    upcoming_releases = []
    team_members = []
    
    try:
        if ScrumProduct:
            active_products = ScrumProduct.objects.filter(active=True).order_by('-created_at')[:5]
        if ScrumProductSprint:
            active_sprints = ScrumProductSprint.objects.filter(active=True, status='in_progress').order_by('end_date')[:5]
        if ScrumProductRelease:
            upcoming_releases = ScrumProductRelease.objects.filter(active=True, status='planned').order_by('release_date')[:5]
        if ScrumProductTeam:
            team_members = ScrumProductTeam.objects.filter(active=True).order_by('name')[:10]
    except Exception as e:
        # Handle any errors when the models aren't fully implemented
        logger.error(f"Error fetching data for scrum product home: {e}")
    
    # If models aren't implemented yet, use sample data for development
    if not active_products:
        active_products = [
            {'id': 1, 'name': 'Customer Portal', 'description': 'Web application for customer self-service', 'progress': 65},
            {'id': 2, 'name': 'Mobile App', 'description': 'iOS and Android mobile application', 'progress': 42},
            {'id': 3, 'name': 'API Gateway', 'description': 'Centralized API management system', 'progress': 78},
            {'id': 4, 'name': 'Admin Dashboard', 'description': 'Internal administration tool', 'progress': 31},
        ]
    
    if not active_sprints:
        active_sprints = [
            {'id': 1, 'name': 'Sprint 24', 'product': 'Customer Portal', 'start_date': '2025-04-01', 'end_date': '2025-04-14', 'progress': 50},
            {'id': 2, 'name': 'Sprint 8', 'product': 'Mobile App', 'start_date': '2025-04-03', 'end_date': '2025-04-17', 'progress': 30},
            {'id': 3, 'name': 'Sprint 16', 'product': 'API Gateway', 'start_date': '2025-03-28', 'end_date': '2025-04-11', 'progress': 75},
        ]
    
    if not upcoming_releases:
        upcoming_releases = [
            {'id': 1, 'name': 'v2.5.0', 'product': 'Customer Portal', 'release_date': '2025-05-15', 'status': 'Planned'},
            {'id': 2, 'name': 'v1.2.0', 'product': 'Mobile App', 'release_date': '2025-04-30', 'status': 'In Development'},
            {'id': 3, 'name': 'v3.0.0', 'product': 'API Gateway', 'release_date': '2025-06-10', 'status': 'Planned'},
        ]
    
    if not team_members:
        team_members = [
            {'id': 1, 'name': 'John Doe', 'role': 'Product Owner', 'product': 'Customer Portal'},
            {'id': 2, 'name': 'Jane Smith', 'role': 'Scrum Master', 'product': 'Customer Portal'},
            {'id': 3, 'name': 'Bob Johnson', 'role': 'Developer', 'product': 'Mobile App'},
            {'id': 4, 'name': 'Alice Williams', 'role': 'Product Owner', 'product': 'Mobile App'},
            {'id': 5, 'name': 'Charlie Brown', 'role': 'QA Engineer', 'product': 'API Gateway'},
        ]
    
    # Prepare chart data
    product_progress_data = {
        'labels': [product['name'] for product in active_products],
        'data': [product['progress'] for product in active_products]
    }
    
    sprint_burndown_data = {
        'labels': ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5', 'Day 6', 'Day 7', 'Day 8', 'Day 9', 'Day 10'],
        'ideal': [100, 90, 80, 70, 60, 50, 40, 30, 20, 10, 0],
        'actual': [100, 95, 92, 85, 80, 70, 65, 55, 40, 30]
    }
    
    velocity_data = {
        'labels': ['Sprint 19', 'Sprint 20', 'Sprint 21', 'Sprint 22', 'Sprint 23', 'Sprint 24'],
        'commitment': [80, 75, 85, 90, 85, 90],
        'completed': [65, 70, 80, 85, 80, 45]  # Last sprint in progress
    }
    
    context = {
        'user': user,
        'page_title': 'Scrum Product Home',
        'active_products': active_products,
        'active_sprints': active_sprints,
        'upcoming_releases': upcoming_releases,
        'team_members': team_members,
        'product_progress_data': product_progress_data,
        'sprint_burndown_data': sprint_burndown_data,
        'velocity_data': velocity_data,
    }
    
    # Make sure Django finds the template by using the correct path
    template_file = 'app_scrum_product/mod_scrum_product_home/scrum_product_home.html'
    return render(request, template_file, context)

@login_required
def scrum_product_home_overview(request, product_id=None):
    """
    Detailed overview for a specific product. If no product_id is provided,
    shows a summary of all products.
    """
    user = request.user
    
    # Sample product data - replace with actual data when models are implemented
    product = None
    sprints = []
    releases = []
    team = []
    
    try:
        if product_id and ScrumProduct:
            product = ScrumProduct.objects.get(id=product_id, active=True)
            
            if ScrumProductSprint:
                sprints = ScrumProductSprint.objects.filter(product=product, active=True).order_by('-end_date')[:10]
            
            if ScrumProductRelease:
                releases = ScrumProductRelease.objects.filter(product=product, active=True).order_by('release_date')[:5]
            
            if ScrumProductTeam:
                team = ScrumProductTeam.objects.filter(product=product, active=True).order_by('name')
    except Exception as e:
        # Handle any errors when the models aren't fully implemented
        logger.error(f"Error fetching product overview data: {e}")
    
    # If models aren't implemented yet, use sample data for development
    if not product:
        product = {
            'id': 1, 
            'name': 'Customer Portal', 
            'description': 'Web application for customer self-service',
            'status': 'Active',
            'progress': 65,
            'start_date': '2025-01-15',
            'target_end_date': '2025-12-31',
            'product_owner': 'John Doe',
            'scrum_master': 'Jane Smith'
        }
    
    if not sprints:
        sprints = [
            {'id': 1, 'name': 'Sprint 24', 'start_date': '2025-04-01', 'end_date': '2025-04-14', 'status': 'In Progress', 'progress': 50},
            {'id': 2, 'name': 'Sprint 23', 'start_date': '2025-03-18', 'end_date': '2025-03-31', 'status': 'Completed', 'progress': 100},
            {'id': 3, 'name': 'Sprint 22', 'start_date': '2025-03-04', 'end_date': '2025-03-17', 'status': 'Completed', 'progress': 95},
        ]
    
    if not releases:
        releases = [
            {'id': 1, 'name': 'v2.5.0', 'release_date': '2025-05-15', 'status': 'Planned', 'progress': 30},
            {'id': 2, 'name': 'v2.4.0', 'release_date': '2025-03-30', 'status': 'Released', 'progress': 100},
            {'id': 3, 'name': 'v2.3.0', 'release_date': '2025-02-15', 'status': 'Released', 'progress': 100},
        ]
    
    if not team:
        team = [
            {'id': 1, 'name': 'John Doe', 'role': 'Product Owner', 'allocation': 100},
            {'id': 2, 'name': 'Jane Smith', 'role': 'Scrum Master', 'allocation': 100},
            {'id': 3, 'name': 'Bob Johnson', 'role': 'Senior Developer', 'allocation': 100},
            {'id': 4, 'name': 'Alice Williams', 'role': 'Developer', 'allocation': 75},
            {'id': 5, 'name': 'Charlie Brown', 'role': 'QA Engineer', 'allocation': 100},
            {'id': 6, 'name': 'Eva Davis', 'role': 'UX Designer', 'allocation': 50},
        ]
    
    context = {
        'user': user,
        'page_title': f'Product Overview: {product["name"] if isinstance(product, dict) else product.name}',
        'product': product,
        'sprints': sprints,
        'releases': releases,
        'team': team,
    }
    
    # Make sure Django finds the template by using the correct path
    template_file = 'app_scrum_product/mod_scrum_product_home/scrum_product_overview.html'
    return render(request, template_file, context)