# Configuration Management

## Overview

JIVAPMS uses a centralized configuration system that manages settings across development and production environments. Configuration files are located in the `/config/` directory and integrated into the Django project.

## Configuration Structure

```
config/
└── config.ini      # Main configuration file
```

## Main Configuration File

### `/config/config.ini`

This is the primary configuration file for the entire project. It uses the INI file format for easy reading and modification.

```ini
# Configuration
[DEFAULT]
# Default settings go here

[DATABASE]
# Database configuration
engine = django.db.backends.sqlite3
name = db.sqlite3

[SECURITY]
# Security settings
debug = False
secret_key = your-secret-key-here

[STATIC_FILES]
# Static files configuration
static_url = /static/
static_root = static/

[MEDIA_FILES]
# Media files configuration
media_url = /media/
media_root = media/

[EMAIL]
# Email configuration
backend = django.core.mail.backends.console.EmailBackend

[LOGGING]
# Logging configuration
level = INFO
```

## Django Settings Integration

### Settings File Structure

The Django project typically has multiple settings files:

```
run/jiva/
├── settings/
│   ├── __init__.py
│   ├── base.py         # Base settings
│   ├── development.py  # Development settings
│   └── production.py   # Production settings
└── config.json         # Additional JSON configuration
```

### Environment-Specific Settings

#### Development Settings (`development.py`)
```python
from .base import *
import configparser
import os

# Read from config.ini
config = configparser.ConfigParser()
config.read(os.path.join(BASE_DIR, '../../../config/config.ini'))

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Database for development
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

#### Production Settings (`production.py`)
```python
from .base import *
import configparser
import os

# Read from config.ini
config = configparser.ConfigParser()
config.read(os.path.join(BASE_DIR, '../../../config/config.ini'))

DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# Production database configuration
DATABASES = {
    'default': {
        'ENGINE': config.get('DATABASE', 'engine'),
        'NAME': config.get('DATABASE', 'name'),
    }
}
```

## Additional Configuration Files

### `config.json`
Located in `/run/jiva/config.json`, this file contains additional configuration in JSON format:

```json
{
    "app_settings": {
        "app_name": "JIVA PMS",
        "version": "1.0.0",
        "description": "Project Management System"
    },
    "features": {
        "kanban": true,
        "scrum": true,
        "analytics": true,
        "blog": true
    },
    "ui_settings": {
        "theme": "default",
        "sidebar_collapsed": false,
        "show_breadcrumbs": true
    },
    "api_settings": {
        "enable_api": true,
        "api_version": "v1",
        "rate_limiting": true
    }
}
```

## Environment Variables

### Development Environment
Set in development scripts or local environment:

```bash
export DJANGO_SETTINGS_MODULE=jivapms.settings.development
export DEBUG=True
export SECRET_KEY=dev-secret-key
```

### Production Environment
Set on PythonAnywhere or production server:

```bash
export DJANGO_SETTINGS_MODULE=jivapms.settings.production
export DEBUG=False
export SECRET_KEY=production-secret-key
```

## Configuration Management Workflow

### 1. Development Configuration

When working in development:

```bash
# Navigate to development environment
. step3.goto_project jiva

# Configuration is automatically loaded from:
# - /config/config.ini (main config)
# - settings/development.py (Django settings)
# - config.json (app-specific settings)
```

### 2. Production Configuration

When deploying to production:

```bash
# Copy to production
./step4.copy_to_prod

# Configuration is loaded from:
# - /config/config.ini (same file)
# - settings/production.py (production Django settings)
# - config.json (same app settings)
```

### 3. Configuration Updates

To update configuration:

1. **Edit main config**:
   ```bash
   # Edit the main configuration
   nano Project/config/config.ini
   ```

2. **Update Django settings** (if needed):
   ```bash
   # Navigate to development
   . step3.goto_project jiva
   
   # Edit settings
   nano jivapms/settings/development.py
   ```

3. **Update app config** (if needed):
   ```bash
   # Edit JSON config
   nano config.json
   ```

4. **Test changes**:
   ```bash
   python manage.py check
   python manage.py runserver
   ```

5. **Deploy changes**:
   ```bash
   cd Project/build/make
   ./step4.copy_to_prod
   ```

## Configuration Categories

### 1. Database Configuration
```ini
[DATABASE]
engine = django.db.backends.sqlite3
name = db.sqlite3
host = localhost
port = 5432
user = jivapms_user
password = secure_password
```

### 2. Security Configuration
```ini
[SECURITY]
debug = False
secret_key = your-very-long-secret-key-here
allowed_hosts = yourdomain.com,www.yourdomain.com
csrf_cookie_secure = True
session_cookie_secure = True
```

### 3. Static and Media Files
```ini
[STATIC_FILES]
static_url = /static/
static_root = /var/www/static/
staticfiles_dirs = static/

[MEDIA_FILES]
media_url = /media/
media_root = /var/www/media/
```

### 4. Email Configuration
```ini
[EMAIL]
backend = django.core.mail.backends.smtp.EmailBackend
host = smtp.gmail.com
port = 587
use_tls = True
host_user = your-email@gmail.com
host_password = your-app-password
```

### 5. Logging Configuration
```ini
[LOGGING]
level = INFO
file = logs/jivapms.log
max_size = 10MB
backup_count = 5
```

## App-Specific Configuration

### Feature Flags
Control which features are enabled:

```json
{
    "features": {
        "kanban": true,
        "scrum": true,
        "analytics": false,
        "blog": true,
        "api": true
    }
}
```

### UI Configuration
Control user interface settings:

```json
{
    "ui_settings": {
        "theme": "dark",
        "sidebar_collapsed": false,
        "show_breadcrumbs": true,
        "items_per_page": 25,
        "date_format": "YYYY-MM-DD"
    }
}
```

### API Configuration
Configure API behavior:

```json
{
    "api_settings": {
        "enable_api": true,
        "api_version": "v1",
        "rate_limiting": true,
        "max_requests_per_hour": 1000,
        "authentication": "token"
    }
}
```

## Configuration Best Practices

### 1. Security
- Never commit sensitive data (passwords, secret keys) to Git
- Use environment variables for sensitive settings
- Different secret keys for development and production

### 2. Environment Separation
- Clear separation between development and production settings
- Use different databases for different environments
- Test configuration changes in development first

### 3. Documentation
- Document all configuration options
- Include examples for each setting
- Keep configuration comments up to date

### 4. Validation
- Validate configuration on startup
- Provide clear error messages for invalid config
- Use sensible defaults where possible

## Troubleshooting Configuration

### Common Issues

1. **Settings Import Errors**
   ```bash
   # Check DJANGO_SETTINGS_MODULE
   echo $DJANGO_SETTINGS_MODULE
   
   # Verify settings file exists
   python manage.py check
   ```

2. **Configuration File Not Found**
   ```bash
   # Check config file path
   ls -la Project/config/config.ini
   
   # Verify relative paths in settings
   ```

3. **Database Connection Issues**
   ```bash
   # Test database connection
   python manage.py dbshell
   
   # Check database settings
   python manage.py check --database default
   ```

4. **Static Files Issues**
   ```bash
   # Collect static files
   python manage.py collectstatic
   
   # Check static files settings
   python manage.py findstatic admin/css/base.css
   ```

### Configuration Debugging

Enable debug logging for configuration:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Add to settings file to debug configuration loading
print(f"Loading configuration from: {config_file_path}")
print(f"Current settings module: {os.environ.get('DJANGO_SETTINGS_MODULE')}")
```
