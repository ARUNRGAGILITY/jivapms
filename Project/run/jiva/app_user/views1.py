from django.shortcuts import render
from app_web.imports.all_view_imports import *
from django.core.exceptions import ImproperlyConfigured
from django.apps import apps
from app_common.mod_app.all_view_imports import *
from . models import *
from . forms import *
import csv
import io
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
# Create your views here.
app_name = "app_user"

class CustomPasswordChangeView(PasswordChangeView):
    template_url = f"{app_name}/user/password_change.html"
    template_name = f"{template_url}"
    success_url = reverse_lazy('user_home')

@login_required
def user_home(request):
    context = {'page': 'user_home'}
    template_file = f"{app_name}/user/user_home.html"
    return render(request, template_file, context)

def logout_page(request):
    logout(request)
    return redirect('/')

@login_required
def home(request):
    context = {'page': 'home'}
    template_file = f"{app_name}/user/home_page.html"
    return render(request, template_file, context)

@login_required
def user_settings(request):
    context = {'page': 'user_settings'}
    template_file = f"{app_name}/user/user_settings.html"
    return render(request, template_file, context)

@login_required
def profile(request):    
    # check if user has profile or create one
    user_profile = None 
    try:
        user_profile = Profile.objects.get(user=request.user)
    except:
        print(f"UserProfile does not exists")
        user_profile = Profile(user=request.user, bio='Enter Bio')
        user_profile.save()
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('user_home')
        else:
            print(f"error in the profile updation {user_form} {profile_form}")

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    template_file = f"{app_name}/user/profile.html"
    return render(request, template_file, context)

# Login Page
def login_page(request):
    # take inputs
    # process inputs
    if request.method == 'POST': 
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.GET.get('next', 'user_home') # Provide a default redirect URL
            return redirect(next_url)
        else:
            print(f">>> === form invalid {form.errors} === <<<")
            # If you want to display form errors, ensure your template can display them
            messages.error(request, 'Username or password is incorrect')
    # send outputs (info, template, request)
    context = {
        'page': 'login',
    }
    template_file = f"{app_name}/user/login.html"
    return render(request, template_file, context)

# help function
def check_reg_code(reg_code):
    reg_codes = RegCode.objects.filter(active=True)
    for code in reg_codes:
        if reg_code == code.reg_code:
            print(f">>> === valid reg code: reg_code:{reg_code}={code.reg_code} === <<<")
            return True
    return False    

# Registration Page (updated)
def register_page(request):
    # take inputs
    reg_codes = RegCode.objects.filter(active=True)
    # process inputs
    if request.method == 'POST':
        reg_code = request.POST.get('reg_code', '')     
        p1 = request.POST.get('password1', '')
        p2 = request.POST.get('password2', '')
        if p1 != p2:
            messages.error(request, f"Passwords do not match.")
            return redirect("register_page")   
        if not check_reg_code(reg_code):
            messages.error(request, f"Invalid or incorrect registration code.")
            return redirect("register_page")        
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  
            return redirect('user_home')
        else:
            for msg in form.error_messages:
                messages.error(request, f"{msg}: {form.error_messages[msg]}")
    # send outputs (info, template, request)
    context = {
        'page': 'register',
    }
    template_file = f"{app_name}/user/register.html"
    return render(request, template_file, context)


########################################################################################
#
#
#
#
########################################################################################

def get_or_create_profile(user):
    """Get the user's profile or create it if it doesn't exist."""
    try:
        return user.profile
    except Profile.DoesNotExist:
        return Profile.objects.create(user=user)


def get_roles_of_user(app_label='app_memberprofilerole', model_name='Role', role_name='Scrum Master'):
    try:
        # Check if the model exists
        model = apps.get_model(app_label, model_name)
        if model is None:
            return []  # model not found

        # Safe filter for admin users
        return model.objects.filter(name=role_name)

    except (LookupError, ImproperlyConfigured, AttributeError):
        # Catch all possible errors and return empty queryset or list
        return []

