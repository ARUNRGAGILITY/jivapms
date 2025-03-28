from app_organization.mod_project.models_project import *

from app_organization.mod_app.all_view_imports import *
from app_organization.mod_backlog.models_backlog import *
from app_organization.mod_backlog.forms_backlog import *
from app_organization.mod_org_release.models_org_release import *
from app_organization.mod_persona.models_persona import *
from app_organization.mod_activity.models_activity import *
from app_organization.mod_collection.models_collection import *

from app_organization.mod_project_detail.models_project_detail import *

from app_organization.mod_step.models_step import *
from app_common.mod_app.all_view_imports import *
from app_jivapms.mod_app.all_view_imports import *

from app_common.mod_app.all_view_imports import *
from app_jivapms.mod_web.views_web import *

app_name = 'app_organization'
app_version = 'v1'

module_name = 'backlog'
module_path = f'mod_backlog'


@login_required
def ajax_project_tree_sorted(request):
    if request.method == 'POST':
        ajax_data = request.POST['sorted_list_data']
        model_name = request.POST['model_name']
        given_app_name = app_name
        if 'app_name' in request.POST:            
            given_app_name = request.POST['app_name']
        new_data = ajax_data.replace("[",'')
        new_data = new_data.replace("]",'')
        sorted_list = new_data.split(",")
        seq = 1
        
        #model_class = globals()[model_name]
        model_class = apps.get_model(given_app_name, model_name)
        logger.debug(f">>> === AJAX UPDATE SORTED === <<<")
        for item in sorted_list:
            str = item.replace('"','')
            position = str.split('_')
            logger.debug(f">>> === AJAX UPDATE SORTED {position} === <<<")
            model_class.objects.filter(pk=position[0]).update(position=seq, author=request.user)
            seq = seq + 1
        context = {'page': 'Sorted Value', 
                   'active_tab': 'sorted_value',
                   'ajax_data': ajax_data}
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


# Sequence the backlog items for addition at top
def seq_add_to_top_err1(ajax_data):
    seq = 2
    new_data = ajax_data.replace("[",'')
    new_data = new_data.replace("]",'')
    sorted_list = new_data.split(",")
    logger.debug(f">>> === SEQ ADD TO TOP: {sorted_list} === <<<")
    for item in sorted_list:
        str = item.replace('"','')
        position = str.split('_')
        Backlog.objects.filter(pk=position[0]).update(position=seq)
        logger.debug(f">>> === SEQ ADD TO TOP: {position[0]} with {seq} === <<<")
        seq += 1
        
def seq_add_to_top(ajax_data):
    seq = 2    
    new_data = ajax_data.strip().replace("[", "").replace("]", "")
    if not new_data:
        logger.debug(">>> === SEQ ADD TO TOP: Empty data list, no processing required === <<<")
        return

    # Process the cleaned data
    sorted_list = new_data.split(",")
    logger.debug(f">>> === SEQ ADD TO TOP: {sorted_list} === <<<")
    for item in sorted_list:
        # Remove extra quotes and validate
        item = item.strip().replace('"', '')        
        if not item:  # Skip empty strings
            continue
        position = item.split('_')
        # Ensure position is valid
        if len(position) < 1 or not position[0].isdigit():
            logger.debug(f">>> === Invalid position format: {item} === <<<")
            continue
        # Update backlog position
        Backlog.objects.filter(pk=position[0]).update(position=seq)
        logger.debug(f">>> === SEQ ADD TO TOP: {position[0]} with {seq} === <<<")
        seq += 1

