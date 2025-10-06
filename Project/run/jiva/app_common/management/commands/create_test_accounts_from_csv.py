import csv
import json  # or use PyYAML for YAML support
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app_organization.mod_organization.models_organization import Organization
from app_memberprofilerole.mod_profile.models_profile import *
from app_memberprofilerole.mod_role.models_role import *
from app_memberprofilerole.mod_member.models_member import Member, MemberOrganizationRole
from app_organization.mod_project.models_project import *
from app_jivapms.mod_app.all_view_imports import *
from app_common.mod_app.all_view_imports import *
from app_organization.mod_project_template.models_project_template import *

class Command(BaseCommand):
    help = 'Generate test user accounts with roles and organization membership from config and CSV'

    def add_arguments(self, parser):
        parser.add_argument('--config', type=str, help="Path to the config file (e.g., config.json)")
        parser.add_argument('--csv', type=str, help="Path to the CSV file for user details (e.g., users.csv)")

    def handle(self, *args, **options):
        config_file = options['config']
        csv_file = options['csv']

        if not config_file or not csv_file:
            self.stdout.write(self.style.ERROR('Please provide both config and CSV file paths.'))
            return

        # Load organization from config file
        with open(config_file, 'r') as file:
            config_data = json.load(file)

        organization_name = config_data['organization_name']

        # Create or get the organization
        organization, created = Organization.objects.get_or_create(name=organization_name)
        self.stdout.write(self.style.SUCCESS(f'Organization: {organization_name} created or already exists'))

        # FEB 2025
        # Project Roles additions
        project_roles = ProjectRole.objects.filter(active=True)
        if project_roles.count() == 0 :
            # create the basic roles
            for project_role in COMMON_PROJECT_ROLE_CONFIG.values():
                db_project_role, created = ProjectRole.objects.get_or_create(role_type=project_role)
                logger.debug(f">>> === CREATED PROJECT ROLE: {project_role} === <<<")
        # Project Templates additions
        project_templates = ProjectTemplate.objects.filter(active=True, org=organization)
        if project_templates.count() == 0 :
            # create the basic project templates
            practices = {
                'Scrum': 'Scrum as per Scrum Guide and general practices',
                'Kanban': 'Kanban as per Lean/Kanban',
                'Scrumban': 'Scrumban as a combination of Scrum and Kanban',
                'Waterfall': 'Waterfall, as a sequential / adaptive lifecycle of project management',
                'Hybrid': 'Hybrid as a combination of Agile and Waterfall',
                'Custom': 'Custom as per organization specific practices',

            }
            for project_template in practices.keys():
                db_project_template, created = ProjectTemplate.objects.get_or_create(org=organization, name=project_template, description=practices[project_template])
                logger.debug(f">>> === CREATED PROJECT TEMPLATE: {project_template} === <<<")

        # END FEB 2025

        # Initialize counters for created and existing objects
        users_created = 0
        users_existing = 0
        members_created = 0
        members_existing = 0
        roles_created = 0
        roles_existing = 0
        member_roles_created = 0
        member_roles_existing = 0

        # Dictionary to hold role objects to avoid duplicate creation
        role_objects = {}

        # Parse the CSV file for user details and create users
        with open(csv_file, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            total_users_processed = 0  # Track how many users have been processed
            for row in reader:
                first_name = row['first_name']
                last_name = row['last_name']
                email = row['email']
                role_name = row['role']

                self.stdout.write(self.style.SUCCESS(f'Processing user: {first_name} {last_name}, Role: {role_name}'))

                # Create the user if they don't already exist
                username = f"{first_name.lower()}.{last_name.lower()}"
                password = 'password123'  # Default password for all users
                user, created = User.objects.get_or_create(username=username, email=email)
                if created:
                    user.set_password(password)
                    user.save()
                    self.stdout.write(self.style.SUCCESS(f'User: {username} created'))
                    users_created += 1
                else:
                    self.stdout.write(self.style.WARNING(f'User: {username} already exists'))
                    users_existing += 1

                # Create the member associated with the user and organization if not already created
                member, created = Member.objects.get_or_create(user=user, org=organization)
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Member: {username} created in organization: {organization_name}'))
                    members_created += 1
                else:
                    self.stdout.write(self.style.WARNING(f'Member: {username} already exists in organization: {organization_name}'))
                    members_existing += 1

                # Check if the role exists, if not, create it
                if role_name not in role_objects:
                    role, created = Role.objects.get_or_create(name=role_name, org=organization)
                    role_objects[role_name] = role  # Cache the role object
                    if created:
                        self.stdout.write(self.style.SUCCESS(f'Role: {role_name} created'))
                        roles_created += 1
                    else:
                        roles_existing += 1
                else:
                    role = role_objects[role_name]
                    roles_existing += 1

                # Assign the user to the role within the organization
                member_org_role, created = MemberOrganizationRole.objects.get_or_create(member=member, org=organization, role=role)
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Assigned {username} to role: {role_name}'))
                    member_roles_created += 1
                else:
                    self.stdout.write(self.style.WARNING(f'{username} already has role: {role_name} in organization: {organization_name}'))
                    member_roles_existing += 1

                total_users_processed += 1  # Increment the user count

            self.stdout.write(self.style.SUCCESS(f'Total users processed: {total_users_processed}'))

        # Final summary output
        self.stdout.write(self.style.SUCCESS('--- Summary ---'))
        self.stdout.write(self.style.SUCCESS(f'Users created: {users_created}, already existed: {users_existing}'))
        self.stdout.write(self.style.SUCCESS(f'Members created: {members_created}, already existed: {members_existing}'))
        self.stdout.write(self.style.SUCCESS(f'Roles created: {roles_created}, already existed: {roles_existing}'))
        self.stdout.write(self.style.SUCCESS(f'Member roles assigned: {member_roles_created}, already existed: {member_roles_existing}'))
        self.stdout.write(self.style.SUCCESS('Successfully processed users from CSV and assigned roles'))
