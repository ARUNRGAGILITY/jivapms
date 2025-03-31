
from app_organization.mod_app.all_model_imports import *
from app_organization.mod_project_board.models_project_board import *
from app_common.mod_common.models_common import *

# this is the created code 
class ProjectBoardState(BaseModelTrackDateImpl):
    
    board = models.ForeignKey('app_organization.ProjectBoard', on_delete=models.CASCADE,
                                related_name="board_states", null=True, blank=True)
    
    wip_limit = models.PositiveIntegerField(default=0)
    apply_wip_limit = models.BooleanField(default=True)

    buffer_column = models.BooleanField(default=False)
    COLUMN_TYPE_CHOICES = [
        ('ToDo', 'ToDo'),
        ('WIP', 'WIP'),
        ('Done', 'Done'),]
    column_type = models.CharField(max_length=10, choices=COLUMN_TYPE_CHOICES, default='ToDo')  
    SUBCOLUMN_PAIRS = [
        ("DOING_DONE", "Doing / Done"),
        ("INPROGRESS_READY", "In Progress / Ready"),
        ("MVP_PERSEVERE", "MVP / Persevere"),
    ]
    subcolumn_pair = models.CharField(
        max_length=30,
        choices=SUBCOLUMN_PAIRS,
        default="DOING_DONE",  # sets default at the DB/model level
        blank=True,
        null=True,
        help_text="Applicable only when buffer_column is True"
    )


    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="author_board_states")
   
    def get_subcolumns(self):
        pair_mapping = {
            "DOING_DONE": ("Doing", "Done"),
            "INPROGRESS_READY": ("In Progress", "Ready"),
            "MVP_PERSEVERE": ("MVP", "Persevere"),
        }
        default_pair = ("Doing", "Done")
        return pair_mapping.get(self.subcolumn_pair, default_pair)


    def __str__(self):
        if self.name:
            return self.name
        else:
            return str(self.id)


# this is the default code

# class ProjectBoardState(BaseModelImpl):
#     project_board = models.ForeignKey('app_organization.ProjectBoard', on_delete=models.CASCADE, 
#                             related_name="project_board_project_board_states", null=True, blank=True)
    
#     author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
#                                related_name="author_project_board_states")
   
        
#     def __str__(self):
#         if self.name:
#             return self.name
#         else:
#             return str(self.id)
