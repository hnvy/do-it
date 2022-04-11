# do-it
A Python program that helps you stay on track with your tasks.

# What is it?
Medicine has many diseases to study, and there is too little time. What is the solution? Consistency.

In Medicine consistency is key: a little and often. There will be no grinding. There will be no cramming.

But what kind of consistency? The "I-have-a-test-coming-up-in-11-days,-and-I-have-25-pages-of-work-to-complete.-As-a-result,-I'll-need-to-work-on-roughly-2.5-pages-every-day" kind.

I've written a Python program to handle this for me. I used to do the aforementioned calculations with a basic calculator in high school. However, as I grew older, more deadlines began to materialise out of nowhere. Calculating how many days are left and how many steps I need to take each day to meet each of these deadlines is too time consuming.

I've been using it for a year and have to say that it's a fantastic productivity tool.

# How does it work?
Very simple.
1. Run the program
2. Choose "add tasks"
3. Enter the details of the task
4. Voila!

# But, what do all these things mean?
- `goal_steps`: number of steps which you need to take. "Steps" can be anything: pages, dishes, pens, pencils, turtles, bananas, peanuts...
- `steps_done`: number of steps you've taken. The way to update this is by going to `data.txt` and changing the value in the `steps_done` field. I know, I need to make this more user-friendly.
- `current_daily_rate`: this is equal to `steps_done / number of days gone since you added the task`. In other words, this is your current number of steps per day.
- `dynamic_target_daily_rate`: the ideal rate which you should be working at in order to achieve your `goal_steps` by the deadline you've set.
- `needs`: number of steps which you need to take, today, in order to match the `dynamic_target_daily_rate`
- `predict_s`: predicted number of steps which you will achieve if you continue at your current rate
- `sPRED_vs_gs`: this `predict_s / goal_steps`. It gives you an idea of how far you're off.
