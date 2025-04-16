import sys
import os
import subprocess
from utils import *
from utils_django import *

DJANGO_PROJECTS_DIRNAME = "dev_env"
PROJECTAREA_DIRNAME = "project_area"

#
# CREATE PROJECT
#
def create_project(project_name, verbose):
    base_dir = get_base_projects_directory()
    env_project_dirname, project_dirname, std_project_name, project_parent_dir = get_project_details(project_name, verbose)      
    verbose_print(verbose, f">>> Env Project: {env_project_dirname} <<<")
    verbose_print(verbose, f">>> Project Name: {project_dirname} <<<")
    verbose_print(verbose, f">>> Project Parent Directory: {project_parent_dir} <<<")
    if not os.path.exists(project_parent_dir):
        os.makedirs(project_parent_dir)
    else:
        print(f"Project '{std_project_name}' already exists in dir '{project_parent_dir}'")
        return
        
    try:
        subprocess.run(["django-admin", "startproject", std_project_name, project_parent_dir],
                                            check=True)
        print(f"Project '{std_project_name}' created successfully in dir '{project_parent_dir}' ")
    except subprocess.CalledProcessError as e:
        print(f"Failed to create Project '{std_project_name}'. Error: {str(e)}")
    
    # Create the common and web apps
    app_name = "common"
    env_project_dirname, project_dirname, std_project_name, project_parent_dir, project_dir, std_app_name, app_dir = get_app_details(project_name, app_name, verbose)
    # special case for certain apps
    src_app_web_files_dir = os.path.join(base_dir, "library", "django_files", "COMMON_APP_FILES")
    copy_directory_contents(src_app_web_files_dir, app_dir)
    app_name = "web"
    env_project_dirname, project_dirname, std_project_name, project_parent_dir, project_dir, std_app_name, app_dir = get_app_details(project_name, app_name, verbose)
    src_app_web_files_dir = os.path.join(base_dir, "library", "django_files", "COMMON_WEB_FILES")
    copy_directory_contents(src_app_web_files_dir, app_dir)
    app_name = "loginsystem"
    env_project_dirname, project_dirname, std_project_name, project_parent_dir, project_dir, std_app_name, app_dir = get_app_details(project_name, app_name, verbose)
    src_app_web_files_dir = os.path.join(base_dir, "library", "django_files", "PRE_BUILT_APPS", "app_loginsystem")
    copy_directory_contents(src_app_web_files_dir, app_dir)
    # copy PROJECT FILES
    var_value_dict = {"__PROJECTNAME__": std_project_name, 
                      "__SITETITLE__": project_name.title(),
                      }
    src_project_files_dir = os.path.join(base_dir, "library", "django_files", "PROJECT_FILES")
    project_dir = os.path.join(project_parent_dir, std_project_name)
    copy_directory_contents(src_project_files_dir, project_dir)
    replace_placeholders_in_files(project_dir, var_value_dict)
    
    # create static and media folder
    static_dir = os.path.join(project_parent_dir, "static")
    media_dir = os.path.join(project_parent_dir, "media")
    create_directory(static_dir)
    create_directory(media_dir)
    
   
#
# CREATE APP
#
def create_app(project_name, app_name, verbose):
    base_dir = get_base_projects_directory()
    env_project_dirname, project_dirname, std_project_name, project_parent_dir, project_dir, std_app_name, app_dir = get_app_details(project_name, app_name, verbose)

    verbose_print(verbose, f">>> Project Directory: {project_dir} <<<")
    verbose_print(verbose, f">>> App Directory: {app_dir} <<<")
    verbose_print(verbose, f">>> Creating app '{std_app_name}' in project '{std_project_name}' <<<")
    if os.path.exists(app_dir):
        print(f"Project '{std_project_name}' / '{std_app_name} already exists in dir '{project_parent_dir}'")
        return
    python_executable = sys.executable
    #print(f">>> ====================== CHECK {python_executable} =================================== <<< ===")
    manage_py = os.path.join(project_parent_dir, 'manage.py')
    # Use subprocess to call manage.py from within its containing directory
    try:
        # Running subprocess from the directory containing manage.py
        subprocess.run([python_executable, manage_py, "startapp", std_app_name], cwd=project_parent_dir, check=True)
        print(f"App '{std_app_name}' created successfully in project '{project_name}' at {app_dir}/")
    except subprocess.CalledProcessError as e:
        print(f"Failed to create app '{std_app_name}'. Error: {str(e)}")
   
    # ========================================================================================================
    # create module for this app
    # ========================================================================================================
    base_dir = get_base_projects_directory()
    mod_app_files = os.path.join(base_dir, "library", "django_files"
                                                , "BASE_APP_STRUCTURE", "mod_files")
    
    src_module_base_files = mod_app_files
    dst_module_base_files = os.path.join(app_dir, "mod_app")
    copy_directory_contents(src_module_base_files, dst_module_base_files)
    verbose_print(verbose, f">>> SRC Module: {src_module_base_files} <<<")
    verbose_print(verbose, f">>> DST Module: {dst_module_base_files} <<<")    
    
    # delete specific files of this created app
    views_file = os.path.join(app_dir, "views.py")
    models_file = os.path.join(app_dir, "models.py")
    delete_specific_file_or_dir(views_file)
    delete_specific_file_or_dir(models_file)
    
    # Create template directories
    template_dir = os.path.join(app_dir, "templates", std_app_name)
    create_directory(template_dir)
    template_mod_app = os.path.join(template_dir, "mod_app")
    create_directory(template_mod_app)
    
    
    
