from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST, require_http_methods, require_GET
from django.utils import timezone
from django.contrib import messages
from django.db.models import Q, Max
from django.db.models import F
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth import logout
from django.shortcuts import redirect

import json

from .models import *

# Helper function to get todos
def get_todos(request, search_query=None, todo_list_id=None):
    # Filter by owner first
    todos = Todo.objects.filter(owner=request.user, active=True, deleted=False)
    
    # Filter by todo list if provided
    if todo_list_id:
        todos = todos.filter(my_todos_id=todo_list_id)
    
    if search_query:
        todos = todos.filter(
            Q(name__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    return todos.order_by('position')

# Helper function to get statistics
def get_stats(request, todo_list_id=None):
    # Start with user's todos
    all_todos = Todo.objects.filter(owner=request.user, active=True, deleted=False)
    
    # Filter by todo list if provided
    if todo_list_id:
        all_todos = all_todos.filter(my_todos_id=todo_list_id)
    
    stats = {
        'total': all_todos.count(),
        'done': all_todos.filter(done=True).count(),
        'todo': all_todos.filter(done=False, blocked=False).count(),
        'blocked': all_todos.filter(blocked=True).count(),
        'wip': all_todos.filter(done=False, blocked=False).exclude(kanban_column__column_type='todo').exclude(kanban_column__column_type='done').count()
    }
    
    return stats

# MyTodos views
@login_required
def my_todos_listx1(request):
    """List view of all todo lists (MyTodos) owned by the user"""
    # Get active lists owned by the user
    todo_lists = MyTodos.objects.filter(owner=request.user, active=True, deleted=False).order_by('position')
    
    # Count of deleted lists for trash button
    trash_count = MyTodos.objects.filter(owner=request.user, deleted=True).count()
    
    context = {
        'todo_lists': todo_lists,
        'all_todo_lists': todo_lists,
        'trash_count': trash_count,
    }
    
    return render(request, 'app_todos/my_todos_list.html', context)
@login_required
def my_todos_list(request):
    """List view of all todo lists (MyTodos) owned by the user"""
    # Get active lists owned by the user
    own_lists = MyTodos.objects.filter(owner=request.user, active=True, deleted=False).order_by('position')
    
    # Get shared lists where the user has access
    shared_lists = MyTodos.objects.filter(
        shares__shared_with=request.user,
        active=True, 
        deleted=False
    ).exclude(owner=request.user).order_by('name')
    
    # Count of deleted lists for trash button
    trash_count = MyTodos.objects.filter(owner=request.user, deleted=True).count()
    
    # Combine all accessible lists
    all_todo_lists = list(own_lists)
    
    # Add shared lists with a prefix for display purposes
    for shared_list in shared_lists:
        if shared_list not in all_todo_lists:  # Avoid duplicates
            shared_list.display_name = f"👥 {shared_list.name} (by {shared_list.owner.username})"
            all_todo_lists.append(shared_list)
    
    context = {
        'todo_lists': own_lists,  # User's own lists
        'shared_lists': shared_lists,  # Lists shared with the user
        'all_todo_lists': all_todo_lists,  # Combined lists
        'trash_count': trash_count,
    }
    
    return render(request, 'app_todos/my_todos_list.html', context)
@login_required
def my_todos_detail(request, list_id):
    """Detail view for a specific todo list - shows todos in this list"""
    todo_list = get_object_or_404(MyTodos, pk=list_id, active=True, deleted=False)
    
    # Check if user has access to this list (owner, shared, or public)
    is_owner = todo_list.owner == request.user
    is_shared = todo_list.is_shared_with(request.user)
    is_public = todo_list.is_public
    
    if not (is_owner or is_shared or is_public):
        messages.error(request, "You don't have permission to view this list.")
        return redirect('todo_app:my_todos_list')
    
    # Check if user can edit (owner or shared with edit permission)
    can_edit = todo_list.can_user_edit(request.user)
    
    # Default to table view, but can be overridden with query param
    view_type = request.GET.get('view', 'table')
    
    if view_type == 'kanban':
        return kanban_view(request, todo_list_id=list_id, read_only=not can_edit)
    elif view_type == 'canvas':
        return canvas_view(request, todo_list_id=list_id, read_only=not can_edit)
    elif view_type == 'calendar':
        return calendar_view(request, todo_list_id=list_id, read_only=not can_edit)
    else:
        return table_view(request, todo_list_id=list_id, read_only=not can_edit)


# Update my_todos_edit view
@require_http_methods(["GET", "POST"])
def my_todos_edit(request, pk):
    """Edit a todo list"""
    todo_list = get_object_or_404(MyTodos, pk=pk)
    
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        
        if not name:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'error': 'List name is required'}, status=400)
            messages.error(request, 'List name is required')
            return redirect('todo_app:my_todos_list')
        
        todo_list.name = name
        todo_list.description = request.POST.get('description', '')
        todo_list.icon = request.POST.get('icon', 'fa-list')
        todo_list.color = request.POST.get('color', 'primary')
        todo_list.is_public = request.POST.get('is_public', False) == 'on'
        todo_list.save()
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success', 'redirect_url': reverse('todo_app:my_todos_list')})
        
        return redirect('todo_app:my_todos_list')
    
    # GET request
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = {
            'id': todo_list.id,
            'name': todo_list.name,
            'description': todo_list.description if todo_list.description else '',
            'icon': todo_list.icon if todo_list.icon else 'fa-list',
            'color': todo_list.color if todo_list.color else 'primary',
        }
        return JsonResponse(data)
    
    # Regular GET - render the form page
    context = {
        'todo_list': todo_list,
        'editing': True,
    }
    return render(request, 'todo_app/my_todos_form.html', context)

# Update my_todos_create view

@require_http_methods(["GET", "POST"])
@login_required
def my_todos_create(request):
    """Create a new todo list"""
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        is_public = request.POST.get('is_public', False) == 'on'
        if not name:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'error': 'List name is required'}, status=400)
            messages.error(request, 'List name is required')
            return redirect('todo_app:my_todos_list')
        
        description = request.POST.get('description', '')
        icon = request.POST.get('icon', 'fa-list')
        color = request.POST.get('color', 'primary')
        
        # Get highest position for this user's lists
        highest_position = MyTodos.objects.filter(owner=request.user).aggregate(Max('position'))['position__max'] or 0
        
        todo_list = MyTodos(
            name=name,
            description=description,
            icon=icon,
            color=color,
            position=highest_position + 1,
            owner=request.user,  # Set the owner to current user
            is_public=is_public,
        )
        todo_list.save()
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'success', 
                'redirect_url': reverse('todo_app:my_todos_detail', args=[todo_list.id])
            })
        
        return redirect('todo_app:my_todos_detail', list_id=todo_list.id)
    
    # GET request
    return render(request, 'app_todos/my_todos_form.html', {'editing': False})

@require_POST
def my_todos_delete(request, pk):
    """Soft delete a todo list"""
    todo_list = get_object_or_404(MyTodos, pk=pk, active=True, deleted=False)
    todo_list.soft_delete()
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success'})
    
    messages.success(request, f'Todo list "{todo_list.name}" moved to trash.')
    return redirect('todo_app:my_todos_list')

@require_POST
def my_todos_restore(request, pk):
    """Restore a deleted todo list"""
    todo_list = get_object_or_404(MyTodos, pk=pk, deleted=True)
    todo_list.restore()
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success'})
    
    messages.success(request, f'Todo list "{todo_list.name}" has been restored.')
    return redirect('todo_app:my_todos_trash')

@login_required
def my_todos_trash(request):
    """View for showing deleted todo lists"""
    deleted_lists = MyTodos.objects.filter(owner=request.user, deleted=True).order_by('-updated_at')
    
    context = {
        'deleted_lists': deleted_lists,
    }
    
    return render(request, 'app_todos/my_todos_trash.html', context)


@require_POST
def my_todos_permanent_delete(request, pk):
    """Permanently delete a todo list"""
    todo_list = get_object_or_404(MyTodos, pk=pk, deleted=True)
    
    # Store name for message
    name = todo_list.name
    
    # Actually delete from database
    todo_list.delete()
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success'})
    
    messages.success(request, f'Todo list "{name}" has been permanently deleted.')
    return redirect('todo_app:my_todos_trash')

@require_POST
def my_todos_reorder(request):
    """Reorder todo lists"""
    data = json.loads(request.body)
    lists = data.get('lists', [])
    
    for list_data in lists:
        list_id = list_data.get('id')
        position = list_data.get('position')
        
        todo_list = get_object_or_404(MyTodos, pk=list_id, active=True, deleted=False)
        todo_list.position = position
        todo_list.save(update_fields=['position'])
    
    return JsonResponse({'status': 'success'})

# Base views
def todo_list(request):
    # Check if there are any lists
    if MyTodos.objects.filter(active=True, deleted=False).exists():
        # Get the first list
        first_list = MyTodos.objects.filter(active=True, deleted=False).order_by('position').first()
        return redirect('todo_app:my_todos_detail', list_id=first_list.id)
    else:
        # No lists, go to the create list page
        return redirect('todo_app:my_todos_list')

