import discord
from discord.ext import commands
import random
import subprocess
import sqlite3
import os
import time
import json
from datetime import datetime

con = sqlite3.connect('flag_transactions.db')
cur = con.cursor()

#x= { "name":"ctf one","description":"description of ctf","flag":"0xdeadbeef"}
#ctfs.append(x)
#print(json.dumps(ctfs))
ctfs = json.load(open('ctfs.json'))

flags = []
for ctf in ctfs:
    flags.append(ctf["flag"])
    print("flag: "+flags[-1])

cur.execute("CREATE TABLE IF NOT EXISTS transactions (date text,user text,flag text,unique(user,flag))")
con.commit()

def submit_flag(flag,user):
    if flag in flags:
        cur.execute("insert into transactions values (datetime(),?,?)",(str(user),str(flag)));
        con.commit()
        return "Flag submitted for user " + str(user) + "!"
    else:
        return "Flag not found!"

def flag_count(user):
    cur.execute("select count(*) from transactions where user = (?)",(str(user),));
    return cur.fetchall()[0][0]

def has_flag(user,flag):
    cur.execute("select count(*) from transactions where user = (?) and flag = (?) ",(str(user),str(flag)));
    return cur.fetchall()[0][0]==1

def count_command(user):
    ret = str(user)+" flags captured:" + str(flag_count(user)) + "\n"
    for ctf in ctfs:
        ret+="> "
	        ret+=ctf["name"]+ "\t"
        if has_flag(user,ctf["flag"]):
            ret+=":white_check_mark:"
        else:
            ret+=":x:"

        ret+="\n"
    return ret

def leaderboards():
    cur.execute("select distinct user from transactions")
    ret=""
    array=[]
    for name in cur.fetchall():
        array.append((name[0],flag_count(name[0])))
    array = (sorted(array,key=lambda a:a[1],reverse=True))
    ret+="Flags count \tName\n "
    for name,count in array:
        ret+="> "+str(count) + "\t" + str(name) + "\n"
    return ret

def run_cmd(cmd):
    result = subprocess.run(cmd,shell=True,stderr=subprocess.STDOUT,stdout=subprocess.PIPE)
    return result.stdout.decode("utf-8")

def get_last_update_time():
    return str(datetime.fromtimestamp(os.stat("operator.py").st_mtime))

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        if message.content[0] == '*':
            print(message.author,":",message.content)
            if message.content.lower().startswith("*flag"):
                await message.channel.send(submit_flag(message.content.split()[1],message.author))
            if message.content.lower().startswith("*count"):
                await message.channel.send(count_command(message.author))
            if message.content.lower().startswith("*leaderboard") or message.content.lower().startswith("*lb"):
                await message.channel.send(leaderboards())
            if message.content.lower().startswith("*version") or message.content.lower().startswith("*v"):
                await message.channel.send("Operator Bot Version 0.1 \n"+get_last_update_time())
            if message.content.lower().startswith("*help") or message.content.lower().startswith("*h"):
                await message.channel.send(open("helpfile.txt",'r').read())


client = MyClient()
client.run((open('token.txt','r').read().splitlines()[0]));
con.close()

