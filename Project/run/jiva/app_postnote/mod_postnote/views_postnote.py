from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import ensure_csrf_cookie

from app.app_postnote.mod_postnote.models_postnote import Project, PostNote
app_name = 'app_postnote'  # Replace with your actual app name
module_path = 'mod_postnote'  # Path to template subdirectory, if any
@ensure_csrf_cookie
def view_project_board(request, project_id):
    """
    View for displaying the project board with post notes
    """
    project = get_object_or_404(Project, id=project_id)
    postnotes = PostNote.objects.filter(project=project)
    
    
    # context = {
    #     'project': project,
    #     'postnotes': postnotes,
    # }
    
    # Get all links for this project
    links = PostNoteLink.objects.filter(
        source__project=project,
        target__project=project
    ).select_related('source', 'target')
    
    links_data = []
    for link in links:
        links_data.append({
            'id': link.id,
            'source_id': link.source.id,
            'target_id': link.target.id,
            'link_type': link.link_type
        })
    
    context = {
        'project': project,
        'postnotes': postnotes,
        'links': links_data
    }
    template_file = f"{app_name}/{module_path}/project/view_project_board.html"
    
    return render(request, template_file, context)

@require_POST
def create_postnote(request, project_id):
    """
    View for creating a new post note via AJAX
    """
    try:
        # Get the project
        project = get_object_or_404(Project, id=project_id)
        
        # Get data from request
        color = request.POST.get('color')
        pos_x = request.POST.get('pos_x')
        pos_y = request.POST.get('pos_y')

        blocked = request.POST.get('blocked', 'false').lower() == 'true'
        creation_date = request.POST.get('creation_date', timezone.now())
        
        # Create new post note
        postnote = PostNote.objects.create(
            project=project,
            title="New Item",
            description="Click to edit description",
            type_name="Task",
            color=color,
            pos_x=float(pos_x),
            pos_y=float(pos_y),
            priority="Critical",
            size="8"
        )
        
        # Return success response with post note data
        return JsonResponse({
            'status': 'success',
            'postnote_id': postnote.id,
            'title': postnote.title,
            'color': postnote.color,
            'type_name': postnote.type_name,
            'priority': postnote.priority,
            'size': postnote.size
        })
        
    except Exception as e:
        # Return error response
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@require_POST
def update_postnote_position(request, postnote_id):
    """
    View for updating the position of a post note via AJAX
    """
    try:
        # Get the post note
        postnote = get_object_or_404(PostNote, id=postnote_id)
        
        # Update position
        postnote.pos_x = float(request.POST.get('pos_x'))
        postnote.pos_y = float(request.POST.get('pos_y'))
        postnote.save(update_fields=['pos_x', 'pos_y', 'updated_at'])
        
        # Return success response
        return JsonResponse({
            'status': 'success'
        })
        
    except Exception as e:
        # Return error response
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@require_POST
def update_postnote_content(request, postnote_id):
    """
    View for updating the content (title or description) of a post note via AJAX
    """
    try:
        # Get the post note
        postnote = get_object_or_404(PostNote, id=postnote_id)
        
        # Check which field to update
        field = request.POST.get('field')
        content = request.POST.get('content')
        
        if field == 'title':
            postnote.title = content
            postnote.save(update_fields=['title', 'updated_at'])
        elif field == 'description':
            postnote.description = content
            postnote.save(update_fields=['description', 'updated_at'])
        elif field == 'type_name':
            postnote.type_name = content
            postnote.save(update_fields=['type_name', 'updated_at'])
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid field'
            }, status=400)
        
        # Return success response
        return JsonResponse({
            'status': 'success'
        })
        
    except Exception as e:
        # Return error response
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@require_POST
def delete_postnote(request, postnote_id):
    """
    View for deleting a post note via AJAX
    """
    try:
        # Get the post note
        postnote = get_object_or_404(PostNote, id=postnote_id)
        
        # Delete the post note
        postnote.delete()
        
        # Return success response
        return JsonResponse({
            'status': 'success'
        })
        
    except Exception as e:
        # Return error response
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)
    


