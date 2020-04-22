import time
import json 
import os
from datetime import date 

# todo 
# 0. write out completed log task result to a local json file
# 1. change task_stack to dictionary, so two "break"s enter in a row could be prohibited by looking up stack entries 
# 2. add comments 
# 3. pretty print completed tasks, for eg convert time interval to readable time format 
# 4. log bugs and learnings 
# 5. add sort to print completed tasks from longest time spent to shortes 
# 6. add a function to manually log tasks 
# 7. add visualization for time spent 
# 8. output task log to a text file 
# 9. improve HCI so could share to a friend to do user test 

time_past_total = 0 
comp_task_queue = {}
pending_task_stack = []
currtask = {}
tasks = {}
print("started working today yayyy \n" + time.ctime(int(time.time())))

# return dictionary item: 
# 	task name: status, time spent, time interval
def task(name, status, time_spent, time_intervals):
	return {name: [status, time_spent, time_intervals]}

def task_add_interval(task, start, stop):
	task_attr = list(task.values())[0]
	time_intervals = task_attr[2]
	time_intervals.append([start, stop])

def task_update_stop(task, stop):
	task_attr = list(task.values())[0]	
	time_intervals = task_attr[2][len(task_attr[2])-1]
	time_start = time_intervals[0]
	if stop == -1:
		stop = time_start 
	time_intervals = [time_start, stop] 
	task_attr[2][len(task_attr[2])-1] = time_intervals

def task_update_status(task, status):
	task_attr = list(task.values())[0]
	task_attr[0] = status

def task_compute_worktime(task):
	task_attr = list(task.values())[0]
	time_intervals = task_attr[2]
	total_time = 0
	for i in range(len(time_intervals)):
		total_time = total_time + time_intervals[i][1] - time_intervals[i][0]

	# convert to readable string 
	total_time = time.gmtime(total_time)
	total_time = time.strftime("%H hours %M mimutes %S seconds", total_time)
	return total_time 

def task_update_time(task):
	task_time = task_compute_worktime(currtask)
	task_attr = list(task.values())[0]
	task_attr[1] = task_time


while(True):
	timer_begin = input("start timer? reply 'yes' or 'ended':\n")
	if timer_begin == "yes":
		task_id = input("task name?:\n")
		if task_id in tasks.keys():
			currtask = {task_id: tasks[task_id]}
			#resume task timer 
			task_resume = time.time()
			task_update_status(currtask, "ongoing")
			task_add_interval(currtask, task_resume, task_resume)
		else:  
			task_status = "ongoing"
			task_time = "0" 
			#start timer
			task_start = time.time()
			task_break = task_start 
			currtask = task(task_id, task_status, task_time, [[task_start, task_break]])
			tasks[task_id] = currtask[task_id]

		print("timer started")	
		print(tasks)
		
		while(True):
			user_cmd = input("input cmd: break/cont/stop:\n")
			
			if user_cmd == "break":
					# print("{} in break: \n".format(task_id))
					task_break = time.time()
					task_update_stop(currtask, task_break)
					task_update_status(currtask, "in break")
					task_update_time(currtask)
					tasks.update(currtask)

					#store task to pending task 
					pending_task_stack.append(currtask)

					print(tasks)

			elif user_cmd == "cont":
				if (pending_task_stack):
					#retrieve task 
					currtask = pending_task_stack.pop(len(pending_task_stack)-1)
					#resume task timer 
					task_resume = time.time()
					task_update_status(currtask, "ongoing")
					task_add_interval(currtask, task_resume, task_resume)
					print(tasks)
				else:
					print("task already ongoing")

			elif user_cmd == "stop":
				# if called after "break," task status could be retrieved from stack 
				if (pending_task_stack):
					currtask = pending_task_stack.pop(len(pending_task_stack)-1)
				# if called after "start" or "cont", update current task terminate time 	
				else: 
					task_stop = time.time()
					task_update_stop(currtask, task_stop)

				task_update_status(currtask, "completed")

				# update total working time 
				task_update_time(currtask)
				tasks.update(currtask)

				#store task to complete queue 
				comp_task_queue[task_id] = currtask[task_id]
				print(tasks)

				break;

	elif timer_begin == ("ended"):
		# display time spent 
		print("today completed: ")
		print(comp_task_queue)

		break; 

log_path = './task_logs' 
os.makedirs(log_path,exist_ok=True) # create directory if needed 
filesuffix = 2  
log_name = ('%s-tasks.json' % (str(date.today())))

while os.path.exists(os.path.join(log_path, log_name)):
	log_name = ('%s-tasks(%s).json' % (str(date.today()), str(filesuffix)))

ff = open(os.path.join(log_path,log_name),'w+')
with ff:
    json.dump(comp_task_queue, ff, indent=4, sort_keys=True)


#       start 
#     /      \
# stop      break 
# |		  /      \
# print  stop    cont
# 		|       /    \ 
# 		print  stop   break 
# 				|
# 				print 
