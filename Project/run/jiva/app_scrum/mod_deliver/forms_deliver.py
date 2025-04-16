
from app_scrum.mod_app.all_form_imports import *
from app_scrum.mod_deliver.models_deliver import *

class DeliverForm(forms.ModelForm):
    class Meta:
        model = Deliver
        fields = ['name', 'description']
    def __init__(self, *args, **kwargs):
        super(DeliverForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()  # Note: No need to pass 'self' here
        self.helper.form_show_labels = False

