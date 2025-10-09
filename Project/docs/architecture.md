# Project Architecture

## Overview

JIVAPMS follows a unique three-tier directory structure that separates development tools, configuration, and production code.

## Directory Structure

### `/build` - Development Tools and Scripts
- **Purpose**: Contains all development-related tools, scripts, and temporary files
- **Git Status**: Not tracked in Git (development only)
- **Key Components**:
  - `app_builder/` - Code generation tools
  - `dev_env/` - Development environment workspace
  - `make/` - Build and deployment scripts
  - `library/` - Django templates and common files

### `/config` - Configuration Management
- **Purpose**: Centralized configuration files
- **Files**: `config.ini` - Main configuration file

### `/run` - Production Code
- **Purpose**: Contains the actual Django project ready for deployment
- **Git Status**: Tracked in Git and deployed to production
- **Structure**: Standard Django project with apps

## Development vs Production Workflow

### Development Environment (`/build/dev_env`)
```
build/dev_env/project_area/env_jiva/jiva/
```
- Working directory for development
- Contains copy of production code
- Changes made here during development
- Not tracked in Git

### Production Environment (`/run`)
```
run/jiva/
```
- Production-ready Django project
- Tracked in Git
- Deployed to PythonAnywhere
- Updated via `step4.copy_to_prod` script

## App Structure

The Django project follows a modular app structure:

### Core Apps
- `app_common/` - Shared utilities and common functionality
- `app_authz/` - Authorization and permissions
- `app_loginsystem/` - Authentication system
- `app_user/` - User management
- `app_web/` - Web interface components

### Domain-Specific Apps
- `app_organization/` - Organization management
- `app_project/` - Project management
- `app_memberprofilerole/` - Member profiles and roles
- `app_kanban/` - Kanban board functionality
- `app_scrum/` - Scrum methodology support
- `app_analytics/` - Analytics and reporting

### Content Apps
- `app_org_blog/` - Organizational blog
- `app_postnote/` - Notes and posts

## Data Flow

1. **Development**: Work in `/build/dev_env/project_area/env_jiva/jiva/`
2. **Testing**: Run Django server in development environment
3. **Production Copy**: Use `step4.copy_to_prod` to copy to `/run/jiva/`
4. **Git Commit**: Commit changes in `/run/jiva/`
5. **Deployment**: Push to PythonAnywhere

## Key Design Principles

1. **Separation of Concerns**: Clear separation between development tools and production code
2. **Automated Workflows**: Scripts handle environment setup and deployment
3. **Code Generation**: Automated CRUD and app generation for rapid development
4. **Version Control**: Only production code is tracked in Git
5. **Deployment Ready**: Production environment is always deployment-ready
