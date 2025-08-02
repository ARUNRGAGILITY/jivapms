from app_organization.mod_project.models_project import *

from app_organization.mod_app.all_view_imports import *
from app_organization.mod_backlog.models_backlog import *
from app_organization.mod_backlog.forms_backlog import *
from app_organization.mod_org_release.models_org_release import *
from app_organization.mod_persona.models_persona import *
from app_organization.mod_activity.models_activity import *
from app_organization.mod_step.models_step import *

from app_jivapms.mod_app.all_view_imports import *

app_name = 'app_organization'
app_version = 'v1'

module_name = 'backlog'
module_path = f'mod_backlog'


@login_required
def create_story_map(request, org_id):    
    projects = Organization.objects.get(pk=org_id).org_projects.filter(active=True)
    organization = Organization.objects.get(pk=org_id)
    project = None 
    personae_count = 0
    personae_count = Persona.objects.filter(organization_id=org_id, project=project).count()
    if request.method == 'POST':
        selected_project_id = request.POST.get('project')
        selected_story_map_option = request.POST.get('story_mapping_name', '').strip()     
        project = Project.objects.get(pk=selected_project_id, active=True)
        
        story_maps = StoryMapping.objects.filter(pro_id=project.id, active=True)
        story_maps_count = story_maps.count()
        print(f"create_story_map OPT1 ====> {selected_project_id} ===> {selected_story_map_option}")
        
        if selected_story_map_option == '2':
            return redirect('create_story_map_from_backlog', pro_id=selected_project_id)
            
                
        else:           
            # create a persona and send the persona id 
            new_persona = Persona.objects.create(name='', organization_id=org_id, project=project) 
            default_activity = Activity.objects.create(name='Default Activity', persona_id=new_persona.id)
            request.session['default_activity_id'] = default_activity.id
            #print(f">>> === DEFAULT ACTIVITY {default_activity.id} === <<<")
            return redirect('create_backlog_from_story_map', pro_id=selected_project_id, persona_id=new_persona.id)
    # if personae_count  > 0:
    #     # Create the personae list for project 
    #     return redirect('list_personae', organization_id=org_id)
       
        
    # send outputs info, template,
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'list_backlogs',
        'org_id': org_id,
       
        'organization': organization,
        'org': organization,
        'projects': projects,
        'page_title': f'Backlog List',
    }       
    template_file = f"{app_name}/{module_path}/story_map/create_story_map.html"
    return render(request, template_file, context)



@login_required
def create_project_story_map(request, org_id, project_id):    
    projects = Organization.objects.get(pk=org_id).org_projects.filter(active=True)
    organization = Organization.objects.get(pk=org_id)
    project = None 
    project = Project.objects.get(pk=project_id, active=True)
    personae_count = 0
    personae_count = Persona.objects.filter(organization_id=org_id, project=project, active=True).count()
    logger.debug(f"BEFORE POST METHOD ====> {personae_count} ===> {project_id}")
    if request.method == 'POST':
        selected_project_id = request.POST.get('project')
        selected_story_map_option = request.POST.get('story_mapping_name')      
        project = Project.objects.get(pk=selected_project_id, active=True)
        
        story_maps = StoryMapping.objects.filter(pro_id=project.id, active=True)
        story_maps_count = story_maps.count()
        print(f"TESTING ====> {selected_project_id} ===> {selected_story_map_option}")
        
        if selected_story_map_option == '2':
            return redirect('create_story_map_from_backlog', pro_id=selected_project_id)
            
                
        else:           
            # Make sure the persona is saved and has an ID
            new_persona = Persona.objects.create(name='', organization_id=org_id, project=project)
            print(f"Created persona with ID: {new_persona.id}")  # Debug line

            # Make sure new_persona.id is not None before redirecting
            if new_persona.id:
                return redirect('create_backlog_from_story_map', pro_id=selected_project_id, persona_id=new_persona.id)
            else:
                # Handle the error case
                print("Error: Persona was not created successfully")
    # if personae_count  > 0:
    #     # Create the personae list for project 
    #     return redirect('list_project_personae', organization_id=org_id, project_id=project_id)
    else:
        return redirect('create_story_map_from_backlog', pro_id=project.id)
       
        
    # send outputs info, template,
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'list_backlogs',
        'org_id': org_id,
        'project_id': project_id,
        'project': project,
        'pro_id': project_id,
        'organization': organization,
        'org': organization,
        'projects': projects,
        'page_title': f'Backlog List',
    }       
    template_file = f"{app_name}/{module_path}/story_map/create_story_map.html"
    return render(request, template_file, context)




from app_organization.mod_backlog.views_project_tree import get_tree_name_id

