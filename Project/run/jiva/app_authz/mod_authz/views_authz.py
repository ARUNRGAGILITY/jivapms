from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.db import transaction, IntegrityError
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse
from functools import wraps
import csv
import io

from app_memberprofilerole.mod_app.all_model_imports import *
from app_organization.mod_organization.models_organization import Organization
from app_common.mod_common.models_common import *
from app_memberprofilerole.mod_role.models_role import Role
from app_memberprofilerole.mod_profile.models_profile import Member, MemberOrganizationRole

from .forms_authz import (
    MemberForm, 
    MemberBatchForm,
    MemberRoleForm,
    MemberRoleBatchForm
)

# Constants for role names
site_admin_str = "Site Admin"
org_admin_str = "Org Admin"

# Decorator function (from your provided code)
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
        is_site_admin = MemberOrganizationRole.objects.filter(
            member__user=user,
            role__name=site_admin_str,
            active=True
        ).exists()

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

# Member Management Views
@login_required
@site_admin_this_org_admin_or_member_of_org
def member_list(request, org_id):
    """List all members of an organization."""
    organization = request.organization
    editable = request.editable
    
    members = Member.objects.filter(org_id=org_id)
    
    context = {
        'members': members,
        'organization': organization,
        'editable': editable,
    }
    
    return render(request, 'app_authz/member_list.html', context)

@login_required
@site_admin_this_org_admin_or_member_of_org
def member_create(request, org_id):
    """Create a new member in the organization."""
    organization = request.organization
    editable = request.editable
    
    if not editable:
        messages.error(request, "You don't have permission to create members.")
        return redirect('app_authz:member_list', org_id=org_id)
    
    if request.method == 'POST':
        form = MemberForm(request.POST)
        if form.is_valid():
            member = form.save(commit=False)
            member.author = request.user
            member.save()
            
            messages.success(request, "Member successfully created")
            return redirect('app_authz:member_list', org_id=org_id)
    else:
        form = MemberForm(initial={'org': organization})
    
    context = {
        'form': form,
        'organization': organization,
        'editable': editable,
        'is_create': True
    }
    
    return render(request, 'app_authz/member_form.html', context)

@login_required
@site_admin_this_org_admin_or_member_of_org
def member_update(request, org_id, member_id):
    """Update an existing member."""
    organization = request.organization
    editable = request.editable
    
    if not editable:
        messages.error(request, "You don't have permission to update members.")
        return redirect('app_authz:member_list', org_id=org_id)
    
    member = get_object_or_404(Member, pk=member_id, org_id=org_id)
    
    if request.method == 'POST':
        form = MemberForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            messages.success(request, "Member successfully updated")
            return redirect('app_authz:member_list', org_id=org_id)
    else:
        form = MemberForm(instance=member)
    
    context = {
        'form': form,
        'organization': organization,
        'editable': editable,
        'member': member,
        'is_create': False
    }
    
    return render(request, 'app_authz/member_form.html', context)

@login_required
@site_admin_this_org_admin_or_member_of_org
def member_delete(request, org_id, member_id):
    """Delete a member."""
    organization = request.organization
    editable = request.editable
    
    if not editable:
        messages.error(request, "You don't have permission to delete members.")
        return redirect('app_authz:member_list', org_id=org_id)
    
    member = get_object_or_404(Member, pk=member_id, org_id=org_id)
    
    if request.method == 'POST':
        # Instead of deleting, set active=False and deleted=True
        member.active = False
        member.deleted = True
        member.save()
        
        messages.success(request, "Member successfully deleted")
        return redirect('app_authz:member_list', org_id=org_id)
    
    context = {
        'object': member,
        'organization': organization,
        'editable': editable,
        'object_name': f"Member: {member.name}"
    }
    
    return render(request, 'app_authz/confirm_delete.html', context)

@login_required
@site_admin_this_org_admin_or_member_of_org
def member_batch_upload(request, org_id):
    """Batch upload members via CSV."""
    organization = request.organization
    editable = request.editable
    
    if not editable:
        messages.error(request, "You don't have permission to batch upload members.")
        return redirect('app_authz:member_list', org_id=org_id)
    
    if request.method == 'POST':
        form = MemberBatchForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            default_org = form.cleaned_data.get('organization') or organization
            
            # Process CSV
            decoded_file = csv_file.read().decode('utf-8')
            csv_data = csv.DictReader(io.StringIO(decoded_file))
            
            # Use the utility function for batch processing
            from .utils import process_member_batch
            success_count, error_count, errors = process_member_batch(
                csv_data, default_org, request.user
            )
            
            # Create message with summary
            message = f"Processed {success_count + error_count} members: {success_count} successful, {error_count} errors."
            if errors:
                message += f" Errors: {'; '.join(errors[:5])}"
                if len(errors) > 5:
                    message += f" and {len(errors) - 5} more."
            
            if success_count > 0:
                messages.success(request, message)
            else:
                messages.error(request, message)
            
            return redirect('app_authz:member_list', org_id=org_id)
    else:
        form = MemberBatchForm(initial={'organization': organization})
    
    context = {
        'form': form,
        'organization': organization,
        'editable': editable,
    }
    
    return render(request, 'app_authz/member_batch_form.html', context)