@login_required
def admin_dashboard(request):
    if not request.user.is_superuser and not request.user.is_staff:
        messages.error(request, "You don't have permission to access the admin dashboard.")
        return redirect('dashboard')
    
    # Count statistics
    total_users = User.objects.count()
    active_users = User.objects.filter(is_active=True).count()
    inactive_users = User.objects.filter(is_active=False).count()  # Soft-deleted users
    admin_users = User.objects.filter(is_superuser=True, is_active=True).count()
    scrum_masters = get_roles_of_user(role_name='Scrum Master').count()
    product_owners = User.objects.filter(is_superuser=False, is_active=True).count()
    team_members = User.objects.filter(is_superuser=False, is_active=True).count()
    
    # Get 5 most recent users
    recent_users = User.objects.all().order_by('-date_joined')[:5]
    
    context = {
        'total_users': total_users,
        'active_users': active_users,
        'inactive_users': inactive_users,
        'admin_users': admin_users,
        'scrum_masters': scrum_masters,
        'product_owners': product_owners,
        'team_members': team_members,
        'recent_users': recent_users,
        'active_tab': 'dashboard'  # Add this line
    }
    
    # send outputs (info, template, request)
    template_file = f"{app_name}/user/admin_dashboard.html"
    return render(request, template_file, context)



@login_required
def dashboard(request):
    """Display the dashboard with user statistics."""
    # User statistics
    total_users = User.objects.count()
    active_users = User.objects.filter(is_active=True).count()
    
    # Calculate new users this month
    first_day_of_month = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    new_users_this_month = User.objects.filter(date_joined__gte=first_day_of_month).count()
    
    # Profiles with images
    profiles_with_images = Profile.objects.exclude(image='').count()
    
    # Recent users
    recent_users = User.objects.order_by('-date_joined')[:5]
    
    # User profile completion status
    user_profile = get_or_create_profile(request.user)
    user_has_image = bool(user_profile.image)
    user_has_bio = bool(user_profile.bio)
    user_has_full_name = bool(request.user.first_name and request.user.last_name)
    user_email_verified = True  # Placeholder, implement email verification if needed
    
    # Calculate overall completion percentage
    completion_items = [user_has_image, user_has_bio, user_has_full_name, user_email_verified]
    user_profile_completion = int((sum(1 for item in completion_items if item) / len(completion_items)) * 100)
    
    context = {
        'page': 'user_dashboard',
        'page_title': 'User Dashboard',
        'total_users': total_users,
        'active_users': active_users,
        'new_users_this_month': new_users_this_month,
        'profiles_with_images': profiles_with_images,
        'recent_users': recent_users,
        'user_has_image': user_has_image,
        'user_has_bio': user_has_bio,
        'user_has_full_name': user_has_full_name,
        'user_email_verified': user_email_verified,
        'user_profile_completion': user_profile_completion,
    }
    # send outputs (info, template, request)
    template_file = f"{app_name}/user/dashboard.html"
    return render(request, template_file, context)



def user_list_basic(request):
    """Display all users with their profiles."""
    users = User.objects.filter(active=True).order_by('username')
    context = {'users': users}
    # send outputs (info, template, request)
    template_file = f"{app_name}/user/user_list_basic.html"
    return render(request, template_file, context)

@login_required
def user_detail(request, user_id):
    if not request.user.is_superuser and not request.user.is_staff:
        messages.error(request, "You don't have permission to access this page.")
        return redirect('dashboard')
    
    user = get_object_or_404(User, id=user_id)

    
    if request.method == 'POST':
        # Toggle user status (active/inactive)
        if 'toggle_status' in request.POST:
            user.is_active = not user.is_active
            user.save()
            status = "activated" if user.is_active else "deactivated"
            messages.success(request, f"User {user.username} has been {status}.")
        
        # Change user type
        if 'user_type' in request.POST:
            user_type = request.POST.get('user_type')
            user.user_type = user_type
            user.save()
            messages.success(request, f"User {user.username} is now a {user.get_user_type_display()}.")
        
        # Soft delete user
        if 'delete_user' in request.POST:
            user.is_active = False
            user.save()
            messages.success(request, f"User {user.username} has been soft-deleted (deactivated).")
            return redirect('user_list')
    

    context = {'user_detail': user, 'active_tab': 'users' }
    # send outputs (info, template, request)
    template_file = f"{app_name}/user/user_detail.html"
    return render(request, template_file, context)

