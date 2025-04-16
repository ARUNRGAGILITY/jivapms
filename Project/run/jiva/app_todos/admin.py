from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from .models import Todo, KanbanColumn, MyTodos

@admin.register(Todo)
class TodoAdmin(DraggableMPTTAdmin):
    list_display = (
        'tree_actions', 
        'indented_title',
        'name', 
        'priority', 
        'done', 
        'blocked',
        'created_at',
        'updated_at'
    )
    list_filter = ('priority', 'done', 'blocked', 'active', 'deleted')
    search_fields = ('name', 'description')
    actions = ['mark_as_done', 'mark_as_undone', 'mark_as_blocked', 'mark_as_unblocked']
    
    def indented_title(self, instance):
        return instance.name
    indented_title.short_description = 'Name'
    
    def mark_as_done(self, request, queryset):
        for obj in queryset:
            obj.mark_done()
        self.message_user(request, f"{queryset.count()} todos marked as done.")
    mark_as_done.short_description = "Mark selected todos as done"
    
    def mark_as_undone(self, request, queryset):
        queryset.update(done=False, done_at=None)
        self.message_user(request, f"{queryset.count()} todos marked as not done.")
    mark_as_undone.short_description = "Mark selected todos as not done"
    
    def mark_as_blocked(self, request, queryset):
        for obj in queryset:
            obj.block()
        self.message_user(request, f"{queryset.count()} todos marked as blocked.")
    mark_as_blocked.short_description = "Mark selected todos as blocked"
    
    def mark_as_unblocked(self, request, queryset):
        for obj in queryset:
            obj.unblock()
        self.message_user(request, f"{queryset.count()} todos marked as unblocked.")
    mark_as_unblocked.short_description = "Mark selected todos as unblocked"

@admin.register(KanbanColumn)
class KanbanColumnAdmin(admin.ModelAdmin):
    list_display = ('name', 'wip_limit', 'is_default', 'column_type', 'position', 'todo_count')
    list_filter = ('is_default', 'column_type')
    search_fields = ('name', 'description')
    ordering = ('position',)
    
    def todo_count(self, obj):
        return obj.todo_count()
    todo_count.short_description = 'Number of Todos'

@admin.register(MyTodos)
class MyTodosAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon', 'color', 'position', 'todo_count', 'done_count', 'active', 'deleted')
    list_filter = ('active', 'deleted')
    search_fields = ('name', 'description')
    ordering = ('position',)
    
    def todo_count(self, obj):
        return obj.todo_count()
    todo_count.short_description = 'Total Todos'
    
    def done_count(self, obj):
        return obj.done_count()
    done_count.short_description = 'Completed Todos'