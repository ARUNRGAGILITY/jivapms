
from app_org_blog.mod_app.all_view_imports import *
from app_org_blog.mod_blog.models_blog import *
from app_org_blog.mod_blog.forms_blog import *

from app_organization.mod_organization.models_organization import *
from app_memberprofilerole.mod_member.models_member import Member, MemberOrganizationRole

from app_common.mod_common.models_common import *
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Count, Q
from django.utils import timezone
from django.utils.text import slugify
from datetime import timedelta
import json
from django.http import JsonResponse

app_name = 'app_org_blog'
app_version = 'v1'

module_name = 'blogs'
module_path = f'mod_blog'

# viewable flag
first_viewable_flag = '__ALL__'  # 'all' or '__OWN__'
viewable_flag = '__ALL__'  # 'all' or '__OWN__'
# Setup dictionaries based on flags
viewable_dict = {} if viewable_flag == '__ALL__' else {'author': user}
first_viewable_dict = {} if first_viewable_flag == '__ALL__' else {'author': user}
def get_viewable_dicts(user, viewable_flag, first_viewable_flag):
    viewable_dict = {} if viewable_flag == '__ALL__' else {'author': user}
    first_viewable_dict = {} if first_viewable_flag == '__ALL__' else {'author': user}
    return viewable_dict, first_viewable_dict

# Custom permission checks
def is_blog_admin(user, blog=None, organization=None):
    """Check if the user is a blog admin for the given blog or organization"""
    if user.is_superuser:
        return True
    
    try:
        member = Member.objects.get(user=user, active=True)
        
        # Check organization-level blog admin
        if organization:
            org_admin_role = MemberOrganizationRole.objects.filter(
                member=member,
                org=organization,
                role__name='Org Admin',  # Using the Org Admin role since we don't have a specific Blog Admin role at org level
                active=True
            ).exists()
            
            if org_admin_role:
                return True
        
        # Check blog-specific admin
        if blog:
            blog_admin = BlogMember.objects.filter(
                blog=blog,
                member=member,
                role='admin',
                active=True
            ).exists()
            
            if blog_admin:
                return True
    
    except (Member.DoesNotExist, MemberOrganizationRole.DoesNotExist):
        pass
    
    return False

def is_blog_writer(user, blog=None):
    """Check if the user is a writer for the given blog"""
    if user.is_superuser or is_blog_admin(user, blog):
        return True
    
    try:
        member = Member.objects.get(user=user, active=True)
        
        # Check blog-specific writer
        if blog:
            blog_writer = BlogMember.objects.filter(
                blog=blog,
                member=member,
                role__in=['writer', 'editor'],  # Both writers and editors can create content
                active=True
            ).exists()
            
            if blog_writer:
                return True
    
    except Member.DoesNotExist:
        pass
    
    return False
