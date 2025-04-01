# this basic import
from app_common.mod_app.all_view_imports import *

# # models
# from app_automate.models_app.models_automate import *
# from app_automate.models_app.models_backlogs import *
# from app_automate.models_app.models_orgs import *
# from app_automate.models_app.models_foundations import *
# # forms
# from app_automate.forms_app.forms_backlogs import *
# from app_automate.forms_app.forms_orgs import *

app_name = 'app_automate'
app_version = 'v1'  
@login_required
def ajax_update_model_list_sorted(request):
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
        print(f">>> === AJAX UPDATE SORTED === <<<")
        for item in sorted_list:
            str = item.replace('"','')
            position = str.split('_')
            print(f">>> === AJAX UPDATE SORTED {position} === <<<")
            model_class.objects.filter(pk=position[0]).update(position=seq, author=request.user)
            seq = seq + 1
        context = {'page': 'Sorted Value', 
                   'active_tab': 'sorted_value',
                   'ajax_data': ajax_data}
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


# @login_required
# def ajax_save_element_text(request):
#     if request.method == 'POST':
#         text_data = request.POST.get('text')
#         object_id = request.POST.get('id')
#         model_name = request.POST.get('model_name')
#         field_name = request.POST.get('field_name')
#         got_app_name = request.POST.get('app_name', app_name)  # Default to a specific app if not provided

#         try:
#             model_class = apps.get_model(got_app_name, model_name)
#             # Update the specified object
#             fields_update = {field_name: text_data}
#             obj = model_class.objects.filter(id=object_id).update(**fields_update, author=request.user)
#             return JsonResponse({'status': 'success', 'updated_records': obj})
#         except LookupError:
#             return JsonResponse({'status': 'error', 'message': 'Model not found.'})
#         except model_class.DoesNotExist:
#             return JsonResponse({'status': 'error', 'message': 'Object not found.'})
#         except Exception as e:
#             return JsonResponse({'status': 'error', 'message': str(e)})

#     return JsonResponse({'status': 'error', 'message': 'Invalid request'})


@login_required
def ajax_save_element_text(request):
    if request.method == 'POST':
        text_data = request.POST.get('text')
        object_id = request.POST.get('id')
        model_name = request.POST.get('model_name')
        field_name = request.POST.get('field_name')
        got_app_name = request.POST.get('app_name', 'default_app_name')  # Default app if not provided

        try:
            # Get the model class
            model_class = apps.get_model(got_app_name, model_name)

            # Fetch the object to be updated
            obj = model_class.objects.get(id=object_id)

            # Handle DateTimeField specifically
            field_type = model_class._meta.get_field(field_name).get_internal_type()
            if field_type == 'DateTimeField':
                # Convert the input string to a timezone-aware datetime
                naive_date = datetime.strptime(text_data, '%Y-%m-%d')  # Adjust format if necessary
                aware_date = make_aware(naive_date, timezone=pytz.UTC)  # Use UTC or your preferred timezone
                setattr(obj, field_name, aware_date)
            else:
                # For other fields, simply set the value
                setattr(obj, field_name, text_data)

            # Set the author field if applicable
            obj.author = request.user

            # Save the updated object
            obj.save()
            print(f">>> === AJAX SAVE ELEMENT TEXT {obj} === <<<")
            return JsonResponse({'status': 'success', 'message': 'Field updated successfully'})
        except LookupError:
            return JsonResponse({'status': 'error', 'message': 'Model not found.'})
        except model_class.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Object not found.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})



