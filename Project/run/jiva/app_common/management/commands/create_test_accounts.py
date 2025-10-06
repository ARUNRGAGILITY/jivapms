from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from app_organization.mod_organization.models_organization import *
from app_memberprofilerole.mod_profile.models_profile import *
from app_memberprofilerole.mod_member.models_member import *
from app_jivapms.mod_app.all_view_imports import *
from app_common.mod_app.all_view_imports import *
import random

role_config = COMMON_ROLE_CONFIG
GIVEN_ORGANIZATION = "ABC Organization"

class Command(BaseCommand):
    help = 'Generate test user accounts with roles and organization membership'

    def handle(self, *args, **kwargs):
        first_names = ["John", "Jane", "Michael", "Michelle", "Chris", "Christina", "David", "Danielle", "James", "Jennifer"]
        last_names = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson", "Moore", "Taylor"]

        # Create the organization
        organization = Organization.objects.create(name=GIVEN_ORGANIZATION)

        # Create the roles using the new role config
        role_objects = {}
        for role_key, role_data in role_config.items():
            role_name = role_data["name"]
            role_objects[role_key] = Role.objects.create(name=role_name, org=organization)

        # Initialize user count
        user_count = 0

        # Calculate total number of users to create from the role config
        total_users = sum(role_data["count"] for role_data in role_config.values())

        # Create users and assign roles
        for role_key, role_data in role_config.items():
            role_name = role_data["name"]
            count = role_data["count"]
            
            for _ in range(count):
                if user_count >= total_users:
                    break
                
                first_name = random.choice(first_names)
                last_name = random.choice(last_names)
                username = f"{first_name.lower()}.{last_name.lower()}{user_count + 1}"
                email = f"{first_name.lower()}.{last_name.lower()}{user_count + 1}@example.com"
                password = 'password123'  # Default password for all fake users
                
                # Create the user
                user = User.objects.create_user(username=username, email=email, password=password)
                
                # Assign the role and organization membership
                role = role_objects[role_key]
                member = Member.objects.create(user=user, org=organization)
                MemberOrganizationRole.objects.create(member=member, org=organization, role=role)
                
                user_count += 1

        self.stdout.write(self.style.SUCCESS('Successfully created test users with roles and organization membership'))
