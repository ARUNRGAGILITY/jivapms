from app_web.imports.all_form_imports import *
from app_user.models import *

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    RegistrationCode = forms.CharField(required=True)
    #groups = forms.ModelMultipleChoiceField(queryset=Group.objects.all(), widget=forms.CheckboxSelectMultiple, required=False)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'RegistrationCode']
        widgets = {
            'username': forms.TextInput(attrs={'autocomplete': 'off'}),
            # Other form field widgets
            'password1': forms.TextInput(attrs={'autocomplete': 'off'}),
        }

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    groups = forms.ModelMultipleChoiceField(queryset=CustomGroup.objects.filter(active=True), widget=forms.CheckboxSelectMultiple, required=False)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Pre-select groups that the user is part of
        if self.instance.pk:
            self.fields['groups'].initial = self.instance.groups.all()

            
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'bio']


class GroupForm(forms.ModelForm):
    class Meta:
        model = CustomGroup
        fields = ['name']

from django import forms
from django.apps import apps
from django.contrib.auth import get_user_model

User = get_user_model()

class AdminUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    # Declare Role model app and name as instance-level attributes
    role_app_name = "app_memberprofilerole"
    role_model_name = "Role"
    role_assignment_model_name = "MemberOrganizationRole"  # adjust this to your actual role-linking model

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'is_active']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        try:
            self.RoleModel = apps.get_model(self.role_app_name, self.role_model_name)
            if self.RoleModel:
                self.fields['role'] = forms.ModelChoiceField(
                    queryset=self.RoleModel.objects.filter(active=True),
                    required=False,
                    label='Role',
                    widget=forms.Select(attrs={'class': 'form-select'})
                )
        except Exception:
            self.RoleModel = None

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user_id = self.instance.id if self.instance else None
        if email and User.objects.filter(email=email).exclude(id=user_id).exists():
            raise forms.ValidationError("Email already exists")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)

        if self.cleaned_data.get('password1'):
            user.set_password(self.cleaned_data['password1'])

        if commit:
            user.save()

            # Assign role (if both Role and Assignment model exist)
            role_instance = self.cleaned_data.get('role')
            if hasattr(self, 'RoleModel') and self.RoleModel and role_instance:
                try:
                    RoleAssignment = apps.get_model(self.role_app_name, self.role_assignment_model_name)
                    if RoleAssignment:
                        RoleAssignment.objects.update_or_create(
                            user=user,
                            defaults={'role': role_instance}
                        )
                except Exception:
                    pass  # Optional: Log or handle error gracefully

        return user


class CSVUploadForm(forms.Form):
    csv_file = forms.FileField(
        label="CSV File",
        help_text="Upload a CSV file with user data",
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': '.csv'}),
        required=False  # Set to not required
    )
    
    csv_text = forms.CharField(
        label="Or paste CSV data",
        required=False,  # Set to not required
        help_text="Paste CSV data directly (must include header row)",
        widget=forms.Textarea(attrs={
            'class': 'form-control', 
            'rows': 8, 
            'placeholder': 'username,email,password,first_name,last_name,user_type\njohn_doe,john@example.com,securepassword123,John,Doe,team_member'
        })
    )
    
    def clean(self):
        cleaned_data = super().clean()
        csv_file = cleaned_data.get('csv_file')
        csv_text = cleaned_data.get('csv_text', '').strip()
        
        # Ensure at least one input method is provided
        if not csv_file and not csv_text:
            raise forms.ValidationError("Please either upload a CSV file or paste CSV data.")
        
        return cleaned_data
    