@login_required
def table_view(request, todo_list_id=None, read_only=False):
    """Table view of todos"""
    search_query = request.GET.get('search', None)
    
    # If todo_list_id is provided, filter todos by that list
    if todo_list_id:
        todo_list = get_object_or_404(MyTodos, pk=todo_list_id, active=True, deleted=False)
        
        # Check if user has access to this list
        if not (todo_list.owner == request.user or todo_list.is_shared_with(request.user) or todo_list.is_public):
            messages.error(request, "You don't have permission to view this list.")
            return redirect('todo_app:my_todos_list')
        
        if todo_list.owner == request.user:
            # User's own list - show all their todos in this list
            todos = Todo.objects.filter(
                # owner=request.user,
                my_todos=todo_list,
                active=True,
                deleted=False
            )
        else:
            # Shared list - show todos in this list regardless of owner
            todos = Todo.objects.filter(
                my_todos=todo_list,
                active=True,
                deleted=False
            )
            
        if search_query:
            todos = todos.filter(
                Q(name__icontains=search_query) | 
                Q(description__icontains=search_query)
            )
            
        # Get stats for this list
        if todo_list.owner == request.user:
            stats = get_stats(request, todo_list_id=todo_list_id)
        else:
            # Custom stats calculation for shared lists
            list_todos = Todo.objects.filter(my_todos=todo_list, active=True, deleted=False)
            stats = {
                'total': list_todos.count(),
                'done': list_todos.filter(done=True).count(),
                'todo': list_todos.filter(done=False, blocked=False).count(),
                'blocked': list_todos.filter(blocked=True).count(),
                'wip': list_todos.filter(done=False, blocked=False).exclude(
                    kanban_column__column_type='todo'
                ).exclude(
                    kanban_column__column_type='done'
                ).count()
            }
    else:
        # Without todo_list_id, show all todos owned by the user
        todos = Todo.objects.filter(
            # owner=request.user,
            active=True,
            deleted=False
        )
        
        if search_query:
            todos = todos.filter(
                Q(name__icontains=search_query) | 
                Q(description__icontains=search_query)
            )
            
        stats = get_stats(request)
        todo_list = None
    
    # Use tree structure for display
    todos = todos.order_by('tree_id', 'lft')
    
    # Get potential parents
    if todo_list and todo_list.owner != request.user:
        # For shared lists, only show tasks in that list as potential parents
        potential_parents = Todo.objects.filter(
            my_todos=todo_list,
            active=True,
            deleted=False
        ).exclude(done=True)
    else:
        # For user's own lists, show their tasks
        potential_parents = Todo.objects.filter(
            owner=request.user,
            active=True,
            deleted=False
        ).exclude(done=True)
        
        # If in a specific list, filter potential parents to that list
        if todo_list_id:
            potential_parents = potential_parents.filter(my_todos_id=todo_list_id)
    
    # Order parents by tree structure
    potential_parents = potential_parents.order_by('tree_id', 'lft')
    
    # Get all todo lists the user has access to
    own_lists = MyTodos.objects.filter(
        owner=request.user,
        active=True,
        deleted=False
    ).order_by('position')
    
    shared_lists = MyTodos.objects.filter(
        shares__shared_with=request.user,
        active=True,
        deleted=False
    )
    
    public_lists = MyTodos.objects.filter(
        is_public=True,
        active=True,
        deleted=False
    ).exclude(owner=request.user)
    
    # Combine all accessible lists
    all_todo_lists = list(own_lists)
    
    # Add shared lists with a prefix
    for shared_list in shared_lists:
        if shared_list not in all_todo_lists:  # Avoid duplicates
            shared_list.display_name = f"👥 {shared_list.name} (by {shared_list.owner.username})"
            all_todo_lists.append(shared_list)
    
    # Add public lists with a prefix
    for public_list in public_lists:
        if public_list not in all_todo_lists:  # Avoid duplicates
            public_list.display_name = f"🌐 {public_list.name} (by {public_list.owner.username})"
            all_todo_lists.append(public_list)
    
    context = {
        'todos': todos,
        'stats': stats,
        'potential_parents': potential_parents,
        'search_query': search_query,
        'todo_list': todo_list,
        'todo_lists': own_lists,  # Only user's lists for dropdown
        'all_todo_lists': all_todo_lists,  # All accessible lists
        'read_only': read_only,
        'shared_lists': shared_lists,
        'public_lists': public_lists,
        'is_owner': todo_list.owner == request.user if todo_list else True
    }
    
    return render(request, 'app_todos/table_view.html', context)

@require_GET
def get_children(request):
    """Get children of a todo for AJAX expansion"""
    parent_id = request.GET.get('parent_id')
    if not parent_id:
        return JsonResponse({'error': 'No parent ID provided'}, status=400)
    
    parent = get_object_or_404(Todo, pk=parent_id)
    children = parent.get_children().filter(active=True, deleted=False).order_by('position')
    
    children_data = []
    for child in children:
        children_data.append({
            'id': child.id,
            'name': child.name,
            'description': child.description if child.description else '',
            'priority': child.priority,
            'done': child.done,
            'blocked': child.blocked,
            'has_children': child.get_children().exists(),
            'children_count': child.get_children().count()
        })
    
    return JsonResponse({'children': children_data})



@login_required
def kanban_view(request, todo_list_id=None, read_only=False):
    """Kanban board view of todos"""
    # If todo_list_id is provided, filter todos by that list
    if todo_list_id:
        todo_list = get_object_or_404(MyTodos, pk=todo_list_id, active=True, deleted=False)
        
        # Check if user has access to this list
        if not (todo_list.owner == request.user or todo_list.is_shared_with(request.user) or todo_list.is_public):
            messages.error(request, "You don't have permission to view this list.")
            return redirect('todo_app:my_todos_list')
        
        if todo_list.owner == request.user:
            # User's own list - show all their todos in this list
            todos = Todo.objects.filter(
                owner=request.user,
                my_todos=todo_list,
                active=True,
                deleted=False
            )
        else:
            # Shared list - show todos in this list regardless of owner
            todos = Todo.objects.filter(
                my_todos=todo_list,
                active=True,
                deleted=False
            )
            
        # Get stats for this list
        if todo_list.owner == request.user:
            stats = get_stats(request, todo_list_id=todo_list_id)
        else:
            # Custom stats calculation for shared lists
            list_todos = Todo.objects.filter(my_todos=todo_list, active=True, deleted=False)
            stats = {
                'total': list_todos.count(),
                'done': list_todos.filter(done=True).count(),
                'todo': list_todos.filter(done=False, blocked=False).count(),
                'blocked': list_todos.filter(blocked=True).count(),
                'wip': list_todos.filter(done=False, blocked=False).exclude(
                    kanban_column__column_type='todo'
                ).exclude(
                    kanban_column__column_type='done'
                ).count()
            }
    else:
        # Without todo_list_id, show all todos owned by the user
        todos = Todo.objects.filter(
            owner=request.user,
            active=True,
            deleted=False
        )
        stats = get_stats(request)
        todo_list = None
    
    # Get or create default columns for this specific list
    # Only create columns if user is the owner
    if todo_list:
        if todo_list.owner == request.user:
            todo_column, _ = KanbanColumn.objects.get_or_create(
                column_type='todo',
                my_todos=todo_list,
                defaults={
                    'name': 'Todo', 
                    'is_default': True,
                    'my_todos': todo_list,
                }
            )
            
            done_column, _ = KanbanColumn.objects.get_or_create(
                column_type='done',
                my_todos=todo_list,
                defaults={
                    'name': 'Done', 
                    'is_default': True,
                    'my_todos': todo_list,
                }
            )
        else:
            # For shared lists, just get the columns
            todo_column = KanbanColumn.objects.filter(
                column_type='todo',
                my_todos=todo_list,
                is_default=True
            ).first()
            
            done_column = KanbanColumn.objects.filter(
                column_type='done',
                my_todos=todo_list,
                is_default=True
            ).first()
            
            # If columns don't exist yet, we can't create them
            if not todo_column or not done_column:
                messages.warning(request, "This list doesn't have kanban columns set up yet.")
                return redirect('todo_app:my_todos_detail', list_id=todo_list.id)
    else:
        # For global view, get or create user's default columns
        todo_column, _ = KanbanColumn.objects.get_or_create(
            column_type='todo',
            my_todos=None,
            defaults={
                'name': 'Todo',
                'is_default': True,
            }
        )
        
        done_column, _ = KanbanColumn.objects.get_or_create(
            column_type='done',
            my_todos=None,
            defaults={
                'name': 'Done',
                'is_default': True,
            }
        )
    
    # Get all columns for this specific list
    if todo_list:
        columns = KanbanColumn.objects.filter(
            active=True, 
            deleted=False,
            my_todos=todo_list
        ).order_by('position')
    else:
        # Global view - show user's personal columns
        columns = KanbanColumn.objects.filter(
            active=True, 
            deleted=False,
            my_todos__isnull=True,
        ).order_by('position')
    
    # Assign todos without a column to the todo column if user can edit
    if not read_only and todo_column and done_column:
        for todo in todos:
            if not todo.kanban_column:
                if todo.done:
                    todo.kanban_column = done_column
                else:
                    todo.kanban_column = todo_column
                
                # Only modify todos the user owns or has edit permission for
                if todo.owner == request.user or (todo.my_todos and todo.my_todos.can_user_edit(request.user)):
                    todo.save()
    
    # Get potential parents
    if todo_list and todo_list.owner != request.user:
        # For shared lists, only show tasks in that list as potential parents
        potential_parents = Todo.objects.filter(
            my_todos=todo_list,
            active=True,
            deleted=False
        ).exclude(done=True)
    else:
        # For user's own lists, show their tasks
        potential_parents = Todo.objects.filter(
            owner=request.user,
            active=True,
            deleted=False
        ).exclude(done=True)
        
        # If in a specific list, filter potential parents to that list
        if todo_list_id:
            potential_parents = potential_parents.filter(my_todos_id=todo_list_id)
    
    # Get all todo lists the user has access to
    own_lists = MyTodos.objects.filter(
        owner=request.user,
        active=True,
        deleted=False
    ).order_by('position')
    
    shared_lists = MyTodos.objects.filter(
        shares__shared_with=request.user,
        active=True,
        deleted=False
    )
    
    public_lists = MyTodos.objects.filter(
        is_public=True,
        active=True,
        deleted=False
    ).exclude(owner=request.user)
    
    # Combine all accessible lists
    all_todo_lists = list(own_lists)
    
    # Add shared lists with a prefix
    for shared_list in shared_lists:
        if shared_list not in all_todo_lists:  # Avoid duplicates
            shared_list.display_name = f"👥 {shared_list.name} (by {shared_list.owner.username})"
            all_todo_lists.append(shared_list)
    
    # Add public lists with a prefix
    for public_list in public_lists:
        if public_list not in all_todo_lists:  # Avoid duplicates
            public_list.display_name = f"🌐 {public_list.name} (by {public_list.owner.username})"
            all_todo_lists.append(public_list)
    
    context = {
        'todos': todos,
        'columns': columns,
        'stats': stats,
        'potential_parents': potential_parents,
        'todo_list': todo_list,
        'todo_lists': own_lists,  # Only user's lists for dropdown
        'all_todo_lists': all_todo_lists,  # All accessible lists
        'read_only': read_only,
        'is_owner': todo_list.owner == request.user if todo_list else True,
        'todo_column': todo_column,
        'done_column': done_column
    }
    
    return render(request, 'app_todos/kanban_view.html', context)

