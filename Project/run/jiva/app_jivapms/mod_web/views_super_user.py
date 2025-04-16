from app_web.mod_app.all_view_imports import *
from app_memberprofilerole.mod_app.all_model_imports import *
from app_memberprofilerole.mod_member.models_member import *
from app_memberprofilerole.mod_role.models_role import *
from app_memberprofilerole.mod_memberorganizationrole.models_memberorganizationrole import *

from app_common.mod_app.all_view_imports import *
from app_jivapms.mod_app.all_view_imports import *
from app_organization.mod_projectmembership.models_projectmembership import *
from app_organization.mod_project.models_project import *

from app_organization.mod_framework.models_framework import *
from app_organization.mod_org_image_map.models_org_image_map import *
from app_organization.org_decorators import *
from app_common.mod_app.all_view_imports import COMMON_ROLE_CONFIG
import logging

app_name = "app_jivapms"
version = "v1"
module_dirname = "mod_web"

# Set up logger
logger = logging.getLogger(__name__)

from app_jivapms.mod_web.helper_web import *
from app_jivapms.mod_web.views_ajax_web import *


def stats(request):
    user = request.user
    
    # Verify user is a superuser
    if not user.is_superuser:
        return redirect('index')
    
    # Get organization data
    organizations = Organization.objects.filter(active=True)
    frameworks = Framework.objects.filter(active=True)
    public_frameworks = Framework.objects.filter(public_framework=True, active=True)
    projects = Project.objects.filter(active=True)
    members = Member.objects.filter(active=True)
    
    # Get the related Organization objects for public frameworks
    org_ids = public_frameworks.values_list('organization__id', flat=True).distinct()
    orgs_with_public_frameworks = Organization.objects.filter(id__in=org_ids)
    all_orgs = Organization.objects.filter(active=True)
    
    # Basic counters
    org_count = organizations.count()
    framework_count = frameworks.count()
    public_framework_count = public_frameworks.count()
    total_projects = projects.count()
    total_members = members.count()
    
    # Get project states for project status chart
    project_states = {}
    for state in ProjectAdministration.PROJECT_STATE_CHOICES:
        count = ProjectAdministration.objects.filter(
            project_state=state[0], 
            active=True
        ).count()
        project_states[state[1]] = count
    
    # Get organization metrics
    org_project_member_counts = []
    org_names = []
    org_project_counts = []
    org_member_counts = []

    for org in all_orgs:
        project_count = org.org_projects.filter(active=True).count()
        member_count = Member.objects.filter(member_roles__org=org, active=True).count()
        org_project_member_counts.append({
            'org_id': org.id,
            'org_name': org.name,
            'project_count': project_count,
            'member_count': member_count,
        })
        # For chart data
        org_names.append(org.name)
        org_project_counts.append(project_count)
        org_member_counts.append(member_count)
    
    # Log key statistics
    logger.info(f"Total organizations: {org_count}")
    logger.info(f"Total frameworks: {framework_count}")
    logger.info(f"Total public frameworks: {public_framework_count}")
    
    # Get user roles
    role_counts = {
        'Site Admin': MemberOrganizationRole.objects.filter(active=True, role__name='Site Admin').count(),
        'Org Admin': MemberOrganizationRole.objects.filter(active=True, role__name='Org Admin').count(),
        'Project Admin': MemberOrganizationRole.objects.filter(active=True, role__name='Project Admin').count(),
        'Other Roles': MemberOrganizationRole.objects.filter(active=True).exclude(
            role__name__in=['Site Admin', 'Org Admin', 'Project Admin']
        ).count()
    }
    
    # Get recent projects (last 10)
    recent_projects = Project.objects.filter(active=True).order_by('-created_at')[:10]
    
    # Get recent members (last 10)
    recent_members = Member.objects.filter(active=True).order_by('-created_at')[:10]
    
    # Get project memberships
    project_memberships = Projectmembership.objects.filter(active=True).order_by('project_role__role_type')[:20]
    
    # Prepare data for charts
    chart_data = {
        'org_names': org_names,
        'org_project_counts': org_project_counts,
        'org_member_counts': org_member_counts,
        'project_states': list(project_states.keys()),
        'project_state_counts': list(project_states.values()),
        'role_names': list(role_counts.keys()),
        'role_counts': list(role_counts.values()),
    }
    
    # Time-based stats (created in the last week, month, year)
    from datetime import datetime, timedelta
    now = datetime.now()
    one_week_ago = now - timedelta(days=7)
    one_month_ago = now - timedelta(days=30)
    
    time_stats = {
        'orgs_last_week': Organization.objects.filter(active=True, created_at__gte=one_week_ago).count(),
        'orgs_last_month': Organization.objects.filter(active=True, created_at__gte=one_month_ago).count(),
        'projects_last_week': Project.objects.filter(active=True, created_at__gte=one_week_ago).count(),
        'projects_last_month': Project.objects.filter(active=True, created_at__gte=one_month_ago).count(),
        'members_last_week': Member.objects.filter(active=True, created_at__gte=one_week_ago).count(),
        'members_last_month': Member.objects.filter(active=True, created_at__gte=one_month_ago).count(),
    }
    
    stats_context = {
        'org_count': org_count,
        'framework_count': framework_count,
        'public_framework_count': public_framework_count,
        'total_projects': total_projects,
        'total_members': total_members,
        'project_memberships': project_memberships,
        'org_project_member_counts': org_project_member_counts,
        'role_counts': role_counts,
        'project_states': project_states,
        'recent_projects': recent_projects,
        'recent_members': recent_members,
        'chart_data': chart_data,
        'time_stats': time_stats,
    }
    
    context = {
        'parent_page': 'home',
        'page': 'stats',
        'page_title': 'Super User Dashboard',
    }
    context.update(stats_context)
    template_url = f"{app_name}/{module_dirname}/super_user/stats.html"
    return render(request, template_url, context)



