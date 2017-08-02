from functools import wraps

def user_passes_test(test_func, login_url=None, 
        redirect_field_name=REDIRECT_FIELD_NAME):

    def decorator(view_func):
        @wraps(view_func, 
               assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            if test_func(request.user):
                return view_func(request, 
                                 *args, **kwargs)
            ...
            from django.contrib.auth.views \
                        import redirect_to_login
            return redirect_to_login(
                path, login_url, redirect_field_name)
        return _wrapped_view
    return decorator

def login_required(function=None, 
            redirect_field_name=REDIRECT_FIELD_NAME, 
            login_url=None):
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated(),
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
    
@login_required
def top_secret_view(request, bunker_id, document_id):
	...

@login_required(login_url="/super_secret/login")
def super_top_secret_view(request, bunker_id, document_id):
	...

