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
        selected_story_map_option = request.POST.get('story_mapping_name')      
        project = Project.objects.get(pk=selected_project_id, active=True)
        
        story_maps = StoryMapping.objects.filter(pro_id=project.id, active=True)
        story_maps_count = story_maps.count()
        #print(f"====> {selected_project_id} ===> {selected_story_map_option}")
        
        if selected_story_map_option == '2':
            return redirect('create_story_map_from_backlog', pro_id=selected_project_id)
            
                
        else:           
            # create a persona and send the persona id 
            new_persona = Persona.objects.create(name='', organization_id=org_id, project=project) 
            default_activity = Activity.objects.create(name='Default Activity', persona_id=new_persona.id)
            request.session['default_activity_id'] = default_activity.id
            #print(f">>> === DEFAULT ACTIVITY {default_activity.id} === <<<")
            return redirect('create_backlog_from_story_map', pro_id=selected_project_id, persona_id=new_persona.id)
    if personae_count  > 0:
        # Create the personae list for project 
        return redirect('list_personae', organization_id=org_id)
       
        
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
    personae_count = Persona.objects.filter(organization_id=org_id, project=project).count()
    logger.debug(f"====> {personae_count} ===> {project_id}")
    if request.method == 'POST':
        selected_project_id = request.POST.get('project')
        selected_story_map_option = request.POST.get('story_mapping_name')      
        project = Project.objects.get(pk=selected_project_id, active=True)
        
        story_maps = StoryMapping.objects.filter(pro_id=project.id, active=True)
        story_maps_count = story_maps.count()
        #print(f"====> {selected_project_id} ===> {selected_story_map_option}")
        
        if selected_story_map_option == '2':
            return redirect('create_story_map_from_backlog', pro_id=selected_project_id)
            
                
        else:           
            # create a persona and send the persona id 
            new_persona = Persona.objects.create(name='', organization_id=org_id, project=project) 
            default_activity = Activity.objects.create(name='Default Activity', persona_id=new_persona.id)
            request.session['default_activity_id'] = default_activity.id
            #print(f">>> === DEFAULT ACTIVITY {default_activity.id} === <<<")
            return redirect('create_backlog_from_story_map', pro_id=selected_project_id, persona_id=new_persona.id)
    if personae_count  > 0:
        # Create the personae list for project 
        return redirect('list_project_personae', organization_id=org_id, project_id=project_id)
       
        
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
    initial_backlog = Backlog.objects.filter(pro=pro, type__in=include_types, active=True)
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
    pro = Project.objects.get(pk=pro_id)
    organization = pro.org
    # send outputs info, template,
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'create_story_map_from_backlog',
        'pro_id': pro_id,
        'pro': pro,
        'project': pro,
        'org': pro.org,
        'organization': pro.org,
        'org_id': pro.org_id,
        'page_title': f'Story Map from Backlog',
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
