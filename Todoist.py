from todoist_api_python.api import TodoistAPI
from canvasapi import Canvas
import json
import os
def setup(tokenjsonlink):
    if not os.path.exists(tokenjsonlink):
        print("Please make sure you inputted the correct filename")
        return
    with open(tokenjsonlink, 'r') as file:
            data = json.loads(file.read())
            return data
def add_task(contents, due_strings, section_ids, main_project):
    if not type(contents) == type(due_strings) == type(section_ids) == type('string'):
        return TypeError("TypeError add_task_to_school, the type of one of the arguments is not " + str(type('string')) + ".")
    api.add_task(
        content = contents,
        due_string = due_strings,
        due_lang = 'en',
        priority = '1',
        section_id = section_ids,
        project_id = main_project
    )
def add_canvas_tasks_to_todoist(courses, TodoistIDs, CanvasIDs, main_project):
    tasks_added = 0
    if type(courses) != type([]) and type(courses) != type(''):
        print("The courses inputted are not in list format!")
        return
    elif type(TodoistIDs) != type(CanvasIDs) != type({'key': 'value'}):
        print("The ID sets inputted are not in dictionary format!")
        return
    if type(courses) == type(''):
        courses = [courses]
    for course in courses:
        print(course)
        coursez = canvas.get_course(CanvasIDs[course])
        assignments = coursez.get_assignments(bucket = 'future')
        duedates = []
        contents = []
        for n in range (999999):
            try:
                duedate = assignments[n].__getattribute__('due_at_date')
                content = assignments[n]
                duedate = str(duedate)[:16] + ' GMT'
                content = str(content)[:-9]
                duedates.append(duedate)
                contents.append(content)
            except:
                break
        if len(contents) == 0:
            continue
        for n in range (0, len(contents)):
            todoisttasks = api.get_tasks(section_id = TodoistIDs[course])
            currenttasks = []
            for task in todoisttasks:
                currenttasks.append(str(task.content))
            if contents[n].strip() in currenttasks:
                continue
            else:
                tasks_added += 1
                print(add_task(contents[n], duedates[n], str(TodoistIDs[course]), main_project))
                print("Adding " + contents[n] + ", due at " + duedates[n])
    print("Added " + str(tasks_added) + " tasks!")
def setup_todoist_ids(data):
    subproject_ids = {}
    for classes in data["Todoist-IDs"]:
        subproject_ids[classes] = data["Todoist-IDs"][classes]
    return subproject_ids
def setup_canvas_ids(data):
    subproject_ids = {}
    for classes in data["Canvas-IDs"]:
        subproject_ids[classes] = data["Canvas-IDs"][classes]
    return subproject_ids
def setup_canvas_courses(data):
    all_classes = []
    for classes in data["Canvas-IDs"]:
        all_classes.append(classes)
    return all_classes
data = setup('testtodoist.json')
api = TodoistAPI(data["Api-Tokens"]["Todoist"])
canvasapiwebsite = data["Api-Tokens"]["Canvas-Link"]
canvasapitoken = data["Api-Tokens"]["Canvas"]
canvas = Canvas(canvasapiwebsite, canvasapitoken)
main_project = data["Todoist-Project"]["Project"]
TodoistIDs = setup_todoist_ids(data)
CanvasIDs = setup_canvas_ids(data)
canvas_courses = setup_canvas_courses(data)
add_canvas_tasks_to_todoist(canvas_courses, TodoistIDs, CanvasIDs, main_project)