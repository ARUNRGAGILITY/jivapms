# Development Workflow

## Overview

JIVAPMS uses a streamlined development workflow that automates environment setup, development, and deployment processes.

## Workflow Steps

### 1. Initial Setup

```bash
cd Project/build/make
./step1.setup_dev_env
```

**What it does**:
- Creates development environment in `/build/dev_env/project_area/env_jiva/`
- Copies production code from `/run/jiva/` to development environment
- Sets up isolated development workspace

### 2. Navigate to Development Environment

```bash
. step3.goto_project jiva
```

**What it does**:
- Changes directory to development environment
- Sets up environment variables
- Prepares for development work

**Optional**: List available projects:
```bash
./step2.list_projects
```

### 3. Development Work

Once in the development environment:

```bash
# Run migrations if needed
python manage.py makemigrations
python manage.py migrate

# Create superuser (if needed)
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

### 4. Testing and Validation

```bash
# Run tests
python manage.py test

# Check for issues
python manage.py check
```

### 5. Deploy to Production

```bash
cd Project/build/make
./step4.copy_to_prod
```

**What it does**:
- Copies all changes from development environment to `/run/jiva/`
- Overwrites production code with development changes
- Prepares code for Git commit and deployment

### 6. Git Workflow

```bash
cd Project/run/jiva
git status
git add -A
git commit -m "Your commit message"
git push
```

## Important Workflow Rules

### ✅ DO
- Always work in the development environment (`/build/dev_env/`)
- Use `step1.setup_dev_env` to refresh development environment
- Use `step4.copy_to_prod` before committing to Git
- Test thoroughly in development before copying to production
- Follow the script-based workflow

### ❌ DON'T
- Never edit files directly in `/run/jiva/` (production)
- Don't commit `/build/` directory to Git
- Don't skip the copy-to-prod step
- Don't work directly in production environment

## Environment Variables and Configuration

### Project Configuration
- Main config: `/config/config.ini`
- Django settings: Located in project settings files
- Environment-specific settings handled automatically

### Database
- Development: Uses local SQLite database
- Production: Database files copied during deployment process

## Development Best Practices

### 1. Clean Development Cycles
```bash
# Start fresh development cycle
./step1.setup_dev_env
. step3.goto_project jiva

# Do your development work
# ... make changes ...

# Test changes
python manage.py runserver

# Deploy when ready
./step4.copy_to_prod
```

### 2. Database Management
```bash
# If you need to reset database
rm db.sqlite3
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 3. App Generation
Use the app builder tools in `/build/app_builder/` for generating new apps and CRUD operations.

### 4. Static Files and Media
- Static files: Collected automatically during deployment
- Media files: Handled by Django's media handling system

## Troubleshooting

### Common Issues

1. **Database Migration Issues**
   ```bash
   # Reset migrations
   find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
   python manage.py makemigrations
   python manage.py migrate
   ```

2. **Permission Issues**
   ```bash
   # Fix script permissions
   chmod +x step*.sh
   ```

3. **Environment Issues**
   ```bash
   # Refresh development environment
   ./step1.setup_dev_env
   ```

## Advanced Workflows

### Working with Multiple Projects
The system supports multiple projects. Use `step2.list_projects` to see available projects and `step3.goto_project <project_name>` to switch between them.

### Custom App Generation
Use the scripts in `/build/app_builder/scripts/` to generate new apps and CRUD operations automatically.
