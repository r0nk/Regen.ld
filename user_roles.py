# Here's what I found but I am not super familiar with "@" or "async"
# so I don't know if i could tell you exactly what I'm looking at.
@bot.command()
async def roles(...):
    rolelist = [r.mention for r in user.roles if r != ctx.guild.default_role]
roles = ", ".join(rolelist)
