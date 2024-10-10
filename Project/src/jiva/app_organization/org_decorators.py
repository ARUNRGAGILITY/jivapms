from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from functools import wraps
from app_memberprofilerole.mod_role.models_role import *
from app_memberprofilerole.mod_member.models_member import *
from app_organization.mod_project.models_project import *
from app_organization.mod_projectmembership.models_projectmembership import *
from app_common.mod_app.all_view_imports import *
from app_jivapms.mod_app.all_view_imports import *

org_admin_str = COMMON_ROLE_CONFIG['ORG_ADMIN']['name']
project_admin_str = COMMON_ROLE_CONFIG['PROJECT_ADMIN']['name']

# ORGANIZATION ACCESS 
def org_access_required(allowed_roles=None):
    if allowed_roles is None:
        allowed_roles = ['Org Admin', 'Project Admin']  # Default roles for access

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            org_id = kwargs.get('org_id')  # Extract org_id from kwargs
            organization = get_object_or_404(Organization, id=org_id)

            # Check if the user is a member of the organization
            user = request.user
            try:
                logger.debug(f">>> === org_access_required {user}:{organization} === <<<")
                member = Member.objects.get(user=request.user, org=organization)
            except Exception as e:
                return HttpResponseForbidden(f"You are not a member of this organization. {str(e)}")

            # Fetch the roles based on allowed_roles
            allowed_roles_objs = Role.objects.filter(name__in=allowed_roles)
            
            logger.debug(f">>> === allowed_roles_objs {allowed_roles_objs} === <<<")
            # Check if the member has one of the allowed roles in this organization
            try:
                org_membership = MemberOrganizationRole.objects.get(member=member, org=organization, role__in=allowed_roles_objs)
            except Exception as e:
                return HttpResponseForbidden(f"You don't have the necessary privileges in this organization. {str(e)}")

            # Proceed with the view and pass member and org_membership along with kwargs
            return view_func(request, member=member, org_membership=org_membership, *args, **kwargs)

        return _wrapped_view
    return decorator



# Configuration for role names
org_admin_str = COMMON_ROLE_CONFIG['ORG_ADMIN']['name']
project_admin_str = COMMON_ROLE_CONFIG['PROJECT_ADMIN']['name']
def org_access_required(allowed_roles=None):
    if allowed_roles is None:
        allowed_roles = [org_admin_str, project_admin_str]  # Use dynamic role names from configuration

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user = request.user
            org_id = kwargs.get('org_id')
            organization = get_object_or_404(Organization, id=org_id)
            member = Member.objects.filter(user_id=user.id).first()
            allowed_roles_objs = Role.objects.filter(name__in=allowed_roles)
            logger.debug(f">>> === ORG_DECORATOR_CHECK1: User:{user},Member:{member},AllowedRoles:{allowed_roles_objs} === <<<")            
            try:
                org_membership = MemberOrganizationRole.objects.get(member_id=member.id, org=organization, role__in=allowed_roles_objs)
                kwargs['member'] = member
                kwargs['org_membership'] = org_membership
                return view_func(request, *args, **kwargs)
            except MemberOrganizationRole.DoesNotExist:
                return HttpResponseForbidden("You do not have the required privileges to access this organization.")

        return _wrapped_view
    return decorator


def project_access_required(allowed_roles=None):
    if allowed_roles is None:
        allowed_roles = ['Viewer', 'Editor', 'Admin']  # Default roles for access

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            project_id = kwargs.get('project_id')
            project = Project.objects.get(id=project_id, active=True)

            # Check if the user is a member of the organization
            try:
                member = Member.objects.get(user=request.user, organization=project.org)
            except Member.DoesNotExist:
                return HttpResponseForbidden("You are not a member of this organization.")

            # Check if the member has a role in the project
            try:
                project_membership = Projectmembership.objects.get(member=member, project=project)
            except Projectmembership.DoesNotExist:
                return HttpResponseForbidden("You are not part of this project.")

            # Check if the user's role is in the allowed roles
            if project_membership.role.name not in allowed_roles:
                return HttpResponseForbidden(f"You must have one of these roles: {', '.join(allowed_roles)} to access this page.")

            # Pass the member and project_membership to the view
            return view_func(request, member, project_membership, *args, **kwargs)

        return _wrapped_view
    return decorator


"""
@project_access_required(allowed_roles=['Viewer', 'Editor', 'Admin'])
def project_detail_view(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    return render(request, 'project_detail.html', {'project': project})

@project_access_required(allowed_roles=['Editor', 'Admin'])
def project_edit_view(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    # Editing logic here
    return render(request, 'project_edit.html', {'project': project})

@project_access_required()
def project_general_view(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    return render(request, 'project_general.html', {'project': project})
    
# Example Usage:
from django.shortcuts import render, get_object_or_404
from .org_decorators import project_access_required

@project_access_required(allowed_roles=['Viewer', 'Editor', 'Admin'])
def project_detail_view(request, member, project_membership, project_id):
    project = get_object_or_404(Project, id=project_id)

    # Now you can access the member and their role in the project
    user_role = project_membership.role.name  # Role of the member in the project

    return render(request, 'project_detail.html', {
        'project': project,
        'member': member,  # You can use member information in the template
        'user_role': user_role,  # Use the role to control what they see or can do
    })


"""