# ============================================================= #
@login_required
def list_blogs(request, organization_id):
    # take inputs
    # process inputs
    user = request.user       
    objects_count = 0    
    show_all = request.GET.get('all', '25')
    objects_per_page = int(show_all) if show_all != 'all' else 25
    pagination_options = [5, 10, 15, 25, 50, 100, 'all']
    selected_bulk_operations = None
    deleted_count = 0
    organization = Organization.objects.get(id=organization_id, active=True, 
                                                **first_viewable_dict)
    
    search_query = request.GET.get('search', '')
    if search_query:
        tobjects = Blog.objects.filter(name__icontains=search_query, 
                                            organization_id=organization_id, **viewable_dict).order_by('position')
    else:
        tobjects = Blog.objects.filter(active=True, organization_id=organization_id).order_by('position')
        deleted = Blog.objects.filter(active=False, deleted=False,
                                organization_id=organization_id,
                               **viewable_dict).order_by('position')
        deleted_count = deleted.count()
    blogs = Blog.objects.filter(active=True, organization_id=organization_id)
    print(f">>> === BLOGS: {blogs} === <<<")
    if show_all == 'all':
        # No pagination, show all records
        page_obj = tobjects
        objects_per_page = tobjects.count()
    else:
        objects_per_page = int(show_all)     
        paginator = Paginator(tobjects, objects_per_page)  
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    
    objects_count = tobjects.count()
    
    
    ## processing the POST
    if request.method == 'POST':
        selected_bulk_operations = request.POST.getlist('bulk_operations')
        bulk_operation = str(selected_bulk_operations[0].strip()) if selected_bulk_operations else None
             
        if 'selected_item' in request.POST:  # Correct the typo here
            selected_items = request.POST.getlist('selected_item')  # Use getlist to ensure all are captured
            for item_id in selected_items:
                item = int(item_id)  # Ensure item_id is converted to int if necessary
                if bulk_operation == 'bulk_delete':
                    object = get_object_or_404(Blog, pk=item, active=True, **viewable_dict)
                    object.active = False
                    object.save()
                    
                elif bulk_operation == 'bulk_done':
                    object = get_object_or_404(Blog, pk=item, active=True, **viewable_dict)
                    object.done = True
                    object.save()
                    
                elif bulk_operation == 'bulk_not_done':
                    object = get_object_or_404(Blog, pk=item, active=True, **viewable_dict)
                    object.done = False
                    object.save()
                    
                elif bulk_operation == 'bulk_blocked':  # Correct the operation check here
                    object = get_object_or_404(Blog, pk=item, active=True, **viewable_dict)
                    object.blocked = True
                    object.save()
                    
                else:
                    redirect('list_blogs', organization_id=organization_id)
            return redirect('list_blogs', organization_id=organization_id)
    
    # send outputs info, template,
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'list_blogs',
        'organization': organization,
        'organization_id': organization_id,
        
        'module_path': module_path,
        'user': user,
        'tobjects': tobjects,
        'page_obj': page_obj,
        'objects_count': objects_count,
        'objects_per_page': objects_per_page,
        'deleted_count': deleted_count,
        'show_all': show_all,
        
        'pagination_options': pagination_options,
        'selected_bulk_operations': selected_bulk_operations,
        'page_title': f'Blog List',
    }       
    template_file = f"{app_name}/{module_path}/list_blogs.html"
    return render(request, template_file, context)





# ============================================================= #
@login_required
def list_deleted_blogs(request, organization_id):
    # take inputs
    # process inputs
    user = request.user       
    objects_count = 0    
    show_all = request.GET.get('all', '25')
    objects_per_page = int(show_all) if show_all != 'all' else 25
    pagination_options = [5, 10, 15, 25, 50, 100, 'all']
    selected_bulk_operations = None
    organization = Organization.objects.get(id=organization_id, active=True, 
                                                **first_viewable_dict)
    
    search_query = request.GET.get('search', '')
    if search_query:
        tobjects = Blog.objects.filter(name__icontains=search_query, 
                                            active=False, deleted=False,
                                            organization_id=organization_id, **viewable_dict).order_by('position')
    else:
        tobjects = Blog.objects.filter(active=False, deleted=False, organization_id=organization_id,
                                            **viewable_dict).order_by('position')        
    
    if show_all == 'all':
        # No pagination, show all records
        page_obj = tobjects
        objects_per_page = tobjects.count()
    else:
        objects_per_page = int(show_all)     
        paginator = Paginator(tobjects, objects_per_page)  
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    objects_count = tobjects.count()
    
    ## processing the POST
    if request.method == 'POST':
        selected_bulk_operations = request.POST.getlist('bulk_operations')
        bulk_operation = str(selected_bulk_operations[0].strip()) if selected_bulk_operations else None
     
        if 'selected_item' in request.POST:  # Correct the typo here
                selected_items = request.POST.getlist('selected_item')  # Use getlist to ensure all are captured
                for item_id in selected_items:
                    item = int(item_id)  # Ensure item_id is converted to int if necessary
                    if bulk_operation == 'bulk_restore':
                        object = get_object_or_404(Blog, pk=item, active=False, **viewable_dict)
                        object.active = True
                        object.save()         
                    elif bulk_operation == 'bulk_erase':
                        object = get_object_or_404(Blog, pk=item, active=False, **viewable_dict)
                        object.active = False  
                        object.deleted = True             
                        object.save()    
                    else:
                        redirect('list_blogs', organization_id=organization_id)
                redirect('list_blogs', organization_id=organization_id)
    
    # send outputs info, template,
    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'list_deleted_blogs',
        'organization': organization,
        'organization_id': organization_id,
        
        'module_path': module_path,
        'user': user,
        'tobjects': tobjects,
        'page_obj': page_obj,
        'objects_count': objects_count,
        'objects_per_page': objects_per_page,
        'show_all': show_all,
        'pagination_options': pagination_options,
        'selected_bulk_operations': selected_bulk_operations,
        'page_title': f'Blog List',
    }       
    template_file = f"{app_name}/{module_path}/list_deleted_blogs.html"
    return render(request, template_file, context)