# GENERAL-HELPER-METHOD
def jivapms_mod_backlog_helper_get_backlog_details(request, project_id):
    # Automate this further
    user = request.user
    member = get_object_or_404(Member, user=user)
    project = Project.objects.get(id=project_id)
    
    # 1. Backlog Super Type
    pbst_name = f"{project.id}_PROJECT_TREE"
    project_backlog_super_type, created = BacklogSuperType.objects.get_or_create(pro=project, name=pbst_name)
    # 2. Backlog Type
    pbst_name = f"{project.id}_PROJECT_TREE"
    project_backlog_type = BacklogType.objects.get(pro=project, name=pbst_name)
    config = PROJECT_WBS_TREE_CONFIG
    created_node = create_or_update_tree_from_config(config, model_name="app_organization.BacklogType", 
                                                     parent=project_backlog_type, project=project)
    tree_structure = list_tree_structure(created_node)
    bt_tree_name_and_id = get_tree_name_id(created_node)
    
    epic_type_id = bt_tree_name_and_id.get("Epic")
    epic_type_node = BacklogType.objects.get(id=epic_type_id, active=True)
    epic_type_parent = epic_type_node.parent
    epic_type_children = epic_type_node.get_active_children()
    backlog_types = epic_type_children
    backlog_types_count = backlog_types.count()
    pb_name = f"{project.id}_PROJECT_TREE"
    project_backlog, created = Backlog.objects.get_or_create(pro=project, name=pb_name, type=project_backlog_type)
    strategic_theme_id = bt_tree_name_and_id.get("Strategic Theme")
    initiative_id = bt_tree_name_and_id.get("Initiative")
    exclude_types = [strategic_theme_id, initiative_id]
    bug_type_id = bt_tree_name_and_id.get("Bug")
    story_type_id = bt_tree_name_and_id.get("User Story")
    tech_task_type_id = bt_tree_name_and_id.get("Technical Task")
    feature_type_id = bt_tree_name_and_id.get("Feature")
    component_type_id = bt_tree_name_and_id.get("Component")
    capability_type_id = bt_tree_name_and_id.get("Capability")
    include_types = [bug_type_id, story_type_id, tech_task_type_id]
    include_type_id_name = {bug_type_id: "Bug", story_type_id: "User Story", tech_task_type_id: "Technical Task"}
    include_collection_types = [feature_type_id, component_type_id, capability_type_id, epic_type_id]
    regular_items_in_backlog = Backlog.objects.filter(pro=project, type__in=include_types, active=True)
    collections_in_backlog = Backlog.objects.filter(pro=project, type__in=include_collection_types, active=True)
    
    send_data = {}
    send_data["backlog_types"] = backlog_types
    send_data['include_type_id_name'] = include_type_id_name
    send_data["include_types"] = include_types
    send_data["include_collection_types"] = include_collection_types
    send_data["count_regular_items_in_backlog"] = regular_items_in_backlog.count()
    send_data["count_collections_in_backlog"] = collections_in_backlog.count()
    send_data["regular_items_in_backlog"] = regular_items_in_backlog
    send_data["count_collections_in_backlog"] = collections_in_backlog.count()
    send_data["collections_in_backlog"] = collections_in_backlog
    return send_data
    

### KANBAN / BOARD SETTINGS
@login_required
def project_tree_board_settings(request, pro_id):
    user = request.user
    member = get_object_or_404(Member, user=user)
    project = Project.objects.get(id=pro_id)
  
    # send outputs (info, template,
    context = {
        'parent_page': '__PARENTPAGE__',
        'page': 'project_tree_board_settings',
        'user': user,
        'member': member,
        'pro': project,
        'project': project,
        'pro_id': pro_id,
        'org': project.org,
        'org_id': project.org_id,
       
    }       
    template_file = f"{app_name}/{module_path}/board_related/project_tree_board_settings.html"
    return render(request, template_file, context)

