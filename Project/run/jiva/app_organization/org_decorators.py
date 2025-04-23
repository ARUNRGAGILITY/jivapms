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


def site_admin_only(view_func):
    """
    Decorator to restrict access to Site Admins only.
    """

    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = request.user

        # Ensure the user is authenticated
        if not user.is_authenticated:
            template_url = "common/error/access_denied.html"
            return render(request, template_url, {})

        # Check if the user has the Site Admin role directly
        is_site_admin = MemberOrganizationRole.objects.filter(
            member__user=user,
            role__name=site_admin_str,  # Assuming 'site_admin_str' is the role name
            active=True
        ).exists()

        # If not a Site Admin, deny access
        if not is_site_admin:
            template_url = "common/error/access_denied.html"
            return render(request, template_url, {})

        return view_func(request, *args, **kwargs)

    return _wrapped_view





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
                #return HttpResponseForbidden("You do not have the required privileges to access this organization.")
                template_url = "common/error/access_denied.html"
                context = {}
                return render(request, template_url, context)

        return _wrapped_view
    return decorator


############################################################################################################
def org_and_pa_only(allowed_roles=None):
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
                return view_func(request, *args, **kwargs)
            except MemberOrganizationRole.DoesNotExist:
                #return HttpResponseForbidden("You do not have the required privileges to access this organization.")
                template_url = "common/error/access_denied.html"
                context = {}
                return render(request, template_url, context)

        return _wrapped_view
    return decorator


############################################################################################################

def org_or_project_access_required(org_allowed_roles=None, project_allowed_roles=None):
    if org_allowed_roles is None:
        org_allowed_roles = [org_admin_str, project_admin_str]
    if project_allowed_roles is None:
        project_allowed_roles = [PROJECT_ADMIN_ROLE_STR, PROJECT_EDITOR_ROLE_STR, PROJECT_VIEWER_ROLE_STR]
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            org_id = kwargs.get('org_id')
            project_id = kwargs.get('project_id', None)  # Project ID might not be present
            user = request.user
            organization = get_object_or_404(Organization, id=org_id)
            project = None
            
            # Attempt to fetch the project if a project ID is provided
            if project_id:
                project = get_object_or_404(Project, pk=project_id, org_id=org_id)

            # Check organization-level access using MemberOrganizationRole
            if org_allowed_roles and has_org_role(user, organization, org_allowed_roles):
                logger.debug(f">>> === ORG_LEVEL_ALLOWED_ACCESS === <<<")
                return view_func(request, *args, **kwargs)

            # Check project-level access using Projectmembership if the project exists
            if project and project_allowed_roles and has_project_role(user, project, project_allowed_roles):
                logger.debug(f">>> === PROJECT_LEVEL_ALLOWED_ACCESS === <<<")
                return view_func(request, *args, **kwargs)

            # If neither check passes, deny access
            #return HttpResponseForbidden("Access denied: You do not have the required permissions.")
            template_url = "common/error/access_denied.html"
            context = {}
            return render(request, template_url, context)
        return _wrapped_view
    return decorator

def has_org_role(user, organization, roles):
    member = Member.objects.filter(user=user).first()
    return MemberOrganizationRole.objects.filter(
        member_id=member.id,
        org=organization,
        role__name__in=roles,
        active=True
    ).exists()

def has_project_role(user, project, roles):
    return Projectmembership.objects.filter(
        member__user=user,
        project=project,
        project_role__role_type__in=roles,
        active=True
    ).exists()

# 
# Org Admin or Project Admin related access
#
def project_related_access_check(allowed_roles=None):
    if allowed_roles is None:
        allowed_roles = [org_admin_str, project_admin_str]  # Use dynamic role names from configuration
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user = request.user
            pro_id = kwargs.get('pro_id')
            org_id = Project.objects.get(id=pro_id).org_id
            organization = get_object_or_404(Organization, id=org_id)
            member = Member.objects.filter(user_id=user.id).first()
            allowed_roles_objs = Role.objects.filter(name__in=allowed_roles)
            logger.debug(f">>> === ORG_DECORATOR_CHECK1: User:{user},Member:{member},AllowedRoles:{allowed_roles_objs} === <<<")            
            try:
                org_membership = MemberOrganizationRole.objects.filter(member_id=member.id, org=organization, role__in=allowed_roles_objs)
                return view_func(request, *args, **kwargs)
            except MemberOrganizationRole.DoesNotExist:
                #return HttpResponseForbidden("You do not have the required privileges to access this organization.")
                template_url = "common/error/access_denied.html"
                context = {}
                return render(request, template_url, context)
        return _wrapped_view
    return decorator

