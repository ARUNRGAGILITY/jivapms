from app_common.mod_common.models_common import *
from app_organization.mod_app.all_model_imports import *
from app_organization.mod_app.all_form_imports import *
from app_organization.mod_backlog.models_backlog import *

from app_organization.mod_release.models_release import *
from app_organization.mod_iteration.models_iteration import *

from app_organization.mod_backlog_type.models_backlog_type import *


# Core Hierarchical System Database
class Backlog(MPTTModel, BaseModelImpl):
    persona = models.ForeignKey('app_organization.Persona', on_delete=models.CASCADE,
                                related_name="persona_backlogs", null=True, blank=True)
    
    pro = models.ForeignKey("app_organization.Project", 
                                       on_delete=models.SET_NULL, 
                                              null=True, blank=True, 
                                              related_name='backlogs')
    parent = TreeForeignKey('self', null=True, blank=True, related_name='Project', on_delete=models.CASCADE)
   
    type = TreeForeignKey("app_organization.BacklogType", null=True, blank=True, 
                          related_name='backlog_types', 
                          on_delete=models.CASCADE)
    
    release = models.ForeignKey('app_organization.OrgRelease', on_delete=models.CASCADE, 
                            related_name="backlog_releases", null=True, blank=True)
    
    iteration = models.ForeignKey('app_organization.OrgIteration', on_delete=models.CASCADE, 
                            related_name="backlog_iteration", null=True, blank=True)
     
    
    # for now label is a char field
    tag =  models.CharField(max_length=256,null=True, blank=True, default='')
          
   
    duration_in_hours = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    

    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, 
                               blank=True, related_name='author_backlogs')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                             related_name='user_backlogs')
   
    class MPTTMeta:
        order_insertion_by = ['position']

    def __str__(self):
        if self.name:
            return self.name
        else:
            return '' + str(self.pk)

    def get_completion_stats(self):
        total_count = self.get_descendants().filter(done=True, active=True).count() + self.get_descendants().filter(done=False, active=True).count()
        completed_count = self.get_descendants().filter(done=True, active=True).count()
        percent_complete = round((completed_count / total_count) * 100, 2) if total_count > 0 else 0.0
        #print(f"====> {completed_count}/{total_count} ===> {percent_complete}")
        return {
            'total_count': total_count,
            'completed_count': completed_count,
            'percent_complete': percent_complete,
        }
    
    def get_active_descendants(self):
        return self.get_descendants().filter(active=True)

    #
    # DEF BLOCK UNBLOCK
    #
    def block(self):
        self.blocked = "blocked"
        self.block_count += 1

    def unblock(self):
        self.blocked = "unblocked"

    ## display 
    def children(self):
        return Backlog.objects.filter(parent=self.pk, active=True)
    
    def serializable_object(self):
        obj = {'name': self.name, 'contents': []}
        for child in self.children():
            obj['children'].append(child.serializable_object())
        return obj
    
    def get_active_children(self):
        return self.get_children().filter(active=True)


# 07122024
# StoryMappingModel

class StoryMapping(BaseModelTrackDateImpl):
    pro = models.ForeignKey("app_organization.Project", 
                                       on_delete=models.SET_NULL, 
                                              null=True, blank=True, 
                                              related_name='project_story_mappings')
    story_name = models.CharField(max_length=256, null=True, blank=True)
    story_id = models.PositiveIntegerField()  # ID of the story being mapped
    release_id = models.PositiveIntegerField()  # ID of the release
    iteration_id = models.PositiveIntegerField(null=True, blank=True)  # ID of the iteration
    activity_id = models.PositiveIntegerField()  # ID of the activity
    step_id = models.PositiveIntegerField()  # ID of the step
    persona_id = models.PositiveIntegerField()  # ID of the persona
    mapped_at = models.DateTimeField(auto_now_add=True)  # Timestamp of the mapping

    class Meta:
        unique_together = ( 'story_id',)
        verbose_name = 'Story Mapping'
        verbose_name_plural = 'Story Mappings'

    def __str__(self):
        return f"Story {self.story_id} mapped to Release {self.release_id}, Activity {self.activity_id}, Step {self.step_id}, Persona {self.persona_id}"
