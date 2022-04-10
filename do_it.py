import time
import datetime
import json
import os
import sys

daily_hours = int(16)
today = datetime.date.today()
with open(os.path.join(sys.path[0], "data.txt"), 'r') as json_file:
    tasks_obj = json.load(json_file)
    name = tasks_obj["name"]
    goal_steps = tasks_obj["goal_steps"]
    steps_done = tasks_obj["steps_done"]
    percentage_done = tasks_obj["percentage_done"]
    steps_left = tasks_obj["steps_left"]
    current_daily_rate = tasks_obj["current_daily_rate"]
    dynamic_target_daily_rate = tasks_obj["dynamic_target_daily_rate"]
    needs = tasks_obj["needs"]
    predict_s = tasks_obj["predict_s"]
    sPRED_vs_gs = tasks_obj["sPRED_vs_gs"]
    date_added = tasks_obj["date_added"]
    days_gone = tasks_obj["days_gone"]
    deadline = tasks_obj["deadline"]
    days_left = tasks_obj["days_left"]
def repeater():
    view_and_update()
    repeat = input("What do you want to do?\n1. Add tasks\n2. Delete tasks\n")
    if repeat == "1":
        adding()
        repeater()
    elif repeat == "2":
        list_of_stats = [name,goal_steps,steps_done,percentage_done,steps_left,current_daily_rate,dynamic_target_daily_rate,needs,predict_s,sPRED_vs_gs,date_added,days_gone,deadline,days_left]
        task_number = int(input("Enter the INDEX of the task which you want to delete: "))
        for list in list_of_stats:
            del list[task_number]
        repeater()
def adding():
    task_name_input = input("Enter the task name: ")
    goal_steps_input = int(input("Enter the number of goal number of steps: "))
    deadline_raw_input = input("Enter the deadline using the YYYY-MM-DD format: ")
    deadline_format_input = datetime.datetime.strptime(deadline_raw_input, "%Y-%m-%d").date()
    days_left_input = int((deadline_format_input - today).days)
    dynamic_target_daily_rate_input = int(goal_steps_input/days_left_input)
    with open(os.path.join(sys.path[0], "data.txt"), 'w') as json_file:
        name.append(task_name_input)
        goal_steps.append(goal_steps_input)
        steps_done.append(0)
        percentage_done.append(0)
        steps_left.append(goal_steps_input)
        current_daily_rate.append(0)
        dynamic_target_daily_rate.append(dynamic_target_daily_rate_input)
        needs.append(0)
        predict_s.append(0)
        sPRED_vs_gs.append(0)
        date_added.append(str(today))
        days_gone.append(1)
        deadline.append(str(deadline_format_input))
        days_left.append(days_left_input)
        json.dump(tasks_obj, json_file, indent=1)
def view_and_update():
    with open(os.path.join(sys.path[0], "data.txt"), 'w') as json_file:
        list_length = len(name)
        for i in range(0,list_length):
            deadline_format = datetime.datetime.strptime(deadline[i], "%Y-%m-%d").date()
            days_left[i] = int((deadline_format - today).days)
            deadline_format = datetime.datetime.strptime(date_added[i], "%Y-%m-%d").date()
            days_gone[i] = int((today - deadline_format).days)
            if days_gone[i] == 0:
                days_gone[i] = 1
            percentage_done[i] = round((steps_done[i]/goal_steps[i])*100,2)
            steps_left[i] = goal_steps[i] - steps_done[i]
            current_daily_rate[i] = round((steps_done[i]/days_gone[i]),2)
            dynamic_target_daily_rate[i] = round((steps_left[i]/days_left[i]),2)
            needs[i] = round(((dynamic_target_daily_rate[i]*days_gone[i])-steps_done[i]),2)
            predict_s[i] = round((current_daily_rate[i]*days_left[i])+steps_done[i],2)
            sPRED_vs_gs[i] = round(((predict_s[i]/goal_steps[i])*100),2)
        json.dump(tasks_obj, json_file, indent=1)
        for i in range(0,list_length):
            print(f"""{i} name: {name[i]}
                    goal_steps|{goal_steps[i]}
                    steps_done|{steps_done[i]}
               percentage_done|{percentage_done[i]}%
                    steps_left|{steps_left[i]}
            current_daily_rate|{current_daily_rate[i]}
     dynamic_target_daily_rate|{dynamic_target_daily_rate[i]}
                         needs|{needs[i]} <<<<-------------------
                     predict_s|{predict_s[i]}
                   sPRED_vs_gs|{sPRED_vs_gs[i]}%
                      deadline|{deadline[i]}
                     days_left|{days_left[i]}
####################################################################""")
repeater()