# SA, this OA editable, or member of this org for viewable
def site_admin_this_org_admin_or_member_of_org(view_func):
    """
    Decorator to check if the user is a Site Admin, Organization Admin, or Member.
    It passes 'editable' status to the view.
    """

    @wraps(view_func)
    def _wrapped_view(request, org_id, *args, **kwargs):
        user = request.user
        
        # Member
        member = Member.objects.filter(user=user).first()
        
        # Fetch the organization
        organization = get_object_or_404(Organization, pk=org_id, active=True)
        
        # Check if user is a Site Admin (general admin role)
        is_site_admin = MemberOrganizationRole.objects.filter(name=site_admin_str).exists()

        # # role id
        # print(f">>> === CHECKING THE ORG ADMIN ROLE : {org_admin_str} === <<<")
        # org_admin_role_id = Role.objects.get(name=org_admin_str, org_id=org_id).id
        # print(f">>> === ORG ADMIN ROLE ID : {org_admin_role_id} === <<<")
        # # Check if the user is an Organization Admin for this organization
        # is_org_admin = MemberOrganizationRole.objects.filter(
        #     member_id=member.id, 
        #     org=organization, 
        #     role=org_admin_role_id,  # Assuming this is the role for Org Admin
        #     active=True
        # ).exists()

        from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

        # Fetching all Org Admin roles within the organization
        print(f">>> === CHECKING THE ORG ADMIN ROLE : {org_admin_str} IN {organization} === <<<")
        check_roles = Role.objects.filter(org_id=org_id)
        print(f">>> === ALL ROLES IN THE ORGANIZATION : {check_roles} === <<<")
        org_admin_roles = Role.objects.filter(name=org_admin_str, org_id=org_id).values_list('id', flat=True)

        if not org_admin_roles:
            print(">>> === No Org Admin role found for this organization === <<<")
            is_org_admin = False
        else:
            print(f">>> === ORG ADMIN ROLE IDs : {list(org_admin_roles)} === <<<")

            # Check if the user has any of these roles in the organization
            is_org_admin = MemberOrganizationRole.objects.filter(
                member_id=member.id, 
                org=organization, 
                role_id__in=org_admin_roles,  # Filter with multiple role IDs
                active=True
            ).exists()

        print(f">>> === IS ORG ADMIN? {is_org_admin} === <<<")


        # Check if the user has any member role within the organization
        is_member = MemberOrganizationRole.objects.filter(
            member_id=member.id,  
            org=organization, 
            active=True
        ).exists()
        
        # Determine if the page is editable
        editable = is_site_admin or is_org_admin

        # If user is not a member and not a Site Admin, raise permission denied
        if not is_member and not is_site_admin:
            template_url = "common/error/access_denied.html"
            context = {}
            return render(request, template_url, context)
        
        # Pass 'editable' and 'organization' to the view
        request.organization = organization
        request.editable = editable
        
        return view_func(request, org_id, *args, **kwargs)

    return _wrapped_view


# OA, this PA editable, or member of this org for viewable
def org_admin_this_project_admin_or_member_of_project(view_func):
    """
    Decorator to check if the user is a Site Admin, Organization Admin, or Member.
    It passes 'editable' status to the view.
    """

    @wraps(view_func)
    def _wrapped_view(request, org_id, project_id, *args, **kwargs):
        user = request.user
        
        # Member
        member = Member.objects.filter(user=user).first()
        
        # Fetch the organization
        organization = get_object_or_404(Organization, pk=org_id, active=True)
        
        # Check if user is a Org Admin (general admin role)
        is_org_admin = MemberOrganizationRole.objects.filter(name=org_admin_str, 
                                                             org=organization).exists()

        # role id
        logger.debug(f">>> === CHECKING THE PROJECT ROLE : {PROJECT_ADMIN_ROLE_STR} === <<<")
        pa_admin_role_str = ProjectRole.objects.get(role_type=PROJECT_ADMIN_ROLE_STR).role_type
        
        # project
        project = get_object_or_404(Project, pk=project_id, org=organization)
        
        # Check if the user is an Project Admin for this Project
        is_project_admin = Projectmembership.objects.filter(
            member_id=member.id, 
            project=project,
            project_role__role_type__in=[pa_admin_role_str],  # Assuming this is the role for Project Admin
            active=True
        ).exists()
        
        # Check if the user has any member role within the organization
        is_member = Projectmembership.objects.filter(
            member_id=member.id,  
            project=project,
            active=True
        ).exists()
        
        # Determine if the page is editable
        editable = is_org_admin or is_project_admin

        # If user is not a member and not a Site Admin, raise permission denied
        if not is_member and not is_org_admin:
            template_url = "common/error/access_denied.html"
            context = {}
            return render(request, template_url, context)
        
        # Pass 'editable' and 'organization' to the view
        request.organization = organization
        request.editable = editable
        
        return view_func(request, org_id, project_id, *args, **kwargs)

    return _wrapped_view
