from app_organization.mod_project_board_cos.models_project_board_cos import *
from app_organization.mod_project_board.models_project_board import *
from app_organization.mod_project.models_project import *
from django.shortcuts import render, redirect, get_object_or_404

module_path = 'mod_project_board_cos'


def _get_selected_board(project):
    board = ProjectBoard.objects.filter(project=project, default_board=True, active=True).first()
    if not board:
        board, _ = ProjectBoard.objects.get_or_create(
            project=project, name='Default Board', defaults={'description': 'Auto-created default board', 'default_board': True}
        )
    return board


def list_project_board_cos(request, project_id):
    project = get_object_or_404(Project, pk=project_id, active=True)
    board = _get_selected_board(project)
    objects = ProjectBoardClassOfService.objects.filter(board=board, active=True).order_by('position', 'name')
    context = {
        'objects_count': objects.count(),
        'page_obj': objects,  # reuse the same template pattern
        'project_id': project.id,
        'project': project,
    }
    return render(request, f"app_organization/{module_path}/list_project_board_cos.html", context)


def list_deleted_project_board_cos(request, project_id):
    project = get_object_or_404(Project, pk=project_id, active=True)
    board = _get_selected_board(project)
    objects = ProjectBoardClassOfService.objects.filter(board=board, active=False, deleted=False).order_by('position', 'name')
    context = {
        'objects_count': objects.count(),
        'page_obj': objects,
        'project_id': project.id,
        'project': project,
    }
    return render(request, f"app_organization/{module_path}/list_deleted_project_board_cos.html", context)


def create_project_board_cos(request, project_id):
    project = get_object_or_404(Project, pk=project_id, active=True)
    board = _get_selected_board(project)
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        color = request.POST.get('color', '').strip()
        ProjectBoardClassOfService.objects.create(board=board, name=name or None, color=color or None)
        return redirect('list_project_board_cos', project_id=project.id)
    return render(request, f"app_organization/{module_path}/create_project_board_cos.html", {'project_id': project.id, 'project': project})


def edit_project_board_cos(request, project_id, cos_id):
    project = get_object_or_404(Project, pk=project_id, active=True)
    obj = get_object_or_404(ProjectBoardClassOfService, pk=cos_id)
    if request.method == 'POST':
        obj.name = request.POST.get('name', '').strip() or obj.name
        obj.color = request.POST.get('color', '').strip() or obj.color
        obj.save()
        return redirect('list_project_board_cos', project_id=project.id)
    return render(request, f"app_organization/{module_path}/edit_project_board_cos.html", {'project_id': project.id, 'object': obj, 'project': project})


def delete_project_board_cos(request, project_id, cos_id):
    obj = get_object_or_404(ProjectBoardClassOfService, pk=cos_id)
    obj.active = False
    obj.save()
    return redirect('list_project_board_cos', project_id=project_id)


def permanent_deletion_project_board_cos(request, project_id, cos_id):
    obj = get_object_or_404(ProjectBoardClassOfService, pk=cos_id)
    obj.deleted = True
    obj.save()
    return redirect('list_deleted_project_board_cos', project_id=project_id)


def view_project_board_cos(request, project_id, cos_id):
    project = get_object_or_404(Project, pk=project_id, active=True)
    obj = get_object_or_404(ProjectBoardClassOfService, pk=cos_id)
    return render(request, f"app_organization/{module_path}/view_project_board_cos.html", {'project_id': project.id, 'object': obj, 'project': project})