@login_required
def canvas_view(request, todo_list_id=None, read_only=False):
    """Canvas view of todos"""
    # If todo_list_id is provided, filter todos by that list
    if todo_list_id:
        todo_list = get_object_or_404(MyTodos, pk=todo_list_id, active=True, deleted=False)
        
        # Check if user has access to this list
        if not (todo_list.owner == request.user or todo_list.is_shared_with(request.user) or todo_list.is_public):
            messages.error(request, "You don't have permission to view this list.")
            return redirect('todo_app:my_todos_list')
        
        if todo_list.owner == request.user:
            # User's own list - show all their todos in this list
            todos = Todo.objects.filter(
                owner=request.user,
                my_todos=todo_list,
                active=True,
                deleted=False
            )
        else:
            # Shared list - show todos in this list regardless of owner
            todos = Todo.objects.filter(
                my_todos=todo_list,
                active=True,
                deleted=False
            )
            
        # Get stats for this list
        if todo_list.owner == request.user:
            stats = get_stats(request, todo_list_id=todo_list_id)
        else:
            # Custom stats calculation for shared lists
            list_todos = Todo.objects.filter(my_todos=todo_list, active=True, deleted=False)
            stats = {
                'total': list_todos.count(),
                'done': list_todos.filter(done=True).count(),
                'todo': list_todos.filter(done=False, blocked=False).count(),
                'blocked': list_todos.filter(blocked=True).count(),
                'wip': list_todos.filter(done=False, blocked=False).exclude(
                    kanban_column__column_type='todo'
                ).exclude(
                    kanban_column__column_type='done'
                ).count()
            }
    else:
        # Without todo_list_id, show all todos owned by the user
        todos = Todo.objects.filter(
            owner=request.user,
            active=True,
            deleted=False
        )
        stats = get_stats(request)
        todo_list = None
    
    # Get potential parents
    if todo_list and todo_list.owner != request.user:
        # For shared lists, only show tasks in that list as potential parents
        potential_parents = Todo.objects.filter(
            my_todos=todo_list,
            active=True,
            deleted=False
        ).exclude(done=True)
    else:
        # For user's own lists, show their tasks
        potential_parents = Todo.objects.filter(
            owner=request.user,
            active=True,
            deleted=False
        ).exclude(done=True)
        
        # If in a specific list, filter potential parents to that list
        if todo_list_id:
            potential_parents = potential_parents.filter(my_todos_id=todo_list_id)
    
    # Get all todo lists the user has access to
    own_lists = MyTodos.objects.filter(
        owner=request.user,
        active=True,
        deleted=False
    ).order_by('position')
    
    shared_lists = MyTodos.objects.filter(
        shares__shared_with=request.user,
        active=True,
        deleted=False
    )
    
    public_lists = MyTodos.objects.filter(
        is_public=True,
        active=True,
        deleted=False
    ).exclude(owner=request.user)
    
    # Combine all accessible lists
    all_todo_lists = list(own_lists)
    
    # Add shared lists with a prefix
    for shared_list in shared_lists:
        if shared_list not in all_todo_lists:  # Avoid duplicates
            shared_list.display_name = f"👥 {shared_list.name} (by {shared_list.owner.username})"
            all_todo_lists.append(shared_list)
    
    # Add public lists with a prefix
    for public_list in public_lists:
        if public_list not in all_todo_lists:  # Avoid duplicates
            public_list.display_name = f"🌐 {public_list.name} (by {public_list.owner.username})"
            all_todo_lists.append(public_list)
    
    context = {
        'todos': todos,
        'stats': stats,
        'potential_parents': potential_parents,
        'todo_list': todo_list,
        'todo_lists': own_lists,  # Only user's lists for dropdown
        'all_todo_lists': all_todo_lists,  # All accessible lists
        'read_only': read_only,
        'is_owner': todo_list.owner == request.user if todo_list else True
    }
    
    return render(request, 'app_todos/canvas_view.html', context)
# all_todo_lists = MyTodos.objects.filter(active=True, deleted=False).order_by('position')
# context['all_todo_lists'] = all_todo_lists
# Todo CRUD operations
@require_http_methods(["GET", "POST"])
@login_required
def todo_create(request):
    """Create a new todo"""
    if request.method == 'POST':
        # Create todo from form data
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        priority = request.POST.get('priority', 'normal')
        blocked = request.POST.get('blocked', False) == 'on'
        parent_id = request.POST.get('parent', None)
        
        # Optional fields
        start_date = request.POST.get('start_date', None)
        due_date = request.POST.get('due_date', None)
        kanban_column_id = request.POST.get('kanban_column', None)
        canvas_x = request.POST.get('canvas_x', 0)
        canvas_y = request.POST.get('canvas_y', 0)
        my_todos_id = request.POST.get('my_todos', None)
        print(f">>> === OWNER: {request.user}=== <<<")
        # Create the todo with the current user as owner
        todo = Todo(
            name=name,
            description=description,
            priority=priority,
            blocked=blocked,
            canvas_x=canvas_x,
            canvas_y=canvas_y,
            owner=request.user  # Set the owner to current user
        )
        
        # Set optional fields if provided
        if parent_id and parent_id != '':
            parent = get_object_or_404(Todo, pk=parent_id)
            # Check if user has access to the parent
            if parent.owner != request.user and not (parent.my_todos and parent.my_todos.can_user_edit(request.user)):
                return JsonResponse({'error': 'You do not have permission to use this parent task'}, status=403)
            todo.parent = parent
        
        if start_date and start_date != '':
            todo.start_date = start_date
        
        if due_date and due_date != '':
            todo.due_date = due_date
        
        if kanban_column_id and kanban_column_id != '':
            kanban_column = get_object_or_404(KanbanColumn, pk=kanban_column_id)
            todo.kanban_column = kanban_column
        
        # Set MyTodos if provided
        if my_todos_id and my_todos_id != '':
            my_todos = get_object_or_404(MyTodos, pk=my_todos_id)
            # Check if user has edit access to the list
            if not my_todos.can_user_edit(request.user):
                return JsonResponse({'error': 'You do not have permission to add to this list'}, status=403)
            todo.my_todos = my_todos
        
        # Save the todo
        todo.save()
        
        # Default response for AJAX
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success', 'id': todo.id})
        
        # If todo belongs to a list, redirect to that list's view
        if todo.my_todos:
            if 'table' in request.META.get('HTTP_REFERER', ''):
                return redirect('todo_app:my_todos_detail', list_id=todo.my_todos.id)
            elif 'kanban' in request.META.get('HTTP_REFERER', ''):
                return redirect('todo_app:my_todos_detail', list_id=todo.my_todos.id, view='kanban')
            else:
                return redirect('todo_app:my_todos_detail', list_id=todo.my_todos.id, view='canvas')
        else:
            # Otherwise redirect to appropriate global view
            if 'table' in request.META.get('HTTP_REFERER', ''):
                return redirect('todo_app:table_view')
            elif 'kanban' in request.META.get('HTTP_REFERER', ''):
                return redirect('todo_app:kanban_view')
            else:
                return redirect('todo_app:canvas_view')
    
    # If GET request, show form (should not happen)
    return redirect('todo_app:todo_list')

