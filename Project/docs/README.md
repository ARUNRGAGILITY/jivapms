# JIVA Project Management System (JIVAPMS)

A custom Django project with specialized conventions for rapid application development and deployment.

## Overview

JIVAPMS is a comprehensive project management system built with Django that follows a unique development workflow designed for rapid prototyping, development, and deployment to platforms like PythonAnywhere.

## Project Structure

```
Project/
├── build/          # Development tools and scripts
├── config/         # Configuration files
├── run/           # Production-ready code (Git tracked)
└── docs/          # Documentation
```

## Key Features

- **Automated Development Workflow**: Scripts for setting up dev environments
- **Code Generation**: Automated CRUD generation and app building tools
- **Dual Environment System**: Separate development and production environments
- **Git Integration**: Smart deployment workflow to production

## Quick Start

1. **Setup Development Environment**
   ```bash
   cd Project/build/make
   ./step1.setup_dev_env
   ```

2. **Navigate to Project**
   ```bash
   . step3.goto_project jiva
   ```

3. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

4. **Deploy to Production**
   ```bash
   ./step4.copy_to_prod
   ```

## Documentation Structure

- [Project Architecture](architecture.md) - Overall system design
- [Development Workflow](development-workflow.md) - How to work with the project
- [Build System](build-system.md) - Build tools and scripts
- [App Builder](app-builder.md) - Code generation tools
- [Configuration](configuration.md) - Configuration management
- [Deployment](deployment.md) - Deployment procedures
- [Conventions](conventions.md) - Project conventions and standards

## Getting Started

For detailed instructions, see the [Development Workflow](development-workflow.md) guide.

## Contributing

Please read our [Conventions](conventions.md) before contributing to the project.
