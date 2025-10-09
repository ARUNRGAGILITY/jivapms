# Build System

## Overview

The build system in `/build/` contains all tools and scripts necessary for development, app generation, and deployment automation.

## Directory Structure

```
build/
├── app_builder/        # Code generation tools
├── dev_env/           # Development environment workspace
├── library/           # Django templates and common files
├── make/              # Build and deployment scripts
├── media/             # Default media files
├── MVP1_templates/    # Base HTML templates
├── project_builder/   # Project building tools
└── stage_env/         # Staging environment
```

## Core Scripts (`/build/make/`)

### Environment Management Scripts

#### `step1.setup_dev_env`
**Purpose**: Sets up development environment from production code

```bash
#!/bin/bash
SRC_DIR=../../src
RUN_DIR=../../run
DEV_ENV_DIR=../dev_env
PROJECT_NAME=jiva
mkdir -p "$DEV_ENV_DIR"/project_area/env_"$PROJECT_NAME"
cp -rpf "$RUN_DIR"/"$PROJECT_NAME" "$DEV_ENV_DIR"/project_area/env_"$PROJECT_NAME"/"$PROJECT_NAME"
```

**What it does**:
- Creates development environment directory structure
- Copies production code to development workspace
- Isolates development work from production

#### `step2.list_projects`
**Purpose**: Lists available projects in the development environment

#### `step3.goto_project`
**Purpose**: Navigates to a specific project's development environment

```bash
#!/bin/bash
BASE_PROJECT_DIR="../dev_env/project_area"
PROJECT_NAME="$1"
PROJECT_DIR="$BASE_PROJECT_DIR/env_$PROJECT_NAME/$PROJECT_NAME"
```

**Usage**:
```bash
. step3.goto_project jiva    # Navigate to jiva project
. step3.goto_project         # Use default project (jiva)
```

#### `step4.copy_to_prod`
**Purpose**: Copies development changes to production environment

```bash
#!/bin/bash
SRC_DIR=../../src
RUN_DIR=../../run
DEV_ENV_DIR=../dev_env
PROJECT_NAME=jiva
cp -rpf "$DEV_ENV_DIR"/project_area/env_"$PROJECT_NAME"/"$PROJECT_NAME" "$RUN_DIR"/.
```

**What it does**:
- Copies all changes from development to production
- Overwrites production code with development version
- Prepares code for Git commit and deployment

### Utility Scripts

#### `initial.create_django_project`
**Purpose**: Creates initial Django project structure

#### `last.delete_project`
**Purpose**: Removes project from development environment

#### `create_test_accounts`
**Purpose**: Creates test user accounts for development

#### `app_builder`
**Purpose**: Launches the app builder tools

#### `gitx`
**Purpose**: Git-related operations

## App Builder System (`/build/app_builder/`)

### Scripts Directory (`/build/app_builder/scripts/`)

#### Core CRUD Generation Scripts

1. **`CRUD_ONE_LEVEL.py`**
   - Generates single-level CRUD operations
   - Creates basic model, views, templates, URLs

2. **`CRUD_TOP_LEVEL.py`**
   - Generates top-level CRUD operations
   - More comprehensive than one-level CRUD

3. **`GENERATE_CONNECTED_CRUD_ONE_LEVEL.py`**
   - Generates connected CRUD operations
   - Handles relationships between models

4. **`GENERATE_CRUD_ONE_LEVEL_PC.py`**
   - Generates CRUD with pagination and custom features

5. **`ONE_LEVEL_TREE_CRUD.py`**
   - Generates tree-structured CRUD operations

6. **`TOP_LEVEL_TREE_CRUD.py`**
   - Generates top-level tree CRUD operations

#### Module Generation Scripts

1. **`module_CRUD_one_level_backup.py`**
   - Backup version of module CRUD generation

2. **`module_org_project_CRUD_one_level.py`**
   - Generates organization-project specific modules

### Generated Output (`/build/app_builder/outcome/`)

Directory structure for generated code:
```
outcome/
├── CRUD_ONE_LEVEL/
├── CRUD_TOP_LEVEL/
├── GENERATE_CONNECTED_CRUD_ONE_LEVEL/
├── GENERATE_CRUD_ONE_LEVEL_PC/
├── module_CRUD_one_level/
└── module_org_project_CRUD_one_level/
```

## Library System (`/build/library/django_files/`)

### Template Categories

1. **`BASE_APP_STRUCTURE/`** - Basic Django app templates
2. **`COMMON_APP_FILES/`** - Shared application files
3. **`COMMON_WEB_FILES/`** - Web interface templates
4. **`CONNECTED_APPS/`** - Templates for connected applications
5. **`NEW_UX/`** - New user experience templates
6. **`PRE_BUILT_APPS/`** - Pre-built application templates
7. **`PROJECT_FILES/`** - Project-level templates
8. **`PROJECT_UX/`** - Project user experience templates
9. **`UX_SAMPLES/`** - User experience samples

## Build Process Flow

### 1. Initial Setup
```bash
step1.setup_dev_env → Creates dev environment from production
```

### 2. Development
```bash
step3.goto_project → Navigate to development workspace
app_builder → Generate code using app builder tools
```

### 3. Testing
```bash
# In development environment
python manage.py runserver
```

### 4. Production Deployment
```bash
step4.copy_to_prod → Copy changes to production
# Then commit to Git from /run/jiva/
```

## Using the App Builder

### Generating a Simple CRUD App

1. Navigate to app builder:
   ```bash
   cd Project/build/app_builder/scripts
   ```

2. Run appropriate script:
   ```bash
   python CRUD_ONE_LEVEL.py
   ```

3. Follow prompts to generate app

4. Generated code appears in `/build/app_builder/outcome/`

5. Copy generated code to development environment

6. Test and refine

7. Use `step4.copy_to_prod` to deploy

### Advanced Code Generation

For complex applications with relationships:
- Use `GENERATE_CONNECTED_CRUD_ONE_LEVEL.py`
- Use tree CRUD scripts for hierarchical data

## Configuration Files

### `reference_value_dict.txt`
Contains reference values and configurations used by code generation scripts.

## Best Practices

1. **Always use scripts**: Don't manually copy files between environments
2. **Test in development**: Always test generated code before production
3. **Version control**: Only commit production code (`/run/jiva/`)
4. **Clean builds**: Use `step1.setup_dev_env` to start fresh when needed
5. **Backup**: Keep backups of working configurations
