from django.http import HttpResponseForbidden
from .helpers import get_user_list

def check_user_access(function):
    def wrap(request, *args, **kwargs):
        user_list = get_user_list()
        if request.user not in user_list:
            return HttpResponseForbidden("You do not have access to this resource.")
        return function(request, *args, **kwargs)
    return wrap

from functools import wraps

def add_viewable_dicts(viewable_flag, first_viewable_flag):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            viewable_dict = {} if viewable_flag == '__ALL__' else {'author': request.user}
            first_viewable_dict = {} if first_viewable_flag == '__ALL__' else {'author': request.user}
            request.viewable_dict = viewable_dict
            request.first_viewable_dict = first_viewable_dict
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator

# # Usage
# @add_viewable_dicts('__OWN__', '__OWN__')
# def some_view(request):
#     items = Item.objects.filter(**request.viewable_dict)
#     return render(request, 'some_template.html', {'items': items})
