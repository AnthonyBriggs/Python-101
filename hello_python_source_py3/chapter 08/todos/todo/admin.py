from todos.todo.models import Todo
from django.contrib import admin

class TodoAdmin(admin.ModelAdmin):
    list_display = ['title', 'importance']
    search_fields = ['title', 'description']

admin.site.register(Todo, TodoAdmin)

