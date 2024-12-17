
from app_organization.mod_app.all_model_imports import *
from app_organization.mod_project.models_project import *
from app_common.mod_common.models_common import *

class Collection(BaseModelImpl):
    project = models.ForeignKey('app_organization.Project', on_delete=models.CASCADE, 
                            related_name="project_collections", null=True, blank=True)
    
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="author_collections")
   
        
    def __str__(self):
        if self.name:
            return self.name
        else:
            return str(self.id)