# Create View
@login_required
def create_blog(request, organization_id):
    user = request.user
    organization = Organization.objects.get(id=organization_id, active=True, 
                                                **first_viewable_dict)
    
    if request.method == 'POST':
        form = BlogForm(request.POST)
        if form.is_valid():
            form.instance.author = user
            form.instance.organization_id = organization_id
            form.save()
        else:
            print(f">>> === form.errors: {form.errors} === <<<")
        return redirect('list_blogs', organization_id=organization_id)
    else:
        form = BlogForm()

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'create_blog',
        'organization': organization,
        'organization_id': organization_id,
        
        'module_path': module_path,
        'form': form,
        'page_title': f'Create Blog',
    }
    template_file = f"{app_name}/{module_path}/create_blog.html"
    return render(request, template_file, context)




# Edit
@login_required
def edit_blog(request, organization_id, blog_id):
    user = request.user
    organization = Organization.objects.get(id=organization_id, active=True, 
                                                **first_viewable_dict)
    
    object = get_object_or_404(Blog, pk=blog_id, active=True,**viewable_dict)
    if request.method == 'POST':
        form = BlogForm(request.POST, instance=object)
        if form.is_valid():
            form.instance.author = user
            form.instance.organization_id = organization_id
            form.save()
        else:
            print(f">>> === form.errors: {form.errors} === <<<")
        return redirect('list_blogs', organization_id=organization_id)
    else:
        form = BlogForm(instance=object)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'edit_blog',
        'organization': organization,
        'organization_id': organization_id,
        
        'module_path': module_path,
        'form': form,
        'object': object,
        'page_title': f'Edit Blog',
    }
    template_file = f"{app_name}/{module_path}/edit_blog.html"
    return render(request, template_file, context)



@login_required
def delete_blog(request, organization_id, blog_id):
    user = request.user
    organization = Organization.objects.get(id=organization_id, active=True, 
                                                **first_viewable_dict)
    
    object = get_object_or_404(Blog, pk=blog_id, active=True,**viewable_dict)
    if request.method == 'POST':
        object.active = False
        object.save()
        return redirect('list_blogs', organization_id=organization_id)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'delete_blog',
        'organization': organization,
        'organization_id': organization_id,
        
        'module_path': module_path,        
        'object': object,
        'page_title': f'Delete Blog',
    }
    template_file = f"{app_name}/{module_path}/delete_blog.html"
    return render(request, template_file, context)


@login_required
def permanent_deletion_blog(request, organization_id, blog_id):
    user = request.user
    organization = Organization.objects.get(id=organization_id, active=True, 
                                                **first_viewable_dict)
    
    object = get_object_or_404(Blog, pk=blog_id, active=False, deleted=False, **viewable_dict)
    if request.method == 'POST':
        object.active = False
        object.deleted = True
        object.save()
        return redirect('list_blogs', organization_id=organization_id)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'permanent_deletion_blog',
        'organization': organization,
        'organization_id': organization_id,
        
        'module_path': module_path,        
        'object': object,
        'page_title': f'Permanent Deletion Blog',
    }
    template_file = f"{app_name}/{module_path}/permanent_deletion_blog.html"
    return render(request, template_file, context)


@login_required
def restore_blog(request,  organization_id, blog_id):
    user = request.user
    object = get_object_or_404(Blog, pk=blog_id, active=False,**viewable_dict)
    object.active = True
    object.save()
    return redirect('list_blogs', organization_id=organization_id)
   