@require_http_methods(["GET"])
def todo_view(request, pk):
    """View a todo's details"""
    todo = get_object_or_404(Todo, pk=pk, active=True, deleted=False)
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = f"""
        <h4>{todo.name}</h4>
        <p class="small text-muted">Priority: {todo.get_priority_display()}</p>
        
        <hr>
        
        <div class="mb-3">
            <h6>Description:</h6>
            <p>{todo.description or 'No description provided.'}</p>
        </div>
        
        <div class="row mb-3">
            <div class="col">
                <h6>Start Date:</h6>
                <p>{todo.start_date.strftime('%Y-%m-%d %H:%M') if todo.start_date else 'Not set'}</p>
            </div>
            <div class="col">
                <h6>Due Date:</h6>
                <p>{todo.due_date.strftime('%Y-%m-%d %H:%M') if todo.due_date else 'Not set'}</p>
            </div>
        </div>
        
        <div class="mb-3">
            <h6>Status:</h6>
            <p>
                {f'<span class="badge bg-success">Done</span>' if todo.done else ''}
                {f'<span class="badge bg-danger">Blocked</span>' if todo.blocked else ''}
                {f'<span class="badge bg-secondary">Active</span>' if not todo.done and not todo.blocked else ''}
            </p>
        </div>
        
        <div class="mb-3">
            <h6>Created:</h6>
            <p>{todo.created_at.strftime('%Y-%m-%d %H:%M')}</p>
        </div>
        
        <div class="mb-3">
            <h6>Last Updated:</h6>
            <p>{todo.updated_at.strftime('%Y-%m-%d %H:%M')}</p>
        </div>
        
        {f'''
        <div class="mb-3">
            <h6>Parent:</h6>
            <p>{todo.parent.name}</p>
        </div>
        ''' if todo.parent else ''}
        
        {f'''
        <div class="mb-3">
            <h6>Children:</h6>
            <ul>
                {"".join([f'<li>{child.name}</li>' for child in todo.get_children()])}
            </ul>
        </div>
        ''' if todo.get_children().exists() else ''}
        """
        
        return HttpResponse(html)
    
    # Non-AJAX response
    return redirect('todo_app:todo_list')

@require_http_methods(["GET", "POST"])
def todo_edit(request, pk):
    """Edit a todo"""
    todo = get_object_or_404(Todo, pk=pk, active=True, deleted=False)
    # Verify the user can edit this todo
    can_edit = todo.owner == request.user or (todo.my_todos and todo.my_todos.can_user_edit(request.user))
    # Check if user can edit this todo
    if not can_edit:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'error': 'You do not have permission to edit this todo'}, status=403)
        messages.error(request, "You don't have permission to edit this todo.")
        return redirect('todo_app:my_todos_list')
    if request.method == 'POST':
        # Update todo from form data
        todo.name = request.POST.get('name')
        todo.description = request.POST.get('description', '')
        todo.priority = request.POST.get('priority', 'normal')
        todo.blocked = request.POST.get('blocked', False) == 'on'
        
        # Update optional fields if provided
        start_date = request.POST.get('start_date', None)
        if start_date and start_date != '':
            todo.start_date = start_date
        else:
            todo.start_date = None
        
        due_date = request.POST.get('due_date', None)
        if due_date and due_date != '':
            todo.due_date = due_date
        else:
            todo.due_date = None
        
        parent_id = request.POST.get('parent', None)
        if parent_id and parent_id != '':
            parent = get_object_or_404(Todo, pk=parent_id)
            todo.parent = parent
        else:
            todo.parent = None
        
        kanban_column_id = request.POST.get('kanban_column', None)
        if kanban_column_id and kanban_column_id != '':
            kanban_column = get_object_or_404(KanbanColumn, pk=kanban_column_id)
            todo.kanban_column = kanban_column
        
        canvas_x = request.POST.get('canvas_x', None)
        if canvas_x and canvas_x != '':
            todo.canvas_x = canvas_x
        
        canvas_y = request.POST.get('canvas_y', None)
        if canvas_y and canvas_y != '':
            todo.canvas_y = canvas_y
        
        my_todos_id = request.POST.get('my_todos', None)
        if my_todos_id and my_todos_id != '':
            my_todos = get_object_or_404(MyTodos, pk=my_todos_id)
            todo.my_todos = my_todos
        else:
            todo.my_todos = None
        
        # Save the todo
        todo.save()
        
        # Default response for AJAX
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success'})
        
        # If todo belongs to a list, redirect to that list's view
        if todo.my_todos:
            if 'table' in request.META.get('HTTP_REFERER', ''):
                return redirect('todo_app:my_todos_detail', list_id=todo.my_todos.id)
            elif 'kanban' in request.META.get('HTTP_REFERER', ''):
                return redirect('todo_app:my_todos_detail', list_id=todo.my_todos.id, view='kanban')
            else:
                return redirect('todo_app:my_todos_detail', list_id=todo.my_todos.id, view='canvas')
        else:
            # Otherwise redirect to appropriate global view
            if 'table' in request.META.get('HTTP_REFERER', ''):
                return redirect('todo_app:table_view')
            elif 'kanban' in request.META.get('HTTP_REFERER', ''):
                return redirect('todo_app:kanban_view')
            else:
                return redirect('todo_app:canvas_view')
    
    # If GET request, return todo data for AJAX
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = {
            'id': todo.id,
            'name': todo.name,
            'description': todo.description,
            'priority': todo.priority,
            'blocked': todo.blocked,
            'parent': todo.parent.id if todo.parent else '',
            'kanban_column': todo.kanban_column.id if todo.kanban_column else '',
            'canvas_x': todo.canvas_x,
            'canvas_y': todo.canvas_y,
            'my_todos': todo.my_todos.id if todo.my_todos else '',
        }
        
        # Handle dates for form
        if todo.start_date:
            data['start_date'] = todo.start_date.strftime('%Y-%m-%dT%H:%M')
        else:
            data['start_date'] = ''
        
        if todo.due_date:
            data['due_date'] = todo.due_date.strftime('%Y-%m-%dT%H:%M')
        else:
            data['due_date'] = ''
        
        return JsonResponse(data)
    
    # Non-AJAX response
    return redirect('todo_app:todo_list')

@require_POST
def todo_delete(request, pk):
    """Soft delete a todo"""
    todo = get_object_or_404(Todo, pk=pk, active=True, deleted=False)
    todo.deleted = True
    todo.active = False
    todo.save()
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success'})
    
    messages.success(request, f'Todo "{todo.name}" has been moved to trash.')
    return redirect('todo_app:todo_list')

@require_POST
def bulk_restore(request):
    """Restore multiple deleted todos"""
    try:
        ids = json.loads(request.POST.get('ids', '[]'))
        if not ids:
            return JsonResponse({'status': 'error', 'message': 'No IDs provided'}, status=400)
        
        # Update all todos in one query
        Todo.objects.filter(pk__in=ids, deleted=True).update(
            deleted=False, 
            active=True
        )
        
        return JsonResponse({'status': 'success', 'count': len(ids)})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@require_POST
def bulk_permanent_delete(request):
    """Permanently delete multiple todos"""
    try:
        ids = json.loads(request.POST.get('ids', '[]'))
        if not ids:
            return JsonResponse({'status': 'error', 'message': 'No IDs provided'}, status=400)
        
        # Delete all todos in one query
        count = Todo.objects.filter(pk__in=ids, deleted=True).delete()[0]
        
        return JsonResponse({'status': 'success', 'count': count})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@require_POST
def todo_restore(request):
    """Restore a deleted todo"""
    todo_id = request.POST.get('id')
    todo = get_object_or_404(Todo, pk=todo_id, deleted=True)
    
    todo.deleted = False
    todo.active = True
    todo.save()
    
    return JsonResponse({'status': 'success'})

@require_POST
def todo_permanent_delete(request):
    """Permanently delete a todo from trash"""
    todo_id = request.POST.get('id')
    todo = get_object_or_404(Todo, pk=todo_id, deleted=True)
    
    # Actually delete from database
    todo.delete()
    
    return JsonResponse({'status': 'success'})

@require_POST
def empty_trash(request):
    """Empty the trash - permanently delete all trash items"""
    # Delete all items in trash
    Todo.objects.filter(deleted=True).delete()
    
    return JsonResponse({'status': 'success'})


@require_POST
def todo_copy(request, pk):
    """Copy a todo"""
    todo = get_object_or_404(Todo, pk=pk, active=True, deleted=False)
    new_todo = todo.copy_node()
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success', 'id': new_todo.id})
    
    messages.success(request, f'Todo "{todo.name}" has been copied.')
    return redirect('todo_app:todo_list')


