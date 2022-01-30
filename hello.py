#!/bin/python
import discord
from discord.ext import commands
import sqlite3
import time
import maya
import random
from datetime import datetime
from dateutil.relativedelta import relativedelta

con = sqlite3.connect('regen.db')
cur = con.cursor()
def initalize_databases():
    cur.execute("CREATE TABLE IF NOT EXISTS Tasks (    User_ID        STRING,    Task_Name      STRING,   Scheduled_Date DATE,    Due_Date       DATETIME,    Time_Est       INTEGER,    Tags           STRING,    State          STRING);")
    con.commit()

initalize_databases()

class Task:
  def __init__(self, name, due,time_est):
    self.name = name
    self.due = due
    self.time_est = time_est
    self.urgency = task_urgency(self)
    taskList = []

  def set_task(self, name):
    self.name = name;

def task_urgency(t):
    n = datetime.now()
    rd = relativedelta(n,t.due)
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
**/add_task** or **/at** ~ This command allows you to add a task with the ability to specify date and time.\n\
*-EX: /add_task Task-Final due:Friday time_est:60*\n\
**/show_all** or **/sa** ~ This command lists your current tasks with their deadlines in order of urgency.\n\
*-EX: Art_Project:2022-01-29 09:17:36 time estimate (minutes): 60*\n\
*Science_Homework:2022-01-29 09:23:04 time estimate (minutes): 60*\n\
*Math_Exam:2022-01-29 09:24:44 time estimate (minutes): 60*\n\
**/edit_task** or **/et** ~ This command allows one to edit the date and time expectation of a task.\n\
*-EX: /edit_task Math_Exam due:feb28 time_est:120*\n\
**/finish_task** or **/ft** ~ This command allows you to remove a task from your personal task list.\n\
*-EX: /finish_task Art_Project*\n\
**/add_schedule** or **/as** ~ This command allows you to schedule tasks for today (Limited up to 8 time estimated hours). \n\
*-EX: ADD SOMETHING HERE FOR \schedule \n\
**/show_schedule** or **/ss** ~ This command lets you to view today's schedule. \n\
*-EX: /show_today* \n\
**/show_employee** or **/se** ~ This command shows employee statistical data. \n\
*-EX: /show_employee*"


def read_task_from_message(msg):
    t = Task("placeholder_tn",datetime.now(),60)
    for i in msg.split()[1:]:
        if "@" in i:
            continue
        elif "due:" in i:
            s=remove_prefix(i,"due:")
            t.due=maya.when(s).datetime()
        elif "time_est:" in i or "time_estimate:" in i:
            s=remove_prefix(i,"time_est:")
            t.time_est=int(s)
        else:
            t.name=i
    return t

def task_sort_key(t):
    return t.urgency

def get_tasks_from_database():
    cur.execute("select * from Tasks")
    task_list=[]
    for name in cur.fetchall():
        t = Task("placeholder_tn",datetime.now(),60)
        t.name = name[1]
        t.due_date=name[3]
        t.time_est=name[4]
        task_list.append(t)
    task_list.sort(key=task_sort_key,reverse=True)
    return task_list

def add_task(user,t):
    if t.name == "placeholder_tn":
        return "No name found, task not added."
    cur.execute("insert into Tasks (User_ID,Task_Name,Due_Date,Time_Est,State) values ( ?,?,?,?,?)",(user.id,t.name,t.due,t.time_est,"NEW"))
    con.commit()
    return "Task "+t.name+" added! Due at "+t.due.strftime('%m/%d/%Y')+" and it should take "+str(t.time_est)+" minutes"

def finish_task(user,msg):
    t = read_task_from_message(msg)
    for i in msg.split()[1:]:
        cur.execute("update Tasks set state='complete' where User_ID = (?) and Task_Name = (?)",(user.id,t.name))
        con.commit()
    return "Task "+t.name+" finished!"

def edit_task(msg):
    t = read_task_from_message(msg)
    cur.execute("update Tasks set Due_Date=(?) where Task_Name = (?)",(t.due,t.name))
    cur.execute("update Tasks set Task_Est_Min=(?) where Task_Name = (?)",(t.time_est,t.name))
    return "Task "+t.name+" updated!"