@login_required
def create_backlog_from_story_map(request, pro_id, persona_id):
    pro = get_object_or_404(Project, pk=pro_id)
    persona = get_object_or_404(Persona, pk=persona_id)
    default_activity_id = request.session.pop('default_activity', None)
    organization = pro.org
    project_id_str = f"{pro_id}_PROJECT_TREE"
    flat_backlog_root = Backlog.objects.filter(pro=pro, name=project_id_str).first()
    
    create_backlog_type = BacklogType.objects.filter(name='User Story').first()
    filters = {}
    releases = OrgRelease.objects.filter(org_id=pro.org_id, active=True)
    activities = Activity.objects.filter(persona_id=persona_id, active=True)
    
    project_id_str = f"{pro_id}_PROJECT_TREE"
    root_project_type = BacklogType.objects.filter(name=project_id_str, active=True).first()
    project_backlog_root = Backlog.objects.filter(pro=pro, name=project_id_str).first()
    bt_tree_name_and_id = get_tree_name_id(root_project_type)
    bug_type_id = bt_tree_name_and_id.get("Bug")
    story_type_id = bt_tree_name_and_id.get("User Story")
    tech_task_type_id = bt_tree_name_and_id.get("Technical Task")
    feature_type_id = bt_tree_name_and_id.get("Feature")
    component_type_id = bt_tree_name_and_id.get("Component")
    capability_type_id = bt_tree_name_and_id.get("Capability")
    include_types = [bug_type_id, story_type_id, tech_task_type_id, feature_type_id, component_type_id, capability_type_id]  
    logger.debug(f"====> {include_types} ===> {persona_id}")  
    initial_backlog = Backlog.objects.filter(pro=pro,   type__in=include_types, active=True)
    logger.debug(f"====> {initial_backlog} ===> {persona_id}")
    backlog = Backlog.objects.filter(pro_id=pro_id, persona_id=persona_id, active=True)
    story_maps = StoryMapping.objects.filter(pro_id=pro_id, persona_id=persona_id)
    #StoryMapping.objects.filter(pro_id=pro_id, persona_id=persona_id).delete()
    if default_activity_id is None:
        default_activity = Activity.objects.get(name='Default Activity', persona_id=persona_id)
        request.session['default_activity_id'] = default_activity.id
        default_activity_id = default_activity.id
    #StoryMapping.objects.all().delete()
    if request.method == 'POST':
        selected_project_id = request.POST.get('project_id')
        selected_persona_id = request.POST.get('persona_id')
        
        if 'submit_activity' in request.POST:
            activity_input = request.POST.get('activity')
            if activity_input:
                activity = Activity.objects.create(
                    name=activity_input,
                    persona_id=selected_persona_id,
                    active=True
                )
                print(f">>> === ACTIVITY {activity} === <<<")
            return redirect('create_backlog_from_story_map', pro_id=selected_project_id, persona_id=selected_persona_id)
        
        elif 'submit_step' in request.POST:
            step_input = request.POST.get('step_input')
            def_activity_id_input = request.POST.get('default_activity_id')
            if step_input:
                step_save = Step.objects.create(
                    name=step_input,
                    persona_id=selected_persona_id,
                    activity_id=def_activity_id_input,
                    active=True
                )
                step_save.save()
                print(f">>> === STEP {step_save} for {default_activity_id} === <<<")
            return redirect('create_backlog_from_story_map', pro_id=selected_project_id, persona_id=selected_persona_id)
        
        elif 'submit_detail' in request.POST:
            detail_input = request.POST.get('detail')
            if detail_input:
                detail = Backlog.objects.create(
                    name=detail_input,
                    persona_id=selected_persona_id,
                    pro_id=selected_project_id,
                    active=True,
                    parent=project_backlog_root,
                    type_id=story_type_id,
                    collection=None,
                )
                print(f">>> === DETAIL {detail} {selected_project_id} {selected_persona_id}=== <<<")
                return redirect('create_backlog_from_story_map', pro_id=selected_project_id, persona_id=selected_persona_id)
    
    # Context for GET request
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'create_backlog_from_story_map',
        'pro_id': pro_id,
        'pro': pro,
        'project': pro,
        'project_id_str': project_id_str,
        'persona_id': persona_id,
        'persona': persona,
        'activities': activities,
        'default_activity_id': default_activity_id,
        'story_maps': story_maps,
        'initial_backlog': initial_backlog,
        'backlog': backlog,
        'releases': releases,
        'org': organization,
        'organization': organization,
        'org_id': organization.id if organization else None,
        'page_title': 'Backlog from Story Map',
    }
    
    template_file = f"{app_name}/{module_path}/story_map/create_backlog_from_story_map.html"
    return render(request, template_file, context)

