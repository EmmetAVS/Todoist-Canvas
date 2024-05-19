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
    if not os.path.exists('prioraddedtasks.json'):
        with open('prioraddedtasks.json', 'w') as f:
            setupdata = {"tasks": []}
            f.write(json.dumps(setupdata, indent=2))
    return data
def add_task(contents, due_strings, section_ids, main_project, link):
    if not type(contents) == type(due_strings) == type(section_ids) == type('string'):
        return TypeError("TypeError add_task_to_school, the type of one of the arguments is not " + str(type('string')) + ".")
    api.add_task(
        content = contents,
        due_string = due_strings,
        due_lang = 'en',
        priority = '1',
        section_id = section_ids,
        project_id = main_project,
        description = link,
        labels = ["Automated", "Canvas"]
    )
def add_canvas_tasks_to_todoist(courses, TodoistIDs, CanvasIDs, main_project, canvasapiwebsite):
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
        links = []
        for n in range (999):
            try:
                duedate = assignments[n].__getattribute__('due_at_date')
                link = str(canvasapiwebsite + "/courses/" + str(CanvasIDs[course]) + "/assignments/" + str(assignments[n].__getattribute__('id')))
                content = assignments[n]
                duedate = str(duedate)[:16] + ' GMT'
                content = str(content)[:-9]
                duedates.append(duedate)
                contents.append(content)
                links.append(link)
            except Exception as err:
                #I should have break here instead of continue but sometimes for some reason it skips over a task without continue
                continue
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
                with open('prioraddedtasks.json', 'r') as f:
                    data = json.loads(f.read())
                    tasksadded = data['tasks']
                    if contents[n] in tasksadded:
                        continue
                tasks_added += 1
                print(add_task(contents[n], duedates[n], str(TodoistIDs[course]), main_project, links[n]))
                with open('prioraddedtasks.json', 'w') as f:
                    tasksadded.append(contents[n])
                    data['tasks'] = tasksadded
                    f.write(json.dumps(data, indent=2))
                print("Adding " + contents[n] + ", due at " + duedates[n])
    print("Added " + str(tasks_added) + " task(s)!")
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
data = setup('C:\\Users\\aarus\\My projects\\Todoist\\todoist.json')
api = TodoistAPI(data["Api-Tokens"]["Todoist"])
canvasapiwebsite = data["Api-Tokens"]["Canvas-Link"]
canvasapitoken = data["Api-Tokens"]["Canvas"]
canvas = Canvas(canvasapiwebsite, canvasapitoken)
main_project = data["Todoist-Project"]["Project"]
TodoistIDs = setup_todoist_ids(data)
CanvasIDs = setup_canvas_ids(data)
canvas_courses = setup_canvas_courses(data)
add_canvas_tasks_to_todoist(canvas_courses, TodoistIDs, CanvasIDs, main_project, canvasapiwebsite)