@require_POST
def todo_mark_done(request, pk):
    """Mark a todo as done"""
    todo = get_object_or_404(Todo, pk=pk, active=True, deleted=False)
    
    # Get the todo's list if it has one
    todo_list = todo.my_todos
    
    is_done = request.POST.get('done', False)
    if is_done in ('true', 'on', '1', True):
        todo.mark_done()
        # Only update column if explicitly requested
        update_column = request.POST.get('update_column', False)
        if update_column in ('true', 'on', '1', True):
            # Get or create done column for the specific list
            done_column, _ = KanbanColumn.objects.get_or_create(
                column_type='done',
                my_todos=todo_list,  # Include the list association
                defaults={
                    'name': 'Done', 
                    'is_default': True,
                    'my_todos': todo_list  # Also in defaults
                }
            )
            todo.kanban_column = done_column
            todo.save()
    else:
        todo.done = False
        todo.done_at = None
        todo.save()
        # Only update column if explicitly requested
        update_column = request.POST.get('update_column', False)
        if update_column in ('true', 'on', '1', True):
            if todo.kanban_column and todo.kanban_column.column_type == 'done':
                # Get or create todo column for the specific list
                todo_column, _ = KanbanColumn.objects.get_or_create(
                    column_type='todo',
                    my_todos=todo_list,  # Include the list association
                    defaults={
                        'name': 'Todo', 
                        'is_default': True,
                        'my_todos': todo_list  # Also in defaults
                    }
                )
                todo.kanban_column = todo_column
                todo.save()
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success', 'done': todo.done})
    
    messages.success(request, f'Todo "{todo.name}" marked as {"done" if todo.done else "not done"}.')
    return redirect('todo_app:todo_list')

@require_POST
def todo_toggle_blocked(request, pk):
    """Toggle blocked status for a todo"""
    todo = get_object_or_404(Todo, pk=pk, active=True, deleted=False)
    
    is_blocked = request.POST.get('blocked', False)
    if is_blocked in ('true', 'on', '1', True):
        todo.block()
    else:
        todo.unblock()
    
    # No column change when blocking/unblocking
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success', 'blocked': todo.blocked})
    
    messages.success(request, f'Todo "{todo.name}" {"blocked" if todo.blocked else "unblocked"}.')
    return redirect('todo_app:kanban_view')


@require_http_methods(["GET", "POST"])
def kanban_column_create(request):
    """Create a new kanban column"""
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        wip_limit = request.POST.get('wip_limit', 0)
        position_choice = request.POST.get('position', 'end')
        
        # Get the current list (if any)
        todo_list_id = request.POST.get('todo_list_id')
        todo_list = None
        if todo_list_id:
            todo_list = get_object_or_404(MyTodos, pk=todo_list_id)
        
        # Determine position based on selection
        # This part remains largely the same, but we add the list filter to queries
        columns_query = KanbanColumn.objects.filter(my_todos=todo_list)
        
        if position_choice == 'beginning':
            # Place at the beginning, but after the todo column
            todo_column = columns_query.filter(column_type='todo', is_default=True).first()
            position = todo_column.position + 1 if todo_column else 0
        elif position_choice == 'end':
            # Place at the end, but before the done column
            done_column = columns_query.filter(column_type='done', is_default=True).first()
            if done_column:
                # Position right before done column
                position = done_column.position
                # Shift done column and any columns after it
                columns_query.filter(position__gte=position).update(position=F('position') + 1)
            else:
                # If no done column, use highest position + 1
                highest_position = columns_query.aggregate(Max('position'))['position__max'] or 0
                position = highest_position + 1
        elif position_choice.startswith('after_'):
            # Place after a specific column
            after_column_id = position_choice.replace('after_', '')
            try:
                after_column = columns_query.get(pk=after_column_id)
                position = after_column.position + 1
                # Shift any columns at or after the new position
                columns_query.filter(position__gte=position).update(position=F('position') + 1)
            except KanbanColumn.DoesNotExist:
                # Fallback to end
                highest_position = columns_query.aggregate(Max('position'))['position__max'] or 0
                position = highest_position + 1
        else:
            # Default to end
            highest_position = columns_query.aggregate(Max('position'))['position__max'] or 0
            position = highest_position + 1
        
        # Create the column with the list association
        column = KanbanColumn(
            name=name,
            description=description,
            wip_limit=wip_limit,
            position=position,
            my_todos=todo_list  # Associate with the list
        )
        column.save()
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success', 'id': column.id})
        
        # Redirect back to the appropriate kanban view
        if todo_list:
            return redirect('todo_app:my_todos_detail', list_id=todo_list.id, view='kanban')
        else:
            return redirect('todo_app:kanban_view')
    
    # If GET request (shouldn't happen)
    return redirect('todo_app:kanban_view')

@require_http_methods(["GET", "POST"])
def kanban_column_edit(request, pk):
    """Edit a kanban column"""
    column = get_object_or_404(KanbanColumn, pk=pk, active=True, deleted=False)
    
    if request.method == 'POST':
        column.name = request.POST.get('name')
        column.description = request.POST.get('description', '')
        column.wip_limit = request.POST.get('wip_limit', 0)
        column.save()
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'success'})
        
        messages.success(request, f'Column "{column.name}" has been updated.')
        return redirect('todo_app:kanban_view')
    
    # If GET request, return column data for AJAX
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = {
            'id': column.id,
            'name': column.name,
            'description': column.description,
            'wip_limit': column.wip_limit,
        }
        return JsonResponse(data)
    
    # Non-AJAX response
    return redirect('todo_app:kanban_view')

@require_POST
def kanban_column_delete(request, pk):
    """Delete a kanban column"""
    column = get_object_or_404(KanbanColumn, pk=pk, active=True, deleted=False)
    
    # Don't allow deleting default columns
    if column.is_default:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'error', 'message': 'Cannot delete default columns'}, status=400)
        
        messages.error(request, 'Cannot delete default columns.')
        return redirect('todo_app:kanban_view')
    
    # Move todos to the default todo column
    todo_column, _ = KanbanColumn.objects.get_or_create(
        column_type='todo',
        defaults={'name': 'Todo', 'is_default': True}
    )
    
    Todo.objects.filter(kanban_column=column).update(kanban_column=todo_column)
    
    column.permanent_delete()
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success'})
    
    messages.success(request, f'Column "{column.name}" has been deleted.')
    return redirect('todo_app:kanban_view')

@require_POST
def move_todo_to_column(request, pk, column_id):
    """Move a todo to a specific kanban column"""
    todo = get_object_or_404(Todo, pk=pk, active=True, deleted=False)
    column = get_object_or_404(KanbanColumn, pk=column_id, active=True, deleted=False)
    
    # Check WIP limit
    if column.wip_limit > 0:
        current_count = Todo.objects.filter(kanban_column=column, active=True, deleted=False).count()
        if current_count >= column.wip_limit and todo.kanban_column != column:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse(
                    {'status': 'error', 'message': f'WIP limit of {column.wip_limit} reached for this column'}, 
                    status=400
                )
            
            messages.error(request, f'WIP limit of {column.wip_limit} reached for column "{column.name}".')
            return redirect('todo_app:kanban_view')
    
    # Handle done status based on column type
    if column.column_type == 'done' and not todo.done:
        todo.mark_done()
    elif column.column_type != 'done' and todo.done and todo.kanban_column and todo.kanban_column.column_type == 'done':
        todo.done = False
        todo.done_at = None
    
    todo.kanban_column = column
    todo.save()
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success'})
    
    messages.success(request, f'Todo "{todo.name}" moved to column "{column.name}".')
    return redirect('todo_app:kanban_view')

# Canvas operations
@require_POST
def update_canvas_position(request, pk):
    """Update canvas position for a todo"""
    todo = get_object_or_404(Todo, pk=pk, active=True, deleted=False)
    
    canvas_x = request.POST.get('canvas_x')
    canvas_y = request.POST.get('canvas_y')
    
    todo.canvas_x = canvas_x
    todo.canvas_y = canvas_y
    todo.save()
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success'})
    
    return redirect('todo_app:canvas_view')

# AJAX routes
@require_http_methods(["GET"])
def api_todos(request):
    """Get all todos as JSON"""
    todos = get_todos()
    
    data = [{
        'id': todo.id,
        'name': todo.name,
        'description': todo.description,
        'priority': todo.priority,
        'priority_display': todo.get_priority_display(),
        'blocked': todo.blocked,
        'done': todo.done,
        'position': todo.position,
        'parent': todo.parent.id if todo.parent else None,
        'kanban_column': todo.kanban_column.id if todo.kanban_column else None,
        'canvas_x': todo.canvas_x,
        'canvas_y': todo.canvas_y,
    } for todo in todos]
    
    return JsonResponse(data, safe=False)

@require_POST
def api_quick_add(request):
    """Quickly add a todo with minimal info"""
    name = request.POST.get('name')
    owner = request.user
    if not name:
        return JsonResponse({'status': 'error', 'message': 'Name is required'}, status=400)
    
    todo = Todo(name=name, owner=owner)
    
    # Check for optional kanban column
    kanban_column_id = request.POST.get('kanban_column', None)
    if kanban_column_id:
        try:
            kanban_column = KanbanColumn.objects.get(pk=kanban_column_id)
            todo.kanban_column = kanban_column
        except KanbanColumn.DoesNotExist:
            pass
    # In the `api_quick_add` function, add support for due_date:
    # Check for optional due date (for calendar view)
    due_date = request.POST.get('due_date', None)
    if due_date:
        try:
            todo.due_date = due_date
        except (ValueError, TypeError):
            pass
    # Check for optional MyTodos
    my_todos_id = request.POST.get('my_todos', None)
    if my_todos_id:
        try:
            my_todos = MyTodos.objects.get(pk=my_todos_id)
            todo.my_todos = my_todos
        except MyTodos.DoesNotExist:
            pass
    
    todo.save()
    
    return JsonResponse({
        'status': 'success',
        'id': todo.id,
        'name': todo.name,
        'my_todos_id': todo.my_todos.id if todo.my_todos else None,
    })

