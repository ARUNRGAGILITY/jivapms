from app_organization.mod_app.all_model_imports import *
from app_organization.mod_project_board.models_project_board import *


class ProjectBoardClassOfService(BaseModelTrackDateImpl):
    board = models.ForeignKey('app_organization.ProjectBoard', on_delete=models.CASCADE,
                              related_name='board_classes_of_service', null=True, blank=True)
    color = models.CharField(max_length=16, blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name='author_board_classes_of_service')

    def __str__(self):
        return self.name or f"CoS {self.id}"