def super_user_admin(request):
    user = request.user
    organization = Organization.objects.filter(active=True)
    
    template_super_user_home_page = f"{app_name}/{module_dirname}/super_user/super_user_homepage.html"
    context = {
        'parent_page': 'home',
        'page': 'super_user_admin',
        'page_title': 'Super User Admin Page',
    }

    template_url = f"{app_name}/{module_dirname}/super_user/super_user_admin.html"
    return render(request, template_url, context)


def org_admin_dashboard(request, org_id):
    """
    Organization Admin Dashboard for users with Org Admin role in a specific organization.
    Displays organization-specific metrics and management options.
    """
    user = request.user
    organization = get_object_or_404(Organization, id=org_id, active=True)
    
    # Check if user has Org Admin role for this organization
    member = Member.objects.filter(user=user).first()
    org_admin_role = Role.objects.filter(name=COMMON_ROLE_CONFIG['ORG_ADMIN']['name']).first()
    
    is_org_admin = MemberOrganizationRole.objects.filter(
        member=member,
        org=organization,
        role=org_admin_role,
        active=True
    ).exists()
    
    if not is_org_admin:
        # If not org admin, redirect to access denied page
        template_url = "common/error/access_denied.html"
        context = {}
        return render(request, template_url, context)
    
    # Organization Statistics
    total_projects = Project.objects.filter(org=organization, active=True).count()
    total_members = MemberOrganizationRole.objects.filter(org=organization, active=True).values('member').distinct().count()
    
    # Get organization's projects
    projects = Project.objects.filter(org=organization, active=True).order_by('-created_at')
    recent_projects = projects[:5]  # Get 5 most recent projects
    
    # Get project states
    project_states = {}
    for state in ProjectAdministration.PROJECT_STATE_CHOICES:
        count = ProjectAdministration.objects.filter(
            project__org=organization,
            project_state=state[0], 
            active=True
        ).count()
        project_states[state[1]] = count
    
    # Get members in this organization
    member_roles = MemberOrganizationRole.objects.filter(
        org=organization,
        active=True
    ).select_related('member', 'role')
    
    # Count by role
    role_counts = {}
    for member_role in member_roles:
        role_name = member_role.role.name
        if role_name in role_counts:
            role_counts[role_name] += 1
        else:
            role_counts[role_name] = 1
    
    # Recent activities (project creations, member additions)
    recent_activities = []
    
    # Recently created projects
    for project in recent_projects:
        recent_activities.append({
            'type': 'project_created',
            'date': project.created_at,
            'name': project.name,
            'id': project.id,
            'creator': project.author.username if project.author else 'Unknown'
        })
    
    # Recently added members (last 5)
    recent_members = MemberOrganizationRole.objects.filter(
        org=organization,
        active=True
    ).order_by('-created_at')[:5]
    
    for member_role in recent_members:
        # Use the property we just added to get a properly formatted name
        if member_role.member and member_role.member.user:
            member_name = member_role.member.name
        else:
            member_name = "Unknown Member"
            
        recent_activities.append({
            'type': 'member_added',
            'date': member_role.created_at,
            'name': member_name,
            'id': member_role.member.id if member_role.member else 0,
            'role': member_role.role.name if member_role.role else "Unknown Role"
        })
    
    # Sort activities by date
    recent_activities.sort(key=lambda x: x['date'], reverse=True)
    recent_activities = recent_activities[:10]  # Get top 10 activities
    
    # Time-based stats 
    from datetime import datetime, timedelta
    now = datetime.now()
    one_month_ago = now - timedelta(days=30)
    
    time_stats = {
        'projects_last_month': Project.objects.filter(
            org=organization, 
            active=True,
            created_at__gte=one_month_ago
        ).count(),
        'members_last_month': MemberOrganizationRole.objects.filter(
            org=organization,
            active=True,
            created_at__gte=one_month_ago
        ).values('member').distinct().count(),
    }
    
    # Prepare data for charts
    project_names = [p.name for p in projects[:10]]  # Limit to 10 projects for the chart
    project_member_counts = []
    
    for project in projects[:10]:
        member_count = Projectmembership.objects.filter(
            project=project,
            active=True
        ).count()
        project_member_counts.append(member_count)
    
    chart_data = {
        'project_names': project_names,
        'project_member_counts': project_member_counts,
        'role_names': list(role_counts.keys()),
        'role_counts': list(role_counts.values()),
        'project_states': list(project_states.keys()),
        'project_state_counts': list(project_states.values()),
    }
    
    context = {
        'parent_page': 'home',
        'page': 'org_admin_dashboard',
        'page_title': f'Organization Admin Dashboard - {organization.name}',
        'organization': organization,
        'total_projects': total_projects,
        'total_members': total_members,
        'recent_projects': recent_projects,
        'member_roles': member_roles,
        'role_counts': role_counts,
        'recent_activities': recent_activities,
        'time_stats': time_stats,
        'chart_data': chart_data,
        'project_states': project_states,
    }
    
    template_url = f"{app_name}/{module_dirname}/org_admin/dashboard.html"
    return render(request, template_url, context)