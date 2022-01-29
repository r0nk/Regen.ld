#!/bin/python
import discord
from discord.ext import commands
import sqlite3
import time
from datetime import datetime

con = sqlite3.connect('regen.db')
cur = con.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS Users ( User_ID   STRING PRIMARY KEY, User_Name STRING);")
con.commit()

cur.execute("CREATE TABLE IF NOT EXISTS Tasks ( Task_ID       INTEGER PRIMARY KEY AUTOINCREMENT, Task_Name     STRING   NOT NULL, Task_Due_Date DATETIME, Task_Est_Min  INTEGER); ")
con.commit()

cur.execute("CREATE TABLE IF NOT EXISTS User_Tasks ( User_ID           STRING  REFERENCES Users (User_ID), Task_ID           INT     REFERENCES Tasks (Task_ID), Task_Is_Completed BOOLEAN DEFAULT (FALSE) ); ")
con.commit()

class Task:
  def __init__(self, name, due,time_est):
    self.name = name
    self.due = due
    self.time_est = time_est
    taskList = []

  def set_task(self, name):
    self.name = name;

def add_task(msg):
    ret = ""
    t = Task("placeholder_tn",datetime.now(),60)
    for i in msg.split()[1:]:
        if "due:" in i:
            print("TODO handle due \n")
        else:
            t.name=i
    if t.name == "placeholder_tn":
        return "No name found, task not added."
    cur.execute("insert into Tasks (Task_Name,Task_Due_Date,Task_Est_Min) values ( ?,datetime(),?)",(t.name,t.time_est))
    con.commit()
    return "Task added!"

def finish_task(msg):
    for i in msg.split()[1:]:
        cur.execute("DELETE FROM Tasks WHERE Task_Name = '?';",(i,))
        con.commit()

def show_tasks(msg):
    cur.execute("select * from Tasks")
    ret=""
    for name in cur.fetchall():
        ret = ret + "* " + name[1] + "\n"
    return ret

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

            if message.content.lower().startswith("/add_task"):
                #if no there is no : then due date is set to a week
               # await message.channel.send(task + " added!")
                await message.channel.send(add_task(message.content.lower()))
                #just lists commands
            elif message.content.lower().startswith("/show_tasks"):
                await message.channel.send(show_tasks(message.content.lower()))
            elif message.content.lower().startswith("/finish_task"):
                await message.channel.send(finish_task(message.content.lower()))
            else:
                await message.channel.send("hmmm...try again")


client = MyClient()
client.run((open('token.txt','r').read().splitlines()[0]));
con.close()