def show_tasks(user,msg):
    cur.execute("select * from Tasks where State != 'complete' and User_ID = (?) ",(user.id,))
    ret=""
    for name in cur.fetchall():
        ret = ret + "* " + str(name[1]) + "\t"+name[3]+"\t"+str(name[4])+"m\n"
    return ret

def schedule(user,msg):
    tasks = get_tasks_from_database()
    minutes_to_work=8*60
    ret="ret"
    for t in tasks:
        cur.execute("update Tasks set Scheduled_Date = DATE('now') where User_ID = (?) and Task_Name = (?)",(user.id,t.name))
        con.commit()
        minutes_to_work=minutes_to_work-t.time_est
        print(t.name+" minutes_to_work:"+str(minutes_to_work))
        if minutes_to_work < 0:
            break
    return ret

def show_schedule(user,msg):
    cur.execute("select * from Tasks where Scheduled_Date = DATE('now') and User_ID = (?)",(user.id,))
    ret="Tasks to do today\n"
    task_count=0
    completed_count=0
    for name in cur.fetchall():
        task_count=task_count+1
        ret = ret + "* " + str(name[1]) + "\t"+name[3]+"\t"+str(name[4])+"m "
        if name[6] == 'complete':
            completed_count=completed_count+1
            ret= ret+ ":white_check_mark:"
        ret=ret+"\n"
    tasks = get_tasks_from_database()
    ret = ret + progress_bar(100*(completed_count/task_count))
    return ret

def progress_bar(amt, change_lenght_of_bar = 2):
	'''
	this function prints out a progress bar 
	based on a percentage form 0% to 100%.
	to shorten the progress bar increase change_lenght_of_bar number:
	1, 2, 5, 10 will produce equal bars
	1  = 100 ticks
	2  =  50 ticks
	5  =  20 ticks
	10 =  10 ticks
	'''

	# extended ascii codes needed to print out the progress bar
	em = bytes([176]).decode('cp437')
	full = bytes([178]).decode('cp437')

	not_amt = 100 - amt
	str = full * round(amt/change_lenght_of_bar) + em * round(not_amt/change_lenght_of_bar)
	return str

def show_employee(msg):
    #gaming, cooking, breathing
    return "Steve Skill Tracking:\n" + progress_bar(random.randint(1,100)) + " gaming\n" + progress_bar(random.randint(1,100))  + " cooking\n" + progress_bar(random.randint(1,100)) + " breathing"

#for each possible command, send it to its resepective function and
# send the user back its output
async def handle_message(message):
    #Docs https://discordpy.readthedocs.io/en/stable/api.html?highlight=message#discord.Message
    mcl=message.content.lower()
    ma=message.author
    if mcl.startswith("/add_task") or mcl.startswith("/at"):
        #if no there is no : then due date is set to a week
        t = read_task_from_message(mcl)
        for member in message.mentions:
            add_task(member,t)
        for r in message.role_mentions:
            for member in r.members:
                add_task(member,t)
        await message.channel.send(add_task(ma,t))
        await message.channel.send(file=discord.File('gifs/to-do.gif'))
        #just lists commands
    elif mcl.startswith("/show_all") or mcl.startswith("/sa"):
        await message.channel.send(show_tasks(ma,mcl))
    elif mcl.startswith("/finish_task") or mcl.startswith("/ft"):
        await message.channel.send(finish_task(ma,mcl))
        await message.channel.send(file=discord.File('gifs/celebration.gif'))
    elif mcl.startswith("/edit_task") or mcl.startswith("/et"):
        await message.channel.send(edit_task(ma,mcl))
    elif mcl.startswith("/add_schedule") or mcl.startswith("/as"):
        await message.channel.send(schedule(ma,mcl))
    elif mcl.startswith("/show_schedule") or mcl.startswith("/ss"):
        await message.channel.send(show_schedule(ma,mcl))
    elif mcl.startswith("/show_employee") or mcl.startswith("/se"):
        await message.channel.send(show_employee(mcl))
    elif mcl.startswith("/help"):
        await message.channel.send(help_task(mcl))
        await message.channel.send(file=discord.File('gifs/help_sent.gif'))
    else:
        await message.channel.send("hmmm...try again")


#handle the discord interface
class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)
        print(datetime.now())

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
