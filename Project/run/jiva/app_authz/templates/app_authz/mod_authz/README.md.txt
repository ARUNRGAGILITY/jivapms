Django Authorization Management App
A Django app for managing users, members, and role assignments in your organization-based system.

Overview
This Django app provides a comprehensive authorization management system for organization-based applications. It allows administrators to:

Manage members within organizations
Assign and manage roles for members
Perform batch operations via CSV uploads
Control access based on organization and role hierarchies
Key Features
Member Management: Add, edit, delete, and list members of organizations
Role Management: Assign and manage roles for members within organizations
Batch Operations: Upload and process member and role data in bulk via CSV
Fine-Grained Permissions: Site admins and organization admins have different capabilities
Django Admin Integration: Full admin interface for backend management
Models Used
This app uses existing models from your project:

Member and MemberOrganizationRole from app_memberprofilerole.mod_profile.models_profile
Organization from app_organization.mod_organization.models_organization
Role from app_memberprofilerole.mod_role.models_role
Installation
See the Installation Guide for detailed setup instructions.

Usage
URL Patterns
The app provides the following URL patterns:

/org/<org_id>/members/ - List all members of an organization
/org/<org_id>/members/create/ - Create a new member
/org/<org_id>/members/<member_id>/update/ - Update a member
/org/<org_id>/members/<member_id>/delete/ - Delete a member
/org/<org_id>/members/batch-upload/ - Batch upload members
/org/<org_id>/member-roles/ - List all member roles
/org/<org_id>/member-roles/create/ - Create a new member role
/org/<org_id>/member-roles/<role_id>/update/ - Update a member role
/org/<org_id>/member-roles/<role_id>/delete/ - Delete a member role
/org/<org_id>/member-roles/batch-upload/ - Batch upload member roles
Permissions
The app uses the decorator site_admin_this_org_admin_or_member_of_org to control access:

Site Admins: Can manage all members and roles across organizations
Organization Admins: Can manage members and roles within their organization
Regular Members: Can view but not edit members and roles in their organization
CSV Templates
The app includes CSV templates for batch operations:

Member CSV Template - For batch uploading members
Member Role CSV Template - For batch assigning roles
Utility Functions
The app provides several utility functions in utils.py:

process_member_batch() - Process a batch of member data from CSV
process_member_role_batch() - Process a batch of member role assignments from CSV
get_member_roles_for_user() - Get all roles for a specific user
is_site_admin() - Check if a user is a Site Admin
is_org_admin() - Check if a user is an Organization Admin
is_member_of_org() - Check if a user is a member of an organization
Dependencies
Django 3.2+
Bootstrap 5 (for templates)
jQuery
DataTables (for enhanced table functionality)
Select2 (for enhanced select dropdowns)
License
This app is provided for your internal use.

