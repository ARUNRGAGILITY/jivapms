
from app_memberprofilerole.mod_app.all_model_imports import *
from app_organization.mod_organization.models_organization import *
from app_common.mod_common.models_common import *

class Profile(BaseModelImpl):
    user = models.OneToOneField(User, related_name='base_profile', on_delete=models.CASCADE, null=True, blank=True)  
    image = models.ImageField(default='user_default_icon.svg', upload_to='profile_pics', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)

    org = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, blank=True,
                            related_name="org_profiles")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="author_profiles")
    def save(self, *args, **kwargs):
        # Custom save logic here
        super(Profile, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.name