@login_required
def create_story_map_from_backlog(request, pro_id):    
    pro = get_object_or_404(Project, pk=pro_id)
    organization = pro.org
    
    # Get or create a default persona for this project
    try:
        # Try to get an existing persona for this project
        persona = Persona.objects.filter(
            organization_id=organization.id,
            project=pro,
            active=True
        ).first()
        
        # If no persona exists, create one
        if not persona:
            persona = Persona.objects.create(
                name='Default Persona',
                organization_id=organization.id,
                project=pro,
                active=True
            )
            created = True
        else:
            created = False
            
    except Exception as e:
        # Fallback: create a new persona with a unique name
        import uuid
        persona = Persona.objects.create(
            name=f'Default Persona {uuid.uuid4().hex[:8]}',
            organization_id=organization.id,
            project=pro,
            active=True
        )
        created = True
    
    # Get project-specific configurations
    project_id_str = f"{pro_id}_PROJECT_TREE"
    root_project_type = BacklogType.objects.filter(name=project_id_str, active=True).first()
    project_backlog_root = Backlog.objects.filter(pro=pro, name=project_id_str).first()
    
    # Get backlog type IDs
    bt_tree_name_and_id = get_tree_name_id(root_project_type)
    bug_type_id = bt_tree_name_and_id.get("Bug")
    story_type_id = bt_tree_name_and_id.get("User Story")
    tech_task_type_id = bt_tree_name_and_id.get("Technical Task")
    feature_type_id = bt_tree_name_and_id.get("Feature")
    component_type_id = bt_tree_name_and_id.get("Component")
    capability_type_id = bt_tree_name_and_id.get("Capability")
    include_types = [bug_type_id, story_type_id, tech_task_type_id, feature_type_id, component_type_id, capability_type_id]
    
    # Get activities for the persona
    activities = Activity.objects.filter(persona_id=persona.id, active=True)
    
    # Get or create default activity if no activities exist
    if not activities.exists():
        default_activity = Activity.objects.create(
            name='Default Activity', 
            persona_id=persona.id,
            active=True
        )
        activities = Activity.objects.filter(persona_id=persona.id, active=True)
        request.session['default_activity_id'] = default_activity.id
    else:
        default_activity = activities.first()
        request.session['default_activity_id'] = default_activity.id
    
    # Get releases for the organization
    releases = OrgRelease.objects.filter(org_id=pro.org_id, active=True)
    
    # Get existing story mappings - DEFINE THIS FIRST
    story_maps = StoryMapping.objects.filter(pro_id=pro_id, persona_id=persona.id, active=True)
    
    # Get existing backlog items for this project
    existing_backlog = Backlog.objects.filter(
        pro=pro, 
        type__in=include_types, 
        active=True
    ).exclude(name=project_id_str)
    
    # Separate mapped and unmapped backlog items
    mapped_story_ids = list(story_maps.values_list('story_id', flat=True)) if story_maps.exists() else []
    unmapped_backlog = existing_backlog.exclude(id__in=mapped_story_ids) if mapped_story_ids else existing_backlog
    
    # Count mapped items for display purposes
    mapped_items_count = len(mapped_story_ids) if mapped_story_ids else 0
    
    # Handle POST requests
    if request.method == 'POST':
        print(f">>> POST request received: {request.POST}")
        print(f">>> Headers: {dict(request.headers)}")
        
        if 'submit_activity' in request.POST:
            activity_input = request.POST.get('activity')
            if activity_input:
                activity = Activity.objects.create(
                    name=activity_input,
                    persona_id=persona.id,
                    active=True
                )
                print(f">>> === ACTIVITY {activity} === <<<")
            return redirect('create_story_map_from_backlog', pro_id=pro_id)
        
        elif 'submit_step' in request.POST:
            step_input = request.POST.get('step_input')
            def_activity_id_input = request.POST.get('default_activity_id')
            if step_input:
                step_save = Step.objects.create(
                    name=step_input,
                    persona_id=persona.id,
                    activity_id=def_activity_id_input,
                    active=True
                )
                step_save.save()
                print(f">>> === STEP {step_save} for {def_activity_id_input} === <<<")
            return redirect('create_story_map_from_backlog', pro_id=pro_id)
        
        elif 'submit_detail' in request.POST:
            detail_input = request.POST.get('detail')
            print(f">>> Detail input: '{detail_input}'")
            print(f">>> Is AJAX: {request.headers.get('X-Requested-With')}")
            
            if detail_input and detail_input.strip():
                try:
                    # Create new backlog item
                    new_backlog = Backlog.objects.create(
                        name=detail_input.strip(),
                        persona_id=persona.id,
                        pro_id=pro_id,
                        active=True,
                        parent=project_backlog_root,
                        type_id=story_type_id,
                        collection=None,
                    )
                    print(f">>> === NEW BACKLOG ITEM {new_backlog} ID: {new_backlog.id} === <<<")
                    
                    # Check if this is an AJAX request
                    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                        print(">>> Returning JSON response")
                        from django.http import JsonResponse
                        return JsonResponse({
                            'status': 'success',
                            'backlog_id': new_backlog.id,
                            'backlog_name': new_backlog.name,
                            'message': 'Backlog item created successfully'
                        })
                    else:
                        print(">>> Returning redirect response")
                        return redirect('create_story_map_from_backlog', pro_id=pro_id)
                        
                except Exception as e:
                    print(f">>> Error creating backlog item: {e}")
                    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                        from django.http import JsonResponse
                        return JsonResponse({
                            'status': 'error',
                            'message': f'Error creating backlog item: {str(e)}'
                        })
                    else:
                        return redirect('create_story_map_from_backlog', pro_id=pro_id)
            else:
                # Handle empty input
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    from django.http import JsonResponse
                    return JsonResponse({
                        'status': 'error',
                        'message': 'Backlog item name cannot be empty'
                    })
                else:
                    return redirect('create_story_map_from_backlog', pro_id=pro_id)
    
    # Context for template
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'create_story_map_from_backlog',
        'pro_id': pro_id,
        'pro': pro,
        'project': pro,
        'project_id_str': project_id_str,
        'persona': persona,
        'persona_id': persona.id,
        'activities': activities,
        'default_activity_id': request.session.get('default_activity_id'),
        'story_maps': story_maps,
        'existing_backlog': existing_backlog,
        'unmapped_backlog': unmapped_backlog,
        'mapped_items_count': mapped_items_count,
        'releases': releases,
        'org': organization,
        'organization': organization,
        'org_id': organization.id,
        'page_title': f'Story Map from Backlog - {pro.name}',
    }       
    
    template_file = f"{app_name}/{module_path}/story_map/create_story_map_from_backlog.html"
    return render(request, template_file, context)


