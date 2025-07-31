from django.utils import timezone

def process_member_batch(csv_data, default_org, author_user):
    """
    Process a batch of member data from CSV.
    
    Args:
        csv_data: CSV DictReader object with parsed data
        default_org: Default organization to use if not specified
        author_user: User creating these members
        
    Returns:
        tuple of (success_count, error_count, errors)
    """
    from django.contrib.auth.models import User
    from app_memberprofilerole.mod_profile.models_profile import Member
    from app_organization.mod_organization.models_organization import Organization
    
    success_count = 0
    error_count = 0
    errors = []
    
    for row in csv_data:
        try:
            # Get or create user by username/email
            username_or_email = row.get('username/email', '').strip()
            user = None
            
            # First try to find by username
            try:
                user = User.objects.get(username=username_or_email)
            except User.DoesNotExist:
                # Then try by email
                try:
                    user = User.objects.get(email=username_or_email)
                except User.DoesNotExist:
                    errors.append(f"User with username/email '{username_or_email}' not found")
                    error_count += 1
                    continue
            
            # Determine organization
            org = default_org
            org_id_in_csv = row.get('organization_id', '').strip()
            if org_id_in_csv:
                try:
                    org = Organization.objects.get(id=org_id_in_csv, active=True)
                except (Organization.DoesNotExist, ValueError):
                    errors.append(f"Organization with ID '{org_id_in_csv}' not found")
                    error_count += 1
                    continue
            
            # Parse other fields
            description = row.get('description', '').strip()
            active_str = row.get('active', 'true').strip().lower()
            active = active_str in ('true', 'yes', '1', 'y')
            
            # Check if member already exists
            member, created = Member.objects.update_or_create(
                user=user,
                org=org,
                defaults={
                    'description': description,
                    'active': active,
                    'author': author_user,
                    'updated_at': timezone.now()
                }
            )
            
            success_count += 1
            
        except Exception as e:
            error_count += 1
            errors.append(f"Error processing row for '{username_or_email}': {str(e)}")
    
    return success_count, error_count, errors

def process_member_role_batch(csv_data, default_org, author_user):
    """
    Process a batch of member role assignments from CSV.
    
    Args:
        csv_data: CSV DictReader object with parsed data
        default_org: Default organization to use if not specified
        author_user: User creating these role assignments
        
    Returns:
        tuple of (success_count, error_count, errors)
    """
    from django.contrib.auth.models import User
    from django.db import transaction
    from app_memberprofilerole.mod_profile.models_profile import Member, MemberOrganizationRole
    from app_memberprofilerole.mod_role.models_role import Role
    from app_organization.mod_organization.models_organization import Organization
    
    success_count = 0
    error_count = 0
    errors = []
    
    for row in csv_data:
        try:
            with transaction.atomic():
                # Get or create user by username/email
                username_or_email = row.get('username/email', '').strip()
                user = None
                
                # First try to find by username
                try:
                    user = User.objects.get(username=username_or_email)
                except User.DoesNotExist:
                    # Then try by email
                    try:
                        user = User.objects.get(email=username_or_email)
                    except User.DoesNotExist:
                        errors.append(f"User with username/email '{username_or_email}' not found")
                        error_count += 1
                        continue
                
                # Determine organization
                org = default_org
                org_id_in_csv = row.get('organization_id', '').strip()
                if org_id_in_csv:
                    try:
                        org = Organization.objects.get(id=org_id_in_csv, active=True)
                    except (Organization.DoesNotExist, ValueError):
                        errors.append(f"Organization with ID '{org_id_in_csv}' not found")
                        error_count += 1
                        continue
                
                # Get or create the member
                member, created = Member.objects.get_or_create(
                    user=user,
                    org=org,
                    defaults={
                        'active': True,
                        'author': author_user
                    }
                )
                
                # Get the role
                role_identifier = row.get('role_name/role_id', '').strip()
                role = None
                
                # Try to get role by ID
                try:
                    if role_identifier.isdigit():
                        role = Role.objects.get(id=role_identifier, active=True)
                    else:
                        # Try by name and organization
                        role = Role.objects.get(name=role_identifier, org=org, active=True)
                except (Role.DoesNotExist, ValueError):
                    errors.append(f"Role '{role_identifier}' not found for organization {org}")
                    error_count += 1
                    continue
                
                # Parse other fields
                active_str = row.get('active', 'true').strip().lower()
                active = active_str in ('true', 'yes', '1', 'y')
                
                # Create or update the member role
                member_role, created = MemberOrganizationRole.objects.update_or_create(
                    member=member,
                    org=org,
                    role=role,
                    defaults={
                        'active': active,
                        'author': author_user,
                        'updated_at': timezone.now()
                    }
                )
                
                success_count += 1
        
        except Exception as e:
            error_count += 1
            errors.append(f"Error processing row for '{username_or_email}': {str(e)}")
    
    return success_count, error_count, errors

def get_member_roles_for_user(user, org=None):
    """
    Get all member roles for a specific user, optionally filtered by organization.
    
    Args:
        user: The User object
        org: Optional Organization object to filter by
        
    Returns:
        QuerySet of MemberOrganizationRole objects
    """
    from app_memberprofilerole.mod_profile.models_profile import Member, MemberOrganizationRole
    
    # Get the member object for this user
    member = Member.objects.filter(user=user, active=True).first()
    
    if not member:
        return MemberOrganizationRole.objects.none()
    
    # Get roles
    roles_query = MemberOrganizationRole.objects.filter(member=member, active=True)
    
    if org:
        roles_query = roles_query.filter(org=org)
    
    return roles_query

def is_site_admin(user):
    """
    Check if the user is a Site Admin.
    
    Args:
        user: The User object
        
    Returns:
        Boolean indicating if the user is a Site Admin
    """
    from app_memberprofilerole.mod_profile.models_profile import MemberOrganizationRole
    
    site_admin_str = "Site Admin"
    
    return MemberOrganizationRole.objects.filter(
        member__user=user,
        role__name=site_admin_str,
        active=True
    ).exists()

def is_org_admin(user, org):
    """
    Check if the user is an Organization Admin for the given organization.
    
    Args:
        user: The User object
        org: The Organization object
        
    Returns:
        Boolean indicating if the user is an Org Admin
    """
    from app_memberprofilerole.mod_profile.models_profile import Member, MemberOrganizationRole
    from app_memberprofilerole.mod_role.models_role import Role
    
    org_admin_str = "Organization Admin"
    
    # Get the member
    member = Member.objects.filter(user=user, active=True).first()
    
    if not member:
        return False
    
    # Get all org admin roles for this organization
    org_admin_roles = Role.objects.filter(name=org_admin_str, org=org).values_list('id', flat=True)
    
    if not org_admin_roles:
        return False
    
    # Check if the user has any of these roles
    return MemberOrganizationRole.objects.filter(
        member=member,
        org=org,
        role_id__in=org_admin_roles,
        active=True
    ).exists()

def is_member_of_org(user, org):
    """
    Check if the user is a member of the given organization.
    
    Args:
        user: The User object
        org: The Organization object
        
    Returns:
        Boolean indicating if the user is a member
    """
    from app_memberprofilerole.mod_profile.models_profile import Member, MemberOrganizationRole
    
    # Get the member
    member = Member.objects.filter(user=user, active=True).first()
    
    if not member:
        return False
    
    # Check if the user has any role in the organization
    return MemberOrganizationRole.objects.filter(
        member=member,
        org=org,
        active=True
    ).exists()