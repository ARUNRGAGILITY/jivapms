
from app_organization.mod_app.all_form_imports import *
from app_organization.mod_work_flow.models_work_flow import *

class WorkFlowForm(forms.ModelForm):
    class Meta:
        model = WorkFlow
        fields = ['name', 'description']
    def __init__(self, *args, **kwargs):
        super(WorkFlowForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()  # Note: No need to pass 'self' here
        self.helper.form_show_labels = False

