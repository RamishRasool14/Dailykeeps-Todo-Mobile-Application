import pytest
from model import App
import uuid

def testAddTask(): # Creates random 10 tasks and tests if they are correctly added to the system
    a1 = App()
    tasks1 = [a1.createRandomTask() for x in range(10)]

    for task in tasks1:
        a1.addTask(task)

    for ind, added_task in enumerate(a1.tasks):
        assert added_task == tasks1[ind] , "Test Failed"

    del a1

def testChangeOrder(): # Creates random 10 tasks and change order of the first and last task
    a2 = App()
    tasks2 = [a2.createRandomTask() for x in range(10)]
    for task in tasks2:
        a2.addTask(task)

    a2.changeOrder(tasks2[-1],tasks2[0])

    assert a2.tasks[0] == tasks2[-1] , "Test Failed"
    assert a2.tasks[-1] == tasks2[0] , "Test Failed"
    
    for ind in range(1,9):
        assert a2.tasks[ind] == tasks2[ind] , "Test Failed"

    del a2

def testDeleteTask():
    a3 = App()
    tasks3 = [a3.createRandomTask() for x in range(5)]
    for task in tasks3:
        a3.addTask(task)

    a3.deleteTask(tasks3[2])
    assert a3.tasks[0] == tasks3[0] , "Test Failed"
    assert a3.tasks[1] == tasks3[1] , "Test Failed"
    assert a3.tasks[2] == tasks3[3] , "Test Failed"
    assert a3.tasks[3] == tasks3[4] , "Test Failed"

def testEditTask():
    a4 = App()
    tasks4 = [a4.createRandomTask() for x in range(5)]
    for task in tasks4:
        a4.addTask(task)

    tasks4[-1].owner_id = 1234
    a4.editTask(-1,tasks4[-1])
    assert a4.tasks[0] == tasks4[0] , "Test Failed"

def testMarkComplete():
    a5 = App()
    tasks5 = [a5.createRandomTask() for x in range(5)]
    for task in tasks5:
        a5.addTask(task)

    a5.markComplete(-1)
    tasks5[-1].done = True
    assert a5.tasks[-1] == tasks5[-1] , "Test Failed"
        