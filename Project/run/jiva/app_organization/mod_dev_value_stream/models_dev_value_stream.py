
from app_organization.mod_app.all_model_imports import *
from app_organization.mod_ops_value_stream.models_ops_value_stream import *
from app_common.mod_common.models_common import *

class DevValueStream(BaseModelImpl):
    ops = models.ForeignKey('app_organization.OpsValueStream', on_delete=models.CASCADE, 
                            related_name="ops_dev_value_streams", null=True, blank=True)
    
    project = models.ForeignKey('app_organization.Project', on_delete=models.CASCADE, 
                            related_name="dev_value_stream_project", null=True, blank=True)
    
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="author_dev_value_streams")
   
        
    def __str__(self):
        return self.name