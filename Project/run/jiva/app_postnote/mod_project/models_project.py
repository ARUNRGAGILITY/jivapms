
from app.app_postnote.mod_app.all_model_imports import *
from app.app_1.mod_common.models_common import *

class Project(BaseModelImpl):
   
    
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="author_Project")
   
        
    def __str__(self):
        return self.name
