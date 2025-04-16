from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone

# Try to import models from other modules
try:
    from app_scrum.mod_app.all_view_imports import *
    from app_scrum.mod_project.models_project import Project
    from app_scrum.mod_product.models_product import Product
    from app_scrum.mod_solution.models_solution import Solution
    from app_scrum.mod_consulting.models_consulting import Consulting
    from app_scrum.mod_sprint.models_sprint import Sprint
    from app_scrum.mod_backlog.models_backlog import Backlog
    from app_scrum.mod_team.models_team import Team
    
except ImportError:
    # If models are not implemented yet, use None as placeholders
    Project = None
    Product = None
    Solution = None
    Consulting = None
    Sprint = None
    Backlog = None
    Team = None

@login_required
def scrum_dashboard(request):
    """
    Main dashboard view for the Scrum app that shows an overview of 
    all projects, products, solutions, and consulting engagements.
    """
    # Get the user
    user = request.user
    
    # GLOBAL DELIVERY TYPES
    global_delivery_types = GLOBAL_DELIVERY_TYPES
    # Sample data - replace with actual data when models are implemented
    projects = []
    products = []
    solutions = []
    consulting = []
    active_sprints = []
    recent_backlogs = []
    teams = []
    
    try:
        # Try to fetch data from actual models if they exist
        if Project:
            projects = Project.objects.filter(active=True).order_by('-created_at')[:5]
        
        if Product:
            products = Product.objects.filter(active=True).order_by('-created_at')[:5]
        
        if Solution:
            solutions = Solution.objects.filter(active=True).order_by('-created_at')[:5]
        
        if Consulting:
            consulting = Consulting.objects.filter(active=True).order_by('-created_at')[:5]
        
        if Sprint:
            active_sprints = Sprint.objects.filter(
                active=True, 
                start_date__lte=timezone.now(),
                end_date__gte=timezone.now()
            ).order_by('end_date')[:5]
        
        if Backlog:
            recent_backlogs = Backlog.objects.filter(active=True).order_by('-created_at')[:10]
        
        if Team:
            teams = Team.objects.filter(active=True).order_by('name')[:5]
            
    except Exception as e:
        # Log any errors for debugging
        print(f"Error fetching data for scrum dashboard: {e}")
    
    # If no data from models yet, use sample data for development
    if not projects:
        projects = [
            {'id': 1, 'name': 'E-Commerce Platform Upgrade', 'description': 'Major upgrade of the existing platform', 'status': 'In Progress', 'progress': 60, 'owner': 'John Smith'},
            {'id': 2, 'name': 'Mobile App Development', 'description': 'New mobile app for customers', 'status': 'Planning', 'progress': 25, 'owner': 'Sarah Johnson'},
            {'id': 3, 'name': 'Data Migration Project', 'description': 'Migrating legacy data to new system', 'status': 'In Progress', 'progress': 45, 'owner': 'David Lee'},
        ]
    
    if not products:
        products = [
            {'id': 1, 'name': 'Customer Portal', 'description': 'Self-service portal for customers', 'status': 'Active', 'progress': 75, 'owner': 'Jane Williams'},
            {'id': 2, 'name': 'Payment Gateway', 'description': 'Payment processing solution', 'status': 'Development', 'progress': 50, 'owner': 'Mike Chen'},
            {'id': 3, 'name': 'Analytics Dashboard', 'description': 'Real-time analytics for managers', 'status': 'Planning', 'progress': 20, 'owner': 'Lisa Brown'},
        ]
    
    if not solutions:
        solutions = [
            {'id': 1, 'name': 'Enterprise Integration Suite', 'description': 'Complete integration solution', 'status': 'Active', 'progress': 65, 'owner': 'Robert Davis'},
            {'id': 2, 'name': 'Cloud Migration Solution', 'description': 'Solution for migrating on-prem to cloud', 'status': 'Development', 'progress': 40, 'owner': 'Emma Wilson'},
        ]
    
    if not consulting:
        consulting = [
            {'id': 1, 'name': 'Agile Transformation', 'description': 'Helping teams adopt agile practices', 'status': 'Active', 'progress': 80, 'client': 'Acme Corp'},
            {'id': 2, 'name': 'DevOps Implementation', 'description': 'Setting up DevOps practices and tools', 'status': 'Active', 'progress': 55, 'client': 'TechSolutions Inc'},
        ]
    
    if not active_sprints:
        active_sprints = [
            {'id': 1, 'name': 'Sprint 24', 'product': 'Customer Portal', 'start_date': '2025-04-01', 'end_date': '2025-04-14', 'progress': 50},
            {'id': 2, 'name': 'Sprint 8', 'product': 'Payment Gateway', 'start_date': '2025-04-03', 'end_date': '2025-04-17', 'progress': 30},
            {'id': 3, 'name': 'Sprint 5', 'product': 'Analytics Dashboard', 'start_date': '2025-03-28', 'end_date': '2025-04-11', 'progress': 75},
        ]
    
    if not recent_backlogs:
        recent_backlogs = [
            {'id': 1, 'title': 'Implement user authentication', 'type': 'Story', 'priority': 'High', 'status': 'In Progress', 'product': 'Customer Portal'},
            {'id': 2, 'title': 'Fix payment processing bug', 'type': 'Bug', 'priority': 'Critical', 'status': 'To Do', 'product': 'Payment Gateway'},
            {'id': 3, 'title': 'Add export to CSV feature', 'type': 'Story', 'priority': 'Medium', 'status': 'In Progress', 'product': 'Analytics Dashboard'},
            {'id': 4, 'title': 'Optimize database queries', 'type': 'Task', 'priority': 'Medium', 'status': 'To Do', 'product': 'Customer Portal'},
            {'id': 5, 'title': 'Create new dashboard widgets', 'type': 'Story', 'priority': 'Low', 'status': 'To Do', 'product': 'Analytics Dashboard'},
        ]
    
    if not teams:
        teams = [
            {'id': 1, 'name': 'Alpha Team', 'members': 5, 'focus': 'Customer Portal', 'velocity': 25},
            {'id': 2, 'name': 'Beta Team', 'members': 7, 'focus': 'Payment Gateway', 'velocity': 30},
            {'id': 3, 'name': 'Gamma Team', 'members': 4, 'focus': 'Analytics Dashboard', 'velocity': 20},
        ]
    
    # Count statistics for charts and metrics
    delivery_types = {
        'projects': len(projects),
        'products': len(products),
        'solutions': len(solutions),
        'consulting': len(consulting),
    }
    
    backlog_status = {
        'to_do': len([b for b in recent_backlogs if b['status'] == 'To Do']),
        'in_progress': len([b for b in recent_backlogs if b['status'] == 'In Progress']),
        'done': len([b for b in recent_backlogs if b['status'] == 'Done']),
    }
    
    # Prepare context for the template
    context = {
        'user': user,
        'page_title': 'Scrum Dashboard',
        'projects': projects,
        'products': products,
        'solutions': solutions,
        'consulting': consulting,
        'active_sprints': active_sprints,
        'recent_backlogs': recent_backlogs,
        'teams': teams,
        'delivery_types': delivery_types,
        'backlog_status': backlog_status,
        'global_delivery_types': global_delivery_types,
    }
    
    template_file = 'app_scrum/mod_dashboard/scrum_dashboard.html'
    return render(request, template_file, context)