@login_required
def profile_update(request):
    """Update the logged-in user's profile."""
    profile = get_or_create_profile(request.user)
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('user_detail', username=request.user.username)
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    template_file = f"{app_name}/user/profile_update.html"
    return render(request, template_file, context)

@login_required
def delete_user(request, user_id):
    """Delete a user (admin only)."""
    if not request.user.is_superuser:
        messages.error(request, 'You do not have permission to delete users.')
        return redirect('user_list')
    
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        username = user.username
        user.delete()
        messages.success(request, f'User {username} has been deleted.')
        return redirect('user_list')
    
    context = {'user_to_delete': user}
    template_file = f"{app_name}/user/delete_user.html"
    return render(request, template_file, context)



@login_required
def bulk_user_actions(request):
    if not request.user.is_superuser and not request.user.is_staff:
        messages.error(request, "You don't have permission to access this page.")
        return redirect('dashboard')
    
    if request.method == 'POST':
        selected_users = request.POST.getlist('selected_users', [])
        bulk_action = request.POST.get('bulk_action', '')
        
        if not selected_users or not bulk_action:
            messages.warning(request, "No users selected or no action specified.")
            return redirect('user_list')
        
        users = User.objects.filter(id__in=selected_users)
        
        # Prevent self-modification
        if str(request.user.id) in selected_users:
            users = users.exclude(id=request.user.id)
            messages.warning(request, "You cannot modify your own account through bulk actions.")
            if users.count() == 0:
                return redirect('user_list')
        
        if bulk_action == 'activate':
            count = users.update(is_active=True)
            messages.success(request, f"Successfully activated {count} users.")
        
        elif bulk_action == 'deactivate':
            count = users.update(is_active=False)
            messages.success(request, f"Successfully deactivated {count} users.")
        
        elif bulk_action == 'change_type':
            user_type = request.POST.get('bulk_user_type', '')
            if user_type in ['admin', 'scrum_master', 'product_owner', 'team_member']:
                count = users.update(user_type=user_type)
                messages.success(request, f"Changed user type to {user_type} for {count} users.")
            else:
                messages.error(request, "Invalid user type specified.")
    
    return redirect('user_list')



# Admin User List with Pagination
@login_required
def user_list(request):
    if not request.user.is_superuser and not request.user.is_staff:
        messages.error(request, "You don't have permission to access this page.")
        return redirect('dashboard')
    # Handle bulk actions
    if request.method == 'POST':
        return bulk_user_actions(request)
    
    query = request.GET.get('q', '')
    user_type = request.GET.get('user_type', '')
    status = request.GET.get('status', '')
    
    users = User.objects.all()
    
    # Apply filters
    if query:
        users = users.filter(
            Q(username__icontains=query) | 
            Q(email__icontains=query) | 
            Q(first_name__icontains=query) | 
            Q(last_name__icontains=query)
        )
    
    if user_type:
        users = users.filter(user_type=user_type)
    
    if status:
        is_active = status == 'active'
        users = users.filter(is_active=is_active)
    
    # Order results
    users = users.order_by('username')
    
    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(users, 10)  # Show 10 users per page
    
    try:
        users_page = paginator.page(page)
    except PageNotAnInteger:
        users_page = paginator.page(1)
    except EmptyPage:
        users_page = paginator.page(paginator.num_pages)
    
    context = {
        'users': users_page,
        'query': query,
        'user_type': user_type,
        'status': status,
        'total_count': paginator.count,
        'active_tab': 'users'  # Add this line
    }
    
    template_file = f"{app_name}/user/user_list.html"
    return render(request, template_file, context)