from django.forms.models import model_to_dict
@login_required
def edit_project_tree_backlog_item(request, pro_id, backlog_item_id):
    user = request.user
    member = get_object_or_404(Member, user=user)
    project = Project.objects.get(id=pro_id)
    backlog_item = Backlog.objects.get(id=backlog_item_id)

    back_to = None
    project_id = None
    back_to_info = request.GET.get('back_to')
    if  back_to_info != None and back_to_info == 'view_project_tree_board':
        back_to = request.GET.get('back_to')
        project_id = request.GET.get('project_id')
    if  back_to_info != None and back_to_info == 'view_iteration_kanban':
        back_to = request.GET.get('back_to')
        org_id = request.GET.get('org_id')
        project_id = request.GET.get('project_id')


    backlog_item_type = backlog_item.type
    backlog_item_parent = backlog_item.parent
    backlog_item_children = backlog_item.get_active_children()
    get_data = jivapms_mod_backlog_helper_get_backlog_details(request, pro_id)
    backlog_types = get_data["backlog_types"]
    form = None 
    form = PBIBacklogForm(request.POST or None, instance=backlog_item, org_id=project.org.id)
    parent_id = backlog_item.parent_id
    logger.debug(f">>> === BACKLOG ITEM: {model_to_dict(backlog_item)} {backlog_item.id} === <<<")
    if request.method == 'POST':
        if form.is_valid():
            print(">>> Form is valid. Saving data...")  # Debugging
            form.instance.parent_id = backlog_item_parent.id
            # form.instance.type = backlog_item_type
            form.instance.author = user
            form.instance.active = True  # Ensure it's always active
            form.save()
            updated_backlog_item = Backlog.objects.get(id=backlog_item_id)
            logger.debug(f">>> === UPDATED BACKLOG ITEM: {model_to_dict(updated_backlog_item)} {backlog_item.id} === <<<")
            if back_to == 'view_project_tree_board' and project_id:
                return redirect(back_to, project_id=project_id)
            if back_to == 'view_iteration_kanban' and project_id:
                return redirect(back_to, org_id=org_id, project_id=project_id)
            
            return redirect('view_project_tree_backlog', pro_id=pro_id)
        else:
            print(f">>> Form errors: {form.errors}")  # Debugging

    else:
        form = PBIBacklogForm(instance=backlog_item, org_id=project.org.id)
    # send outputs (info, template,
    context = {
        'parent_page': '__PARENTPAGE__',
        'page': 'edit_project_tree_backlog_item',
        'user': user,
        'member': member,
        'pro': project,
        'project': project,
        'pro_id': pro_id,
        'org': project.org,
        'org_id': project.org_id,
        'backlog_types': backlog_types,
        'form': form,
        'backlog_item': backlog_item,
        'backlog_item_type': backlog_item_type,
        'backlog_item_parent': backlog_item_parent,
        'backlog_item_children': backlog_item_children,
    }       
    template_file = f"{app_name}/{module_path}/edit_project_tree_backlog_item.html"
    return render(request, template_file, context)

##########################################################################################################
# 
#
#
#
##########################################################################################################
import csv
@login_required
def export_backlog_csv(request):
    # Create HTTP response with CSV content type
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="backlog.csv"'

    # Create a CSV writer
    writer = csv.writer(response)

    # Write CSV Header
    writer.writerow(['ID', 'Title', 'Description', 'Status', 'Created Date', 'Assigned To'])

    # Fetch backlog data (Modify based on your actual model fields)
    backlogs = Backlog.objects.filter()

    for backlog in backlogs:
        writer.writerow([
            backlog.id,
            backlog.title,
            backlog.description,
            backlog.status,
            backlog.created_at.strftime('%Y-%m-%d'),  # Formatting date
            backlog.assigned_to.username if backlog.assigned_to else "Unassigned"
        ])

    return response