@login_required
def ajax_save_related_model(request):
    if request.method == 'POST':
        text_data = request.POST.get('text')  # New text data to be saved
        parent_object_id = request.POST.get('parent_id')  # ID of the parent object (e.g., Organization)
        parent_model_name = request.POST.get('parent_model')  # Model name of the parent object (e.g., Organization)
        parent_model_key = request.POST.get('parent_model_key')  # Field name to link the parent object (e.g., 'organization')
        child_model_name = request.POST.get('child_model')  # Model name of the child object (e.g., OrganizationDetail)
        field_name = request.POST.get('field_name')  # Field name to update
        app_name = request.POST.get('app_name')  # App name

        try:
            # Step 1: Get the parent model class dynamically
            parent_model_class = apps.get_model(app_name, parent_model_name)
            print(f"Parent model class found: {parent_model_class}")

            # Step 2: Fetch the parent object (e.g., Organization)
            parent_obj = parent_model_class.objects.get(id=parent_object_id)
            print(f"Parent object found: {parent_obj}")

            # Step 3: Get the child model class dynamically
            child_model_class = apps.get_model(app_name, child_model_name)
            print(f"Child model class found: {child_model_class}")

            # Step 4: Check if the child object exists for the given parent
            # Assuming there is a ForeignKey or OneToOneField from OrganizationDetail to Organization
            kwargs = {parent_model_key: parent_obj}
            child_obj, created = child_model_class.objects.get_or_create(**kwargs)  # Assuming 'organization' is the ForeignKey

            if created:
                print(f"New {child_model_name} object created for Parent ID {parent_object_id}")
            else:
                print(f"{child_model_name} object exists for Parent ID {parent_object_id}")

            # Step 5: Update the specific field in the child object
            if hasattr(child_obj, field_name):
                setattr(child_obj, field_name, text_data)
                child_obj.save()
                print(f"{field_name} updated for {child_model_name} object.")
                return JsonResponse({'status': 'success', 'created': created, 'created_id': child_obj.id, 'updated_records': 1})
            else:
                return JsonResponse({'status': 'error', 'message': f"Field '{field_name}' not found in model '{child_model_name}'."})

        except parent_model_class.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': f'{parent_model_name} not found.'})
        except child_model_class.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': f'{child_model_name} not found.'})
        except LookupError:
            return JsonResponse({'status': 'error', 'message': 'Model not found.'})
        except IntegrityError as e:
            print(f"IntegrityError: {str(e)}")
            return JsonResponse({'status': 'error', 'message': str(e)})
        except Exception as e:
            print(f"Error: {str(e)}")
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

#
#
# Purpose is to create new record with foreign keys 
# e.g., backlog, with name '' and pro_id, persona_id as kwargs from the request POST
@login_required
def ajax_create_record(request):
    if request.method == 'POST':
        try:
            # Extract data from POST request
            app_name = request.POST.get('app_name')  # App name
            model_name = request.POST.get('model_name')  # Model name (e.g., 'Backlog')
            field_name = request.POST.get('field_name', 'name')  # Field to set (default to 'name')
            additional_fields = request.POST.dict()  # All other fields passed as kwargs
            
            # Remove reserved keys that aren't part of the kwargs for object creation
            reserved_keys = ['csrfmiddlewaretoken', 'app_name', 'model_name', 'field_name']
            kwargs = {key: value for key, value in additional_fields.items() if key not in reserved_keys}
            
            # Ensure required keys are present
            if not app_name or not model_name:
                return JsonResponse({'status': 'error', 'message': 'Missing app_name or model_name.'}, status=400)

            # Dynamically get the model class
            model_class = apps.get_model(app_name, model_name)
            if not model_class:
                return JsonResponse({'status': 'error', 'message': 'Model not found.'}, status=400)

            # Add default field (e.g., 'name') to kwargs if not provided
            if field_name not in kwargs:
                kwargs[field_name] = ''

            # Create the object in a transaction to ensure data integrity
            with transaction.atomic():
                new_obj = model_class.objects.create(**kwargs)

            return JsonResponse({
                'status': 'success',
                'created_id': new_obj.id,
                'message': f'New {model_name} created successfully.',
                'id': new_obj.id
            })

        except LookupError:
            return JsonResponse({'status': 'error', 'message': 'Invalid model specified.'}, status=400)
        except IntegrityError as e:
            return JsonResponse({'status': 'error', 'message': f'Database error: {str(e)}'}, status=500)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Unexpected error: {str(e)}'}, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)