@login_required
def storymap_group_steps(request, pro_id, persona_id):
    pro = get_object_or_404(Project, pk=pro_id)
    persona = get_object_or_404(Persona, pk=persona_id)
    organization = pro.org

    # Fetch all active activities and unmapped steps
    activities = Activity.objects.filter(active=True, persona=persona)
    # Fetch updated unmapped steps including 'Default Activity'
    unmapped_steps = Step.objects.filter(
        Q(activity__isnull=True) | Q(activity__name='Default Activity'),
        persona_id=persona_id,
        active=True
    )


       
    # send outputs info, template,
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'storymap_group_steps',
        'pro_id': pro_id,
        'pro': pro,
        'project': pro,
        'org': pro.org,
        'persona_id': persona_id,
        'persona': persona,
        'activities': activities,
        'unmapped_steps': unmapped_steps,
        'organization': pro.org,
        'org_id': pro.org_id,
        'page_title': f'Group Steps to Activities',
    }       
    template_file = f"{app_name}/{module_path}/story_map/storymap_group_steps.html"
    return render(request, template_file, context)




###################################################################################################
@login_required
def ajax_map_steps_to_activity(request):
    if request.method == 'POST':
        step_ids = request.POST.getlist('step_ids[]')
        activity_id = request.POST.get('activity_id')
        persona_id = request.POST.get('persona_id')

        try:
            activity = Activity.objects.get(id=activity_id)
            Step.objects.filter(id__in=step_ids).update(activity=activity)
            # Fetch updated unmapped steps
            unmapped_steps = Step.objects.filter(activity__isnull=True, persona_id=persona_id, active=True)

            return JsonResponse({'status': 'success', 'message': 'Step updated successfully.'})
        except Step.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Step not found.'})
        except Activity.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Activity not found.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})


@login_required
def ajax_unmap_steps_from_activity(request):
    if request.method == 'POST':
        step_ids = request.POST.getlist('step_ids[]')

        try:
            Step.objects.filter(id__in=step_ids).update(activity=None)
            return JsonResponse({'status': 'success', 'message': 'Steps unassigned from activity.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request.'})


# ajax
@login_required
def ajax_storymap_right_pane_content(request):
    if request.method == 'POST':
        user = request.user
        pro_id = request.POST.get('pro_id')
        pro = Project.objects.get(pk=pro_id)
        persona_id = request.POST.get('persona_id')
        persona = Persona.objects.get(pk=persona_id)
        default_activity_id = request.session.get('default_activity_id')
        organization = pro.org
        
        activities = Activity.objects.filter(active=True, persona=persona)  # Fetch activities
        releases = OrgRelease.objects.filter(active=True, org=organization)  # Fetch releases
        # send outputs info, template,
        context = {
            'parent_page': '___PARENTPAGE___',
            'page': 'create_story_map_from_backlog',
            'pro_id': pro_id,
            'pro': pro,
            'project': pro,
            'org': pro.org,
            'organization': pro.org,
            'default_activity_id': default_activity_id,
            'activities': activities,
            'releases': releases,
            'org_id': pro.org_id,
            'page_title': f'Story Map from Backlog',
        }       
        template_file = f"{app_name}/{module_path}/story_map/ajax_storymap_right_pane_content.html"
        
        html_content = render_to_string(template_file, context)
        #print(f">>> === {html_content} === <<<")
        return JsonResponse({'html': html_content})

    return JsonResponse({'error': 'true', 'message': 'Invalid Request: Use POST method.'})    



@login_required
def ajax_storymap_refresh_steps_row(request):
    if request.method == 'POST':
        user = request.user
        pro_id = request.POST.get('pro_id')
        pro = Project.objects.get(pk=pro_id)
        persona_id = request.POST.get('persona_id')
        persona = Persona.objects.get(pk=persona_id)
        organization = pro.org
        # Fetch the required data
        activities = Activity.objects.filter(active=True, persona_id=persona_id).prefetch_related('activity_steps')
        # context
        context = {
            'activities': activities,
            'persona': persona,
            'pro': pro,
            'organization': organization,
            'org_id': organization.id,
            'pro_id': pro_id,
            'persona_id': persona_id,
        }
        # Render the partial HTML
        template_file = f"{app_name}/{module_path}/story_map/partial_steps_row.html"
        steps_html = render_to_string(template_file, context)
    
        return JsonResponse({"status": "success", "html": steps_html})
    return JsonResponse({"status": "error", "message": "Invalid request method."}, status=400)

@login_required
def ajax_storymap_refresh_details_row(request):
    if request.method == 'POST':
        user = request.user
        pro_id = request.POST.get('pro_id')
        pro = Project.objects.get(pk=pro_id)
        persona_id = request.POST.get('persona_id')
        persona = Persona.objects.get(pk=persona_id)
        organization = pro.org
        # Fetch the required data
        activities = Activity.objects.filter(active=True, persona_id=persona_id).prefetch_related('activity_steps')
        backlog = Backlog.objects.filter(active=True, pro_id=pro_id, persona_id=persona_id) 
        # context
        context = {
            'activities': activities,
            'backlog': backlog,
            'persona': persona,
            'pro': pro,
            'organization': organization,
            'org_id': organization.id,
            'pro_id': pro_id,
            'persona_id': persona_id,
        }
        # Render the partial HTML
        template_file = f"{app_name}/{module_path}/story_map/partial_details_row.html"
        steps_html = render_to_string(template_file, context)
    
        return JsonResponse({"status": "success", "html": steps_html})
    return JsonResponse({"status": "error", "message": "Invalid request method."}, status=400)