@login_required
def view_blog(request, organization_id, blog_id):
    user = request.user
    organization = Organization.objects.get(id=organization_id, active=True, 
                                                **first_viewable_dict)
    
    object = get_object_or_404(Blog, pk=blog_id, active=True,**viewable_dict)
    
    # Increment view count
    object.views_count += 1
    object.save(update_fields=['views_count'])
    
    # Get comments
    comments = BlogComment.objects.filter(blog=object, parent_comment=None, active=True).order_by('-created_at')
    
    # Handle comment form
    if request.method == 'POST' and 'comment_content' in request.POST:
        comment_content = request.POST.get('comment_content')
        parent_id = request.POST.get('parent_comment_id')
        
        if comment_content:
            parent_comment = None
            if parent_id:
                parent_comment = BlogComment.objects.get(id=parent_id)
                
            BlogComment.objects.create(
                blog=object,
                author=user,
                content=comment_content,
                parent_comment=parent_comment
            )
            return redirect('view_blog', organization_id=organization_id, blog_id=blog_id)

    # Check permissions
    can_edit = is_blog_admin(user, object, organization) or is_blog_writer(user, object)

    context = {
        'parent_page': '___PARENTPAGE___',
        'page': 'view_blog',
        'organization': organization,
        'organization_id': organization_id,
        
        'module_path': module_path,
        'object': object,
        'page_title': f'View Blog',
        'comments': comments,
        'can_edit': can_edit,
    }
    template_file = f"{app_name}/{module_path}/view_blog.html"
    return render(request, template_file, context)

# Blog Dashboard
@login_required
def blog_dashboard(request, organization_id):
    user = request.user
    organization = get_object_or_404(Organization, id=organization_id, active=True)
    
    # Check if user is a blog admin
    if not is_blog_admin(user, organization=organization):
        messages.error(request, "You do not have permission to access the blog dashboard.")
        return redirect('list_blogs', organization_id=organization_id)
    
    # Get stats for the dashboard
    total_blogs = Blog.objects.filter(organization=organization, active=True).count()
    published_blogs = Blog.objects.filter(organization=organization, active=True, status='published').count()
    draft_blogs = Blog.objects.filter(organization=organization, active=True, status='draft').count()
    archived_blogs = Blog.objects.filter(organization=organization, active=True, status='archived').count()
    
    # Recent blogs
    recent_blogs = Blog.objects.filter(organization=organization, active=True).order_by('-created_at')[:5]
    
    # Popular blogs (most viewed)
    popular_blogs = Blog.objects.filter(organization=organization, active=True, status='published').order_by('-views_count')[:5]
    
    # Activity over time (blogs created per month)
    now = timezone.now()
    six_months_ago = now - timedelta(days=180)
    
    # Get blog members (writers, editors, admins)
    blog_admins = BlogMember.objects.filter(
        blog__organization=organization, 
        role='admin',
        active=True
    ).select_related('member', 'blog').order_by('member__user__username')
    
    blog_writers = BlogMember.objects.filter(
        blog__organization=organization, 
        role='writer',
        active=True
    ).select_related('member', 'blog').order_by('member__user__username')
    
    blog_editors = BlogMember.objects.filter(
        blog__organization=organization, 
        role='editor',
        active=True
    ).select_related('member', 'blog').order_by('member__user__username')
    
    # Activity data for chart - database agnostic approach
    from django.db.models.functions import TruncMonth
    
    blog_activity = Blog.objects.filter(
        organization=organization,
        created_at__gte=six_months_ago
    ).annotate(
        month=TruncMonth('created_at')
    ).values('month').annotate(
        count=Count('id')
    ).order_by('month')
    
    # Format for chart.js
    activity_labels = []
    activity_data = []
    
    for entry in blog_activity:
        month = entry['month'].strftime('%b %Y')
        activity_labels.append(month)
        activity_data.append(entry['count'])
    
    # Prepare chart data
    chart_data = {
        'activity': {
            'labels': activity_labels,
            'data': activity_data
        },
        'status': {
            'labels': ['Published', 'Draft', 'Archived'],
            'data': [published_blogs, draft_blogs, archived_blogs]
        }
    }
    
    context = {
        'parent_page': 'blog_dashboard',
        'page': 'blog_dashboard',
        'page_title': 'Blog Dashboard',
        'organization': organization,
        'organization_id': organization_id,
        
        # Stats
        'total_blogs': total_blogs,
        'published_blogs': published_blogs,
        'draft_blogs': draft_blogs,
        'archived_blogs': archived_blogs,
        
        # Recent and popular content
        'recent_blogs': recent_blogs,
        'popular_blogs': popular_blogs,
        
        # Blog team members
        'blog_admins': blog_admins,
        'blog_writers': blog_writers,
        'blog_editors': blog_editors,
        
        # Chart data
        'chart_data': json.dumps(chart_data),
    }
    
    template_file = f"{app_name}/{module_path}/blog_dashboard.html"
    return render(request, template_file, context)