from app_memberprofilerole.mod_member.models_member import *
from app_memberprofilerole.mod_role.models_role import *
@login_required
def batch_user_upload(request):
    if not request.user.is_superuser and not request.user.is_staff:
        messages.error(request, "You don't have permission to access this page.")
        return redirect('dashboard')
    
    results = {
        'created': [],
        'errors': [],
        'total': 0
    }
    
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_content = None
            
            # Handle file upload if present
            if request.FILES and 'csv_file' in request.FILES:
                csv_file = request.FILES['csv_file']
                try:
                    csv_content = csv_file.read().decode('utf-8')
                except UnicodeDecodeError:
                    messages.error(request, "The uploaded file is not a valid CSV file or contains invalid characters.")
                    return render(request, 'accounts/batch_user_upload.html', {'form': form, 'results': results})
            
            # Handle text input if present (and file not provided)
            elif form.cleaned_data.get('csv_text', '').strip():
                csv_content = form.cleaned_data['csv_text']
            # No CSV content provided
            if not csv_content:
                messages.error(request, "Please upload a CSV file or paste CSV data.")
                return render(request, 'accounts/batch_user_upload.html', {'form': form, 'results': results})
            
            # Process the CSV content
            try:
                csv_reader = csv.reader(io.StringIO(csv_content))
                headers = next(csv_reader, None)  # Skip header row
                
                if not headers:
                    messages.error(request, "The CSV data is empty or has no headers.")
                    return render(request, 'accounts/batch_user_upload.html', {'form': form, 'results': results})
                
                # Check if proper headers exist
                required_fields = ['username', 'email', 'password']
                missing_fields = [field for field in required_fields if field not in headers]
                
                if missing_fields:
                    messages.error(request, f"CSV file is missing required headers: {', '.join(missing_fields)}")
                    return render(request, 'accounts/batch_user_upload.html', {'form': form, 'results': results})
                
                # Process each row
                for i, row in enumerate(csv_reader, 1):
                    # Skip empty rows
                    if not any(cell.strip() for cell in row):
                        continue
                    
                    results['total'] += 1
                    
                    # Handle rows with fewer columns than headers
                    if len(row) < len(headers):
                        row.extend([''] * (len(headers) - len(row)))
                    
                    # Create a dictionary from headers and row values
                    row_data = dict(zip(headers, row))
                    
                    try:
                        # Basic validation
                        if not row_data.get('username') or not row_data.get('email') or not row_data.get('password'):
                            raise ValidationError("Username, email, and password are required")
                        
                        # Check if user exists
                        if User.objects.filter(username=row_data.get('username')).exists():
                            raise ValidationError(f"Username '{row_data.get('username')}' already exists")
                        
                        if User.objects.filter(email=row_data.get('email')).exists():
                            raise ValidationError(f"Email '{row_data.get('email')}' already exists")
                        
                        # Validate user type
                        valid_user_types = ['admin', 'scrum_master', 'product_owner', 'team_member']
                        # # Validate user role
                        role_name = row_data.get('role', 'team_member').strip()
                        try:
                            roles = Role.objects.filter(active=True)
                            print(f">>> === {roles} === <<<")
                            role = Role.objects.get(name=role_name)
                        except Role.DoesNotExist:
                            # Default to team member if role doesn't exist
                            role = Role.objects.get(name='TeamMember')

                        # Create the user
                        user = User(
                            username=row_data.get('username'),
                            email=row_data.get('email'),
                            first_name=row_data.get('first_name', ''),
                            is_active=True
                            )
                        user.save()
                        # Member Organization Role setting the Member,Role
                        member = Member.objects.filter(active=True, user=user).first()
                        if member:
                            memberorgrole = MemberOrganizationRole.objects.filter(active=True, member=member).first()
                            if memberorgrole:
                                memberorgrole.role = role
                                memberorgrole.save()
                            else:
                                memberorgrole = MemberOrganizationRole.objects.create(member=member, role=role)
                                memberorgrole.save()
                        else:
                            member = Member.objects.create(user=user)
                            memberorgrole = MemberOrganizationRole.objects.create(member=member, role=role)
                            memberorgrole.save()
                            member.save()
                        
                        # Set password
                        password = row_data.get('password')
                        try:
                            validate_password(password, user)
                        except ValidationError as e:
                            raise ValidationError(f"Password validation failed: {', '.join(e.messages)}")
                        
                        user.set_password(password)
                        user.save()
                        
                        # Create profile
                        Profile.objects.get_or_create(user=user)
                        
                        results['created'].append({
                            'username': user.username,
                            'email': user.email,
                            'user_type': role_name,
                        })
                        
                    except ValidationError as e:
                        results['errors'].append({
                            'row': i,
                            'data': row_data,
                            'error': str(e)
                        })
                    except Exception as e:
                        results['errors'].append({
                            'row': i,
                            'data': row_data,
                            'error': f"Unexpected error: {str(e)}"
                        })
                
                if results['created']:
                    messages.success(request, f"Successfully created {len(results['created'])} users.")
                
                if results['errors']:
                    messages.warning(request, f"Failed to create {len(results['errors'])} users due to errors.")
                
                if not results['created'] and not results['errors']:
                    messages.warning(request, "No valid data found to process.")
                
            except Exception as e:
                messages.error(request, f"Error processing CSV data: {str(e)}")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = CSVUploadForm()
    context = {'form': form, 'results': results}
    template_file = f"{app_name}/user/batch_user_upload.html"
    return render(request, template_file, context)