@require_POST
def api_reorder_todos(request):
    """Reorder todos based on position"""
    data = json.loads(request.body)
    todos = data.get('todos', [])
    
    for todo_data in todos:
        todo_id = todo_data.get('id')
        position = todo_data.get('position')
        
        todo = get_object_or_404(Todo, pk=todo_id, active=True, deleted=False)
        todo.position = position
        todo.save(update_fields=['position'])
    
    return JsonResponse({'status': 'success'})






# Add the calendar_view function:
@login_required
def calendar_view(request, todo_list_id=None, read_only=False):
    """Calendar view of todos (based on due dates)"""
    # If todo_list_id is provided, filter todos by that list
    if todo_list_id:
        todo_list = get_object_or_404(MyTodos, pk=todo_list_id, active=True, deleted=False)
        
        # Check if user has access to this list
        if not (todo_list.owner == request.user or todo_list.is_shared_with(request.user) or todo_list.is_public):
            messages.error(request, "You don't have permission to view this list.")
            return redirect('todo_app:my_todos_list')
        
        if todo_list.owner == request.user:
            # User's own list - show all their todos in this list
            todos = Todo.objects.filter(
                owner=request.user,
                my_todos=todo_list,
                active=True,
                deleted=False
            )
        else:
            # Shared list - show todos in this list regardless of owner
            todos = Todo.objects.filter(
                my_todos=todo_list,
                active=True,
                deleted=False
            )
            
        # Get stats for this list
        if todo_list.owner == request.user:
            stats = get_stats(request, todo_list_id=todo_list_id)
        else:
            # Custom stats calculation for shared lists
            list_todos = Todo.objects.filter(my_todos=todo_list, active=True, deleted=False)
            stats = {
                'total': list_todos.count(),
                'done': list_todos.filter(done=True).count(),
                'todo': list_todos.filter(done=False, blocked=False).count(),
                'blocked': list_todos.filter(blocked=True).count(),
                'wip': list_todos.filter(done=False, blocked=False).exclude(
                    kanban_column__column_type='todo'
                ).exclude(
                    kanban_column__column_type='done'
                ).count()
            }
    else:
        # Without todo_list_id, show all todos owned by the user
        todos = Todo.objects.filter(
            owner=request.user,
            active=True,
            deleted=False
        )
        stats = get_stats(request)
        todo_list = None
    
    # Only include todos with due dates for the calendar
    todos_with_due_date = todos.exclude(due_date__isnull=True)
    
    # Format todos for the calendar
    calendar_events = []
    for todo in todos_with_due_date:
        color = "primary"
        if todo.done:
            color = "success"
        elif todo.blocked:
            color = "danger"
        elif todo.priority == 'critical':
            color = "danger"
        elif todo.priority == 'high':
            color = "warning"
        elif todo.priority == 'medium':
            color = "info"
        elif todo.priority == 'low':
            color = "success"
        
        # Add ownership indicator for shared lists
        title = todo.name
        if todo_list and todo_list.owner != request.user and todo.owner != request.user:
            title = f"{title} (by {todo.owner.username})"
        
        calendar_events.append({
            'id': todo.id,
            'title': title,
            'start': todo.due_date.isoformat(),
            'end': (todo.due_date + timezone.timedelta(hours=1)).isoformat() if todo.due_date else None,
            'allDay': False,
            'backgroundColor': color,
            'borderColor': color,
            'textColor': 'white',
            'extendedProps': {
                'done': todo.done,
                'blocked': todo.blocked,
                'priority': todo.priority,
                'description': todo.description,
                'can_edit': todo.owner == request.user or (todo.my_todos and todo.my_todos.can_user_edit(request.user))
            }
        })
    
    # Get potential parents
    if todo_list and todo_list.owner != request.user:
        # For shared lists, only show tasks in that list as potential parents
        potential_parents = Todo.objects.filter(
            my_todos=todo_list,
            active=True,
            deleted=False
        ).exclude(done=True)
    else:
        # For user's own lists, show their tasks
        potential_parents = Todo.objects.filter(
            owner=request.user,
            active=True,
            deleted=False
        ).exclude(done=True)
        
        # If in a specific list, filter potential parents to that list
        if todo_list_id:
            potential_parents = potential_parents.filter(my_todos_id=todo_list_id)
    
    # Get all todo lists the user has access to
    own_lists = MyTodos.objects.filter(
        owner=request.user,
        active=True,
        deleted=False
    ).order_by('position')
    
    shared_lists = MyTodos.objects.filter(
        shares__shared_with=request.user,
        active=True,
        deleted=False
    )
    
    public_lists = MyTodos.objects.filter(
        is_public=True,
        active=True,
        deleted=False
    ).exclude(owner=request.user)
    
    # Combine all accessible lists
    all_todo_lists = list(own_lists)
    
    # Add shared lists with a prefix
    for shared_list in shared_lists:
        if shared_list not in all_todo_lists:  # Avoid duplicates
            shared_list.display_name = f"👥 {shared_list.name} (by {shared_list.owner.username})"
            all_todo_lists.append(shared_list)
    
    # Add public lists with a prefix
    for public_list in public_lists:
        if public_list not in all_todo_lists:  # Avoid duplicates
            public_list.display_name = f"🌐 {public_list.name} (by {public_list.owner.username})"
            all_todo_lists.append(public_list)
    
    context = {
        'todos': todos,
        'calendar_events': json.dumps(calendar_events),
        'stats': stats,
        'potential_parents': potential_parents,
        'todo_list': todo_list,
        'todo_lists': own_lists,  # Only user's lists for dropdown
        'all_todo_lists': all_todo_lists,  # All accessible lists
        'read_only': read_only,
        'is_owner': todo_list.owner == request.user if todo_list else True
    }
    
    return render(request, 'app_todos/calendar_view.html', context)

@require_http_methods(["GET"])
def api_get_stats(request):
    """Get statistics for todos"""
    list_id = request.GET.get('list_id', None)
    stats = get_stats(request, todo_list_id=list_id)
    
    return JsonResponse(stats)

@require_POST
def api_reorder_columns(request):
    """Reorder kanban columns"""
    data = json.loads(request.body)
    columns = data.get('columns', [])
    
    for column_data in columns:
        column_id = column_data.get('id')
        position = column_data.get('position')
        
        column = get_object_or_404(KanbanColumn, pk=column_id)
        column.position = position
        column.save(update_fields=['position'])
    
    return JsonResponse({'status': 'success'})

@login_required
def trash_view(request):
    """View deleted todos"""
    # Get soft deleted todos owned by the user
    deleted_todos = Todo.objects.filter(owner=request.user, deleted=True).order_by('-updated_at')
    
    # Get all todo lists for tabs
    all_todo_lists = MyTodos.objects.filter(owner=request.user, active=True, deleted=False).order_by('position')
    
    context = {
        'deleted_todos': deleted_todos,
        'all_todo_lists': all_todo_lists,
    }
    
    return render(request, 'app_todos/trash_view.html', context)




# Add these functions to your views.py file

@require_POST
def my_todos_bulk_delete(request):
    """Soft delete multiple todo lists at once"""
    try:
        ids = json.loads(request.POST.get('ids', '[]'))
        if not ids:
            return JsonResponse({'status': 'error', 'message': 'No IDs provided'}, status=400)
        
        # Soft delete all lists in one operation
        count = 0
        for list_id in ids:
            try:
                todo_list = MyTodos.objects.get(pk=list_id, active=True, deleted=False)
                todo_list.soft_delete()
                count += 1
            except MyTodos.DoesNotExist:
                continue
        
        messages.success(request, f'{count} todo lists moved to trash.')
        return redirect('todo_app:my_todos_list')
    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
        return redirect('todo_app:my_todos_list')

@require_POST
def my_todos_bulk_restore(request):
    """Restore multiple deleted todo lists at once"""
    try:
        ids = json.loads(request.POST.get('ids', '[]'))
        if not ids:
            return JsonResponse({'status': 'error', 'message': 'No IDs provided'}, status=400)
        
        # Restore all lists in one operation
        count = 0
        for list_id in ids:
            try:
                todo_list = MyTodos.objects.get(pk=list_id, deleted=True)
                todo_list.restore()
                count += 1
            except MyTodos.DoesNotExist:
                continue
        
        messages.success(request, f'{count} todo lists restored.')
        return redirect('todo_app:my_todos_trash')
    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
        return redirect('todo_app:my_todos_trash')