# Manage blog members
@login_required
def manage_blog_members(request, organization_id, blog_id=None):
    user = request.user
    organization = get_object_or_404(Organization, id=organization_id, active=True)
    
    if blog_id:
        blog = get_object_or_404(Blog, id=blog_id, organization=organization, active=True)
        # Check if user is a blog admin for this specific blog
        if not is_blog_admin(user, blog, organization):
            messages.error(request, "You do not have permission to manage members for this blog.")
            return redirect('view_blog', organization_id=organization_id, blog_id=blog_id)
    else:
        blog = None
        # Check if user is a blog admin at organization level
        if not is_blog_admin(user, organization=organization):
            messages.error(request, "You do not have permission to manage blog members.")
            return redirect('list_blogs', organization_id=organization_id)
    
    # Handle form submission
    if request.method == 'POST':
        form = BlogMemberForm(request.POST, organization=organization)
        if form.is_valid():
            blog_member = form.save(commit=False)
            
            if blog:
                blog_member.blog = blog
            else:
                blog_id = request.POST.get('blog_id')
                if blog_id:
                    blog_member.blog = get_object_or_404(Blog, id=blog_id, organization=organization)
                else:
                    messages.error(request, "Please select a blog.")
                    return redirect('manage_blog_members', organization_id=organization_id)
            
            # Check if this member already has a role for this blog
            existing = BlogMember.objects.filter(blog=blog_member.blog, member=blog_member.member).first()
            if existing:
                existing.role = blog_member.role
                existing.active = True
                existing.save()
                messages.success(request, f"Updated role for {blog_member.member.user.username} to {blog_member.get_role_display()}.")
            else:
                blog_member.save()
                messages.success(request, f"Added {blog_member.member.user.username} as {blog_member.get_role_display()}.")
            
            if blog:
                return redirect('manage_blog_members', organization_id=organization_id, blog_id=blog.id)
            else:
                return redirect('manage_blog_members', organization_id=organization_id)
    else:
        form = BlogMemberForm(organization=organization)
    
    # Get blogs for dropdown if no specific blog
    blogs = None
    if not blog:
        blogs = Blog.objects.filter(organization=organization, active=True)
    
    # Get current members for this blog
    if blog:
        blog_members = BlogMember.objects.filter(blog=blog, active=True).select_related('member', 'member__user')
    else:
        blog_members = BlogMember.objects.filter(blog__organization=organization, active=True).select_related('member', 'member__user', 'blog')
    
    context = {
        'parent_page': 'blog_dashboard',
        'page': 'manage_blog_members',
        'page_title': f'Manage Blog Members{f" for {blog.title}" if blog else ""}',
        'organization': organization,
        'organization_id': organization_id,
        'blog': blog,
        'blogs': blogs,
        'form': form,
        'blog_members': blog_members,
    }
    
    template_file = f"{app_name}/{module_path}/manage_blog_members.html"
    return render(request, template_file, context)

@login_required
def remove_blog_member(request, organization_id, member_id):
    user = request.user
    organization = get_object_or_404(Organization, id=organization_id, active=True)
    
    if request.method == 'POST':
        blog_member = get_object_or_404(BlogMember, id=member_id, active=True)
        
        # Check permissions - must be admin of the blog or org-level blog admin
        if not is_blog_admin(user, blog_member.blog, organization):
            messages.error(request, "You do not have permission to remove members from this blog.")
            return redirect('list_blogs', organization_id=organization_id)
        
        # Soft delete the blog member
        blog_member.active = False
        blog_member.save()
        
        messages.success(request, f"Removed {blog_member.member.user.username} from {blog_member.blog.title}.")
        
        # Return to the appropriate page
        if request.POST.get('return_to_blog'):
            return redirect('manage_blog_members', organization_id=organization_id, blog_id=blog_member.blog.id)
        else:
            return redirect('manage_blog_members', organization_id=organization_id)
    
    return redirect('list_blogs', organization_id=organization_id)

