from . usermgmt_decorators import superuser_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.utils.decorators import method_decorator
from app_1.mod_app.all_view_imports import *
from app_1.mod_app.utils import paginate_queryset
from django.http import HttpResponse
from django.views.decorators.http import require_POST
import csv
@superuser_required
def user_management(request):
    # Fetch all users from the database
    users_list = User.objects.filter(is_active=True).order_by('id')
    print(f">>> === {users_list} <<<")
    # Handle search query
    search_query = request.GET.get('search', '').strip()
    if search_query:
        # Filter the queryset based on the search query AND ensure they're active
        users_list = users_list.filter(
            (Q(username__icontains=search_query) | Q(email__icontains=search_query)) & Q(is_active=True)
        )
    else:
        # If no search, just filter for active users
        users_list = users_list.filter(is_active=True)
    
    print(f"users_list: {users_list}")

    # Paginate the queryset using the common function
    users, items_per_page = paginate_queryset(request, users_list, default_per_page=10)
    context = {'users': users, 'items_per_page': items_per_page, 'search_query': search_query,}

    return render(request, 'app_usermgmt/user_management.html', context)
@superuser_required
def add_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        User.objects.create_user(username=username, password=password, email=email)
        messages.success(request, 'app_usermgmt/User added successfully.')
        return redirect('user_management')
    return render(request, 'app_usermgmt/add_user.html')

@superuser_required
def modify_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        password = request.POST.get('password')
        if password:
            user.set_password(password)
        user.save()
        messages.success(request, 'app_usermgmt/User modified successfully.')
        return redirect('user_management')
    return render(request, 'app_usermgmt/modify_user.html', {'user': user})

@superuser_required
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = False
    user.save()
    messages.success(request, 'app_usermgmt/User deleted successfully.')
    return redirect('user_management')


@superuser_required
def bulk_add_users(request):
    if request.method == 'POST':
        users_data = request.POST.get('users', '').strip()  # Get the raw input and remove leading/trailing spaces
        if not users_data:
            messages.error(request, 'No users provided.')
            return redirect('bulk_add_users')

        success_count = 0
        error_messages = []

        # Split the input by lines
        for line in users_data.splitlines():
            line = line.strip()  # Remove leading/trailing spaces from each line
            if not line:
                continue  # Skip empty lines

            # Split the line by commas
            parts = [part.strip() for part in line.split(',')]
            if len(parts) != 3:
                error_messages.append(f"Invalid format: '{line}'. Expected 'username,password,email'.")
                continue

            username, password, email = parts

            # Validate the data
            if not username or not password or not email:
                error_messages.append(f"Missing data in line: '{line}'. All fields (username, password, email) are required.")
                continue

            # Check if the username or email already exists
            if User.objects.filter(username=username).exists():
                error_messages.append(f"Username '{username}' already exists.")
                continue
            if User.objects.filter(email=email).exists():
                error_messages.append(f"Email '{email}' is already in use.")
                continue

            # Create the user
            try:
                User.objects.create_user(username=username, password=password, email=email)
                success_count += 1
            except Exception as e:
                error_messages.append(f"Error creating user '{username}': {str(e)}")

        # Display success and error messages
        if success_count > 0:
            messages.success(request, f'Successfully added {success_count} user(s).')
        if error_messages:
            for error in error_messages:
                messages.error(request, error)

        return redirect('user_management')

    return render(request, 'app_usermgmt/bulk_add_users.html')
@superuser_required
def bulk_delete_users(request):
     # Handle search query
    users = User.objects.filter(is_active=True).order_by('id')
    users_list = users
    search_query = request.GET.get('search', '').strip()
    if search_query:
        # Filter the queryset based on the search query
        users_list = users_list.filter(
            Q(username__icontains=search_query) | Q(email__icontains=search_query) | Q(is_active=True)
    )
    print(f"users_list: {users_list}")

    # Paginate the queryset using the common function
    users, items_per_page = paginate_queryset(request, users_list, default_per_page=10)
    if request.method == 'POST':
        user_ids = request.POST.getlist('user_ids')
        User.objects.filter(id__in=user_ids,is_active=True).update(is_active=False)
        messages.success(request, 'app_usermgmt/Users deleted in bulk successfully.')
        #return redirect('user_management')
        return redirect('bulk_delete_users')
    
        
    context = {'users': users, 'items_per_page': items_per_page, 'search_query': search_query,}
    return render(request, 'app_usermgmt/bulk_delete_users.html', context)

@superuser_required
def bulk_modify_users(request):
    
    
    if request.method == 'POST':
        # Handle POST request (form submission)
        user_ids = request.POST.getlist('user_ids')
        new_username = request.POST.get('new_username')
        new_email = request.POST.get('new_email')
        new_password = request.POST.get('new_password')
        
        # Fetch users based on selected IDs
        users = User.objects.filter(id__in=user_ids, is_active=True)
        
        # Modify selected users
        for user in users:
            if new_username:
                user.username = new_username
            if new_email:
                user.email = new_email
            if new_password:
                user.set_password(new_password)
            user.save()
        
        messages.success(request, 'Users modified in bulk successfully.')
        return redirect('user_management')
    else:
        # Fetch all users from the database
        users_list = User.objects.filter(is_active=True).order_by('id')
        # Handle search query
        search_query = request.GET.get('search', '').strip()
        if search_query:
            # Filter the queryset based on the search query AND ensure they're active
            users_list = users_list.filter(
                (Q(username__icontains=search_query) | Q(email__icontains=search_query)) & Q(is_active=True)
            )
        else:
            # If no search, just filter for active users
            users_list = users_list.filter(is_active=True)
        # Pagination: Show 10 users per page
        # Paginate the queryset using the common function
        users, items_per_page = paginate_queryset(request, users_list, default_per_page=10)
    
    context = {'users': users, 'items_per_page': items_per_page, 'search_query': search_query,}
    return render(request, 'app_usermgmt/bulk_modify_users.html', context)


