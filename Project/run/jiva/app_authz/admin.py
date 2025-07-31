from django.contrib import admin
from app_memberprofilerole.mod_profile.models_profile import Member, MemberOrganizationRole

class MemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'org', 'active', 'deleted', 'created_at', 'updated_at')
    list_filter = ('active', 'deleted', 'org')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name', 'org__name')
    readonly_fields = ('created_at', 'updated_at')
    raw_id_fields = ('user', 'org', 'author')
    fieldsets = (
        (None, {
            'fields': ('user', 'org', 'description')
        }),
        ('Status', {
            'fields': ('active', 'deleted', 'blocked', 'blocked_count', 'done', 'done_at', 'approved')
        }),
        ('Metadata', {
            'fields': ('author', 'created_at', 'updated_at', 'completed_at', 'position')
        }),
    )

class MemberOrganizationRoleAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'member', 'org', 'role', 'active', 'created_at', 'updated_at')
    list_filter = ('active', 'role', 'org')
    search_fields = ('member__user__username', 'member__user__email', 'org__name', 'role__name')
    readonly_fields = ('created_at', 'updated_at')
    raw_id_fields = ('member', 'org', 'role', 'author')
    fieldsets = (
        (None, {
            'fields': ('member', 'org', 'role')
        }),
        ('Status', {
            'fields': ('active', 'deleted', 'blocked', 'blocked_count', 'done', 'done_at', 'approved')
        }),
        ('Metadata', {
            'fields': ('author', 'created_at', 'updated_at', 'completed_at', 'position')
        }),
    )

# Register models with the custom admin classes
admin.site.register(Member, MemberAdmin)
admin.site.register(MemberOrganizationRole, MemberOrganizationRoleAdmin)