@require_POST
def my_todos_bulk_permanent_delete(request):
    """Permanently delete multiple todo lists at once"""
    try:
        ids = json.loads(request.POST.get('ids', '[]'))
        if not ids:
            return JsonResponse({'status': 'error', 'message': 'No IDs provided'}, status=400)
        
        # Permanently delete all lists
        count = 0
        for list_id in ids:
            try:
                todo_list = MyTodos.objects.get(pk=list_id, deleted=True)
                todo_list.delete()
                count += 1
            except MyTodos.DoesNotExist:
                continue
        
        messages.success(request, f'{count} todo lists permanently deleted.')
        return redirect('todo_app:my_todos_trash')
    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
        return redirect('todo_app:my_todos_trash')

@require_POST
def my_todos_empty_trash(request):
    """Permanently delete all todo lists in trash"""
    count = MyTodos.objects.filter(deleted=True).count()
    MyTodos.objects.filter(deleted=True).delete()
    
    messages.success(request, f'Trash emptied. {count} lists permanently deleted.')
    return redirect('todo_app:my_todos_trash')

@require_POST
def my_todos_copy(request, pk):
    """Create a copy of an existing todo list"""
    original_list = get_object_or_404(MyTodos, pk=pk, active=True, deleted=False)
    max_position = MyTodos.objects.aggregate(Max('position'))['position__max']
    position = (max_position or 0) + 1
    # Create a copy with "(Copy)" added to the name
    new_list = MyTodos(
        name=f"{original_list.name} (Copy)",
        description=original_list.description,
        icon=original_list.icon,
        color=original_list.color,
        # Get the highest position and add 1
        position=position,
        owner=original_list.owner,
    )
    new_list.save()
    
    # If AJAX request
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'status': 'success', 'id': new_list.id})
    
    messages.success(request, f'Todo list "{original_list.name}" has been copied.')
    return redirect('todo_app:my_todos_list')

# list search
def search_lists(request):
    """Search for todo lists"""
    query = request.GET.get('q', '').strip()
    results = []
    
    if query:
        # Search in the database
        lists = MyTodos.objects.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query),
            active=True, 
            deleted=False
        ).order_by('position')
        
        # Format results
        results = [
            {
                'id': list_obj.id,
                'name': list_obj.name,
                'description': list_obj.description,
                'icon': list_obj.icon,
                'color': list_obj.color,
                'todo_count': list_obj.todo_count(),
                'done_count': list_obj.done_count()
            }
            for list_obj in lists
        ]
    
    return JsonResponse({'results': results})

# global search
def global_search(request):
    """Global search for both lists and todos"""
    query = request.GET.get('q', '').strip()
    results = {
        'lists': [],
        'todos': []
    }
    
    if query:
        # Search in todo lists
        lists = MyTodos.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query),
            active=True, 
            deleted=False
        ).order_by('position')
        
        # Format list results
        results['lists'] = [
            {
                'id': list_obj.id,
                'name': list_obj.name,
                'description': list_obj.description,
                'icon': list_obj.icon,
                'color': list_obj.color,
                'todo_count': list_obj.todo_count(),
                'done_count': list_obj.done_count()
            }
            for list_obj in lists
        ]
        
        # Search in todos
        todos = Todo.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query),
            active=True, 
            deleted=False
        ).order_by('-updated_at')[:20]  # Limit to 20 recent results
        
        # Format todo results
        results['todos'] = [
            {
                'id': todo.id,
                'name': todo.name,
                'description': todo.description if todo.description else '',
                'priority': todo.priority,
                'list_id': todo.my_todos_id,
                'list_name': todo.my_todos.name if todo.my_todos else 'No List',
                'done': todo.done,
                'blocked': todo.blocked
            }
            for todo in todos
        ]
    
    return JsonResponse(results)

# list level delete restore permanent delete
def list_trash_view(request, list_id):
    """View deleted todos for a specific list"""
    todo_list = get_object_or_404(MyTodos, pk=list_id)
    
    # Get deleted todos for this list
    deleted_todos = Todo.objects.filter(
        my_todos=todo_list,
        deleted=True
    ).order_by('-updated_at')
    
    # Get all todo lists for tabs
    all_todo_lists = MyTodos.objects.filter(active=True, deleted=False).order_by('position')
    
    context = {
        'deleted_todos': deleted_todos,
        'todo_list': todo_list,
        'all_todo_lists': all_todo_lists,
    }
    
    return render(request, 'app_todos/list_trash_view.html', context)

@require_POST
def list_bulk_restore(request, list_id):
    """Restore multiple deleted todos for a specific list"""
    try:
        ids = json.loads(request.POST.get('ids', '[]'))
        if not ids:
            return JsonResponse({'status': 'error', 'message': 'No IDs provided'}, status=400)
        
        # Update all todos in one query
        Todo.objects.filter(
            pk__in=ids, 
            deleted=True,
            my_todos_id=list_id
        ).update(
            deleted=False, 
            active=True
        )
        
        return JsonResponse({'status': 'success', 'count': len(ids)})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@require_POST
def list_bulk_permanent_delete(request, list_id):
    """Permanently delete multiple todos from a specific list's trash"""
    try:
        ids = json.loads(request.POST.get('ids', '[]'))
        if not ids:
            return JsonResponse({'status': 'error', 'message': 'No IDs provided'}, status=400)
        
        # Delete all todos in one query
        count = Todo.objects.filter(
            pk__in=ids, 
            deleted=True,
            my_todos_id=list_id
        ).delete()[0]
        
        return JsonResponse({'status': 'success', 'count': count})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    
def insights_viewa1(request):
    """Show insights and analytics for todo lists"""
    # Get all active lists
    all_lists = MyTodos.objects.filter(active=True, deleted=False, owner=request.user).order_by('position')
    
    # Collect stats for each list
    list_stats = []
    for todo_list in all_lists:
        todos = Todo.objects.filter(my_todos=todo_list, active=True, deleted=False, owner=request.user)
        list_stats.append({
            'id': todo_list.id,
            'name': todo_list.name,
            'icon': todo_list.icon,
            'color': todo_list.color,
            'total': todos.count(),
            'done': todos.filter(done=True).count(),
            'todo': todos.filter(done=False, blocked=False).count(),
            'blocked': todos.filter(blocked=True).count(),
            'completion_rate': round(todos.filter(done=True).count() / todos.count() * 100 if todos.count() > 0 else 0, 1),
            'recently_completed': todos.filter(done=True).order_by('-done_at')[:5],
            'overdue': todos.filter(due_date__lt=timezone.now(), done=False).count(),
            'due_soon': todos.filter(due_date__gte=timezone.now(), 
                                    due_date__lte=timezone.now() + timezone.timedelta(days=3), 
                                    done=False).count()
        })
    
    # Calculate overall stats
    all_todos = Todo.objects.filter(active=True, deleted=False, owner=request.user) 
    overall_stats = {
        'total': all_todos.count(),
        'done': all_todos.filter(done=True).count(),
        'todo': all_todos.filter(done=False, blocked=False).count(),
        'blocked': all_todos.filter(blocked=True).count(),
        'completion_rate': round(all_todos.filter(done=True).count() / all_todos.count() * 100 if all_todos.count() > 0 else 0, 1),
        'critical': all_todos.filter(priority='critical', done=False).count(),
        'high': all_todos.filter(priority='high', done=False).count(),
        'overdue': all_todos.filter(due_date__lt=timezone.now(), done=False).count(),
        'due_soon': all_todos.filter(due_date__gte=timezone.now(), 
                                   due_date__lte=timezone.now() + timezone.timedelta(days=3), 
                                   done=False).count()
    }
    
    # Get recently completed todos
    recently_completed = all_todos.filter(done=True).order_by('-done_at')[:10]
    
    # Get todos due soon
    due_soon_todos = all_todos.filter(
        due_date__gte=timezone.now(), 
        due_date__lte=timezone.now() + timezone.timedelta(days=3), 
        done=False
    ).order_by('due_date')[:10]
    
    # Get overdue todos
    overdue_todos = all_todos.filter(
        due_date__lt=timezone.now(), 
        done=False
    ).order_by('due_date')[:10]
    
    context = {
        'list_stats': list_stats,
        'overall_stats': overall_stats,
        'recently_completed': recently_completed,
        'due_soon_todos': due_soon_todos,
        'overdue_todos': overdue_todos,
        'all_todo_lists': all_lists,
    }
    
    return render(request, 'app_todos/insights.html', context)
