
from app_organization.mod_app.all_form_imports import *
from app_organization.mod_blog.models_blog import *
import re
# class BlogForm(forms.ModelForm):
#     class Meta:
#         model = Blog
#         fields = ['name', 'description', 'content']
#     def __init__(self, *args, **kwargs):
#         super(BlogForm, self).__init__(*args, **kwargs)
#         self.helper = FormHelper()  # Note: No need to pass 'self' here
#         self.helper.form_show_labels = False
class BlogForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 20,
            'cols': 80,
            'class': 'form-control',
            'placeholder': 'Enter your blog content in Markdown format...',
            'style': 'font-family: "Courier New", monospace; white-space: pre-wrap;'
        }),
        help_text='You can use Markdown syntax including Mermaid diagrams'
    )
    
    class Meta:
        model = Blog
        fields = ['name', 'content', 'description']
    
    def __init__(self, *args, **kwargs):
        super(BlogForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
    
    # NO clean_content method - let Django save exactly what's typed!