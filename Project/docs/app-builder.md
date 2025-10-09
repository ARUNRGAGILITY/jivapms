# App Builder Documentation

## Overview

The App Builder is a powerful code generation system that automates the creation of Django apps, CRUD operations, and complete modules. It's located in `/build/app_builder/` and provides various scripts for different types of app generation.

## Architecture

```
app_builder/
├── scripts/           # Code generation scripts
├── outcome/          # Generated code output
├── adv_scripts/      # Advanced generation scripts
└── test/            # Test configurations
```

## Available Generation Scripts

### Basic CRUD Generation

#### 1. CRUD_ONE_LEVEL.py
**Purpose**: Generates basic single-level CRUD operations

**Features**:
- Basic model with standard fields
- List, create, read, update, delete views
- Bootstrap-based templates
- URL configuration
- Basic form handling

**Usage**:
```bash
cd Project/build/app_builder/scripts
python CRUD_ONE_LEVEL.py
```

**Generated Structure**:
```
models.py      # Django model definition
views.py       # CRUD views
forms.py       # Django forms
urls.py        # URL patterns
templates/     # HTML templates
  ├── list.html
  ├── detail.html
  ├── create.html
  └── update.html
```

#### 2. CRUD_TOP_LEVEL.py
**Purpose**: Generates comprehensive top-level CRUD with advanced features

**Features**:
- Enhanced model with metadata
- Advanced filtering and searching
- Pagination support
- Bulk operations
- Export functionality
- Advanced permissions

### Connected CRUD Generation

#### 3. GENERATE_CONNECTED_CRUD_ONE_LEVEL.py
**Purpose**: Generates CRUD operations for related models

**Features**:
- Foreign key relationships
- Related model management
- Nested forms
- Inline editing
- Relationship validation

**Use Cases**:
- Parent-child relationships (e.g., Organization → Projects)
- One-to-many relationships
- Managing related data together

#### 4. GENERATE_CRUD_ONE_LEVEL_PC.py
**Purpose**: Generates CRUD with pagination and custom features

**Features**:
- Built-in pagination
- Custom field handling
- Advanced form widgets
- File upload support
- Custom validation

### Tree Structure Generation

#### 5. ONE_LEVEL_TREE_CRUD.py
**Purpose**: Generates CRUD for tree-structured data

**Features**:
- Hierarchical data support
- Parent-child navigation
- Tree display widgets
- Drag-and-drop reordering
- Breadcrumb navigation

#### 6. TOP_LEVEL_TREE_CRUD.py
**Purpose**: Generates comprehensive tree CRUD operations

**Features**:
- Multi-level tree support
- Advanced tree operations
- Tree visualization
- Bulk tree operations

### Module Generation

#### 7. module_CRUD_one_level_backup.py
**Purpose**: Backup version of module CRUD generation

#### 8. module_org_project_CRUD_one_level.py
**Purpose**: Generates organization-project specific modules

**Features**:
- Organization context
- Project management
- Role-based access
- Multi-tenant support

## Configuration System

### reference_value_dict.txt
Contains configuration values used by generation scripts:

```python
# Sample configuration values
APP_PREFIX = "app_"
MODEL_PREFIX = "Model"
DEFAULT_FIELDS = ["name", "description", "created_at", "updated_at"]
TEMPLATE_THEME = "bootstrap4"
```

## Using the App Builder

### Step 1: Choose Generation Type

Determine what type of app you need:
- **Simple CRUD**: Use `CRUD_ONE_LEVEL.py`
- **Advanced CRUD**: Use `CRUD_TOP_LEVEL.py`
- **Related Models**: Use `GENERATE_CONNECTED_CRUD_ONE_LEVEL.py`
- **Tree Structure**: Use tree CRUD scripts
- **Complete Module**: Use module generation scripts

### Step 2: Run Generation Script

```bash
cd Project/build/app_builder/scripts
python CRUD_ONE_LEVEL.py
```