@login_required
def view_project_tree_backlog(request, pro_id):
        
    # vars
    backlog_deleted = False
    backlog_deleted_count = 0
    backlog_items = []
    backlog_types = []
    backlog_items_count = 0
    
    
    user = request.user
    member = get_object_or_404(Member, user=user)
    project = Project.objects.get(id=pro_id)
    
    
    # IMPORTANT items
    # 1. Backlog Super Type
    # 2. Backlog Type
    # 3. Backlog
     
    # 1. Backlog Super Type
    pbst_name = f"{project.id}_PROJECT_TREE"
    project_backlog_super_type, created = BacklogSuperType.objects.get_or_create(pro=project, name=pbst_name)
    logger.debug(f">>> === BACKLOG SUPER TYPE: {project_backlog_super_type} {project_backlog_super_type.id} === <<<")
    
    # 2. Backlog Type
    check_model_rec_count("*** TreeBacklog: Step1a***", BacklogType, pbst_name)
    pbst_name = f"{project.id}_PROJECT_TREE"
    project_backlog_type, created = BacklogType.objects.get_or_create(pro=project, name=pbst_name)
    check_model_rec_count("*** TreeBacklog: Step1b***", BacklogType, pbst_name)
    
    # 2.1 Create the Backlog Type from the Config as a Schema
    # 2.1.1 Get the Config
    config = PROJECT_WBS_TREE_CONFIG
    
    # 2.1.2 Create the Backlog Type from the Config as a Schema
    check_model_rec_count("*** TreeBacklog: Step2a***", BacklogType, pbst_name)
    created_node = create_or_update_tree_from_config(config, model_name="app_organization.BacklogType", parent=project_backlog_type, project=project)
    project_backlog_type = BacklogType.objects.get(pro=project, name=pbst_name)
    check_model_rec_count("*** TreeBacklog: Step2b***", BacklogType, pbst_name)
    logger.debug(f">>> === **** TEST AGAIN **** BACKLOG TYPE: {project_backlog_type} {project_backlog_type.id} === <<<")
    # 2.1.3 Get the Backlog Types
    # Display the structure of the created node
    tree_structure = list_tree_structure(created_node)
    # Optional: Log or return the structure for further use
    logger.info("\n".join(tree_structure))
    
    # 2.1.4 Get the Backlog Types as a ref dictionary {name: id}   
    bt_tree_name_and_id = get_tree_name_id(created_node)
    logger.debug(f"Backlog Type Tree Name ID: {bt_tree_name_and_id}")
    
    # 2.2 Get the Epic level id and its children
    epic_type_id = bt_tree_name_and_id.get("Epic")
    epic_type_node = BacklogType.objects.get(id=epic_type_id, active=True)
    epic_type_parent = epic_type_node.parent
    epic_type_children = epic_type_node.get_active_children()
    backlog_types = epic_type_children
    backlog_types_count = backlog_types.count()
    logger.debug(f">>> === EPIC TYPE: {epic_type_node} {epic_type_id} {backlog_types} === <<<")
    
    
    # 3. Backlog
    # 3.1 Create the Backlog Project Tree Root Node
    pb_name = f"{project.id}_PROJECT_TREE"
    project_backlog, created = Backlog.objects.get_or_create(pro=project, name=pb_name, type=project_backlog_type)
    logger.debug(f">>> === BACKLOG: {project_backlog} {project_backlog.id} === <<<")
    
    # 3.2 Test creation
    # create a backlog item, here you can create a backlog item with the type you want and Project Parent as root node
    # later we can move that to the desired location
    # backlog_item_name = "Test Epic - CHECK"
    # backlog_item_type_id = bt_tree_name_id.get("Epic")
    # created_bi = Backlog.objects.create(pro=project, name=backlog_item_name, parent=project_backlog, type_id=backlog_item_type_id)
    # logger.debug(f">>> === BACKLOG ITEM: {created_bi} {created_bi.id} {created_bi.type}=== <<<")
    # list_created = Backlog.objects.filter(pro=project, parent=project_backlog, type_id=backlog_item_type_id)
    # logger.debug(f">>> === BACKLOG ITEM: {created_bi} {created_bi.id} === <<<")
    # logger.debug(f">>> === BACKLOG ITEM LIST: {list_created} === <<<")
    
    # 3.3 Get the Backlog Items
    
    strategic_theme_id = bt_tree_name_and_id.get("Strategic Theme")
    initiative_id = bt_tree_name_and_id.get("Initiative")
    exclude_types = [strategic_theme_id, initiative_id]
    bug_type_id = bt_tree_name_and_id.get("Bug")
    story_type_id = bt_tree_name_and_id.get("User Story")
    tech_task_type_id = bt_tree_name_and_id.get("Technical Task")
    feature_type_id = bt_tree_name_and_id.get("Feature")
    component_type_id = bt_tree_name_and_id.get("Component")
    capability_type_id = bt_tree_name_and_id.get("Capability")
    include_types = [bug_type_id, story_type_id, tech_task_type_id]
    include_collection_types = [feature_type_id, component_type_id, capability_type_id, epic_type_id]

    #backlog_epic_items = Backlog.objects.filter(pro=project, parent=project_backlog).exclude(type__in=exclude_types)
    backlog_epic_items = Backlog.objects.filter(pro=project, type__in=include_types, active=True)
    #backlog_epic_items = Backlog.objects.filter(pro=project, parent=project_backlog)
    backlog_epic_items_count = backlog_epic_items.count()
    #logger.debug(f">>> === BACKLOG ITEMS: {backlog_epic_items_count} {backlog_epic_items} === <<<")


    # 3.4 Get the epics of this backlog
    epics_in_backlog = Backlog.objects.filter(pro=project, type__in=include_collection_types, active=True)
    #epics_in_backlog = {epic.id: epic for epic in backlog_epic_items if epic.type.id == epic_type_id}
    #logger.debug(f">>> === EPICS IN THIS BACKLOG: {epics_in_backlog} === <<<")
    
    
    # 3.5 Filter options
    filters = {}
    ## Adding the filter option
    # Extract filter_by parameter
    filter_by = request.GET.get('filter_by', '').strip()  # Default to empty string if not provided

    # Handle "unmapped" case
    if filter_by == 'unmapped':
        filters['parent'] = project_backlog
        logger.debug(f">>> === Filters unmapped: {filters} unmapped === <<<")
    elif filter_by == 'deleted':
        filters['active'] = False
        logger.debug(f">>> === Filters deleted: {filters} deleted === <<<") 
    elif filter_by == 'all_items':
        filters = {}
        logger.debug(f">>> === Filters allitems: {filters} all_items === <<<")
    elif filter_by.startswith('filter_'):
        # Extract the collection ID from the filter_by parameter
        collection_id = filter_by.replace('filter_', '')
        
        if "|" in collection_id:  # Ensure it's a valid numeric ID
            release_id, iteration_id = collection_id.split("|")
            filters['release_id'] = int(release_id)
            filters['iteration_id'] = int(iteration_id)
            logger.debug(f">>> === Release, Iteration Filters Collection: {filters} match === <<<")
        
        elif collection_id.isdigit():  # Ensure it's a valid numeric ID
            filters['parent_id'] = int(collection_id)
            logger.debug(f">>> === Filters Collection: {filters} match === <<<")
    
    backlog_summary = request.POST.get('backlog_summary')
    add_action = request.POST.get('add_action')
    action = request.POST.get('read_action', '').strip().lower()
    collection_id = request.POST.get("collection_id")
    selected_items = request.POST.get("selected_items", "").split(",")
    type_of_bi = request.POST.get("type")
    ajax_data = request.POST.get("seq_list_data")
    
    version_action = request.POST.get('read_version_action', '').strip().lower()
    version_id = request.POST.get("version_id")
    input_release_id = None
    input_iteration_id = None
    logger.debug(f">>> === VERSION ID: {version_id} === <<<")
    if version_id and "|" in version_id:
        input_release_id, input_iteration_id = version_id.split("|")
    selected_version_items = request.POST.get("selected_version_items", "").split(",")
    logger.debug(f">>> === VERSION ACTION: {version_action} === <<<")   
    
    # ################################ DEMO PROJECT ######################################### #
    # # Get the project details
    # if project name contains string "_SDEMO" in the end then it is a demo project
    project_backlog_count = Backlog.objects.filter(pro=project, parent=project_backlog, active=True).count()
    if project.name.endswith("_SDEMO") and project_backlog_count == 0:
        story_type_id = bt_tree_name_and_id.get("User Story")
        tech_task_type_id = bt_tree_name_and_id.get("Technical Task")
        # create 30 stories and 30 tech tasks of various size 1,2,3,5,8,13 by random
        TEST_CHOICES = [1, 2, 3, 5, 8, 13]
        for i in range(30):
            story_size = random.choice(TEST_CHOICES)
            tech_task_size = random.choice(TEST_CHOICES)
            story_name = f"Story {i+1} - {story_size}"
            tech_task_name = f"Tech Task {i+1} - {tech_task_size}"
            story = Backlog.objects.create(pro=project, name=story_name, parent=project_backlog, type_id=story_type_id, size=story_size, position=i)
            story.save()
            tech_task = Backlog.objects.create(pro=project, name=tech_task_name, parent=project_backlog, type_id=tech_task_type_id, size=tech_task_size, position=i)
            tech_task.save()
            logger.debug(f">>> === DEMO PROJECT: {story} {story.id} {tech_task} {tech_task.id} === <<<")
    # ######################################################################################## #



    from app_organization.mod_org_board.models_org_board import ProjectBoardCard
    
    # WORKING PREVIOUS VERSION
    # #logger.debug(f">>> === AJAX DATA: {ajax_data} === <<<")
    if 'deleted' in filter_by:
        display_backlog_items = Backlog.objects.filter(pro=project, type__in=backlog_types, **filters).prefetch_related(
            Prefetch(
                'board_cards',
                queryset=ProjectBoardCard.objects.filter(active=True).select_related('state', 'board', 'swimlane'),
                to_attr='prefetched_card'  # Use singular as it will contain only one card
            )
        ).order_by('position').order_by('position')
    else:
        display_backlog_items = Backlog.objects.filter(pro=project, active=True, type__in=backlog_types, **filters).prefetch_related(
                Prefetch(
                    'board_cards',
                    queryset=ProjectBoardCard.objects.filter(active=True).select_related('state', 'board', 'swimlane'),
                    to_attr='prefetched_card'  # Use singular as it will contain only one card
                )
            ).order_by('position').order_by('position')
    logger.debug(f">>> === DISPLAY DATA : {display_backlog_items} === <<<")
    
    for item in display_backlog_items:
        for card in item.prefetched_card:
            logger.debug(f"Backlog: {item.name}, State: {card.state.name if card.state else 'No State'}")
    # test_display = None
    
    
    if action == 'assign':
        #logger.debug(f">>> === Assigning Items: {selected_items} to Collection: {collection_id} === <<<")
        for each_item in selected_items:
            backlog_item = Backlog.objects.get(id=each_item)
            if collection_id == 'Others':
                backlog_item.parent = project_backlog
            elif collection_id == "deleted":
                backlog_item.active = False
            else:
                backlog_item.parent = Backlog.objects.get(id=collection_id)
            backlog_item.save() 
      
        #logger.debug(f">>> === Items {selected_items} assigned to collection {collection_id} successfully! === <<<")
        return redirect("view_project_tree_backlog", pro_id=pro_id)
       
    elif action == "unassign":
        #logger.debug(f">>> === UnAssigning Items: {selected_items} from Collection: {collection_id} === <<<")
        for each_item in selected_items:
            backlog_item = Backlog.objects.get(id=each_item)
            backlog_item.parent = project_backlog
            if collection_id == "deleted":
                backlog_item.active = True
            backlog_item.save()
        #display_backlog_items = Backlog.objects.filter(pro=project, active=True, type__in=include_types)
        #logger.debug(f">>> === Items {selected_items} unassigned from collection {collection_id} successfully! === <<<")
        
        return redirect("view_project_tree_backlog", pro_id=pro_id)
    else:        
        logger.debug(f">>> === Invalid action: {action} === <<<")
    
    
    
    if version_action == 'assign':
        logger.debug(f">>> === Assigning Items: {selected_version_items} to Version: {version_id} === <<<")
        for each_item in selected_version_items:
            if each_item != '':
                backlog_item = Backlog.objects.get(id=each_item)
            
                if version_id == "Others":
                    backlog_item.release_id = None
                    backlog_item.iteration_id = None
                elif version_id == "deleted":
                    backlog_item.active = False
                else:
                    backlog_item.release = OrgRelease.objects.get(id=input_release_id)
                    backlog_item.iteration = OrgIteration.objects.get(id=input_iteration_id)
                backlog_item.save() 
      
        #logger.debug(f">>> === Items {selected_items} assigned to collection {collection_id} successfully! === <<<")
        return redirect("view_project_tree_backlog", pro_id=pro_id)
       
    elif version_action == "unassign":
        logger.debug(f">>> === UnAssigning Items: {selected_version_items} from Version: {collection_id} === <<<")
        for each_item in selected_version_items:
            backlog_item = Backlog.objects.get(id=each_item)
            backlog_item.release_id = None
            backlog_item.iteration_id = None
            if version_id == "deleted":
                backlog_item.active = False
            backlog_item.save()
        #display_backlog_items = Backlog.objects.filter(pro=project, active=True, type__in=include_types)
        #logger.debug(f">>> === Items {selected_items} unassigned from collection {collection_id} successfully! === <<<")
        
        return redirect("view_project_tree_backlog", pro_id=pro_id)
    
    
    if add_action == 'add':
        #logger.debug(f">>> === ADD ACTION: {add_action} === <<<")
        if 'add_to_top' in request.POST:
            #logger.debug(f">>> === ADD TO TOP:  === <<<")
            
            # Create the new backlog item with a temporary position
            create_backlog_item = Backlog.objects.create(
                pro=project,
                name=backlog_summary,
                parent=project_backlog,
                position=0,  # Temporary; will be updated
                created_by=user,
                type_id=type_of_bi
            )
            
            # Update positions of existing items
            Backlog.objects.filter(pro=project, parent=project_backlog, active=True).exclude(id=create_backlog_item.id).update(
                position=models.F('position') + 1
            )

            # Set the new item's position to 1
            create_backlog_item.position = 1
            create_backlog_item.save()

            # Regenerate display_backlog_items
            backlog_epic_items = Backlog.objects.filter(pro=project, active=True, type__in=backlog_types)
            seq_add_to_top(ajax_data)
            #logger.debug(f">>> === ADD TO TOP: {create_backlog_item} {create_backlog_item.id} === <<<")
            display_backlog_items = Backlog.objects.filter(pro=project, active=True, type__in=backlog_types).order_by('position')
            
        if 'add_to_bottom' in request.POST:
            #logger.debug(f">>> === ADD TO BOTTOM:  === <<<")

            # Find the current maximum position in the existing items
            max_position = Backlog.objects.filter(pro=project, parent=project_backlog, active=True).aggregate(
                max_position=models.Max('position')
            )['max_position'] or 0  # Default to 0 if no items exist

            # Create the new backlog item with the next available position
            create_backlog_item = Backlog.objects.create(
                pro=project,
                name=backlog_summary,
                parent=project_backlog,
                position=max_position + 1,  # Next position
                created_by=user,
                type_id=type_of_bi
            )
            display_backlog_items = Backlog.objects.filter(pro=project, active=True, type__in=backlog_types).order_by('position')
            # Regenerate display_backlog_items
            #logger.debug(f">>> === ADD TO BOTTOM: {create_backlog_item} {create_backlog_item.id} === <<<")
            return redirect("view_project_tree_backlog", pro_id=pro_id)
    
    # test
    #logger.debug(f">>> === EPICS IN THIS BACKLOG: {epics_in_backlog} === <<<")
    
    
    backlog_items_count = len(display_backlog_items)
    #logger.debug(f">>> === BACKLOG ITEMS COUNT: {display_backlog_items} === <<<")
    
    
    # Organization Releases from OrgReleases
    org_releases = OrgRelease.objects.filter(org=project.org, active=True)
    
     # Fetch current and next iterations based on dates
    today = date.today()
    current_iteration = None
    next_iteration = None
   
    
    ##########################################################################
    # Changing the current iteration by date selection
    ##########################################################################
    if project.project_release:
        details = get_project_release_and_iteration_details(project.id)
        current_release = details.get("current_release")
        current_iteration = details.get("current_iteration")
        next_iteration = details.get("next_iteration")
        logger.debug(f">>> === CURRENT RELEASE: {current_release} === <<<")
        logger.debug(f">>> === CURRENT ITERATION: {current_iteration} === <<<")
        logger.debug(f">>> === NEXT ITERATION: {next_iteration} === <<<")
        
    ########## ADDING PROJECT TEMPLATE DETAILS ##########
    project_detail = project.project_details if hasattr(project, 'project_details') else None
    logger.debug(f">>> === PROJECT DETAIL: {project_detail}, PROJECT_DETAILS: {project_detail.template} === <<<")
    
    
    

    
    # send outputs (info, template,
    context = {
        'parent_page': '__PARENTPAGE__',
        'page': 'view_project_tree_backlog',
        'user': user,
        'member': member,
        'pro': project,
        'project': project,
        'pro_id': pro_id,
        'project_detail': project_detail,
        'org': project.org,
        'org_id': project.org_id,
        
        'backlog_epic_items': backlog_epic_items,
        
        'backlog_deleted': backlog_deleted,
        'backlog_deleted_count': backlog_deleted_count,
        'backlog_items': backlog_items,
        'backlog_types': backlog_types,
        'backlog_items_count': backlog_items_count,
        'backlog_types_count': backlog_types_count,
        'display_backlog_items': display_backlog_items,
        
        'epics_in_backlog': epics_in_backlog,
        'epic_type_parent': epic_type_parent,

        'org_releases': org_releases,
        
        'project_backlog_super_type_url': f"/org/backlog_super_type/list_backlog_super_types/{pro_id}/",
        'project_backlog_type_url': f"/org/backlog_type/list_backlog_types/{pro_id}/{project_backlog_type.id}/",
        'project_backlog_url': f"/org/backlog/list_backlogs/{pro_id}/{project_backlog.id}/",
        
        'current_iteration': current_iteration,
        'next_iteration': next_iteration,
        
        'page_title': f'View Project Tree Backlog',
        "STATUS_CHOICES": STATUS_CHOICES,
        "SIZE_CHOICES": SIZE_CHOICES,
        "FLAT_BACKLOG_NAME_ICONS": FLAT_BACKLOG_NAME_ICONS,
        'COMMON_BACKLOG_TYPES': COMMON_BACKLOG_TYPES,
        'ICON_MAPPING': ICON_MAPPING,
    }       
    template_file = f"{app_name}/{module_path}/view_project_tree_backlog.html"
    return render(request, template_file, context)