# Public blog views
def public_blog_list(request, organization_id):
    """Public view for blog listing, accessible to everyone"""
    organization = get_object_or_404(Organization, id=organization_id, active=True)
    
    # Only show published blogs to non-authenticated users
    if request.user.is_authenticated:
        blogs = Blog.objects.filter(organization=organization, active=True)
    else:
        blogs = Blog.objects.filter(organization=organization, active=True, status='published')
    
    # Handle category filtering
    category = request.GET.get('category')
    if category:
        blogs = blogs.filter(category=category)
    
    # Handle search
    search_query = request.GET.get('search')
    if search_query:
        blogs = blogs.filter(
            Q(title__icontains=search_query) | 
            Q(content__icontains=search_query) |
            Q(summary__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(blogs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get all categories for filtering
    categories = Blog.objects.filter(
        organization=organization, 
        active=True
    ).exclude(category='').values_list('category', flat=True).distinct()
    
    # Count blogs in each category for the sidebar
    category_counts = {}
    for cat in categories:
        category_counts[cat] = Blog.objects.filter(
            organization=organization,
            active=True,
            category=cat
        ).count()
    
    context = {
        'organization': organization,
        'organization_id': organization_id,
        'page_obj': page_obj,
        'categories': categories,
        'category_counts': category_counts,
        'selected_category': category,
        'search_query': search_query,
        'page_title': f'{organization.name} Blog',
    }
    
    template_file = f"{app_name}/{module_path}/public_blog_list.html"
    return render(request, template_file, context)

def public_blog_detail(request, organization_id, blog_id=None, slug=None):
    """Public view for a single blog post"""
    organization = get_object_or_404(Organization, id=organization_id, active=True)
    
    # Get blog by ID or slug
    if blog_id:
        blog = get_object_or_404(Blog, id=blog_id, organization=organization, active=True)
    elif slug:
        blog = get_object_or_404(Blog, slug=slug, organization=organization, active=True)
    else:
        # No identifier provided
        return redirect('public_blog_list', organization_id=organization_id)
    
    # Only allow viewing published blogs for non-authenticated users
    if not request.user.is_authenticated and blog.status != 'published':
        messages.error(request, "This blog post is not available.")
        return redirect('public_blog_list', organization_id=organization_id)
    
    # Increment view count
    blog.views_count += 1
    blog.save(update_fields=['views_count'])
    
    # Get comments
    comments = BlogComment.objects.filter(blog=blog, parent_comment=None, active=True).order_by('-created_at')
    
    # Handle comment form for authenticated users
    if request.user.is_authenticated and request.method == 'POST' and 'comment_content' in request.POST:
        comment_content = request.POST.get('comment_content')
        parent_id = request.POST.get('parent_comment_id')
        
        if comment_content:
            parent_comment = None
            if parent_id:
                parent_comment = BlogComment.objects.get(id=parent_id)
                
            BlogComment.objects.create(
                blog=blog,
                author=request.user,
                content=comment_content,
                parent_comment=parent_comment
            )
            return redirect('public_blog_detail', organization_id=organization_id, blog_id=blog.id)
    
    # Get related blogs based on category
    related_blogs = Blog.objects.filter(
        organization=organization,
        category=blog.category,
        active=True,
        status='published'
    ).exclude(id=blog.id).order_by('-published_at')[:3]
    
    context = {
        'organization': organization,
        'organization_id': organization_id,
        'blog': blog,
        'comments': comments,
        'related_blogs': related_blogs,
        'can_comment': request.user.is_authenticated,
        'page_title': blog.title or blog.name,
    }
    
    template_file = f"{app_name}/{module_path}/public_blog_detail.html"
    return render(request, template_file, context)

