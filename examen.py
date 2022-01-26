# Romain HENRY EPSI I2 DEV

import time
import datetime

global pump1_production
global pump2_production
global tank_current_storage
global tank_max_storage
global machine1_consumption
global machine2_consumption
global motor_stock_current_storage
global wheel_stock_current_storage

pump1_production = 10
pump2_production = 20
tank_current_storage = 0
tank_max_storage = 50
machine1_consumption = 25
machine2_consumption = 5
motor_stock_current_storage = 0
wheel_stock_current_storage = 0

global final_time

begin_time = datetime.datetime.now()
final_time = begin_time + datetime.timedelta(minutes=1)

stop_thread = False

class my_task():

    name = None
    priority = -1
    period = -1
    execution_time = -1
    next_ready_time = -1
    state = "SLEEPING"


    def __init__(self, name, priority, period, execution_time):

        self.name = name
        self.priority = priority
        self.period = period
        self.execution_time = execution_time
        self.next_ready_time = datetime.datetime.now()
        self.state = "READY"


    def update_state(self):

        if self.next_ready_time < datetime.datetime.now() :
            
            current_task.state = "READY"

        print("\t" + self.name + " : " + self.state + "\t(Deadline = " + self.next_ready_time.strftime("%H:%M:%S") + ", Priority = " + str(self.priority) + ")")



    def run(self):

        global pump1_production
        global pump2_production
        global tank_current_storage
        global tank_max_storage
        global machine1_consumption
        global machine2_consumption
        global motor_stock_current_storage
        global wheel_stock_current_storage

        # Update execution_time
        self.next_ready_time  += datetime.timedelta(seconds=self.period)

        # Start task
        print("\t" + self.name + " : Starting (" + datetime.datetime.now().strftime("%H:%M:%S") + ")")

        self.state = "RUNNING"

        time.sleep(self.execution_time)

        if self.name == "Pump 1":
            tank_current_storage += pump1_production
            if tank_current_storage > tank_max_storage:
                tank_current_storage = tank_max_storage
            print("\t" + self.name + " : produce " + str(pump1_production) + " oil - Current tank storage : " + str(tank_current_storage))

        elif self.name == "Pump 2":
            tank_current_storage += pump2_production
            if tank_current_storage > tank_max_storage:
                tank_current_storage = tank_max_storage
            print("\t" + self.name + " : produce " + str(pump2_production) + " oil - Current tank storage : " + str(tank_current_storage))

        elif self.name == "Machine 1":
            if tank_current_storage >= machine1_consumption:
                tank_current_storage -= machine1_consumption
                motor_stock_current_storage +=1
                print("\t" + self.name + " : produce 1 motor - Current tank storage : " + str(tank_current_storage) + " - Current motor stock storage : " + str(motor_stock_current_storage))


        elif self.name == "Machine 2":
            if tank_current_storage >= machine2_consumption:
                tank_current_storage -= machine2_consumption
                wheel_stock_current_storage +=1
                print("\t" + self.name + " : produce 1 wheel - Current tank storage : " + str(tank_current_storage) + " - Current wheel stock storage : " + str(wheel_stock_current_storage))
        else:
            return


        # Stop task
        print("\t" + self.name + " : Ending (" + datetime.datetime.now().strftime("%H:%M:%S") + ")")

        self.state = "SLEEPING"


####################################################################################################
#
#
#
####################################################################################################
if __name__ == '__main__':


    # Instanciation of task objects
    task_list = []
    task_list.append(my_task(name="Pump 1", 	priority=3, period=5, 	execution_time=2))
    task_list.append(my_task(name="Pump 2", 	priority=3, period=15, 	execution_time=3))
    task_list.append(my_task(name="Machine 1", 	priority=1, period=5, 	execution_time=5))
    task_list.append(my_task(name="Machine 2", 	priority=1, period=5, 	execution_time=3))


    while(not stop_thread):

        time_now = datetime.datetime.now()

        print("\nScheduler : " + time_now.strftime("%H:%M:%S"))


        # Update task state : SLEEPING => READY
        for current_task in task_list:
                
            current_task.update_state()

        # Search for task with higher priority
        task_to_run = None
        task_higher_priority = 0

        for current_task in task_list:

            if tank_current_storage == tank_max_storage:
                if current_task.name == "Pump 1" or "Pump 2":
                    current_task.priority = 1
            
            if wheel_stock_current_storage / 4 > motor_stock_current_storage:
                if current_task.name == "Machine 1":
                    current_task.priority = 3
                if current_task.name == "Machine 2":
                    current_task.priority = 1
            
            if wheel_stock_current_storage / 4 < motor_stock_current_storage:
                if current_task.name == "Machine 1":
                    current_task.priority = 1
                if current_task.name == "Machine 2":
                    current_task.priority = 3
            
            if tank_current_storage == 0:
                if current_task.name == "Pump 1" or "Pump 2":
                    current_task.priority = 3


            if (current_task.state == "READY") & (current_task.priority > task_higher_priority) :
            
                task_higher_priority = current_task.priority
                task_to_run = current_task

        now = datetime.datetime.now()

        if now < final_time:
            # Start task
            if task_to_run == None :
                time.sleep(5)
                
            else :
                task_to_run.run()
        else:
            print("System Shutdown")
            print("Total Production in one minute")
            print("Motor Production : " + str(motor_stock_current_storage) + " - Wheel Production : " + str(wheel_stock_current_storage))
            number_couple_moteur_wheels = 0
            while(1):
                if motor_stock_current_storage >=1 and wheel_stock_current_storage >= 4:
                    number_couple_moteur_wheels +=1
                    motor_stock_current_storage -= 1
                    wheel_stock_current_storage -= 4
                else:
                    break
            print("Number of couple (1 moteur and 4 wheels) created : " + str(number_couple_moteur_wheels))

            stop_thread = True