@superuser_required
def bulk_undelete_users(request):
     # Handle search query
    users = User.objects.filter(is_active=False).order_by('id')
    users_list = users
    search_query = request.GET.get('search', '').strip()
    if search_query:
        # Filter the queryset based on the search query
        users_list = users_list.filter(
            Q(username__icontains=search_query) | Q(email__icontains=search_query) | Q(is_active=True)
    )
    print(f"users_list: {users_list}")

    # Paginate the queryset using the common function
    users, items_per_page = paginate_queryset(request, users_list, default_per_page=10)
    if request.method == 'POST':
        user_ids = request.POST.getlist('user_ids')
        User.objects.filter(id__in=user_ids,is_active=False).update(is_active=True)
        messages.success(request, 'app_usermgmt/Users undeleted in bulk successfully.')
        #return redirect('user_management')
        return redirect('bulk_undelete_users')
    
        
    context = {'users': users, 'items_per_page': items_per_page, 'search_query': search_query,}
    return render(request, 'app_usermgmt/bulk_undelete_users.html', context)




@superuser_required
def bulk_add_users_from_csv(request):
    if request.method == 'POST':
        users_data = request.POST.get('users', '').strip()  # Get textarea input
        csv_file = request.FILES.get('csv_file')  # Get uploaded CSV file

        success_count = 0
        error_messages = []

        # Process CSV file if uploaded
        if csv_file:
            try:
                decoded_file = csv_file.read().decode('utf-8').splitlines()
                csv_reader = csv.reader(decoded_file)
                for row in csv_reader:
                    if len(row) != 3:
                        error_messages.append(f"Invalid CSV format: '{row}'. Expected 'username,password,email'.")
                        continue

                    username, password, email = row
                    if not username or not password or not email:
                        error_messages.append(f"Missing data in row: '{row}'. All fields (username, password, email) are required.")
                        continue

                    if User.objects.filter(username=username).exists():
                        error_messages.append(f"Username '{username}' already exists.")
                        continue
                    if User.objects.filter(email=email).exists():
                        error_messages.append(f"Email '{email}' is already in use.")
                        continue

                    try:
                        User.objects.create_user(username=username, password=password, email=email)
                        success_count += 1
                    except Exception as e:
                        error_messages.append(f"Error creating user '{username}': {str(e)}")

            except Exception as e:
                error_messages.append(f"Error processing CSV file: {str(e)}")

        # Process textarea input if provided
        elif users_data:
            for line in users_data.splitlines():
                line = line.strip()
                if not line:
                    continue

                parts = [part.strip() for part in line.split(',')]
                if len(parts) != 3:
                    error_messages.append(f"Invalid format: '{line}'. Expected 'username,password,email'.")
                    continue

                username, password, email = parts
                if not username or not password or not email:
                    error_messages.append(f"Missing data in line: '{line}'. All fields (username, password, email) are required.")
                    continue

                if User.objects.filter(username=username).exists():
                    error_messages.append(f"Username '{username}' already exists.")
                    continue
                if User.objects.filter(email=email).exists():
                    error_messages.append(f"Email '{email}' is already in use.")
                    continue

                try:
                    User.objects.create_user(username=username, password=password, email=email)
                    success_count += 1
                except Exception as e:
                    error_messages.append(f"Error creating user '{username}': {str(e)}")

        else:
            error_messages.append("No input provided. Please enter users or upload a CSV file.")

        # Display success and error messages
        if success_count > 0:
            messages.success(request, f'Successfully added {success_count} user(s).')
        if error_messages:
            for error in error_messages:
                messages.error(request, error)

        return redirect('bulk_add_users_from_csv')

    return render(request, 'app_usermgmt/bulk_add_users_from_csv.html')



@superuser_required
def export_users(request):
    """
    Export all active users to a CSV file
    """
    # Create the HttpResponse with CSV header
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="users_export.csv"'
    
    # Create CSV writer
    writer = csv.writer(response)
    
    # Write header row
    writer.writerow(['Username', 'Email', 'First Name', 'Last Name', 'SuperUser', 'Staff Status', 'Active'])
    
    # Get all active users
    users = User.objects.filter(is_active=True)
    
    # Apply search filter if present
    search_query = request.GET.get('search', '').strip()
    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) | 
            Q(email__icontains=search_query)
        )
    
    # Write user data rows
    for user in users:
        writer.writerow([
            user.username,
            user.email,
            user.first_name,
            user.last_name,
            'Yes' if user.is_superuser else 'No',
            'Yes' if user.is_staff else 'No',
            'Yes' if user.is_active else 'No'
        ])
    
    return response



@superuser_required
@require_POST
def export_selected_users(request):
    """
    Export only selected users to a CSV file
    """
    user_ids = request.POST.getlist('user_ids')
    
    # Create the HttpResponse with CSV header
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="selected_users_export.csv"'
    
    # Create CSV writer
    writer = csv.writer(response)
    
    # Write header row
    writer.writerow(['Username', 'Email', 'First Name', 'Last Name', 'SuperUser', 'Staff Status', 'Active'])
    
    # Get selected users
    if user_ids:
        users = User.objects.filter(id__in=user_ids)
        
        # Write user data rows
        for user in users:
            writer.writerow([
                user.username,
                user.email,
                user.first_name,
                user.last_name,
                'Yes' if user.is_superuser else 'No',
                'Yes' if user.is_staff else 'No',
                'Yes' if user.is_active else 'No'
            ])
    
    return response