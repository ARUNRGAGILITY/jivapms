
from app_organization.mod_app.all_view_imports import *
from app_organization.mod_project.models_project import *
from app_organization.mod_project.forms_project import *
from app_common.mod_app.all_view_imports import *
from app_organization.mod_organization.models_organization import *
from app_common.mod_common.models_common import *
from app_memberprofilerole.mod_role.models_role import *
from app_jivapms.mod_app.all_view_imports import *
from app_organization.org_decorators import *
from app_organization.mod_projectmembership.models_projectmembership import *
from app_organization.mod_project_template.models_project_template import *
from app_organization.mod_project_roadmap.models_project_roadmap import *
from app_organization.mod_project_detail.forms_project_detail import *
from app_organization.mod_project_template.forms_project_template import *
from app_organization.mod_dev_value_stream.models_dev_value_stream import *

from app_organization.mod_backlog.models_backlog import *

app_name = 'app_organization'
app_version = 'v1'

module_name = 'projects'
module_path = f'mod_project'
from app_organization.mod_backlog.views_project_tree import  get_tree_name_id
@login_required
def project_roadmap(request, org_id, project_id):
    user = request.user
    org_id = int(org_id)
    project_id = int(project_id)
    org = Organization.objects.get(pk=org_id)
    project = Project.objects.get(pk=project_id)
    #project_roadmaps = ProjectRoadmap.objects.filter(pro=project, roadmap_name="HIGH-LEVEL-ROADMAP").delete()
    #logger.debug(f">>> === TEST: PROJECT ROADMAP: {project_roadmaps} === <<<")
    
    project_roadmap = ProjectRoadmap.objects.get_or_create(pro=project, roadmap_name="HIGH-LEVEL-ROADMAP", active=True)
    
    project_id_str = f"{project_id}_PROJECT_TREE"
    BACKLOG_TYPE_NODE_OBJ = BacklogType.objects.get(name=project_id_str)
    logger.debug(f">>> === TEST: PROJECT ROADMAP: {BACKLOG_TYPE_NODE_OBJ} === <<<")
    bt_tree_name_and_id = get_tree_name_id(BACKLOG_TYPE_NODE_OBJ)
    #logger.debug(f">>> === TEST: PROJECT ROADMAP: {bt_tree_name_and_id} === <<<")
    epic_type_id = bt_tree_name_and_id.get("Epic")
    epic_type_node, created = BacklogType.objects.get_or_create(id=epic_type_id)    
    
    bug_type_id = bt_tree_name_and_id.get("Bug")
    story_type_id = bt_tree_name_and_id.get("User Story")
    tech_task_type_id = bt_tree_name_and_id.get("Technical Task")
    
    feature_type_id = bt_tree_name_and_id.get("Feature")
    component_type_id = bt_tree_name_and_id.get("Component")
    capability_type_id = bt_tree_name_and_id.get("Capability")
    
    # display roadmap
    # display_roadmap = Backlog.objects.filter(pro=project, type=epic_type_node, active=True)
    include_roadmap_items = [epic_type_node,  feature_type_id, component_type_id, capability_type_id]
    display_roadmap = Backlog.objects.filter(pro=project, type__in=include_roadmap_items, active=True)
    
    # Prepare tasks for Gantt chart
    tasks = []
    for idx, item in enumerate(display_roadmap):   
            tasks.append({
                "id": str(item.id),
                "name": f"{item.type.name}: {item.name}",
                # Default start date as today if missing
                "start": item.start_date.strftime("%Y-%m-%d") if item.start_date else date.today().strftime("%Y-%m-%d"),
                # Default end date as start_date + 2 days if end_date is missing
                "end": (item.end_date if item.end_date else (
                    item.start_date if item.start_date else date.today()) + timedelta(days=5)
                ).strftime("%Y-%m-%d"),
                "progress": item.progress if item.progress is not None else 10,  # Default progress is 0%
                "type": item.type.name,
                "custom_class": "gantt-bar-" + item.type.name.lower().replace(" ", "-")  # Generates class like 'gantt-bar-epic'
            })

    # Prepare the context for the template
    context = {
        'parent_page': 'Projects',
        'page': 'list_projects',
        'organization': project.org,
        'org': org,
        'org_id': org_id,
        'user': user,
        'project': project,
        'project_roadmap': project_roadmap,
        'display_roadmap': display_roadmap,
        'tasks': tasks,
        'tasks_json': json.dumps(tasks),
        
        'page_title': f"{project.name} Roadmap",
    }

    template_file = f"{app_name}/{module_path}/project_roadmap/project_roadmap.html"
    return render(request, template_file, context)
    
    
@login_required
def ajax_update_project_roadmap(request):
    if request.method == "POST":
        try:
            # Parse JSON data from request
            data = json.loads(request.body)
            task_id = data.get('id')
            start = data.get('start')
            end = data.get('end')
            progress = data.get('progress')

            # Fetch task from database
            task = Backlog.objects.get(id=task_id)
            
            # Parse ISO 8601 datetime strings, ignoring time part
            start_date = datetime.fromisoformat(start.replace('Z', '')).date()  # Converts to date
            end_date = datetime.fromisoformat(end.replace('Z', '')).date()


            # Update fields
            task.start_date = start_date
            task.end_date = end_date
            task.progress = progress
            task.save()  # Save changes

            # Return success response
            return JsonResponse({"status": "success", "message": "Task updated successfully."})
        except Backlog.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Task not found."}, status=404)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)

    return JsonResponse({"status": "error", "message": "Invalid request."}, status=400)
