
from app_memberprofilerole.mod_app.all_model_imports import *
from app_organization.mod_organization.models_organization import *
from app_common.mod_common.models_common import *
from app_memberprofilerole.mod_role.models_role import *
from app_memberprofilerole.mod_profile.models_profile import *

class Member(BaseModelImpl):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, 
                             related_name="member")
    org = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True, 
                                     related_name="org_members")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="author_members")
   
    def __str__(self):
        if self.user != None and self.org != None:
            return f"{self.user.username}"
        else:
            return "test"
            
    @property
    def name(self):
        """Return a properly formatted member name"""
        if not self.user:
            return "No User"
            
        if self.user.first_name and self.user.last_name:
            return f"{self.user.first_name} {self.user.last_name}"
        elif self.user.first_name:
            return self.user.first_name
        else:
            return self.user.username
   
class MemberOrganizationRole(BaseModelImpl):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, null=True, blank=True,
                               related_name="member_roles")
    org = models.ForeignKey(Organization, on_delete=models.CASCADE, null=True, blank=True, 
                                     related_name="mro_members")
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True, blank=True,
                             related_name="role_members")
    
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="author_mro")

    class Meta:
        unique_together = ('member', 'org', 'role')

    def __str__(self):
        if self.member != None  and self.org != None and self.role != None:
            return f"{self.member.user.username} - {self.org.name} - {self.role.name}"
        else:
            return "test"


# This is a generic definition
# Dec 13 12 2024 
# planned to use generically and easy to access
# SuperUser/SiteAdmin/OrgAdmin/ProjectAdmin


class MemberProfileRole(BaseModelImpl):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, null=True, blank=True,
                               related_name="list_members")
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True,
                                related_name="list_profiles")
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=True, blank=True,
                             related_name="list_roles")
    
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="author_memprorole")

    class Meta:
        unique_together = ('member', 'profile', 'role')

    def __str__(self):
        if self.member != None  and self.org != None and self.role != None:
            return f"{self.member.user.username} - {self.profile.name} - {self.role.name}"
        else:
            return "test"




# Pre-requisites
# 1. User should be created, and all users will by default have no access to system / site / org / project
# 2. User should be assigned as member of org to get access to org and projects
# 3. User should be assigned as project specific roles, default is no view 
# 4. Anyone siteadmin/orgadmin/projectadmin cannot see project data unless assigned with privileges

# Site Admin can manage entire site
# Can create/admin organizations and assign org admins
# Site admin cannot see org data or project data 
class SiteAdmin(BaseModelImpl):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, null=True, blank=True,
                               related_name="site_admin_roles")
   
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="author_siteadmin")

   

    def __str__(self):
        if self.member != None  and self.org != None and self.role != None:
            return f"{self.member.user.username}"
        else:
            return "SiteAdmin"

# Org Admin can manage organization
# Can create/admin own created orgs and assigned orgs, and create/admin project admins
# Org cannot see project data
class OrgAdmin(BaseModelImpl):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, null=True, blank=True,
                               related_name="ORGADMINROLES")
   
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="author_orgadmin")

   

    def __str__(self):
        if self.member != None  and self.org != None and self.role != None:
            return f"{self.member.user.username}"
        else:
            return "OrgAdmin"

# Project Admin can manage project
# Can create/admin own created projects and assigned projects
# Can assign project specific roles to members of orgs
class ProjectAdmin(BaseModelImpl):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, null=True, blank=True,
                               related_name="project_admin_roles")
   
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="author_projectadmin")

   

    def __str__(self):
        if self.member != None  and self.org != None and self.role != None:
            return f"{self.member.user.username}"
        else:
            return "ProjectAdmin"
        