
from app_scrum.mod_app.all_model_imports import *
from app_organization.mod_organization.models_organization import *
from app_common.mod_common.models_common import *

class Deliver(BaseModelImpl):
    organization = models.ForeignKey('app_organization.Organization', on_delete=models.CASCADE, 
                            related_name="organization_delivers", null=True, blank=True)
    
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="author_delivers")
    
        
    def __str__(self):
        if self.name:
            return self.name
        else:
            return str(self.id)
