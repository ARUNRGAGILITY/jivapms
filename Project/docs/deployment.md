# Deployment Guide

## Overview

JIVAPMS uses a streamlined deployment process that copies development code to a production-ready directory and deploys to PythonAnywhere. The deployment system ensures that only tested, production-ready code is committed to Git and deployed.

## Deployment Architecture

```
Development Environment     Production Environment      Git Repository      PythonAnywhere
─────────────────────      ────────────────────      ──────────────      ──────────────
/build/dev_env/    ────▶   /run/jiva/        ────▶   GitHub/GitLab  ────▶  Live Site
project_area/               (Git tracked)              Repository           
env_jiva/jiva/             (Deployment ready)                               
(Not tracked)                                                               
```

## Deployment Process

### Step 1: Development Phase

Work in the development environment:

```bash
cd Project/build/make
./step1.setup_dev_env       # Setup development environment
. step3.goto_project jiva   # Navigate to development workspace

# Do your development work
python manage.py runserver  # Test locally
```

### Step 2: Pre-Deployment Testing

Before deploying, ensure everything works:

```bash
# Run tests
python manage.py test

# Check for issues
python manage.py check

# Verify migrations
python manage.py makemigrations --dry-run
python manage.py migrate --fake-initial

# Test static files
python manage.py collectstatic --dry-run
```

### Step 3: Copy to Production

Copy development changes to production environment:

```bash
cd Project/build/make
./step4.copy_to_prod
```

**What this does**:
- Copies all files from `/build/dev_env/project_area/env_jiva/jiva/` to `/run/jiva/`
- Overwrites production code with development version
- Prepares code for Git commit

### Step 4: Git Workflow

Commit and push production-ready code:

```bash
cd Project/run/jiva

# Check what changed
git status
git diff

# Stage changes
git add -A

# Commit with meaningful message
git commit -m "Add user authentication system"

# Push to repository
git push origin main
```

### Step 5: Deploy to PythonAnywhere

#### Option A: Automatic Deployment (Recommended)

Set up automatic deployment on PythonAnywhere:

1. **Configure Git Hook**:
   ```bash
   # On PythonAnywhere console
   cd /home/yourusername/mysite
   git pull origin main
   ```

2. **Setup Automatic Pull**:
   Create a webhook or scheduled task to pull changes automatically.

#### Option B: Manual Deployment

1. **Access PythonAnywhere Console**:
   ```bash
   # Navigate to your project directory
   cd /home/yourusername/mysite
   
   # Pull latest changes
   git pull origin main
   
   # Install/update requirements
   pip install -r requirements.txt
   
   # Run migrations
   python manage.py migrate
   
   # Collect static files
   python manage.py collectstatic --noinput
   
   # Restart web app
   touch /var/www/yourusername_pythonanywhere_com_wsgi.py
   ```

## Production Environment Setup

### Initial PythonAnywhere Setup

1. **Create PythonAnywhere Account**
2. **Clone Repository**:
   ```bash
   git clone https://github.com/yourusername/your-repo.git mysite
   cd mysite
   ```

3. **Setup Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Configure Web App**:
   - Source code: `/home/yourusername/mysite`
   - Working directory: `/home/yourusername/mysite`
   - WSGI file: Configure Django WSGI

5. **Database Setup**:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py collectstatic
   ```

### WSGI Configuration

Edit the WSGI file on PythonAnywhere:

```python
import os
import sys

# Add project directory to sys.path
path = '/home/yourusername/mysite'
if path not in sys.path:
    sys.path.append(path)

# Set Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'jivapms.settings.production'

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

## Environment-Specific Configurations

### Development Settings
```python
# jivapms/settings/development.py
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
```

### Production Settings
```python
# jivapms/settings/production.py
DEBUG = False
ALLOWED_HOSTS = ['yourusername.pythonanywhere.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

STATIC_URL = '/static/'
STATIC_ROOT = '/home/yourusername/mysite/static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = '/home/yourusername/mysite/media/'

# Security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
```

## Database Management

### Development Database

- SQLite database in development environment
- Automatically created and managed
- Not committed to Git (in .gitignore)

### Production Database

