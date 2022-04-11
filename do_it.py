# * Start

import time
import datetime
import json
import os
import sys

# * Initialises the preset data

today = datetime.date.today() # This sets the date for today

with open(os.path.join(sys.path[0], "data.txt"), 'r') as json_file: # Opens up data.txt as json_file in read mode
    tasks_obj = json.load(json_file) # Loads the JSON file and assigns it to the variable tasks_obj
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

# * The main program

def repeater(): # This is a function for keeping the program in a repeating loop
    view_and_update() # This is the first thing that runs which the program is launched. This is so that it gives the most up-to-date stats
    
    repeat = input("What do you want to do?\n1. Add tasks\n2. Delete tasks\n")
    
    if repeat == "1":
        adding()
        repeater()
        
    elif repeat == "2":
        list_of_stats = [
        name,
        goal_steps,
        steps_done,
        percentage_done,
        steps_left,
        current_daily_rate,
        dynamic_target_daily_rate,
        needs,
        predict_s,
        sPRED_vs_gs,
        date_added,
        days_gone,
        deadline,
        days_left] # This is a list of all the lists that are found in the JSON file. We use it to prevent repetition.
        
        task_number = int(input("Enter the INDEX of the task which you want to delete: ")) # The index is displayed before each task name.
        for list in list_of_stats: # This loops around each of the items listed in list_of_stats, and deletes them
            del list[task_number]
        repeater()

def adding(): # This function is for adding a new task to the program
    task_name_input = input("Enter the task name: ")
    goal_steps_input = int(input("Enter the number of goal number of steps: ")) # Goal number of steps
    deadline_raw_input = input("Enter the deadline using the YYYY-MM-DD format: ") # Raw date (i.e., it is not formatted)
    deadline_format_input = datetime.datetime.strptime(deadline_raw_input, "%Y-%m-%d").date() # This formats the deadline_raw_input into a date which Python can use to work with
    days_left_input = int((deadline_format_input - today).days) # This calculates the number of days left until the deadline. It works by subtracting the deadline from today's date. It turns this value into an integer.
    dynamic_target_daily_rate_input = int(goal_steps_input/days_left_input) # This calculates the ideal rate which you should be working at in order to achieve your goal_steps by the deadline you've set.
    
    with open(os.path.join(sys.path[0], "data.txt"), 'w') as json_file: # This opens up data.txt in writing mode so that it can add the data which the user has entered
        name.append(task_name_input)
        goal_steps.append(goal_steps_input)
        steps_done.append(0) # This is number of steps you've taken. The way to update this is by going to data.txt and changing the value in the steps_done field. I know, I need to make this more user-friendly.
        percentage_done.append(0)
        steps_left.append(goal_steps_input)
        current_daily_rate.append(0)
        dynamic_target_daily_rate.append(dynamic_target_daily_rate_input)
        needs.append(0)
        predict_s.append(0)
        sPRED_vs_gs.append(0)
        date_added.append(str(today))
        days_gone.append(1) # The minimum number of days gone MUST be 1. If it is zero, it will give an error. This is because you CANNOT divide by zero :).
        deadline.append(str(deadline_format_input)) # The date needs to saved as a string
        days_left.append(days_left_input)
        json.dump(tasks_obj, json_file, indent=1)

def view_and_update(): # This function refreshes the columns
    with open(os.path.join(sys.path[0], "data.txt"), 'w') as json_file:
        # Prints the tasks found in each JSON array
        list_length = len(name) # Counts how many tasks there are
        
        for i in range(0,list_length): # This loops around each of the items in JSON file, and updates them
            deadline_format = datetime.datetime.strptime(deadline[i], "%Y-%m-%d").date()
            days_left[i] = int((deadline_format - today).days)
            deadline_format = datetime.datetime.strptime(date_added[i], "%Y-%m-%d").date()
            days_gone[i] = int((today - deadline_format).days)
            if days_gone[i] == 0: # This corrects any potential error in the days_gone. As I have previously stated, the number of days gone cannot be zero.
                days_gone[i] = 1
            percentage_done[i] = round((steps_done[i]/goal_steps[i])*100,2) # This is the % of steps done. It divides the steps which you have done by the goal number of steps
            steps_left[i] = goal_steps[i] - steps_done[i]
            current_daily_rate[i] = round((steps_done[i]/days_gone[i]),2) # This is your current number of steps per day
            dynamic_target_daily_rate[i] = round((steps_left[i]/days_left[i]),2) # This is the ideal rate which you should be working at in order to achieve your goal_steps by the deadline you've set
            needs[i] = round(((dynamic_target_daily_rate[i]*days_gone[i])-steps_done[i]),2) # This is the number of steps which you need to take, today, in order to match the dynamic_target_daily_rate
            predict_s[i] = round((current_daily_rate[i]*days_left[i])+steps_done[i],2) # This is the predicted number of steps which you will achieve if you continue at your current rate
            sPRED_vs_gs[i] = round(((predict_s[i]/goal_steps[i])*100),2) # this predict_s / goal_steps. It gives you an idea of how far you're off.
        json.dump(tasks_obj, json_file, indent=1) # This dumps all the of the Python-style updates above into data.txt, BUT this time it formats them into JSON objects
        
        for i in range(0,list_length): # This simply loops around the file and prints everything for you
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

repeater() # My primitive method of looping the program :)
