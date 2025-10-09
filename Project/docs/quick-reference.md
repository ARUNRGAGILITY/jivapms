# Quick Reference Guide

## Essential Commands

### Setup and Navigation
```bash
# Setup development environment
cd Project/build/make
./step1.setup_dev_env

# Navigate to project
. step3.goto_project jiva

# List available projects
./step2.list_projects
```

### Development Commands
```bash
# Run development server
python manage.py runserver

# Database operations
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

# Static files
python manage.py collectstatic

# Testing
python manage.py test
```

### Deployment Commands
```bash
# Copy to production
cd Project/build/make
./step4.copy_to_prod

# Git workflow
cd Project/run/jiva
git add -A
git commit -m "Your message"
git push
```

## Directory Structure Quick Reference

```
Project/
├── build/                    # Development tools (not in Git)
│   ├── app_builder/         # Code generation
│   ├── dev_env/            # Development workspace
│   ├── make/               # Scripts (step1-4)
│   └── library/            # Templates
├── config/                  # Configuration files
│   └── config.ini          # Main config
├── run/                    # Production code (in Git)
│   └── jiva/              # Django project
└── docs/                   # Documentation
```

## App Builder Quick Reference

### Generate Basic CRUD
```bash
cd Project/build/app_builder/scripts
python CRUD_ONE_LEVEL.py
```

### Generate Connected CRUD
```bash
python GENERATE_CONNECTED_CRUD_ONE_LEVEL.py
```

### Generate Tree CRUD
```bash
python ONE_LEVEL_TREE_CRUD.py
```

## Common File Locations

### Configuration
- Main config: `Project/config/config.ini`
- Django settings: `Project/run/jiva/jivapms/settings/`
- App config: `Project/run/jiva/config.json`

### Development
- Dev workspace: `Project/build/dev_env/project_area/env_jiva/jiva/`
- Generated code: `Project/build/app_builder/outcome/`

### Production
- Production code: `Project/run/jiva/`
- Django manage.py: `Project/run/jiva/manage.py`

## Workflow Checklist

### Starting Development
- [ ] Run `step1.setup_dev_env`
- [ ] Navigate with `. step3.goto_project jiva`
- [ ] Start development server
- [ ] Create/modify code

### Before Deployment
- [ ] Test all changes
- [ ] Run `python manage.py check`
- [ ] Run tests
- [ ] Verify migrations

### Deployment
- [ ] Run `step4.copy_to_prod`
- [ ] Check git status
- [ ] Commit with meaningful message
- [ ] Push to repository
- [ ] Verify live site

## Troubleshooting Quick Fixes

### Database Issues
```bash
# Reset database
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### Static Files Issues
```bash
python manage.py collectstatic --clear
```

### Import Errors
```bash
python manage.py check
# Check INSTALLED_APPS in settings
```

### Permission Issues
```bash
chmod +x step*.sh  # Fix script permissions
```

## App Structure Template

```
app_[name]/
├── __init__.py
├── admin.py
├── apps.py
├── models.py
├── views.py
├── forms.py
├── urls.py
├── tests.py
├── migrations/
└── templates/
    └── app_[name]/
        ├── [model]_list.html
        ├── [model]_detail.html
        └── [model]_form.html
```

## Model Template

```python
from django.db import models
from django.contrib.auth.models import User

class YourModel(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name
```

## URL Pattern Template

```python
from django.urls import path
from . import views

app_name = 'app_name'

urlpatterns = [
    path('', views.ModelListView.as_view(), name='model_list'),
    path('create/', views.ModelCreateView.as_view(), name='model_create'),
    path('<int:pk>/', views.ModelDetailView.as_view(), name='model_detail'),
    path('<int:pk>/update/', views.ModelUpdateView.as_view(), name='model_update'),
    path('<int:pk>/delete/', views.ModelDeleteView.as_view(), name='model_delete'),
]
```

## Important URLs

### Development
- Local server: `http://localhost:8000`
- Admin: `http://localhost:8000/admin`

### Production
- PythonAnywhere: `https://yourusername.pythonanywhere.com`
- Admin: `https://yourusername.pythonanywhere.com/admin`

## Git Commands Reference

```bash
# Check status
git status

# Stage changes
git add -A

# Commit
git commit -m "Descriptive message"

# Push
git push origin main

# Check history
git log --oneline

# Rollback (careful!)
git reset --hard HEAD~1
```

## Environment Variables

### Development
```bash
export DJANGO_SETTINGS_MODULE=jivapms.settings.development
export DEBUG=True
```

### Production
```bash
export DJANGO_SETTINGS_MODULE=jivapms.settings.production
export DEBUG=False
```

## Key Files to Remember

- `Project/build/make/step*.sh` - Main workflow scripts
- `Project/config/config.ini` - Configuration
- `Project/run/jiva/manage.py` - Django management
- `Project/run/jiva/requirements.txt` - Dependencies
- `Project/docs/` - Documentation
