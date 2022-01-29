#!/bin/python
import discord
from discord.ext import commands

class Task:
  def __init__(self, name, due):
    self.name = name
    self.due = due
    taskList = []

  def set_task(self, name):
    self.name = name;


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content[0] == '/':
            print(message.author,":",message.content)
            if message.content.lower().startswith("/hello"):
                await message.channel.send("hello world!")
                #recieve task, optional date
            else if message.content.lower().startswith("/add_task"):
                #if no there is no : then due date is set to a week
                task = message.content.slice(1).split(' '); # Split all spaces so you can get the command out of the message
                await message.channel.send(task + " added!")
                #just lists commands
            else if message.content.lower().startswith("/show_tasks"):
                await message.channel.send("This is a list of tasks")
            else if message.content.lower().startswith("/finish_task"):
                await message.channel.send("mark a task as completed for a user")
            else
                await message.channel.send("hmmm...try again")


client = MyClient()
client.run((open('token.txt','r').read().splitlines()[0]));
con.close()
