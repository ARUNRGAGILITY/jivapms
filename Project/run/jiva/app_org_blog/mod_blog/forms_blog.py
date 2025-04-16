
from app_org_blog.mod_app.all_form_imports import *
from app_org_blog.mod_blog.models_blog import *
from markdownx.fields import MarkdownxFormField
from django.utils.text import slugify

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['name', 'description', 'title', 'summary', 'content', 'featured_image', 'status', 'category', 'tags']
        
    content = MarkdownxFormField(required=False, help_text="Use Markdown for formatting")
    
    def __init__(self, *args, **kwargs):
        super(BlogForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = True
        
        # Add Bootstrap classes
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            
        # Special styling for specific fields
        self.fields['content'].widget.attrs['rows'] = 10
        self.fields['summary'].widget.attrs['rows'] = 3
        
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        # Auto-generate slug from title if not provided
        if not instance.slug and instance.title:
            instance.slug = slugify(instance.title)
            
        if commit:
            instance.save()
        return instance

class BlogCommentForm(forms.ModelForm):
    class Meta:
        model = BlogComment
        fields = ['content']
        
    def __init__(self, *args, **kwargs):
        super(BlogCommentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
        
        # Add Bootstrap classes
        self.fields['content'].widget.attrs.update({
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Write your comment here...'
        })

class BlogMemberForm(forms.ModelForm):
    class Meta:
        model = BlogMember
        fields = ['member', 'role']
        
    def __init__(self, *args, **kwargs):
        organization = kwargs.pop('organization', None)
        super(BlogMemberForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        
        # If organization is provided, filter members to that organization
        if organization:
            self.fields['member'].queryset = Member.objects.filter(org=organization, active=True)