@login_required
def ajax_refresh_release_rows(request):
    if request.method == "POST":
        try:
            # Get specific release ID if provided
            release_id = request.POST.get('release_id', None)
            pro_id = request.POST.get('pro_id')
            persona_id = request.POST.get('persona_id')

            releases = OrgRelease.objects.filter(active=True, org_id=request.user.org_id)
            activities = Activity.objects.prefetch_related('activity_steps').filter(active=True)
            story_maps = StoryMapping.objects.filter(active=True, pro_id=pro_id, persona_id=persona_id)

            if release_id:
                releases = releases.filter(id=release_id)

            # Render the partial HTML
            context = {
                'releases': releases,
                'activities': activities,
                'story_maps': story_maps
            }
            template_file = f"{app_name}/{module_path}/story_map/partial_release_rows.html"
            release_rows_html = render_to_string(
                template_file,context
            )
            return JsonResponse({"status": "success", "html": release_rows_html})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    return JsonResponse({"status": "error", "message": "Invalid request method."}, status=405)


@login_required
def ajax_refresh_release_rows(request):
    if request.method == "POST":
        try:
            release_ids = request.POST.getlist('release_ids', [])  # Get list of specific release IDs
            pro_id = request.POST.get('pro_id')
            persona_id = request.POST.get('persona_id')
            project = Project.objects.get(pk=pro_id)
            organization = project.org
            releases = OrgRelease.objects.filter(active=True, org_id=project.org.id)
            if release_ids:
                releases = releases.filter(id__in=release_ids)

            activities = Activity.objects.prefetch_related('activity_steps').filter(active=True)
            story_maps = StoryMapping.objects.filter(active=True, pro_id=pro_id, persona_id=persona_id)

            # Render the partial HTML
            context = {
                'releases': releases,
                'activities': activities,
                'story_maps': story_maps
            }
            template_file = f"{app_name}/{module_path}/story_map/partial_release_rows.html"
            release_rows_html = {
                str(release.id): render_to_string(
                    template_file,
                    context,
                    request=request,
                )
                for release in releases
            }
            return JsonResponse({"status": "success", "html": release_rows_html})
        except Exception as e:
            print(f">>> === {e} === <<<")
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    return JsonResponse({"status": "error", "message": "Invalid request method."}, status=405)



@login_required
def ajax_update_backlog_release(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            backlog_id = data.get('backlog_id')
            release_id = data.get('release_id')

            if not backlog_id:
                return JsonResponse({"status": "error", "message": "Backlog ID is required."}, status=400)

            # Update the backlog item
            backlog_item = Backlog.objects.get(id=backlog_id)
            backlog_item.release_id = None
            backlog_item.save()
            
            # update the mapping
            story_map = StoryMapping.objects.filter(story_id=backlog_id).update(active=False)
           
            return JsonResponse({"status": "success", "message": "Backlog item updated successfully."})
        except Backlog.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Backlog item not found."}, status=404)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)
    return JsonResponse({"status": "error", "message": "Invalid request method."}, status=405)


@login_required
def ajax_storymap_group_steps(request):
    if request.method == 'POST':
        project_id = request.POST.get('project_id')
        persona_id = request.POST.get('persona_id')
        activity_name = request.POST.get('activity_name')
        step_ids = request.POST.getlist('step_ids[]')

        if not activity_name or not step_ids:
            return JsonResponse({'status': 'error', 'message': 'Activity name or steps missing.'})

        try:
            # Create the new activity
            activity = Activity.objects.create(name=activity_name, persona_id=persona_id)

            # Associate steps with the new activity
            Step.objects.filter(id__in=step_ids).update(activity=activity)

            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})



## Activity and Steps drag and drop 

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

@login_required
def ajax_update_step_position(request):
    """Update the position of steps within an activity or unmapped steps"""
    if request.method == 'POST':
        try:
            position_data = json.loads(request.POST.get('position_data', '[]'))
            activity_id = request.POST.get('activity_id')  # Can be None for unmapped steps
            persona_id = request.POST.get('persona_id')
            
            if not persona_id:
                return JsonResponse({'status': 'error', 'message': 'Persona ID is required'})
            
            # Update each step's position
            for item in position_data:
                step_id = item.get('id')
                position = item.get('position')
                
                try:
                    step = Step.objects.get(id=step_id, persona_id=persona_id)
                    step.position = position
                    
                    # If activity_id is provided, ensure the step is assigned to that activity
                    if activity_id:
                        activity = Activity.objects.get(id=activity_id, persona_id=persona_id)
                        step.activity = activity
                    else:
                        # If no activity_id, this is an unmapped step
                        step.activity = None
                    
                    step.save()
                except (Step.DoesNotExist, Activity.DoesNotExist):
                    continue
            
            return JsonResponse({'status': 'success', 'message': 'Step position updated successfully'})
            
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})