@require_POST
def update_postnote_attributes(request, postnote_id):
    """
    View for updating multiple attributes of a post note via AJAX
    """
    try:
        # Get the post note
        postnote = get_object_or_404(PostNote, id=postnote_id)
        #print("PostNote fields:", dir(postnote)) 
        # Get data from request
        type_name = request.POST.get('type_name')
        color = request.POST.get('color')
        title = request.POST.get('title')
        description = request.POST.get('description')
        priority = request.POST.get('priority')
        size = request.POST.get('size')
        # Get the blocked value as a string and convert to boolean
        blocked_str = request.POST.get('blocked', 'false').lower()
        blocked = blocked_str == 'true'

        # Now always update the blocked status, regardless of its value
        postnote.blocked = blocked
        # Update only the provided fields
        if type_name:
            postnote.type_name = type_name
        if color:
            postnote.color = color
        if title:
            postnote.title = title
        if description:
            postnote.description = description
        if priority:
            postnote.priority = priority
        if size:
            postnote.size = size
      
        
        # Save the changes
        postnote.save()
        
        # Return success response
        return JsonResponse({
            'status': 'success',
            'postnote_id': postnote.id,
            'type_name': postnote.type_name,
            'color': postnote.color,
            'title': postnote.title,
            'description': postnote.description,
            'priority': postnote.priority,
            'size': postnote.size,
            'blocked': postnote.blocked,
        })
        
    except Exception as e:
        # Return error response
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)
    


from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from app.app_postnote.mod_postnote.models_postnote import PostNote

@require_POST
def update_acceptance_criteria(request, postnote_id):
    """
    View for updating the acceptance criteria of a post note via AJAX
    """
    try:
        # Get the post note
        postnote = get_object_or_404(PostNote, id=postnote_id)
        
        # Get data from request
        acceptance_criteria = request.POST.get('acceptance_criteria')
        
        # Update the acceptance criteria
        postnote.acceptance_criteria = acceptance_criteria
        postnote.save(update_fields=['acceptance_criteria', 'updated_at'])
        
        # Return success response
        return JsonResponse({
            'status': 'success',
            'postnote_id': postnote.id,
            'acceptance_criteria': postnote.acceptance_criteria
        })
        
    except Exception as e:
        # Return error response
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@require_POST
def get_acceptance_criteria(request, postnote_id):
    """
    View for getting the acceptance criteria of a post note via AJAX
    """
    try:
        # Get the post note
        postnote = get_object_or_404(PostNote, id=postnote_id)
        
        # Return success response with acceptance criteria
        return JsonResponse({
            'status': 'success',
            'postnote_id': postnote.id,
            'acceptance_criteria': postnote.acceptance_criteria or ""
        })
        
    except Exception as e:
        # Return error response
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)
    
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from app.app_postnote.mod_postnote.models_postnote import *


@require_POST
def create_postnote_link(request):
    """
    View for creating a link between two post notes via AJAX
    """
    try:
        # Get data from request
        source_id = request.POST.get('source_id')
        target_id = request.POST.get('target_id')
        link_type = request.POST.get('link_type')
        
        # Validate inputs
        if not source_id or not target_id or not link_type:
            return JsonResponse({
                'status': 'error',
                'message': 'Missing required fields'
            }, status=400)
        
        # Get the post notes
        source = get_object_or_404(PostNote, id=source_id)
        target = get_object_or_404(PostNote, id=target_id)
        
        # Check if link already exists
        existing_link = PostNoteLink.objects.filter(
            source=source,
            target=target,
            link_type=link_type
        ).first()
        
        if existing_link:
            return JsonResponse({
                'status': 'error',
                'message': 'Link already exists'
            }, status=400)
        
        # Create the link
        link = PostNoteLink.objects.create(
            source=source,
            target=target,
            link_type=link_type
        )
        
        # Return success response
        return JsonResponse({
            'status': 'success',
            'link_id': link.id,
            'source_id': source_id,
            'target_id': target_id,
            'link_type': link_type
        })
        
    except Exception as e:
        # Return error response
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@require_POST
def delete_postnote_link(request, link_id):
    """
    View for deleting a link between post notes via AJAX
    """
    try:
        # Get the link
        link = get_object_or_404(PostNoteLink, id=link_id)
        
        # Delete the link
        link.delete()
        
        # Return success response
        return JsonResponse({
            'status': 'success'
        })
        
    except Exception as e:
        # Return error response
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)


    


