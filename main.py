from discord.ext import commands, tasks
import discord
import json
import random

with open("messages.txt", "r", encoding="utf-8") as f:

    messages = f.readlines()

with open("data.json", "r", encoding="utf-8") as f:

    read = json.load(f)

with open("dm.txt", "r", encoding="utf-8") as f:

    dmmessage = f.read()


bot = commands.Bot(command_prefix="!", help_command=None, user_bot=True)


@tasks.loop(seconds=read["timeout"])
async def sendmsg():

    channel = bot.get_channel(read["kanalid"])

    await channel.send(random.choice(messages))


@bot.event
async def on_ready():

    print(f"{bot.user} account is logged in!")

    await bot.change_presence(status=discord.Status.idle, activity=discord.Game(read["status"]))

    sendmsg.start()


@bot.event
async def on_message(payload):

    with open("log.txt", "+r", encoding="utf-8") as f:

        if not f"{payload.author}\n" in f.readlines():
            
            f.seek(0)

            if not bot.user.id == payload.author.id:

                if payload.channel.type == discord.ChannelType.private:

                    await payload.channel.send(dmmessage)

                    f.write(f"{payload.author}\n")
                    f.close()

                else:

                    channel = bot.get_channel(read["kanalid"])

                    if payload.channel.id == channel.id:

                        if "" in payload.content:

                            dm = await payload.author.create_dm()

                            await dm.send(dmmessage)

                            f.write(f"{payload.author}\n")
                            f.close()


bot.run(read["token"])
