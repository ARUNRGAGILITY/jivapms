from django import forms
from django.contrib.auth.models import User
from app_memberprofilerole.mod_app.all_model_imports import *
from app_organization.mod_organization.models_organization import Organization
from app_memberprofilerole.mod_role.models_role import Role
from app_memberprofilerole.mod_profile.models_profile import Member, MemberOrganizationRole
import csv
import io


class MemberForm(forms.ModelForm):
    user = forms.ModelChoiceField(
        queryset=User.objects.filter(is_active=True),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control select2'})
    )
    org = forms.ModelChoiceField(
        queryset=Organization.objects.filter(active=True),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control select2'})
    )

    class Meta:
        model = Member
        fields = ['user', 'org', 'description', 'active']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class MemberBatchForm(forms.Form):
    csv_file = forms.FileField(
        label='CSV File',
        help_text='Upload a CSV file with columns: username/email, organization_id, description (optional), active (true/false)'
    )
    organization = forms.ModelChoiceField(
        queryset=Organization.objects.filter(active=True),
        required=False,
        help_text='Optional default organization if not specified in CSV'
    )

    def clean_csv_file(self):
        csv_file = self.cleaned_data['csv_file']
        if not csv_file.name.endswith('.csv'):
            raise forms.ValidationError('File is not a CSV file')
        
        # Validate CSV structure
        decoded_file = csv_file.read().decode('utf-8')
        csv_data = csv.reader(io.StringIO(decoded_file))
        headers = next(csv_data, None)
        
        required_columns = ['username/email']
        
        if not all(col in headers for col in required_columns):
            raise forms.ValidationError(f'CSV must contain these columns: {", ".join(required_columns)}')
        
        # Reset file pointer
        csv_file.seek(0)
        return csv_file


class MemberRoleForm(forms.ModelForm):
    member = forms.ModelChoiceField(
        queryset=Member.objects.filter(active=True),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control select2'})
    )
    org = forms.ModelChoiceField(
        queryset=Organization.objects.filter(active=True),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control select2'})
    )
    role = forms.ModelChoiceField(
        queryset=Role.objects.filter(active=True),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control select2'})
    )

    class Meta:
        model = MemberOrganizationRole
        fields = ['member', 'org', 'role', 'active']
        widgets = {
            'active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, org_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        # If an organization ID is provided, filter roles and members by that organization
        if org_id:
            self.fields['org'].initial = org_id
            self.fields['org'].widget.attrs['readonly'] = True
            self.fields['role'].queryset = Role.objects.filter(active=True, org_id=org_id)
            self.fields['member'].queryset = Member.objects.filter(active=True, org_id=org_id)


class MemberRoleBatchForm(forms.Form):
    csv_file = forms.FileField(
        label='CSV File',
        help_text='Upload a CSV file with columns: username/email, role_name/role_id, organization_id (optional), active (true/false)'
    )
    organization = forms.ModelChoiceField(
        queryset=Organization.objects.filter(active=True),
        required=False,
        help_text='Optional default organization if not specified in CSV'
    )

    def clean_csv_file(self):
        csv_file = self.cleaned_data['csv_file']
        if not csv_file.name.endswith('.csv'):
            raise forms.ValidationError('File is not a CSV file')
        
        # Validate CSV structure
        decoded_file = csv_file.read().decode('utf-8')
        csv_data = csv.reader(io.StringIO(decoded_file))
        headers = next(csv_data, None)
        
        required_columns = ['username/email', 'role_name/role_id']
        
        if not all(col in headers for col in required_columns):
            raise forms.ValidationError(f'CSV must contain these columns: {", ".join(required_columns)}')
        
        # Reset file pointer
        csv_file.seek(0)
        return csv_file