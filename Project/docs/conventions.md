# Project Conventions and Standards

## Overview

JIVAPMS follows specific conventions and standards to ensure consistency, maintainability, and rapid development. These conventions are enforced throughout the project structure, code generation, and development workflow.

## Directory Structure Conventions

### Top-Level Structure
```
Project/
├── build/          # Never committed to Git
├── config/         # Configuration files (committed)
├── run/           # Production code (committed to Git)
└── docs/          # Documentation (committed)
```

### App Naming Convention
All Django apps follow the `app_` prefix convention:

```
app_[domain_name]/
├── app_common/           # Shared utilities
├── app_authz/           # Authorization
├── app_user/            # User management
├── app_organization/    # Organization management
├── app_project/         # Project management
└── app_[custom_name]/   # Custom apps
```

### File Naming Conventions

#### Python Files
- `models.py` - Model definitions
- `views.py` - View logic
- `forms.py` - Django forms
- `urls.py` - URL patterns
- `admin.py` - Admin interface
- `apps.py` - App configuration
- `tests.py` - Test cases
- `utils.py` - Utility functions
- `serializers.py` - API serializers (if using DRF)

#### Template Files
```
templates/
└── app_[name]/
    ├── [model]_list.html      # List view
    ├── [model]_detail.html    # Detail view
    ├── [model]_form.html      # Create/Update form
    ├── [model]_delete.html    # Delete confirmation
    └── [model]_base.html      # Base template for app
```

#### Static Files
```
static/
├── css/
│   ├── base.css           # Base styles
│   └── app_[name].css     # App-specific styles
├── js/
│   ├── base.js            # Base JavaScript
│   └── app_[name].js      # App-specific JavaScript
└── img/
    └── app_[name]/        # App-specific images
```

## Code Conventions

### Model Conventions

#### Base Model Pattern
```python
from django.db import models
from django.contrib.auth.models import User

class BaseModel(models.Model):
    """Base model with common fields"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='%(class)s_created'
    )
    
    class Meta:
        abstract = True
```

#### Model Naming
- Use singular nouns: `Project`, `User`, `Organization`
- Use PascalCase: `ProjectMember`, `UserProfile`
- Descriptive names: `ProjectTimeEntry`, not `TimeEntry`

#### Field Naming
```python
class Project(BaseModel):
    name = models.CharField(max_length=200)              # Required fields first
    description = models.TextField(blank=True)           # Optional fields after
    start_date = models.DateField(null=True, blank=True) # Use snake_case
    end_date = models.DateField(null=True, blank=True)
    
    # Foreign keys
    organization = models.ForeignKey(
        'app_organization.Organization',
        on_delete=models.CASCADE,
        related_name='projects'
    )
    
    # Many-to-many relationships
    members = models.ManyToManyField(
        User,
        through='ProjectMembership',
        related_name='member_projects'
    )
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Projects'
        
    def __str__(self):
        return self.name
```

### View Conventions

#### Class-Based Views
```python
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

class ProjectListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'app_project/project_list.html'
    context_object_name = 'projects'
    paginate_by = 25
    
    def get_queryset(self):
        return Project.objects.filter(
            organization__members=self.request.user
        ).order_by('name')

class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'app_project/project_form.html'
    success_url = reverse_lazy('app_project:project_list')
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
```

#### URL Naming
```python
# urls.py
from django.urls import path
from . import views

app_name = 'app_project'

urlpatterns = [
    path('', views.ProjectListView.as_view(), name='project_list'),
    path('create/', views.ProjectCreateView.as_view(), name='project_create'),
    path('<int:pk>/', views.ProjectDetailView.as_view(), name='project_detail'),
    path('<int:pk>/update/', views.ProjectUpdateView.as_view(), name='project_update'),
    path('<int:pk>/delete/', views.ProjectDeleteView.as_view(), name='project_delete'),
]
```

### Form Conventions

```python
from django import forms
from .models import Project

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'start_date', 'end_date', 'organization']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if self.user:
            self.fields['organization'].queryset = (
                self.user.organization_set.all()
            )
```

### Template Conventions

#### Base Template Structure
```html
<!-- templates/base.html -->
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}JIVA PMS{% endblock %}</title>
    {% load static %}
    <link href="{% static 'css/base.css' %}" rel="stylesheet">
    {% block extra_css %}{% endblock %}
</head>
<body>
    <nav class="navbar">
        {% include 'navbar.html' %}
    </nav>
    
    <main class="container">
        {% block content %}{% endblock %}
    </main>
    
    <script src="{% static 'js/base.js' %}"></script>
    {% block extra_js %}{% endblock %}
</body>
</html>
```

#### List Template Pattern
```html
<!-- templates/app_project/project_list.html -->
{% extends 'base.html' %}

{% block title %}Projects - {{ block.super }}{% endblock %}

{% block content %}
<div class="page-header">
    <h1>Projects</h1>
    <a href="{% url 'app_project:project_create' %}" class="btn btn-primary">
        Create Project
    </a>
</div>

<div class="table-responsive">
    <table class="table table-striped">
        <thead>
            <tr>
                <th>Name</th>
                <th>Organization</th>
                <th>Start Date</th>
                <th>Actions</th>
            </tr>
        </thead>
        <tbody>
            {% for project in projects %}
            <tr>
                <td>
                    <a href="{% url 'app_project:project_detail' project.pk %}">
                        {{ project.name }}
                    </a>
                </td>
                <td>{{ project.organization.name }}</td>
                <td>{{ project.start_date|date:"M d, Y" }}</td>
                <td>
                    <a href="{% url 'app_project:project_update' project.pk %}" 
                       class="btn btn-sm btn-outline-primary">Edit</a>
                </td>
            </tr>
            {% empty %}
            <tr>
                <td colspan="4" class="text-center">No projects found.</td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</div>

{% if is_paginated %}
    {% include 'pagination.html' %}
{% endif %}
{% endblock %}
```

