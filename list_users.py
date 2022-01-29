# This block creates and prints a member_list using
# the member.name values from the ctx.message.server.members list.

member_list = ''
for member in ctx.message.server.members:
    member_list += member.name
print(member_list)