# Member Role Management Views
@login_required
@site_admin_this_org_admin_or_member_of_org
def member_role_list(request, org_id):
    """List all member roles of an organization."""
    organization = request.organization
    editable = request.editable
    
    member_roles = MemberOrganizationRole.objects.filter(org_id=org_id)
    
    context = {
        'member_roles': member_roles,
        'organization': organization,
        'editable': editable,
    }
    
    return render(request, 'app_authz/member_role_list.html', context)

@login_required
@site_admin_this_org_admin_or_member_of_org
def member_role_create(request, org_id):
    """Create a new member role in the organization."""
    organization = request.organization
    editable = request.editable
    
    if not editable:
        messages.error(request, "You don't have permission to create member roles.")
        return redirect('app_authz:member_role_list', org_id=org_id)
    
    if request.method == 'POST':
        form = MemberRoleForm(request.POST, org_id=org_id)
        if form.is_valid():
            try:
                member_role = form.save(commit=False)
                member_role.author = request.user
                member_role.save()
                
                messages.success(request, "Member role successfully created")
                return redirect('app_authz:member_role_list', org_id=org_id)
            except IntegrityError:
                messages.error(request, "This member role combination already exists.")
    else:
        form = MemberRoleForm(org_id=org_id, initial={'org': organization})
    
    context = {
        'form': form,
        'organization': organization,
        'editable': editable,
        'is_create': True
    }
    
    return render(request, 'app_authz/member_role_form.html', context)

@login_required
@site_admin_this_org_admin_or_member_of_org
def member_role_update(request, org_id, role_id):
    """Update an existing member role."""
    organization = request.organization
    editable = request.editable
    
    if not editable:
        messages.error(request, "You don't have permission to update member roles.")
        return redirect('app_authz:member_role_list', org_id=org_id)
    
    member_role = get_object_or_404(MemberOrganizationRole, pk=role_id, org_id=org_id)
    
    if request.method == 'POST':
        form = MemberRoleForm(request.POST, instance=member_role, org_id=org_id)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Member role successfully updated")
                return redirect('app_authz:member_role_list', org_id=org_id)
            except IntegrityError:
                messages.error(request, "This member role combination already exists.")
    else:
        form = MemberRoleForm(instance=member_role, org_id=org_id)
    
    context = {
        'form': form,
        'organization': organization,
        'editable': editable,
        'member_role': member_role,
        'is_create': False
    }
    
    return render(request, 'app_authz/member_role_form.html', context)

@login_required
@site_admin_this_org_admin_or_member_of_org
def member_role_delete(request, org_id, role_id):
    """Delete a member role."""
    organization = request.organization
    editable = request.editable
    
    if not editable:
        messages.error(request, "You don't have permission to delete member roles.")
        return redirect('app_authz:member_role_list', org_id=org_id)
    
    member_role = get_object_or_404(MemberOrganizationRole, pk=role_id, org_id=org_id)
    
    if request.method == 'POST':
        # Instead of deleting, set active=False
        member_role.active = False
        member_role.save()
        
        messages.success(request, "Member role successfully deleted")
        return redirect('app_authz:member_role_list', org_id=org_id)
    
    context = {
        'object': member_role,
        'organization': organization,
        'editable': editable,
        'object_name': f"Member Role: {member_role}"
    }
    
    return render(request, 'app_authz/confirm_delete.html', context)

@login_required
@site_admin_this_org_admin_or_member_of_org
def member_role_batch_upload(request, org_id):
    """Batch upload member roles via CSV."""
    organization = request.organization
    editable = request.editable
    
    if not editable:
        messages.error(request, "You don't have permission to batch upload member roles.")
        return redirect('app_authz:member_role_list', org_id=org_id)
    
    if request.method == 'POST':
        form = MemberRoleBatchForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            default_org = form.cleaned_data.get('organization') or organization
            
            # Process CSV
            decoded_file = csv_file.read().decode('utf-8')
            csv_data = csv.DictReader(io.StringIO(decoded_file))
            
            # Use the utility function for batch processing
            from .utils import process_member_role_batch
            success_count, error_count, errors = process_member_role_batch(
                csv_data, default_org, request.user
            )
            
            # Create message with summary
            message = f"Processed {success_count + error_count} member roles: {success_count} successful, {error_count} errors."
            if errors:
                message += f" Errors: {'; '.join(errors[:5])}"
                if len(errors) > 5:
                    message += f" and {len(errors) - 5} more."
            
            if success_count > 0:
                messages.success(request, message)
            else:
                messages.error(request, message)
            
            return redirect('app_authz:member_role_list', org_id=org_id)
    else:
        form = MemberRoleBatchForm(initial={'organization': organization})
    
    context = {
        'form': form,
        'organization': organization,
        'editable': editable,
    }
    
    return render(request, 'app_authz/member_role_batch_form.html', context)