@login_required
def ajax_create_child_element(request):
    if request.method == 'POST':
        text_data = request.POST.get('text')  # New text data to be saved
        parent_object_id = request.POST.get('parent_id')  # ID of the parent object (e.g., Organization)
        parent_model_name = request.POST.get('parent_model')  # Model name of the parent object (e.g., Organization)
        parent_model_key = request.POST.get('parent_model_key')  # Field name to link the parent object (e.g., 'organization')
        child_model_name = request.POST.get('child_model')  # Model name of the child object (e.g., OrganizationDetail)
        field_name = request.POST.get('field_name')  # Field name to update
        app_name = request.POST.get('app_name')  # App name

        try:
            # Step 1: Get the parent model class dynamically
            parent_model_class = apps.get_model(app_name, parent_model_name)
            print(f"Parent model class found: {parent_model_class}")

            # Step 2: Fetch the parent object (e.g., Organization)
            parent_obj = parent_model_class.objects.get(id=parent_object_id)
            print(f"Parent object found: {parent_obj}")

            # Step 3: Get the child model class dynamically
            child_model_class = apps.get_model(app_name, child_model_name)
            print(f"Child model class found: {child_model_class}")

            # Step 4: Directly create a new child object
            # Use kwargs to dynamically assign the ForeignKey based on input
            kwargs = {parent_model_key: parent_obj, 'name': text_data}

            # Directly create a new child object using kwargs
            child_obj = child_model_class.objects.create(**kwargs)
            print(f">>> === Child object created: {child_obj} === <<<")
            return JsonResponse({
                'status': 'success',
                'created_id': child_obj.id,
                'message': f"New {child_model_name} created with ID {child_obj.id}",
                'id': child_obj.id
            })

           

        except parent_model_class.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': f'{parent_model_name} not found.'})
        except child_model_class.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': f'{child_model_name} not found.'})
        except LookupError:
            return JsonResponse({'status': 'error', 'message': 'Model not found.'})
        except IntegrityError as e:
            print(f"IntegrityError: {str(e)}")
            return JsonResponse({'status': 'error', 'message': str(e)})
        except Exception as e:
            print(f"Error: {str(e)}")
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request'})


@login_required
def ajax_update_task_done_state(request):
    if request.method == 'POST':
        user = request.user
        id = request.POST.get('id', None)
        done = request.POST.get('done', None)
        
        model_name = request.POST['model_name']
        given_app_name = app_name
        if 'app_name' in request.POST:            
            given_app_name = request.POST['app_name']
        
        model_class = apps.get_model(given_app_name, model_name)
        if id and done:
            object = model_class.objects.filter(id=id).first()
            if object:
                object.done = done.lower() == 'true'
                object.completed_at = timezone.now()
                
                 # Calculate duration in hours
                if object.created_at and object.completed_at:
                    duration = object.completed_at - object.created_at
                    object.duration_in_hours = duration.total_seconds() / 3600  # Convert seconds to hours
                
                object.save()
                return JsonResponse({'success': True})      

    return JsonResponse({'success': False})



@login_required
def ajax_update_row_task_done_state(request):
    if request.method == 'POST':
        user = request.user
        id = request.POST.get('id', None)
        done = request.POST.get('done', None)
        row_id = request.POST.get('row_id', None)
        model_name = request.POST['model_name']
        given_app_name = app_name
        if 'app_name' in request.POST:            
            given_app_name = request.POST['app_name']
        
        model_class = apps.get_model(given_app_name, model_name)
        if id and done:
            object = model_class.objects.filter(id=id).first()
            if object:
                object.done = done.lower() == 'true'
                object.completed_at = timezone.now()
                
                 # Calculate duration in hours
                if object.created_at and object.completed_at:
                    duration = object.completed_at - object.created_at
                    object.duration_in_hours = duration.total_seconds() / 3600  # Convert seconds to hours
                
                object.save()
                return JsonResponse({'success': True, 'row_id': row_id})      

    return JsonResponse({'success': False})

@login_required
def COMMON_set_project_id(request, context):
    # Check if 'project_id' exists in GET and is not None or empty
    project_id = request.GET.get('project_id') or request.session.get('project_id')
    if project_id:
        context['project_id'] = project_id
    else:
        context['project_id'] = None
        # Update the session with the project_id if found
        request.session['project_id'] = context['project_id']
    
@login_required
def COMMON_get_project_id_from_session(request):
    return request.session.get('project_id', None)