#
# CREATE MOD
#    
def create_mod(project_name, app_name, mod_name, verbose):
    base_dir = get_base_projects_directory()
    env_project_dirname, project_dirname, std_project_name, project_parent_dir, project_dir, std_app_name, app_dir = get_app_details(project_name, app_name, verbose)
    std_mod_name = f"mod_{mod_name}"
    mod_dir = app_dir + f"/{std_mod_name}"
    if os.path.exists(mod_dir):
        print(f"Project '{std_project_name}' / '{std_app_name} / '{std_mod_name} already exists in dir '{project_parent_dir}'")
        return
    verbose_print(verbose, f">>> Module: {mod_dir} <<<")
    
    # Create template directories
    template_dir = os.path.join(app_dir, "templates", std_app_name)
    create_directory(template_dir)
    template_mod_name = os.path.join(template_dir, f"{std_mod_name}")
    create_directory(template_mod_name)
    
    # create placeholder files for now or copy from existing 
    
    # create the module directory
    create_directory(mod_dir)
    
    create_empty_file(os.path.join(mod_dir, "__init__.py"))
    create_empty_file(os.path.join(mod_dir, f"urls_{mod_name}.py"))
    fill_empty_urls_file(os.path.join(mod_dir, f"urls_{mod_name}.py"))
    create_empty_file(os.path.join(mod_dir, f"models_{mod_name}.py"))
    create_empty_file(os.path.join(mod_dir, f"views_{mod_name}.py"))
    create_empty_file(os.path.join(mod_dir, f"forms_{mod_name}.py"))
    if mod_name == "app":
        create_empty_file(os.path.join(mod_dir, f"urls_app.py")) 
    
    # update the urls_app.py of the app based on the modules
    generate_urls(app_dir, "urls_app")
    

def fill_empty_urls_file(urls_file_path):    
    with open(urls_file_path, 'w') as urls_file:
        urls_file.write("from django.urls import include, path\n\n")
        urls_file.write("urlpatterns = [\n")
        urls_file.write("]\n")
    print(f"Created empty URLs file: {urls_file_path}")
    
#
# UPDATE APP URLS_APP after module finalizations
#    
def update_app_urls(project_name, app_name, verbose):
    base_dir = get_base_projects_directory()
    env_project_dirname, project_dirname, std_project_name, project_parent_dir, project_dir, std_app_name, app_dir = get_app_details(project_name, app_name, verbose)
    # update the urls_app.py of the app based on the modules
    generate_urls(app_dir, "urls_app")
    
    
usage = """
Usage: django.py django <projectname> [--verbose] or django.py django <projectname>.<appname> [--verbose] or django.py django projetname.appname.modname

"""



def main():
    if len(sys.argv) < 3 or sys.argv[1] != "django":
        print("Usage: django.py django <projectname> [--verbose] or django.py django <projectname>.<appname>.<mod_name> [--verbose]")
        sys.exit(1)

    verbose = '--verbose' in sys.argv
    parts = sys.argv[2].split('.')
    
    if len(parts) == 1:
        create_project(parts[0], verbose)
    elif len(parts) == 2:
        create_app(parts[0], parts[1], verbose)
    elif len(parts) == 3:
        create_mod(parts[0], parts[1], parts[2], verbose)
    else:
        print("Invalid command format. Use 'django.py django projectname' or 'django.py django projectname.appname' or django.py django projectname.appname.modname.")
        sys.exit(1)

if __name__ == "__main__":
    main()