@require_POST
def create_postnote_link(request):
    """
    View for creating a link between two post notes via AJAX
    """
    try:
        # Get data from request
        source_id = request.POST.get('source_id')
        target_id = request.POST.get('target_id')
        link_type = request.POST.get('link_type')
        source_position = request.POST.get('source_position', 'right')
        target_position = request.POST.get('target_position', 'left')
        
        # Validate inputs
        if not source_id or not target_id or not link_type:
            return JsonResponse({
                'status': 'error',
                'message': 'Missing required fields'
            }, status=400)
        
        # Get the post notes
        source = get_object_or_404(PostNote, id=source_id)
        target = get_object_or_404(PostNote, id=target_id)
        
        # Check if link already exists
        existing_link = PostNoteLink.objects.filter(
            source=source,
            target=target,
            link_type=link_type
        ).first()
        
        if existing_link:
            return JsonResponse({
                'status': 'error',
                'message': 'Link already exists'
            }, status=400)
        
        # Create the link
        link = PostNoteLink.objects.create(
            source=source,
            target=target,
            link_type=link_type,
            source_position=source_position,
            target_position=target_position
        )
        
        # Return success response
        return JsonResponse({
            'status': 'success',
            'link_id': link.id,
            'source_id': source_id,
            'target_id': target_id,
            'link_type': link_type,
            'source_position': source_position,
            'target_position': target_position
        })
        
    except Exception as e:
        # Return error response
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@require_POST
def get_postnote_links(request, project_id):
    """
    View for getting all links for a project via AJAX
    """
    try:
        # Get all post notes in the project
        post_notes = PostNote.objects.filter(project_id=project_id)
        
        # Get all links involving these post notes
        links = PostNoteLink.objects.filter(
            source__in=post_notes,
            target__in=post_notes
        ).select_related('source', 'target')
        
        # Format links data
        links_data = []
        for link in links:
            links_data.append({
                'id': link.id,
                'source_id': link.source.id,
                'target_id': link.target.id,
                'link_type': link.link_type,
                'source_position': link.source_position,
                'target_position': link.target_position
            })
        
        # Return success response
        return JsonResponse({
            'status': 'success',
            'links': links_data
        })
        
    except Exception as e:
        # Return error response
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)
    

# @require_POST
# def get_postnote_links(request, project_id):
#     """
#     View for getting all links for a project via AJAX
#     """
#     try:
#         # Get all post notes in the project
#         post_notes = PostNote.objects.filter(project_id=project_id)
        
#         # Get all links involving these post notes
#         links = PostNoteLink.objects.filter(
#             source__in=post_notes,
#             target__in=post_notes
#         ).select_related('source', 'target')
        
#         # Format links data
#         links_data = []
#         for link in links:
#             links_data.append({
#                 'id': link.id,
#                 'source_id': link.source.id,
#                 'target_id': link.target.id,
#                 'link_type': link.link_type
#             })
        
#         # Return success response
#         return JsonResponse({
#             'status': 'success',
#             'links': links_data
#         })
        
#     except Exception as e:
#         # Return error response
#         return JsonResponse({
#             'status': 'error',
#             'message': str(e)
#         }, status=400)