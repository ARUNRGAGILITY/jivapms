from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def paginate_queryset(request, queryset, default_per_page=10):
    """
    Paginates a queryset based on the request's 'page' and 'per_page' parameters.

    Args:
        request: The Django request object.
        queryset: The queryset to paginate.
        default_per_page: The default number of items per page.

    Returns:
        A paginated queryset and the number of items per page.
    """
    if not queryset.exists():
        # Return empty list and default per_page for consistency
        return [], default_per_page
    # Get the 'per_page' parameter from the request (default to default_per_page)
    per_page = request.GET.get('per_page', default_per_page)
    if per_page == 'all':
        per_page = queryset.count()  # Show all items
    else:
        per_page = int(per_page)

    # Paginate the queryset
    paginator = Paginator(queryset, per_page)
    page = request.GET.get('page')

    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver the first page
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver the last page
        paginated_queryset = paginator.page(paginator.num_pages)

    return paginated_queryset, per_page