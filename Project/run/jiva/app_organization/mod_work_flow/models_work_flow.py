
from app_organization.mod_app.all_model_imports import *
from app_organization.mod_project.models_project import *
from app_common.mod_common.models_common import *

class WorkFlow(BaseModelImpl):
    pro = models.ForeignKey('app_organization.Project', on_delete=models.CASCADE, 
                            related_name="pro_work_flows", null=True, blank=True)
    
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="author_work_flows")
   
        
    def __str__(self):
        return self.name