## Development Workflow Conventions

### Git Conventions

#### Commit Message Format
```
[TYPE]: Brief description (50 chars max)

Detailed explanation if needed (72 chars per line)

- Bullet points for specific changes
- Reference issue numbers: #123
```

#### Commit Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

#### Branch Naming (if using branches)
- `feature/user-authentication`
- `fix/login-validation`
- `docs/api-documentation`

### Code Generation Conventions

#### Generated App Structure
```python
# Generated by app builder
class GeneratedModel(BaseModel):
    """Generated model following JIVAPMS conventions"""
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = f"{self.__class__.__name__}s"
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('app_name:model_detail', kwargs={'pk': self.pk})
```

### Testing Conventions

#### Test File Structure
```python
# tests.py
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Project

class ProjectModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
    def test_project_creation(self):
        project = Project.objects.create(
            name='Test Project',
            created_by=self.user
        )
        self.assertEqual(project.name, 'Test Project')
        self.assertEqual(str(project), 'Test Project')

class ProjectViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
    def test_project_list_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('app_project:project_list'))
        self.assertEqual(response.status_code, 200)
```

## Database Conventions

### Migration Naming
- Use descriptive names: `0002_add_project_status_field.py`
- Group related changes: `0003_update_user_permissions.py`

### Field Conventions
```python
# Standard field types and constraints
name = models.CharField(max_length=200)              # Names: 200 chars
description = models.TextField(blank=True)           # Descriptions: TextField
email = models.EmailField(unique=True)              # Emails: unique
slug = models.SlugField(unique=True)                # Slugs: unique
status = models.CharField(max_length=20, choices=STATUS_CHOICES)
is_active = models.BooleanField(default=True)       # Boolean flags
created_at = models.DateTimeField(auto_now_add=True) # Timestamps
```

## CSS and JavaScript Conventions

### CSS Naming (BEM methodology)
```css
/* Block */
.project-card { }

/* Element */
.project-card__title { }
.project-card__description { }

/* Modifier */
.project-card--featured { }
.project-card__title--large { }
```

### JavaScript Conventions
```javascript
// Use modern JavaScript (ES6+)
class ProjectManager {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.init();
    }
    
    init() {
        this.bindEvents();
    }
    
    bindEvents() {
        // Event binding logic
    }
}

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', function() {
    const projectManager = new ProjectManager('project-container');
});
```

## API Conventions (if using Django REST Framework)

### Serializer Conventions
```python
from rest_framework import serializers
from .models import Project

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'start_date', 'created_at']
        read_only_fields = ['id', 'created_at']

class ProjectListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list views"""
    class Meta:
        model = Project
        fields = ['id', 'name', 'start_date']
```

### API URL Conventions
```python
# api/urls.py
from rest_framework.routers import DefaultRouter
from . import viewsets

router = DefaultRouter()
router.register(r'projects', viewsets.ProjectViewSet)
urlpatterns = router.urls
```

## Security Conventions

### Authentication and Authorization
```python
# Always check permissions
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

class ProjectCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = 'app_project.add_project'
    
    def get_queryset(self):
        # Always filter by user context
        return Project.objects.filter(
            organization__members=self.request.user
        )
```

### Input Validation
```python
# Always validate and sanitize input
def clean_name(self):
    name = self.cleaned_data.get('name')
    if not name:
        raise forms.ValidationError("Name is required")
    return name.strip().title()
```

## Performance Conventions

### Query Optimization
```python
# Use select_related and prefetch_related
projects = Project.objects.select_related(
    'organization', 'created_by'
).prefetch_related('members')

# Use only() for specific fields
project_names = Project.objects.only('name', 'id')
```

### Caching
```python
from django.core.cache import cache

def get_project_stats(project_id):
    cache_key = f'project_stats_{project_id}'
    stats = cache.get(cache_key)
    if not stats:
        stats = calculate_stats(project_id)
        cache.set(cache_key, stats, 300)  # 5 minutes
    return stats
```

## Documentation Conventions

### Code Documentation
```python
def create_project(name, organization, user):
    """
    Create a new project with proper validation and permissions.
    
    Args:
        name (str): Project name (max 200 characters)
        organization (Organization): Organization instance
        user (User): User creating the project
        
    Returns:
        Project: Created project instance
        
    Raises:
        ValidationError: If name is invalid or user lacks permissions
    """
    # Implementation
```

### README Structure
Each app should have a README.md with:
- Purpose and description
- Model relationships
- View descriptions
- URL patterns
- Template locations
- Special considerations

## Deployment Conventions

### Environment Settings
- `development.py` - Local development
- `production.py` - Live deployment
- `testing.py` - Test environment

### Static Files
- Always run `collectstatic` before deployment
- Use versioning for static files in production
- Compress CSS/JS in production

These conventions ensure consistency across the entire JIVAPMS project and make it easier for developers to understand and contribute to the codebase.
