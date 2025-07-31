Authorization Management App Installation Guide
This guide will help you set up and configure the app_authz Django app for managing users, members, and role assignments in your project.

Installation
Create the app directory structure Create the directory structure as follows in your Django project:
app_authz/
├── __init__.py
├── admin.py
├── apps.py
├── forms.py
├── models.py
├── tests.py
├── urls.py
├── utils.py
├── views.py
└── templates/
    └── app_authz/
        ├── member_list.html
        ├── member_form.html
        ├── member_batch_form.html
        ├── member_role_list.html
        ├── member_role_form.html
        ├── member_role_batch_form.html
        └── confirm_delete.html
Copy the files Copy all the provided files into their respective locations in the app directory structure.
Add the app to your INSTALLED_APPS Add 'app_authz' to your INSTALLED_APPS in your project's settings.py:
python
INSTALLED_APPS = [
    # ...
    'app_authz',
    # ...
]
Include app URLs in your project's urls.py Add the following to your project's urls.py:
python
from django.urls import path, include

urlpatterns = [
    # ...
    path('authz/', include('app_authz.urls')),
    # ...
]
Dependencies
This app depends on:

Django (tested with 3.2+)
Your existing models:
Member and MemberOrganizationRole from app_memberprofilerole.mod_profile.models_profile
Organization from app_organization.mod_organization.models_organization
Role from app_memberprofilerole.mod_role.models_role
BaseModelImpl from one of your modules
Features
The app provides:

Member Management:
List all members of an organization
Create, update, and delete members
Batch upload members via CSV
Member Role Management:
List all member roles in an organization
Assign, update, and remove roles from members
Batch assign roles via CSV
Permission System:
Uses the site_admin_this_org_admin_or_member_of_org decorator
Site admins and organization admins can manage members
Regular members can view but not edit
Usage
Managing Members
Navigate to /authz/org/<org_id>/members/ to view and manage members
Use the "Add Member" button to add individual members
Use the "Batch Upload" button to upload multiple members via CSV
Managing Member Roles
Navigate to /authz/org/<org_id>/member-roles/ to view and manage member roles
Use the "Add Member Role" button to assign roles to members
Use the "Batch Assign Roles" button to assign roles to multiple members via CSV
CSV Formats
Member CSV Format:
username/email,organization_id,description,active
john.doe@example.com,123,"Marketing team member",true
janedoe,456,"IT department",false
Member Role CSV Format:
username/email,role_name/role_id,organization_id,active
john.doe@example.com,Reviewer,123,true
janedoe,Editor,456,true
user@example.com,Site Admin,,true
Utility Functions
The app provides several utility functions in utils.py:

process_member_batch(): Process a batch of member data from CSV
process_member_role_batch(): Process a batch of member role assignments from CSV
get_member_roles_for_user(): Get all roles for a specific user
is_site_admin(): Check if a user is a Site Admin
is_org_admin(): Check if a user is an Organization Admin
is_member_of_org(): Check if a user is a member of an organization
Frontend Requirements
The app templates are designed for Bootstrap 5 and assume:

A base template named base.html with:
A content block named {% block content %}
An extra JavaScript block named {% block extra_js %}
JavaScript libraries:
jQuery
DataTables
Select2
If you're using different frontend libraries, you may need to adjust the templates.

Customization
You can customize the app by:

Overriding the templates by creating matching template files in your project's templates directory
Extending the forms or views in your own custom code
Modifying the admin site registration in admin.py