@login_required
def ajax_update_checkbox_state(request):
    if request.method == 'POST':
        user = request.user
        object_id = request.POST.get('id', None)
        checkbox_field = request.POST.get('checkbox_field', None)  # Field name dynamically passed
        checkbox_value = request.POST.get('checkbox_value', None)  # New value for the checkbox
        model_name = request.POST.get('model_name', None)
        given_app_name = request.POST.get('app_name', app_name)  # Use default app_name if not provided

        if not (object_id and checkbox_field and checkbox_value and model_name):
            return JsonResponse({'success': False, 'error': 'Missing parameters'})

        # Get the model class dynamically
        model_class = apps.get_model(given_app_name, model_name)
        print(f">>>>>>> Model class: {model_class}  ===> {model_name}")
        # Ensure the field exists in the model
        if not hasattr(model_class, checkbox_field):
            return JsonResponse({'success': False, 'error': f'Field "{checkbox_field}" does not exist in {model_name}'})

        # Fetch and update the object
        obj = model_class.objects.filter(id=object_id).first()
        if obj:
            setattr(obj, checkbox_field, checkbox_value.lower() == 'true')  # Update checkbox field dynamically
            print(f">>>>>>> CHECK THIS Object: {obj} {checkbox_field} {checkbox_value}")
            # If the checkbox is a "done" field, update completion time
            if checkbox_field == 'done' and checkbox_value.lower() == 'true':
                obj.completed_at = timezone.now()

                # Calculate duration in hours if created_at exists
                if hasattr(obj, 'created_at') and obj.created_at:
                    duration = obj.completed_at - obj.created_at
                    obj.duration_in_hours = duration.total_seconds() / 3600  # Convert to hours

            obj.save()
            return JsonResponse({'success': True, 'object_id': object_id})

    return JsonResponse({'success': False})



@login_required
# this is a simple select/option update
def ajax_update_select_box(request):
    if request.method == 'POST':
        object_id = request.POST.get('id', None)
        field_name = request.POST.get('field_name', None)  # Field name passed dynamically
        new_value = request.POST.get('new_value', None)  # Updated value
        model_name = request.POST.get('model_name', None)
        given_app_name = request.POST.get('app_name', None)

        if not (object_id and field_name and new_value and model_name):
            return JsonResponse({'success': False, 'error': 'Missing parameters'})

        model_class = apps.get_model(given_app_name, model_name)

        # Ensure the field exists in the model before updating
        if not hasattr(model_class, field_name):
            return JsonResponse({'success': False, 'error': f'Field "{field_name}" does not exist in {model_name}'})

        # Fetch and update the object
        obj = model_class.objects.filter(id=object_id).first()
        if obj:
            setattr(obj, field_name, new_value)  # Set the field dynamically
            obj.save()
            return JsonResponse({'success': True, 'updated_field': field_name, 'new_value': new_value})

    return JsonResponse({'success': False})



@login_required
# This will update one of the row as default in the entire rows set, as default or selected
def ajax_update_default_radio_box(request):
    if request.method == 'POST':
        object_id = request.POST.get('id', None)
        field_name = request.POST.get('field_name', None)  # Field to update (e.g., 'default_board')
        model_name = request.POST.get('model_name', None)
        given_app_name = request.POST.get('app_name', None)

        if not (object_id and field_name and model_name):
            return JsonResponse({'success': False, 'error': 'Missing parameters'})

        model_class = apps.get_model(given_app_name, model_name)

        # Ensure the field exists in the model before updating
        if not hasattr(model_class, field_name):
            return JsonResponse({'success': False, 'error': f'Field "{field_name}" does not exist in {model_name}'})

        # Set all records to False before setting the selected one to True
        model_class.objects.filter(active=True).update(**{field_name: False})

        # Fetch and update the selected object
        obj = model_class.objects.filter(id=object_id, active=True).first()
        if obj:
            setattr(obj, field_name, True)  # Set selected record as default
            obj.save()
            return JsonResponse({'success': True, 'updated_field': field_name, 'new_value': True})

    return JsonResponse({'success': False, 'error': 'Invalid request'})



@login_required
# Update a specific field with value
def ajax_update_app_model_field_value(request):
    if request.method == 'POST':
        object_id = request.POST.get('id', None)
        field_name = request.POST.get('field_name', None)  # Field name passed dynamically
        new_value = request.POST.get('new_value', None)  # Updated value
        model_name = request.POST.get('model_name', None)
        given_app_name = request.POST.get('app_name', None)
        print(f">>> === Model class: {field_name}  ===> {new_value} === <<<")
        if not (object_id and field_name and new_value and model_name):
            return JsonResponse({'success': False, 'error': 'Missing parameters'})

        model_class = apps.get_model(given_app_name, model_name)

        # Ensure the field exists in the model before updating
        if not hasattr(model_class, field_name):
            return JsonResponse({'success': False, 'error': f'Field "{field_name}" does not exist in {model_name}'})

        # Fetch and update the object
        obj = model_class.objects.filter(id=object_id).first()
        if obj:
            setattr(obj, field_name, new_value)  # Set the field dynamically
            obj.save()
            
            return JsonResponse({'success': True, 'updated_field': field_name, 'new_value': new_value})

    return JsonResponse({'success': False})



