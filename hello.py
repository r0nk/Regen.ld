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

        if message.content[0] == '*':
            print(message.author,":",message.content)
            if message.content.lower().startswith("*hello"):
                await message.channel.send("hello world!")

client = MyClient()
client.run((open('token.txt','r').read().splitlines()[0]));
con.close()