def insights_view(request):
    """Show insights and analytics for todo lists"""
    # Get all active lists (both owned and shared with edit permission)
    own_lists = MyTodos.objects.filter(active=True, deleted=False, owner=request.user).order_by('position')
    shared_lists = MyTodos.objects.filter(
        shares__shared_with=request.user, 
        shares__can_edit=True,
        active=True, 
        deleted=False
    ).exclude(owner=request.user)
    
    # Combine all lists
    all_lists = list(own_lists) + list(shared_lists)
    
    # Collect stats for each list
    list_stats = []
    for todo_list in all_lists:
        # Get todos for this list - use direct query rather than related name
        todos = Todo.objects.filter(my_todos=todo_list, active=True, deleted=False)
        
        # Get user contribution stats for this list
        user_todos = todos.filter(owner=request.user)
        user_contribution = user_todos.count()
        total_list_items = todos.count()
        
        # Calculate contribution percentage only if there are items
        if total_list_items > 0:
            contribution_percentage = round((user_contribution / total_list_items * 100), 1)
        else:
            contribution_percentage = 0
        
        # Get all contributors to this list using a direct query
        contributors = User.objects.filter(
            todos__my_todos=todo_list,
            todos__active=True,
            todos__deleted=False
        ).distinct()
        
        contributor_stats = []
        for contributor in contributors:
            contributor_todos = todos.filter(owner=contributor)
            contributor_done = contributor_todos.filter(done=True).count()
            contributor_total = contributor_todos.count()
            
            # Calculate contributor percentage
            if total_list_items > 0:
                contributor_percentage = round((contributor_total / total_list_items * 100), 1)
            else:
                contributor_percentage = 0
                
            contributor_stats.append({
                'username': contributor.username,
                'is_current_user': contributor == request.user,
                'total': contributor_total,
                'done': contributor_done,
                'percentage': contributor_percentage
            })
        
        # Sort contributors by contribution percentage (highest first)
        contributor_stats.sort(key=lambda x: x['percentage'], reverse=True)
        
        list_stats.append({
            'id': todo_list.id,
            'name': todo_list.name,
            'icon': todo_list.icon,
            'color': todo_list.color,
            'is_shared': todo_list.owner != request.user,
            'owner_username': todo_list.owner.username,
            'total': total_list_items,
            'done': todos.filter(done=True).count(),
            'todo': todos.filter(done=False, blocked=False).count(),
            'blocked': todos.filter(blocked=True).count(),
            'completion_rate': round(todos.filter(done=True).count() / total_list_items * 100 if total_list_items > 0 else 0, 1),
            'user_contribution': user_contribution,
            'contribution_percentage': contribution_percentage,
            'contributors': contributor_stats,
            'recently_completed': todos.filter(done=True).order_by('-done_at')[:5],
            'overdue': todos.filter(due_date__lt=timezone.now(), done=False).count(),
            'due_soon': todos.filter(due_date__gte=timezone.now(), 
                                   due_date__lte=timezone.now() + timezone.timedelta(days=3), 
                                   done=False).count()
        })
    
    # Calculate overall stats with direct queries
    user_owned_todos = Todo.objects.filter(owner=request.user, active=True, deleted=False)
    shared_list_todos = Todo.objects.filter(
        my_todos__shares__shared_with=request.user,
        active=True, 
        deleted=False
    )
    
    # Combine distinct todos
    all_todos = (user_owned_todos | shared_list_todos).distinct()
    total_todos = all_todos.count()
    
    # Calculate overall stats safely
    overall_stats = {
        'total': total_todos,
        'done': all_todos.filter(done=True).count(),
        'todo': all_todos.filter(done=False, blocked=False).count(),
        'blocked': all_todos.filter(blocked=True).count(),
        'completion_rate': round(all_todos.filter(done=True).count() / total_todos * 100 if total_todos > 0 else 0, 1),
        'critical': all_todos.filter(priority='critical', done=False).count(),
        'high': all_todos.filter(priority='high', done=False).count(),
        'overdue': all_todos.filter(due_date__lt=timezone.now(), done=False).count(),
        'due_soon': all_todos.filter(due_date__gte=timezone.now(), 
                                   due_date__lte=timezone.now() + timezone.timedelta(days=3), 
                                   done=False).count()
    }
    
    # Get recently completed todos
    recently_completed = all_todos.filter(done=True).order_by('-done_at')[:10]
    
    # Get todos due soon
    due_soon_todos = all_todos.filter(
        due_date__gte=timezone.now(), 
        due_date__lte=timezone.now() + timezone.timedelta(days=3), 
        done=False
    ).order_by('due_date')[:10]
    
    # Get overdue todos
    overdue_todos = all_todos.filter(
        due_date__lt=timezone.now(), 
        done=False
    ).order_by('due_date')[:10]
    
    context = {
        'list_stats': list_stats,
        'overall_stats': overall_stats,
        'recently_completed': recently_completed,
        'due_soon_todos': due_soon_todos,
        'overdue_todos': overdue_todos,
        'all_todo_lists': all_lists,
    }
    
    return render(request, 'app_todos/insights.html', context)


@login_required
def shared_with_me(request):
    """View lists shared with the current user"""
    shares = TodoShare.objects.filter(shared_with=request.user).select_related('todo_list')
    todo_lists = MyTodos.objects.filter(owner=request.user, active=True, deleted=False)
    my_lists = MyTodos.objects.filter(owner=request.user, active=True, deleted=False)
    context = {
        'shares': shares,
        'todo_lists': todo_lists,
        'all_todo_lists': todo_lists,
        'my_lists': my_lists,
    }
    
    return render(request, 'app_todos/shared_with_me.html', context)


def custom_logout(request):
    logout(request)
    return redirect('todo_app:login')

@login_required
def account_profile(request):
    user = request.user
    
    # Create profile if it doesn't exist
    if not hasattr(user, 'account_profile'):
        account_profile = AccountProfile.objects.create(user=user)
    else:
        account_profile = user.account_profile
    
    if request.method == 'POST':
        # Update user information
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        
        # Update profile information
        account_profile.bio = request.POST.get('bio', '')
        account_profile.website = request.POST.get('website', '')
        
        # Handle profile picture upload
        if 'profile_picture' in request.FILES:
            account_profile.profile_picture = request.FILES['profile_picture']
        
        # Handle password change
        current_password = request.POST.get('current_password', '')
        new_password = request.POST.get('new_password', '')
        confirm_password = request.POST.get('confirm_password', '')
        
        if current_password and new_password and confirm_password:
            if new_password == confirm_password:
                # Verify current password
                if user.check_password(current_password):
                    user.set_password(new_password)
                    messages.success(request, 'Password updated successfully!')
                else:
                    messages.error(request, 'Current password is incorrect.')
            else:
                messages.error(request, 'New passwords do not match.')
        
        # Save changes
        user.save()
        account_profile.save()
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('todo_app:account_profile')
    todo_lists = MyTodos.objects.filter(owner=request.user, active=True, deleted=False)
    context = {
        'user': user,
        'account_profile': account_profile,
        'all_todo_lists': todo_lists,
    }
    return render(request, 'app_todos/account_profile.html', context)

@login_required
def user_stats(request):
    user = request.user
    
    # Get counts of tasks
    total_tasks = Todo.objects.filter(owner=user, active=True).count()
    completed_tasks = Todo.objects.filter(owner=user, active=True, done=True).count()
    
    # Return as JSON
    return JsonResponse({
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks
    })


@login_required
def toggle_public(request, pk):
    """Toggle public/private status of a todo list"""
    todo_list = get_object_or_404(MyTodos, pk=pk, owner=request.user, active=True, deleted=False)
    
    if request.method == 'POST':
        todo_list.is_public = not todo_list.is_public
        todo_list.save()
        
        if todo_list.is_public:
            messages.success(request, f"List '{todo_list.name}' is now public.")
        else:
            messages.success(request, f"List '{todo_list.name}' is now private.")
    
    return redirect('todo_app:share_todo_list', pk=pk)

@login_required
def share_todo_list(request, pk):
    """Share a todo list with another user"""
    todo_list = get_object_or_404(MyTodos, pk=pk, owner=request.user, active=True, deleted=False)
    
    if request.method == 'POST':
        # Get username or email to share with
        shared_with_username = request.POST.get('username', '').strip()
        can_edit = request.POST.get('can_edit', False) == 'on'
        
        try:
            # Find the user to share with
            
            shared_with = User.objects.get(username=shared_with_username)
            
            # Don't share with yourself
            if shared_with == request.user:
                messages.error(request, "You can't share a list with yourself.")
                return redirect('todo_app:share_todo_list', pk=pk)
            
            # Create share record (or update if already exists)
            share, created = TodoShare.objects.update_or_create(
                todo_list=todo_list,
                shared_with=shared_with,
                defaults={
                    'shared_by': request.user,
                    'can_edit': can_edit
                }
            )
            
            if created:
                messages.success(request, f"List shared with {shared_with.username}.")
            else:
                messages.success(request, f"Share permissions updated for {shared_with.username}.")
            
            return redirect('todo_app:share_todo_list', pk=pk)
            
        except User.DoesNotExist:
            messages.error(request, f"User '{shared_with_username}' not found.")
            return redirect('todo_app:share_todo_list', pk=pk)
    
    # GET request - show sharing form
    current_shares = TodoShare.objects.filter(todo_list=todo_list).select_related('shared_with')
    
    context = {
        'todo_list': todo_list,
        'current_shares': current_shares,
        'all_todo_lists': MyTodos.objects.filter(owner=request.user, active=True, deleted=False)
    }
    
    return render(request, 'app_todos/share_todo_list.html', context)


@login_required
def remove_share(request, pk, user_id):
    """Remove a share for a todo list"""
    # Ensure the user is the owner of the list
    todo_list = get_object_or_404(MyTodos, pk=pk, owner=request.user, active=True, deleted=False)
    
    if request.method == 'POST':
        # Find the share
        share = get_object_or_404(TodoShare, todo_list=todo_list, shared_with_id=user_id)
        username = share.shared_with.username
        share.delete()
        
        messages.success(request, f"List is no longer shared with {username}.")
    
    return redirect('todo_app:share_todo_list', pk=pk)