def list_tree_structure(node, level=0):
    """
    Recursively lists the tree structure starting from the given node.
    
    Args:
        node (Model): The root node from which to start listing.
        level (int): The current depth level (used for indentation).

    Returns:
        list: A nested representation of the tree structure.
    """
    tree_structure = []
    indent = " " * (level * 4)  # Indentation for display
    tree_structure.append(f"{indent}- {node.name} (ID: {node.id})")
    
    # Recursively list child nodes
    for child in node.get_active_children():
        tree_structure.extend(list_tree_structure(child, level=level + 1))
    
    return tree_structure


def get_tree_name_id(node, level=0):
    """
    Recursively lists the tree structure starting from the given node.
    
    Args:
        node (Model): The root node from which to start listing.
        level (int): The current depth level (used for indentation).

    Returns:
        list: A nested representation of the tree structure.
    """
    tree_structure = {}
    node_details = {node.name: node.id}
    tree_structure.update(node_details)
    
    # Recursively list child nodes
    for child in node.get_active_children():
        tree_structure.update(get_tree_name_id(child, level=level + 1))
    
    return tree_structure


def create_or_update_tree_from_config(config, model_name, parent=None, project=None):
    """
    Creates or updates tree nodes in the database based on a configuration dictionary.

    Args:
        config (dict): The tree structure as a dictionary.
        model_name (str): The name of the model, including the app name (e.g., "myapp.BacklogSuperType").
        parent (Model): The parent node (None for the root).
        project (Model): The project this tree belongs to.

    Returns:
        Model: The root node or updated tree node.
    """
    from django.apps import apps
    
    # Resolve the model from the model_name string
    model = apps.get_model(model_name)

    # Find or create the current node
    node, created = model.objects.get_or_create(
        pro=project,
        name=config["name"],
        parent=parent,
        defaults={"name": config["name"]}  # Add any default values for fields here
    )

    if created:
        logger.debug(f"Created new node: {node.name}")
    else:
        logger.debug(f"Node already exists: {node.name}")

    # Compare and update children
    existing_children = list(node.get_active_children())
    config_children = config.get("children", [])

    # Match existing children to configuration
    matched_children = set()
    for child_config in config_children:
        # Check for a matching child
        matching_child = next(
            (child for child in existing_children if child.name == child_config["name"]),
            None
        )
        if matching_child:
            # Recursively update the child
            create_or_update_tree_from_config(
                child_config, model_name, parent=node, project=project
            )
            matched_children.add(matching_child)
        else:
            # Create a new child node
            create_or_update_tree_from_config(
                child_config, model_name, parent=node, project=project
            )

    # Remove unmatched existing children
    unmatched_children = [child for child in existing_children if child not in matched_children]
    for unmatched_child in unmatched_children:
        logger.warning(f"Unmatched child node found in DB: {unmatched_child.name}. Consider deleting.")

    return node