@login_required
def ajax_move_step_to_activity(request):
    """Move a step from one activity to another (including unmapped)"""
    if request.method == 'POST':
        try:
            step_id = request.POST.get('step_id')
            target_activity_id = request.POST.get('target_activity_id')  # Can be None for unmapped
            persona_id = request.POST.get('persona_id')
            new_position = request.POST.get('new_position', 1)
            
            if not step_id or not persona_id:
                return JsonResponse({'status': 'error', 'message': 'Step ID and persona ID are required'})
            
            step = Step.objects.get(id=step_id, persona_id=persona_id)
            
            # Update the step's activity assignment
            if target_activity_id:
                target_activity = Activity.objects.get(id=target_activity_id, persona_id=persona_id)
                step.activity = target_activity
            else:
                step.activity = None  # Unmapped
            
            step.position = new_position
            step.save()
            
            return JsonResponse({'status': 'success', 'message': 'Step moved successfully'})
            
        except (Step.DoesNotExist, Activity.DoesNotExist):
            return JsonResponse({'status': 'error', 'message': 'Step or activity not found'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


# You don't need any database migrations since you already have 
# the position field in your BaseModelImpl!



# Add these new view functions to your views_story_map.py file

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

@login_required
def ajax_update_step_position(request):
    """Update the position of steps within an activity or unmapped steps"""
    if request.method == 'POST':
        try:
            position_data = json.loads(request.POST.get('position_data', '[]'))
            activity_id = request.POST.get('activity_id')  # Can be None for unmapped steps
            persona_id = request.POST.get('persona_id')
            
            if not persona_id:
                return JsonResponse({'status': 'error', 'message': 'Persona ID is required'})
            
            # Update each step's position
            for item in position_data:
                step_id = item.get('id')
                position = item.get('position')
                
                try:
                    step = Step.objects.get(id=step_id, persona_id=persona_id)
                    step.position = position
                    
                    # If activity_id is provided, ensure the step is assigned to that activity
                    if activity_id:
                        activity = Activity.objects.get(id=activity_id, persona_id=persona_id)
                        step.activity = activity
                    else:
                        # If no activity_id, this is an unmapped step
                        step.activity = None
                    
                    step.save()
                except (Step.DoesNotExist, Activity.DoesNotExist):
                    continue
            
            return JsonResponse({'status': 'success', 'message': 'Step position updated successfully'})
            
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


@login_required
def ajax_update_activity_name(request):
    """Update the name of an activity"""
    if request.method == 'POST':
        try:
            activity_id = request.POST.get('activity_id')
            activity_name = request.POST.get('activity_name', '').strip()
            
            if not activity_id or not activity_name:
                return JsonResponse({'status': 'error', 'message': 'Activity ID and name are required'})
            
            activity = Activity.objects.get(id=activity_id)
            activity.name = activity_name
            activity.save()
            
            return JsonResponse({'status': 'success', 'message': 'Activity name updated successfully'})
            
        except Activity.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Activity not found'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


@login_required
def ajax_move_step_to_activity(request):
    """Move a step from one activity to another (including unmapped)"""
    if request.method == 'POST':
        try:
            step_id = request.POST.get('step_id')
            target_activity_id = request.POST.get('target_activity_id')  # Can be None for unmapped
            persona_id = request.POST.get('persona_id')
            new_position = request.POST.get('new_position', 1)
            
            if not step_id or not persona_id:
                return JsonResponse({'status': 'error', 'message': 'Step ID and persona ID are required'})
            
            step = Step.objects.get(id=step_id, persona_id=persona_id)
            
            # Update the step's activity assignment
            if target_activity_id:
                target_activity = Activity.objects.get(id=target_activity_id, persona_id=persona_id)
                step.activity = target_activity
            else:
                step.activity = None  # Unmapped
            
            step.position = new_position
            step.save()
            
            return JsonResponse({'status': 'success', 'message': 'Step moved successfully'})
            
        except (Step.DoesNotExist, Activity.DoesNotExist):
            return JsonResponse({'status': 'error', 'message': 'Step or activity not found'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


# You don't need any database migrations since you already have 
# the position field in your BaseModelImpl!


@login_required
def ajax_add_activity(request):
    """Add a new activity for a persona"""
    if request.method == 'POST':
        try:
            activity_name = request.POST.get('activity_name', '').strip()
            persona_id = request.POST.get('persona_id')
            
            if not activity_name:
                return JsonResponse({'status': 'error', 'message': 'Activity name is required'})
            
            if not persona_id:
                return JsonResponse({'status': 'error', 'message': 'Persona ID is required'})
            
            # Get the persona
            persona = Persona.objects.get(id=persona_id)
            
            # Get the highest position for activities in this persona
            max_position = Activity.objects.filter(
                persona_id=persona_id, 
                active=True
            ).aggregate(models.Max('position'))['position__max'] or 0
            
            # Create the new activity
            activity = Activity.objects.create(
                name=activity_name,
                persona=persona,
                position=max_position + 1,
                active=True,
                author=request.user
            )
            
            return JsonResponse({
                'status': 'success', 
                'message': 'Activity added successfully',
                'activity_id': activity.id,
                'activity_name': activity.name
            })
            
        except Persona.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Persona not found'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})



# Add these new view functions to your views_story_map.py file
########################
#
#
#
#
#
#
########################
# Add these new view functions to your views_story_map.py file

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

@login_required
def ajax_update_activity_position(request):
    """Update the position of activities for a persona"""
    if request.method == 'POST':
        try:
            position_data = json.loads(request.POST.get('position_data', '[]'))
            persona_id = request.POST.get('persona_id')
            
            if not persona_id:
                return JsonResponse({'status': 'error', 'message': 'Persona ID is required'})
            
            # Update each activity's position
            for item in position_data:
                activity_id = item.get('id')
                position = item.get('position')
                
                try:
                    activity = Activity.objects.get(id=activity_id, persona_id=persona_id)
                    activity.position = position
                    activity.save()
                except Activity.DoesNotExist:
                    continue
            
            return JsonResponse({'status': 'success', 'message': 'Activity position updated successfully'})
            
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


@login_required
def ajax_update_step_position(request):
    """Update the position of steps within an activity or unmapped steps"""
    if request.method == 'POST':
        try:
            position_data = json.loads(request.POST.get('position_data', '[]'))
            activity_id = request.POST.get('activity_id')  # Can be None for unmapped steps
            persona_id = request.POST.get('persona_id')
            
            if not persona_id:
                return JsonResponse({'status': 'error', 'message': 'Persona ID is required'})
            
            # Update each step's position
            for item in position_data:
                step_id = item.get('id')
                position = item.get('position')
                
                try:
                    step = Step.objects.get(id=step_id, persona_id=persona_id)
                    step.position = position
                    
                    # If activity_id is provided, ensure the step is assigned to that activity
                    if activity_id:
                        activity = Activity.objects.get(id=activity_id, persona_id=persona_id)
                        step.activity = activity
                    else:
                        # If no activity_id, this is an unmapped step
                        step.activity = None
                    
                    step.save()
                except (Step.DoesNotExist, Activity.DoesNotExist):
                    continue
            
            return JsonResponse({'status': 'success', 'message': 'Step position updated successfully'})
            
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


@login_required
def ajax_update_activity_name(request):
    """Update the name of an activity"""
    if request.method == 'POST':
        try:
            activity_id = request.POST.get('activity_id')
            activity_name = request.POST.get('activity_name', '').strip()
            
            if not activity_id or not activity_name:
                return JsonResponse({'status': 'error', 'message': 'Activity ID and name are required'})
            
            activity = Activity.objects.get(id=activity_id)
            activity.name = activity_name
            activity.save()
            
            return JsonResponse({'status': 'success', 'message': 'Activity name updated successfully'})
            
        except Activity.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Activity not found'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


@login_required
def ajax_move_step_to_activity(request):
    """Move a step from one activity to another (including unmapped)"""
    if request.method == 'POST':
        try:
            step_id = request.POST.get('step_id')
            target_activity_id = request.POST.get('target_activity_id')  # Can be None for unmapped
            persona_id = request.POST.get('persona_id')
            new_position = request.POST.get('new_position', 1)
            
            if not step_id or not persona_id:
                return JsonResponse({'status': 'error', 'message': 'Step ID and persona ID are required'})
            
            step = Step.objects.get(id=step_id, persona_id=persona_id)
            
            # Update the step's activity assignment
            if target_activity_id:
                target_activity = Activity.objects.get(id=target_activity_id, persona_id=persona_id)
                step.activity = target_activity
            else:
                step.activity = None  # Unmapped
            
            step.position = new_position
            step.save()
            
            return JsonResponse({'status': 'success', 'message': 'Step moved successfully'})
            
        except (Step.DoesNotExist, Activity.DoesNotExist):
            return JsonResponse({'status': 'error', 'message': 'Step or activity not found'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


# You don't need any database migrations since you already have 
# the position field in your BaseModelImpl!


@login_required
def ajax_add_activity(request):
    """Add a new activity for a persona"""
    if request.method == 'POST':
        try:
            activity_name = request.POST.get('activity_name', '').strip()
            persona_id = request.POST.get('persona_id')
            
            if not activity_name:
                return JsonResponse({'status': 'error', 'message': 'Activity name is required'})
            
            if not persona_id:
                return JsonResponse({'status': 'error', 'message': 'Persona ID is required'})
            
            # Get the persona
            persona = Persona.objects.get(id=persona_id)
            
            # Get the highest position for activities in this persona
            max_position = Activity.objects.filter(
                persona_id=persona_id, 
                active=True
            ).aggregate(models.Max('position'))['position__max'] or 0
            
            # Create the new activity
            activity = Activity.objects.create(
                name=activity_name,
                persona=persona,
                position=max_position + 1,
                active=True,
                author=request.user
            )
            
            return JsonResponse({
                'status': 'success', 
                'message': 'Activity added successfully',
                'activity_id': activity.id,
                'activity_name': activity.name
            })
            
        except Persona.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Persona not found'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


@login_required
def ajax_add_step(request):
    """Add a new step for a persona (unmapped by default)"""
    if request.method == 'POST':
        try:
            step_name = request.POST.get('step_name', '').strip()
            persona_id = request.POST.get('persona_id')
            
            if not step_name:
                return JsonResponse({'status': 'error', 'message': 'Step name is required'})
            
            if not persona_id:
                return JsonResponse({'status': 'error', 'message': 'Persona ID is required'})
            
            # Get the persona
            persona = Persona.objects.get(id=persona_id)
            
            # Get the highest position for unmapped steps in this persona
            max_position = Step.objects.filter(
                persona_id=persona_id,
                activity__isnull=True,
                active=True
            ).aggregate(models.Max('position'))['position__max'] or 0
            
            # Create the new step (unmapped by default)
            step = Step.objects.create(
                name=step_name,
                persona=persona,
                activity=None,  # Unmapped
                position=max_position + 1,
                active=True,
                author=request.user
            )
            
            return JsonResponse({
                'status': 'success', 
                'message': 'Step added successfully',
                'step_id': step.id,
                'step_name': step.name
            })
            
        except Persona.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Persona not found'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

@login_required
def ajax_delete_step(request):
    """Delete a step"""
    if request.method == 'POST':
        try:
            step_id = request.POST.get('step_id')
            
            if not step_id:
                return JsonResponse({'status': 'error', 'message': 'Step ID is required'})
            
            step = Step.objects.get(id=step_id)
            
            # No permission check needed - just delete
            step.active = False
            step.save()
            
            return JsonResponse({'status': 'success', 'message': 'Step deleted successfully'})
            
        except Step.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Step not found'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


@login_required
def ajax_delete_activity(request):
    """Delete an activity and unmap all its steps"""
    if request.method == 'POST':
        try:
            activity_id = request.POST.get('activity_id')
            
            if not activity_id:
                return JsonResponse({'status': 'error', 'message': 'Activity ID is required'})
            
            activity = Activity.objects.get(id=activity_id)
            
            # Unmap all steps from this activity
            Step.objects.filter(activity=activity).update(activity=None)
            
            # Soft delete the activity
            activity.active = False
            activity.save()
            
            return JsonResponse({'status': 'success', 'message': 'Activity deleted successfully'})
            
        except Activity.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Activity not found'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


# # Only allow users to delete their own created items
# if step.author != request.user:
#     return JsonResponse({'status': 'error', 'message': 'Permission denied'})



import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Count

@login_required
def ajax_get_deleted_activities(request):
    """Get list of deleted activities for a persona"""
    if request.method == 'POST':
        try:
            persona_id = request.POST.get('persona_id')
            
            if not persona_id:
                return JsonResponse({'status': 'error', 'message': 'Persona ID is required'})
            
            # Get deleted activities with count of steps that became unmapped when this activity was deleted
            deleted_activities = Activity.objects.filter(
                persona_id=persona_id,
                active=False
            ).annotate(
                # Count unmapped steps that might have belonged to this activity
                step_count=Count('activity_steps', filter=models.Q(activity_steps__active=True, activity_steps__activity__isnull=True))
            ).values(
                'id', 
                'name', 
                'step_count',
                'updated_at'
            ).order_by('-updated_at')
            
            return JsonResponse({
                'status': 'success', 
                'activities': list(deleted_activities)
            })
            
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


@login_required
def ajax_get_deleted_steps(request):
    """Get list of deleted steps for a persona"""
    if request.method == 'POST':
        try:
            persona_id = request.POST.get('persona_id')
            
            if not persona_id:
                return JsonResponse({'status': 'error', 'message': 'Persona ID is required'})
            
            # Get deleted steps with activity name
            deleted_steps = Step.objects.filter(
                persona_id=persona_id,
                active=False
            ).select_related('activity').values(
                'id',
                'name',
                'activity__name',
                'updated_at'
            ).order_by('-updated_at')
            
            # Format the data
            steps_data = []
            for step in deleted_steps:
                steps_data.append({
                    'id': step['id'],
                    'name': step['name'],
                    'activity_name': step['activity__name'],
                    'updated_at': step['updated_at']
                })
            
            return JsonResponse({
                'status': 'success', 
                'steps': steps_data
            })
            
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


@login_required
def ajax_restore_activities(request):
    """Restore deleted activities (steps were unmapped, not deleted)"""
    if request.method == 'POST':
        try:
            activity_ids = json.loads(request.POST.get('activity_ids', '[]'))
            
            if not activity_ids:
                return JsonResponse({'status': 'error', 'message': 'No activity IDs provided'})
            
            # Restore the activities only
            # Steps were unmapped (activity set to None) when activity was deleted, not actually deleted
            restored_count = Activity.objects.filter(
                id__in=activity_ids,
                active=False
            ).update(active=True)
            
            # Note: Steps are still unmapped and need to be manually reassigned if needed
            # This is by design since the user might want to reorganize them
            
            return JsonResponse({
                'status': 'success', 
                'message': f'{restored_count} activities restored successfully. Steps remain unmapped.'
            })
            
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


@login_required
def ajax_restore_steps(request):
    """Restore deleted steps"""
    if request.method == 'POST':
        try:
            step_ids = json.loads(request.POST.get('step_ids', '[]'))
            
            if not step_ids:
                return JsonResponse({'status': 'error', 'message': 'No step IDs provided'})
            
            # Restore the steps
            restored_count = Step.objects.filter(
                id__in=step_ids,
                active=False
            ).update(active=True)
            
            return JsonResponse({
                'status': 'success', 
                'message': f'{restored_count} steps restored successfully'
            })
            
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


@login_required
def ajax_permanent_delete_activity(request):
    """Permanently delete an activity (optional - for admin use)"""
    if request.method == 'POST':
        try:
            activity_id = request.POST.get('activity_id')
            
            if not activity_id:
                return JsonResponse({'status': 'error', 'message': 'Activity ID is required'})
            
            activity = Activity.objects.get(id=activity_id, active=False)
            
            # Delete all associated steps first
            Step.objects.filter(activity=activity).delete()
            
            # Then delete the activity
            activity.delete()
            
            return JsonResponse({'status': 'success', 'message': 'Activity permanently deleted'})
            
        except Activity.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Activity not found or not deleted'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


@login_required
def ajax_permanent_delete_step(request):
    """Permanently delete a step (optional - for admin use)"""
    if request.method == 'POST':
        try:
            step_id = request.POST.get('step_id')
            
            if not step_id:
                return JsonResponse({'status': 'error', 'message': 'Step ID is required'})
            
            step = Step.objects.get(id=step_id, active=False)
            step.delete()
            
            return JsonResponse({'status': 'success', 'message': 'Step permanently deleted'})
            
        except Step.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Step not found or not deleted'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})