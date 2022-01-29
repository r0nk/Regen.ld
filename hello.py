#!/bin/python
import discord
from discord.ext import commands
import sqlite3
import time
import maya
from datetime import datetime
from dateutil.relativedelta import relativedelta

con = sqlite3.connect('regen.db')
cur = con.cursor()
def initalize_databases():
    cur.execute("CREATE TABLE IF NOT EXISTS Users ( User_ID   STRING PRIMARY KEY, User_Name STRING);")
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS Tasks ( Task_ID       INTEGER PRIMARY KEY AUTOINCREMENT, Task_Name     STRING   NOT NULL, Task_Due_Date DATETIME, Task_Est_Min  INTEGER); ")
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS User_Tasks ( User_ID           STRING  REFERENCES Users (User_ID), Task_ID           INT     REFERENCES Tasks (Task_ID), Task_Is_Completed BOOLEAN DEFAULT (FALSE) ); ")
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS Scheduler (  User_ID   STRING PRIMARY KEY REFERENCES User_Tasks (User_ID),     Task_List STRING REFERENCES Tasks (Task_Name),    Date      DATE);  ")
    con.commit()

initalize_databases()

class Task:
  def __init__(self, name, due,time_est):
    self.name = name
    self.due = due
    self.time_est = time_est
    taskList = []

  def set_task(self, name):
    self.name = name;

def task_urgency(t):
    n = datetime.now()
    rd = relative_delta(n,t.due)
    hours_till_deadline=(rd.days*24+rd.hours)
    return 1 - (hours_till_deadline + (t.time_est/10))

#https://stackoverflow.com/questions/16891340/remove-a-prefix-from-a-string
def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text  # or whatever

def help_task(msg):
    # Gives a message informing the user of the current commands for the bot
    return "**Thank you for using regen.ld!**\n\
regen.ld currently has four commands for users' disposal:\n\
**/add_task** ~ This command allows you to add a task with the ability to specify date and time.\n\
*-EX: /add_task Task-Final due:Friday time_est:60*\n\
**/show_tasks** ~ This command lists your current tasks with their deadlines in order of urgency.\n\
*-EX: Art_Project:2022-01-29 09:17:36 time estimate (minutes): 60*\n\
*Science_Homework:2022-01-29 09:23:04 time estimate (minutes): 60*\n\
*Math_Exam:2022-01-29 09:24:44 time estimate (minutes): 60*\n\
**/edit_task** ~ This command allows one to edit the date and time expectation of a task.\n\
*-EX: /edit_task Math_Exam due:feb28 time_est:120*\n\
**/finish_task** ~ This command allows you to remove a task from your personal task list.\n\
*EX: /finish_task Art_Project*"

def read_task_from_message(msg):
    t = Task("placeholder_tn",datetime.now(),60)
    for i in msg.split()[1:]:
        if "@" in i:
            #TODO handle user role tagging
            print("TODO handle user role tagging")
        elif "due:" in i:
            s=remove_prefix(i,"due:")
            t.due=maya.when(s).datetime()
        elif "time_est:" in i or "time_estimate:" in i:
            s=remove_prefix(i,"time_est:")
            t.time_est=int(s)
        else:
            t.name=i
    return t

def add_task(msg):
    ret = ""
    t = read_task_from_message(msg) 
    if t.name == "placeholder_tn":
        return "No name found, task not added."
    cur.execute("insert into Tasks (Task_Name,Task_Due_Date,Task_Est_Min) values ( ?,datetime(),?)",(t.name,t.time_est))
    con.commit()
    return "Task "+t.name+" added! Due at "+t.due.strftime('%m/%d/%Y')+" and it should take "+str(t.time_est)+" minutes"

def finish_task(msg):
    for i in msg.split()[1:]:
        #TODO this should check if no other member has this task before deleting,
        #TODO this is write that the task was completed to the completed tasks log
        cur.execute("DELETE FROM Tasks WHERE Task_Name = '?';",(i,))
        con.commit()

def edit_task(msg):
    t = read_task_from_message(msg)
    cur.execute("update Tasks set Task_Due_Date=(?) where Task_Name = (?)",(t.due,t.name))
    cur.execute("update Tasks set Task_Est_Min=(?) where Task_Name = (?)",(t.time_est,t.name))
    return "Task "+t.name+" updated!"

def show_tasks(msg):
    #TODO this should only show tasks that are assigned to the user calling
    cur.execute("select * from Tasks")
    ret=""
    for name in cur.fetchall():
        ret = ret + "* " + name[1] + "\t"+name[2]+"\t"+str(name[3])+"m\n"
    return ret

def shedule(msg):
    return "TODO schedule here"

#for each possible command, send it to its resepective function and 
# send the user back its output
async def handle_message(message):
    #Docs https://discordpy.readthedocs.io/en/stable/api.html?highlight=message#discord.Message
    #TODO message.mentions targets a list of users
    #TODO role_mentions gets a list of roles
    #TODO also role.members
    if message.content.lower().startswith("/add_task") or message.content.lower().startswith("/add") or message.content.lower().startswith("/a"):
        #if no there is no : then due date is set to a week
        # await message.channel.send(task + " added!")
        await message.channel.send(add_task(message.content.lower()))
        #just lists commands
    elif message.content.lower().startswith("/show_tasks") or message.content.lower().startswith("/show") or message.content.lower().startswith("/s"):
        await message.channel.send(show_tasks(message.content.lower()))
    elif message.content.lower().startswith("/finish_task") or message.content.lower().startswith("/finish") or message.content.lower().startswith("/f"):
        await message.channel.send(finish_task(message.content.lower()))
    elif message.content.lower().startswith("/edit_task") or message.content.lower().startswith("/edit") or message.content.lower().startswith("/e"):
        await message.channel.send(edit_task(message.content.lower()))
    elif message.content.lower().startswith("/schedule") or message.content.lower().startswith("/sched") or message.content.lower().startswith("/s"):
        await message.channel.send(schedule(message.content.lower()))
    elif message.content.lower().startswith("/help"):
        await message.channel.send(help_task(message.content.lower()))
    else:
        await message.channel.send("hmmm...try again")


#handle the discord interface
class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content[0] == '/':
            print(message.author,":",message.content)
            #recieve task, optional date
            await handle_message(message)

client = MyClient()
client.run((open('token.txt','r').read().splitlines()[0]));
con.close()