@login_required
def module_dashboard(request, module_type):
    """
    Dashboard view for a specific module type (project, product, solution, consulting)
    """
    # Get the user
    user = request.user
    
    # Define the title based on module type
    module_titles = {
        'project': 'Project Dashboard',
        'product': 'Product Dashboard',
        'solution': 'Solution Dashboard',
        'consulting': 'Consulting Dashboard',
    }
    
    page_title = module_titles.get(module_type, 'Module Dashboard')
    
    # Placeholder for module-specific data
    module_items = []
    
    try:
        # Fetch data based on module type
        if module_type == 'project' and Project:
            module_items = Project.objects.filter(active=True).order_by('-created_at')
        elif module_type == 'product' and Product:
            module_items = Product.objects.filter(active=True).order_by('-created_at')
        elif module_type == 'solution' and Solution:
            module_items = Solution.objects.filter(active=True).order_by('-created_at')
        elif module_type == 'consulting' and Consulting:
            module_items = Consulting.objects.filter(active=True).order_by('-created_at')
    except Exception as e:
        # Log any errors for debugging
        print(f"Error fetching data for {module_type} dashboard: {e}")
    
    # Sample data if models are not yet implemented
    if not module_items:
        if module_type == 'project':
            module_items = [
                {'id': 1, 'name': 'E-Commerce Platform Upgrade', 'description': 'Major upgrade of the existing platform', 'status': 'In Progress', 'progress': 60, 'owner': 'John Smith'},
                {'id': 2, 'name': 'Mobile App Development', 'description': 'New mobile app for customers', 'status': 'Planning', 'progress': 25, 'owner': 'Sarah Johnson'},
                {'id': 3, 'name': 'Data Migration Project', 'description': 'Migrating legacy data to new system', 'status': 'In Progress', 'progress': 45, 'owner': 'David Lee'},
                {'id': 4, 'name': 'API Gateway Implementation', 'description': 'New API gateway for microservices', 'status': 'Planning', 'progress': 15, 'owner': 'Michael Brown'},
                {'id': 5, 'name': 'Security Audit Remediation', 'description': 'Addressing findings from security audit', 'status': 'In Progress', 'progress': 55, 'owner': 'Jessica Kim'},
            ]
        elif module_type == 'product':
            module_items = [
                {'id': 1, 'name': 'Customer Portal', 'description': 'Self-service portal for customers', 'status': 'Active', 'progress': 75, 'owner': 'Jane Williams'},
                {'id': 2, 'name': 'Payment Gateway', 'description': 'Payment processing solution', 'status': 'Development', 'progress': 50, 'owner': 'Mike Chen'},
                {'id': 3, 'name': 'Analytics Dashboard', 'description': 'Real-time analytics for managers', 'status': 'Planning', 'progress': 20, 'owner': 'Lisa Brown'},
                {'id': 4, 'name': 'Mobile App', 'description': 'Native mobile app for customers', 'status': 'Active', 'progress': 85, 'owner': 'Chris Taylor'},
                {'id': 5, 'name': 'Admin Console', 'description': 'Admin control panel for internal staff', 'status': 'Development', 'progress': 40, 'owner': 'Amanda Garcia'},
            ]
        elif module_type == 'solution':
            module_items = [
                {'id': 1, 'name': 'Enterprise Integration Suite', 'description': 'Complete integration solution', 'status': 'Active', 'progress': 65, 'owner': 'Robert Davis'},
                {'id': 2, 'name': 'Cloud Migration Solution', 'description': 'Solution for migrating on-prem to cloud', 'status': 'Development', 'progress': 40, 'owner': 'Emma Wilson'},
                {'id': 3, 'name': 'Data Analytics Platform', 'description': 'End-to-end data analytics solution', 'status': 'Planning', 'progress': 10, 'owner': 'Nathan Zhang'},
                {'id': 4, 'name': 'IoT Management Solution', 'description': 'Platform for IoT device management', 'status': 'Active', 'progress': 70, 'owner': 'Sophia Martinez'},
            ]
        elif module_type == 'consulting':
            module_items = [
                {'id': 1, 'name': 'Agile Transformation', 'description': 'Helping teams adopt agile practices', 'status': 'Active', 'progress': 80, 'client': 'Acme Corp'},
                {'id': 2, 'name': 'DevOps Implementation', 'description': 'Setting up DevOps practices and tools', 'status': 'Active', 'progress': 55, 'client': 'TechSolutions Inc'},
                {'id': 3, 'name': 'Product Strategy Workshop', 'description': 'Defining product strategy and roadmap', 'status': 'Completed', 'progress': 100, 'client': 'Global Retail'},
                {'id': 4, 'name': 'Scrum Team Coaching', 'description': 'Ongoing coaching for scrum teams', 'status': 'Active', 'progress': 60, 'client': 'FinTech Enterprises'},
                {'id': 5, 'name': 'Digital Transformation Strategy', 'description': 'Strategic planning for digital transformation', 'status': 'Planning', 'progress': 25, 'client': 'Manufacturing Inc'},
            ]
    
    # Prepare context for the template
    context = {
        'user': user,
        'page_title': page_title,
        'module_type': module_type,
        'module_items': module_items,
    }
    
    template_file = f'app_scrum/mod_dashboard/{module_type}_dashboard.html'
    return render(request, template_file, context)