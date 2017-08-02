# Create your views here.

from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth import authenticate, login, logout

from django.views.generic.create_update \
    import update_object, delete_object
    
from todos.todo.models import Todo, importance_choices

def todo_login(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    error_msg = ''
    
    if (username and password):
        # check password, log user in+redirect if ok
        user = authenticate(
            username=username,
            password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse(todo_index))
            else:
                error_msg = ("Your account has "
                    "been disabled!")
        else:
            error_msg = ("Your username and password "
                "were incorrect!")
            password = ''
        
    return render_to_response('todo_login.tmpl', 
        {'username': username,
         'password': password,
         'error_msg': error_msg,
    })

def todo_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse(todo_login))

def todo_index(request):
    if request.user.id is None:
        return HttpResponseRedirect(reverse(todo_login))
    todos = Todo.objects.filter(owner=request.user
                ).order_by('importance', 'title')
    return render_to_response(
        'index.tmpl',
        {'todos': todos,
         'choices': importance_choices,
         'user': request.user,
         'error_msg': request.GET.get('error_msg', ''),
        })

def add_todo(request):
    t = Todo(title = request.POST['title'],
             description = request.POST['description'],
             importance = request.POST['importance'],
             owner=request.user)
    t.save()
    return HttpResponseRedirect(reverse(todo_index))

def update_todo(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id)
    if todo.owner.id != request.user.id:
        return HttpResponseRedirect(reverse(todo_index)+"?error_msg=That's not your todo!")
    return update_object(
        request,
        object_id=todo_id,
        model=Todo, 
        template_name='templates/todo_form.tmpl',
        post_save_redirect='/todos/%(id)s'
    )
    
def delete_todo(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id)
    if todo.owner.id != request.user.id:
        return HttpResponseRedirect(reverse(todo_index)+"?error_msg=That's not your todo!")
    return delete_object(
        request,
        object_id=todo_id,
        model=Todo, 
        template_name='templates/todo_confirm_delete.tmpl',
        post_delete_redirect='..'
    )
    
    
