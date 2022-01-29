# /add_task goto_store due:tuesday time_est:60 
import random

# tasks
tasks = ['goto_store',
		 'goto_class',
		 'finish_math_hw',
		 'finish_cs_hw']

# days of the week
days = ['monday', 'tuesday', 'wendsday', 'thursday', 'friday', 'saturday', 'sunday']

# times in seconds
times = [60, 120, 3600]

# create tasks
ntasks = 200
for i in range(ntasks):
	print('/add_task ', random.choice(tasks), ' due:', random.choice(days), ' time_est:', random.choice(times), sep='')