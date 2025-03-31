
from app.app_postnote.mod_app.all_form_imports import *
from app.app_postnote.mod_project.models_project import *
from app.app_1.mod_app.all_form_imports import *
from app.app_1.mod_app.all_model_imports import *
from app.app_1.mod_app.all_view_imports import *

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description']
    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()  # Note: No need to pass 'self' here
        self.helper.form_show_labels = False

