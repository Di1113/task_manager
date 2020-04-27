import os
import json
import time
from datetime import date

# todo 
# print out task in chronological order 
# add log summary, like total work hour, break hour, start and end time, last hours 
def conver2report(log_path):
    report = "## log: %s\n" % os.path.basename(log_path)
    report += "===============================================\n"
    with open(log_path,'r') as f:
        task_logs = json.load(f)
    task_i = 0
    for task in task_logs.items():
        task_index = task_i
        task_name, task_descrip = task 
        status, total_time, time_intervals = task_descrip
        time_log = "    task: \#%d\n    name: %s \n  status: %s \n" % (task_i, task_name, status)
        time_log += "   spent: %s\n" % total_time
        
        for i in range(len(time_intervals)):
            time_log += "-----------------------------------------------\n"
            start, stop = time_intervals[i]
            duration = time.gmtime(stop - start) 
            # slot_index = str(time_intervals.index(time_slots))
            # start, stop = time_slots
            start_time = time.asctime(time.localtime(start))
            stop_time = time.asctime(time.localtime(stop))
            duration_time = time.strftime("%H hours %M mimutes %S seconds", duration)
            time_log += " session: \#%d \n" % i
            time_log += "duration: %s\n" % duration_time
            time_log += "   start: %s \n    stop: %s \n" % (start_time, stop_time)
            if i != (len(time_intervals)-1):
                breaktime = time.gmtime(time_intervals[i+1][0] - time_intervals[i][1])
                break_time = time.strftime("%H hours %M mimutes %S seconds", breaktime)
                time_log += "   break: %s\n" % break_time
        time_log += "===============================================\n"
        report += time_log
        task_i += 1 
    return report
    # print(report)	
        # print(task_name)


log_dir = "./task_logs"
log_name = "2020-04-27-tasks.json"
log_path = os.path.join(log_dir,log_name)
report_path = './task_reports' 
os.makedirs(report_path,exist_ok=True) # create directory if needed 
filesuffix = 1  
report_name = ('%s-report.md' % (str(date.today())))

if os.path.exists(os.path.join(report_path, report_name)):
    log_name = ('%s-report(%s).md' % (str(date.today()), str(filesuffix)))

report = conver2report(log_path)
print("dsf")
print(report)
print(report,  file=open(os.path.join(report_path,report_name),'w+'))
# ff = open(os.path.join(report_path,report_name),'w+')
# with ff:
#     ff.write(report)      
#     # print(report, file=ff)
#     ff.close()
