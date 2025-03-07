
from app_organization.mod_app.all_model_imports import *
from app_organization.mod_project.models_project import *
from app_common.mod_common.models_common import *
from app_organization.mod_project_board.models_project_board import *
# class ProjectBoardSwimlane(BaseModelImpl):
#     project = models.ForeignKey('app_organization.Project', on_delete=models.CASCADE, 
#                             related_name="project_project_board_swimlanes", null=True, blank=True)
    
#     author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
#                                related_name="author_project_board_swimlanes")
   
        
#     def __str__(self):
#         if self.name:
#             return self.name
#         else:
#             return str(self.id)
class ProjectBoardSwimLane(BaseModelTrackDateImpl):
    board = models.ForeignKey('app_organization.ProjectBoard', on_delete=models.CASCADE,
                                related_name="board_swim_lanes", null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="author_board_swim_lanes")
   
        
    def __str__(self):
        if self.name:
            return self.name
        else:
            return str(self.id)