@login_required
def create_user(request):
    if not request.user.is_superuser and not request.user.is_staff:
        messages.error(request, "You don't have permission to access this page.")
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = AdminUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create a profile
            Profile.objects.get_or_create(user=user)
            messages.success(request, f"User {user.username} created successfully.")
            return redirect('user_detail', user_id=user.id)
    else:
        form = AdminUserCreationForm(initial={'is_active': True})
    
    context = {'form': form,'active_tab': 'users'  }
    template_file = f"{app_name}/user/create_user.html"
    return render(request, template_file, context)


@login_required
def edit_user(request, user_id):
    if not request.user.is_superuser and not request.user.is_staff:
        messages.error(request, "You don't have permission to access this page.")
        return redirect('dashboard')
    
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        form = AdminUserCreationForm(request.POST, instance=user)
        # Remove password validation if password fields are empty
        if not request.POST.get('password1') and not request.POST.get('password2'):
            form.fields['password1'].required = False
            form.fields['password2'].required = False
        
        if form.is_valid():
            user = form.save(commit=False)
            # Only set password if provided
            if request.POST.get('password1'):
                user.set_password(form.cleaned_data['password1'])
            user.save()
            messages.success(request, f"User {user.username} updated successfully.")
            return redirect('user_detail', user_id=user.id)
    else:
        form = AdminUserCreationForm(instance=user)
        # Make password fields not required for editing
        form.fields['password1'].required = False
        form.fields['password2'].required = False
    
    
    context ={'form': form, 'user_obj': user, 'active_tab': 'users' }
    template_file = f"{app_name}/user/edit_user.html"
    return render(request, template_file, context)


@login_required
def delete_user(request, user_id):
    if not request.user.is_superuser and not request.user.is_staff:
        messages.error(request, "You don't have permission to access this page.")
        return redirect('dashboard')
    
    user = get_object_or_404(User, id=user_id)
    
    # Prevent self-deletion
    if user == request.user:
        messages.error(request, "You cannot delete your own account.")
        return redirect('user_list')
    
    if request.method == 'POST':
        # Soft delete by deactivating
        user.is_active = False
        user.save()
        messages.success(request, f"User {user.username} has been deactivated.")
    
    return redirect('user_list')


@login_required
def bulk_user_actions(request):
    if not request.user.is_superuser and not request.user.is_staff:
        messages.error(request, "You don't have permission to access this page.")
        return redirect('dashboard')
    
    if request.method == 'POST':
        selected_users = request.POST.getlist('selected_users', [])
        bulk_action = request.POST.get('bulk_action', '')
        
        if not selected_users or not bulk_action:
            messages.warning(request, "No users selected or no action specified.")
            return redirect('user_list')
        
        users = User.objects.filter(id__in=selected_users)
        
        # Prevent self-modification
        if str(request.user.id) in selected_users:
            users = users.exclude(id=request.user.id)
            messages.warning(request, "You cannot modify your own account through bulk actions.")
            if users.count() == 0:
                return redirect('user_list')
        
        if bulk_action == 'activate':
            count = users.update(is_active=True)
            messages.success(request, f"Successfully activated {count} users.")
        
        elif bulk_action == 'deactivate':
            count = users.update(is_active=False)
            messages.success(request, f"Successfully deactivated {count} users.")
        
        elif bulk_action == 'change_type':
            user_type = request.POST.get('bulk_user_type', '')
            if user_type in ['admin', 'scrum_master', 'product_owner', 'team_member']:
                count = users.update(user_type=user_type)
                messages.success(request, f"Changed user type to {user_type} for {count} users.")
            else:
                messages.error(request, "Invalid user type specified.")
    
    return redirect('user_list')


