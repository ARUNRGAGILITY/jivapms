
from app_memberprofilerole.mod_app.all_form_imports import *
from app_memberprofilerole.mod_member.models_member import *

class MemberorganizationroleForm(forms.ModelForm):
    first_name = forms.CharField(max_length=150, required=False, label="First Name")
    last_name = forms.CharField(max_length=150, required=False, label="Last Name")
    email = forms.EmailField(required=False, label="Email")

    class Meta:
        model = MemberOrganizationRole
        fields = ['member', 'org', 'role']  # Keep original fields

    def __init__(self, *args, **kwargs):
        org_id = kwargs.pop('org_id', None)  # Capture the organization ID from kwargs
        super(MemberorganizationroleForm, self).__init__(*args, **kwargs)

        if org_id:
            # Filter roles to only show roles for the given organization
            self.fields['role'].queryset = Role.objects.filter(org_id=org_id)
            
            # Filter members to only show members belonging to the given organization
            self.fields['member'].queryset = Member.objects.filter(org_id=org_id)

        # Populate user fields if editing an existing entry
        if self.instance and self.instance.member and self.instance.member.user:
            self.fields['first_name'].initial = self.instance.member.user.first_name
            self.fields['last_name'].initial = self.instance.member.user.last_name
            self.fields['email'].initial = self.instance.member.user.email

    def save(self, commit=True):
        instance = super().save(commit=False)

        # Update the User model fields
        if instance.member and instance.member.user:
            user = instance.member.user
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.email = self.cleaned_data['email']

            if commit:
                user.save()  # Save user changes
                instance.save()  # Save MemberOrganizationRole changes

        return instance
