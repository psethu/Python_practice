# Author: Sethu Prakasam
# Program description: Modifying global variables within threads which have been spawned in processes which have also been created in this program.
# Details: Processes have their own address space. This is why we need thread_client2 to affect a global variable global_num

from multiprocessing import Process
import threading

NUM_PROCESSES = 3

processes = []
a_list = []
global_num = 0

def sending_events_thread(process_num, thread_num):
	name = process_num+"___"+threading.currentThread().getName()
	#print(name+"---start")
	global global_num
	for i in range(1000000):
		global_num += 1
	print(name+"---"+str(global_num))
	#print(name+"---end")

def function_processes(name, a_list):
	# log process at start
	print(name+"---start")
	# do computations
	for i in range(10000000): # 10 million test
		pass
	process_num = name[-1]
	a_list.append(process_num) # 1, 2, or 3
	a_list.append(process_num+process_num) # 11, 22, or 33

	#for val in a_list:
	#	print(name+"---"+val)

	thread_client = threading.Thread(target=sending_events_thread, args=([process_num, global_num]))
	thread_client2 = threading.Thread(target=sending_events_thread, args=([process_num, global_num]))
	#thread_client3 = threading.Thread(target=sending_events_thread, args=([process_num, global_num]))

	thread_client.start()
	thread_client2.start()
	#thread_client3.start()

	thread_client.join()
	thread_client2.join()
	#thread_client3.join()

	# log process at end
	#print(name+"---end")

for i in range(NUM_PROCESSES):
	process_name = "process_"+str(i+1)
	processes.append(Process(target=function_processes, args=[process_name, a_list]))

for p in processes:
	p.start()

for p in processes:
	p.join()
