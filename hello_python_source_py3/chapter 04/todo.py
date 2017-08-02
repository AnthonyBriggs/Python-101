import os
import pickle
import textwrap

todos = []


def create_todo(todos, title, description, level):
    todo = {
        'title' : title,
        'description' : description,
        'level' : level,
    }
    todos.append(todo)
    sort_todos()
    return "Created '%s'." % title

def capitalize(todo):
    todo['level'] = todo['level'].upper()
    return todo


def show_todo(todo, index):
    wrapped_title = textwrap.wrap(todo['title'], 16)
    wrapped_descr = textwrap.wrap(todo['description'], 24)
    
    output = str(index+1).ljust(8) + "  "
    output += wrapped_title[0].ljust(16) + "  "
    output += wrapped_descr[0].ljust(24) + "  "
    output += todo['level'].ljust(16)
    output += "\n"
    
    max_len = max(len(wrapped_title),
                  len(wrapped_descr))
    for index in range(1, max_len):
        output += " " * 8 + "  " 
        if index < len(wrapped_title):
            output += wrapped_title[index].ljust(16) + "  "
        else:
            output += " " * 16 + "  "
        if index < len(wrapped_descr):
            output += wrapped_descr[index].ljust(24) + "  "
        else:
            output += " " * 24 + "  "
        output += "\n"
        
    return output

def sort_todos():
    global todos
    important = [capitalize(todo) for todo in todos
                 if todo['level'].lower() == 'important']
    unimportant = [todo for todo in todos
                   if todo['level'].lower() == 'unimportant']
    medium = [todo for todo in todos
              if todo['level'].lower() != 'important' and
                 todo['level'].lower() != 'unimportant']
    todos = important + medium + unimportant

def show_todos(todos):
    output = ("Item      Title             "
              "Description               Level\n")
    for index, todo in enumerate(todos):
        output += show_todo(todo, index)
    return output

def delete_todo(todos, which):
    if not which.isdigit():
        return ("'" + which +
            "' needs to be the number of a todo!")
    which = int(which)
    if which < 1 or which > len(todos):
        return ("'" + str(which) +
            "' needs to be the number of a todo!")
    del todos[which-1]
    return "Deleted todo #" + str(which)

def edit_todo(todos, which, title, description, level):
    if not which.isdigit():
        return ("'" + which +
            "' needs to be the number of a todo!")
    which = int(which)
    if which < 1 or which > len(todos):
        return ("'" + str(which) +
            "' needs to be the number of a todo!")
    
    todo = todos[which-1]
    if title != "":
        todo['title'] = title
    if description != "":
        todo['description'] = description
    if level != "":
        todo['level'] = level
    
    sort_todos()
    return "Edited todo #" + str(which)

def test(todos, abcd, ijkl):
    return "Command 'test' returned:\n" + \
        "abcd: " + abcd + "\nijkl: " + ijkl


commands = {
    'new' : [create_todo, ['title', 'description', 'level']],
    'show' : [show_todos, []],
    'delete' : [delete_todo, ['which']],
    'edit': [edit_todo, ['which', 'title', 'description', 'level']],
    'test' : [test, ['abcd', 'ijkl']],
}

def save_todo_list():
    save_file = open("todos.pickle", "wb")
    pickle.dump(todos, save_file)
    save_file.close()

def load_todo_list():
    global todos
    if os.access("todos.pickle", os.F_OK):
        save_file = open("todos.pickle", "rb")
        todos = pickle.load(save_file)


def main_loop():
    load_todo_list()
    while 1:
        user_input = input("> ")
        if user_input.lower().startswith("quit"):
            print("Exiting...")
            save_todo_list()
            break
        print(run_command(user_input))

def get_input(fields):
    user_input = {}
    for field in fields:
        user_input[field] = input(field + " > ")
    return user_input

def get_function(command_name):
    return commands[command_name][0]

def get_fields(command_name):
	return commands[command_name][1]

def run_command(user_input, data=None):
    user_input = user_input.lower()
    if user_input not in commands:
        return user_input + "?" \
               " I don't know what that command is."
    else:
        the_func = get_function(user_input)
    
    if data is None:
        the_fields = get_fields(user_input)
        data = get_input(the_fields)
    return the_func(todos, **data)

if __name__ == '__main__':
    main_loop()

