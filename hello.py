#!/bin/python
import discord
from discord.ext import commands

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
            if message.content.lower().startswith("/add_task"):
                await message.channel.send("add task here")
            if message.content.lower().startswith("/show_tasks"):
                await message.channel.send("This is a list of tasks")
            if message.content.lower().startswith("/finish_task"):
                await message.channel.send("mark a task as completed for a user")

client = MyClient()
client.run((open('token.txt','r').read().splitlines()[0]));
con.close()