```bash
# Backup production database
cp db.sqlite3 db.sqlite3.backup.$(date +%Y%m%d)

# Apply migrations
python manage.py migrate

# Load initial data (if needed)
python manage.py loaddata initial_data.json
```

## Static Files Management

### Development
```bash
# Static files served by Django development server
python manage.py collectstatic
```

### Production
```bash
# Collect static files for production
python manage.py collectstatic --noinput

# Static files served by web server
```

## Deployment Checklist

### Pre-Deployment
- [ ] All tests pass
- [ ] Code review completed
- [ ] No debug print statements
- [ ] Migrations created and tested
- [ ] Static files work correctly
- [ ] No sensitive data in code
- [ ] Requirements.txt updated

### Deployment
- [ ] `step4.copy_to_prod` executed
- [ ] Git status checked
- [ ] Meaningful commit message
- [ ] Code pushed to repository
- [ ] PythonAnywhere updated
- [ ] Migrations applied
- [ ] Static files collected

### Post-Deployment
- [ ] Site loads correctly
- [ ] All features work
- [ ] No error logs
- [ ] Database intact
- [ ] Admin interface accessible
- [ ] User authentication works

## Rollback Procedures

### Git Rollback
```bash
# Check commit history
git log --oneline

# Rollback to previous commit
git reset --hard HEAD~1

# Force push (be careful!)
git push --force origin main
```

### Database Rollback
```bash
# Restore from backup
cp db.sqlite3.backup.20241008 db.sqlite3

# Rollback migrations
python manage.py migrate app_name 0001
```

### PythonAnywhere Rollback
```bash
# Pull previous version
git checkout HEAD~1

# Apply database backup
# Restart web app
```

## Monitoring and Maintenance

### Log Monitoring
```bash
# Check Django logs
tail -f /var/log/yourusername.pythonanywhere.com.error.log

# Check server logs
tail -f /var/log/yourusername.pythonanywhere.com.server.log
```

### Performance Monitoring
- Monitor response times
- Check database query performance
- Monitor static file loading
- Track error rates

### Regular Maintenance
- Database backups
- Log rotation
- Dependency updates
- Security updates

## Troubleshooting Deployment

### Common Issues

1. **Import Errors**
   ```bash
   # Check Python path
   python -c "import sys; print(sys.path)"
   
   # Verify Django settings
   python manage.py check
   ```

2. **Static Files Not Loading**
   ```bash
   # Collect static files
   python manage.py collectstatic --noinput
   
   # Check static file settings
   python manage.py findstatic admin/css/base.css
   ```

3. **Database Issues**
   ```bash
   # Check database connection
   python manage.py dbshell
   
   # Apply migrations
   python manage.py migrate
   ```

4. **Permission Issues**
   ```bash
   # Fix file permissions
   chmod -R 755 /home/yourusername/mysite
   
   # Fix database permissions
   chmod 664 db.sqlite3
   ```

### Debug Mode in Production
**Never enable DEBUG=True in production!**

For debugging in production:
```python
# Use logging instead
import logging
logger = logging.getLogger(__name__)
logger.error(f"Debug info: {debug_data}")
```

## Automated Deployment Scripts

### Deploy Script
Create a deployment script:

```bash
#!/bin/bash
# deploy.sh

echo "Starting deployment..."

# Copy to production
cd Project/build/make
./step4.copy_to_prod

# Git operations
cd ../../run/jiva
git add -A
git commit -m "$1"  # Commit message as parameter
git push origin main

echo "Deployment complete!"
```

Usage:
```bash
./deploy.sh "Add new user management features"
```

### PythonAnywhere Update Script
```bash
#!/bin/bash
# update_production.sh (run on PythonAnywhere)

cd /home/yourusername/mysite
git pull origin main
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
touch /var/www/yourusername_pythonanywhere_com_wsgi.py

echo "Production updated!"
```

## Best Practices

1. **Always test in development before deployment**
2. **Use meaningful commit messages**
3. **Keep production and development environments as similar as possible**
4. **Backup before major deployments**
5. **Monitor the site after deployment**
6. **Use staging environment for complex changes**
7. **Document all deployment procedures**
8. **Keep deployment scripts updated**