### Step 3: Provide Input

Scripts will prompt for:
- App name
- Model name
- Field definitions
- Relationships (if applicable)
- Template preferences

### Step 4: Review Generated Code

Generated code appears in `/build/app_builder/outcome/[SCRIPT_NAME]/`

Review generated files:
- `models.py` - Check model definition
- `views.py` - Verify view logic
- `forms.py` - Validate form fields
- `templates/` - Check UI templates
- `urls.py` - Verify URL patterns

### Step 5: Integrate into Project

1. Copy generated files to development environment:
   ```bash
   cd Project/build/make
   . step3.goto_project jiva
   ```

2. Create new app directory:
   ```bash
   mkdir app_[your_app_name]
   ```

3. Copy generated files to app directory

4. Update main `settings.py`:
   ```python
   INSTALLED_APPS = [
       # ... existing apps
       'app_your_app_name',
   ]
   ```

5. Update main `urls.py`:
   ```python
   urlpatterns = [
       # ... existing patterns
       path('your_app/', include('app_your_app_name.urls')),
   ]
   ```

### Step 6: Test and Refine

1. Run migrations:
   ```bash
   python manage.py makemigrations app_your_app_name
   python manage.py migrate
   ```

2. Test the app:
   ```bash
   python manage.py runserver
   ```

3. Navigate to `http://localhost:8000/your_app/`

### Step 7: Deploy

```bash
cd Project/build/make
./step4.copy_to_prod
```

## Advanced Features

### Custom Templates

The app builder uses templates from `/build/library/django_files/`:

- **BASE_APP_STRUCTURE**: Basic app templates
- **COMMON_WEB_FILES**: Web interface templates
- **NEW_UX**: Modern UI templates

### Customization Options

#### Model Customization
- Add custom fields
- Define relationships
- Set up validation rules
- Configure metadata

#### View Customization
- Custom filtering
- Search functionality
- Pagination settings
- Permission handling

#### Template Customization
- UI themes
- Custom styling
- JavaScript integration
- Responsive design

## Generated Code Structure

### Typical Generated App Structure
```
app_[name]/
├── __init__.py
├── admin.py
├── apps.py
├── models.py          # Generated model
├── views.py           # CRUD views
├── forms.py           # Django forms
├── urls.py            # URL patterns
├── migrations/
└── templates/
    └── app_[name]/
        ├── list.html
        ├── detail.html
        ├── create.html
        ├── update.html
        └── delete.html
```

### Model Features
```python
class GeneratedModel(models.Model):
    # Standard fields
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    
    # Metadata fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # User tracking
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = "Generated Models"
```

### View Features
```python
# List view with pagination and search
class ModelListView(ListView)

# Detail view with related objects
class ModelDetailView(DetailView)

# Create view with form validation
class ModelCreateView(CreateView)

# Update view with permission checking
class ModelUpdateView(UpdateView)

# Delete view with confirmation
class ModelDeleteView(DeleteView)
```

## Best Practices

### 1. Planning
- Define your data model clearly before generation
- Consider relationships between models
- Plan your URL structure

### 2. Generation
- Use descriptive names for apps and models
- Follow Django naming conventions
- Test generated code before customization

### 3. Customization
- Make a backup before major customizations
- Document custom changes
- Test thoroughly after modifications

### 4. Integration
- Follow the project's app naming conventions
- Update documentation for new apps
- Ensure proper permissions are set

## Troubleshooting

### Common Issues

1. **Import Errors**
   - Check app is in `INSTALLED_APPS`
   - Verify import paths in generated code

2. **Template Not Found**
   - Ensure templates are in correct directory
   - Check template names in views

3. **URL Conflicts**
   - Verify URL patterns don't conflict
   - Use proper namespacing

4. **Migration Issues**
   - Run `makemigrations` for new app
   - Handle model relationships carefully

### Getting Help

- Check generated code for comments
- Review the reference configuration
- Test with simple examples first
- Use the development environment for testing
