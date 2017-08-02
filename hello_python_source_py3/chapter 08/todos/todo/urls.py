from django.conf.urls.defaults import *

from . import views
from .models import Todo

urlpatterns = patterns('',
    (r'^login$', views.todo_login),
    (r'^logout$', views.todo_logout),
        
    (r'^$', views.todo_index),
    (r'^add$', views.add_todo),
    (r'^(?P<todo_id>\d+)$', views.update_todo),
    (r'^(?P<todo_id>\d+)/delete$', views.delete_todo),
)

# old stuff...
from django.views.generic.create_update \
    import update_object, delete_object
old = (
    (r'^(?P<object_id>\d+\old)$', 
     update_object, 
     {'model': Todo, 
      'template_name': 'templates/todo_form.html',
      'post_save_redirect': '/todos/%(id)s',
     }),
      
    (r'^(?P<object_id>\d+)/deleteold$', 
     delete_object, 
     {'model': Todo, 
      'template_name': 'templates/todo_confirm_delete.html',
      'post_delete_redirect': '..',
     }),
)
