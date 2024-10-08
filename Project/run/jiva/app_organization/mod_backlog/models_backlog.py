from app_common.mod_common.models_common import *
from app_organization.mod_app.all_model_imports import *
from app_organization.mod_app.all_form_imports import *
from app_organization.mod_backlog.models_backlog import *
from app_organization.mod_backlog_type.models_backlog_type import *


# Core Hierarchical System Database
class Backlog(MPTTModel, BaseModelImpl):
  
    
    pro = models.ForeignKey("app_organization.Project", 
                                       on_delete=models.SET_NULL, 
                                              null=True, blank=True, 
                                              related_name='backlogs')
    parent = TreeForeignKey('self', null=True, blank=True, related_name='Project', on_delete=models.CASCADE)
   
    type = TreeForeignKey("BacklogType", null=True, blank=True, 
                          related_name='backlog_types', 
                          on_delete=models.CASCADE)
     
    
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
        return self.name

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