def create_tree_from_config(config, model_name, parent=None, project=None):
    """
    Recursively creates tree nodes in the database from a configuration dictionary.

    Args:
        config (dict): The tree structure as a dictionary.
        model_name (str): The name of the model, including the app name (e.g., "myapp.BacklogSuperType").
        parent (Model): The parent node (None for the root).
        project (Model): The project this tree belongs to.

    Returns:
        Model: The created node.
    """
    # Resolve the model from the model_name string
    model = apps.get_model(model_name)
    
    # Create the current node
    node = model.objects.create(
        pro=project,
        name=config["name"],
        parent=parent  # Assuming the model has a `parent` field for hierarchical relations
    )
    
    # Recursively create child nodes if present
    children = config.get("children", [])
    for child_config in children:
        create_tree_from_config(child_config, model_name=model_name, parent=node, project=project)
    
    return node


# create an ajax function to edit, move, delete, add backlog item




def map_nearest_iteration(request):
    from datetime import date

    # Get current date
    today = date.today()

    # Fetch current and next iterations based on dates
    current_iteration = OrgIteration.objects.filter(iteration_start_date__lte=today, iteration_end_date__gte=today, active=True).first()
    next_iteration = OrgIteration.objects.filter(iteration_start_date__gt=today, active=True).order_by('iteration_start_date').first()

    # Fetch backlog items
    backlog_items = Backlog.objects.filter(status='pending')

    context = {
        'current_iteration': current_iteration,
        'next_iteration': next_iteration,
        'backlog_items': backlog_items,
    }
    return render(request, 'backlog_iteration_view.html', context)
