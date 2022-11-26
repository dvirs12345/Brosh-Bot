# Author - Dvir Sadon
import discord
import random
from discord.ext import commands
from discord import FFmpegPCMAudio


TOKEN = "ODg5ODQ3MDk5OTIxOTMyMzEw.YUnMsQ.ktgnoV3yt55Qy6oIjF5LSZsUQ4c"


bot = commands.Bot(command_prefix='!')


@bot.event
async def on_message(message):
    print(message.content)

    await bot.process_commands(message)


@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))


@bot.command(name="hello")
async def hello(ctx):
    await ctx.send("Hello there " + str(ctx.message.author).split("#")[0])


@bot.command(name="קאדר")
async def bruh(ctx):
    await ctx.send("קאדרים עושים ביחד")


@bot.command(name="random")
async def random_func(ctx):
    args = ctx.message.content.split(" ")[1::]
    if len(args) > 2 or len(args) <= 0:
        return
    elif len(args) == 1:
        await ctx.send(str(random.randint(0, int(args[0]))))
    else:
        await ctx.send(str(random.randint(int(args[0]), int(args[1]))))


@bot.command(name="snail")
async def snail(ctx):
    username = str(ctx.message.author).split("#")[0]
    if snails.snail_exists(username):
        await ctx.send(snails.get_snail_by_owner(username).toString())
    else:
        # Create new snail
        mySnail = Snail("Default", username)
        snails.add_snail(mySnail)
        await ctx.send("New snail was created")


@bot.command(name="setname")
async def setname(ctx, arg):
    snails.set_name(str(ctx.message.author).split("#")[0], arg)


@bot.command(name="race")
async def race(ctx):
    args = ctx.message.content.split(" ")[1::]
    if args:
        username = str(ctx.message.author).split("#")[0]
        myrace = make_race(args, username)
        myrace.simulate_game()
        results = myrace.get_leaderboard()
        await ctx.send(get_race_results_to_display(results))
        add_race_exp(results)


@bot.command(name="ping")
async def ping(ctx):
    ctx.send("pong")


@bot.command(name="pong")
async def pong(ctx):
    ctx.send("ping")


@bot.command(name="vcjoin")
async def join(ctx):
    if ctx.author.voice:
        voice = await ctx.message.author.voice.channel.connect()
    else:
        await ctx.send("Cant join when you are not in a vc")


@bot.command(name="vcleave")
async def leave(ctx):
    if ctx.voice_client.is_connected():
        await ctx.guild.voice_client.disconnect()
    else:
        await ctx.send("I am not in a voice channel")


@bot.command(name="korn")
async def korn(ctx):
    if ctx.author.voice:
        if not str(ctx.message.author).split("#")[0] == "SBCPackers":
            voice = await ctx.message.author.voice.channel.connect()
            source = FFmpegPCMAudio('yada_eghh.wav')
            player = voice.play(source)

        else:
            await ctx.send("Fuck off palomo")
    else:
        await ctx.send("You are not in a voice channel")


def make_race(args, owner):
    race_snails = [snails.get_snail_by_owner(owner)]
    for i in args:
        race_snails.append(snails.get_snail_by_owner(i))

    return Race(race_snails)


def get_race_results_to_display(results):
    to_display = ""
    print(results)
    for i in range(len(results)):
        to_display += (str(i + 1) + ". " + str(results[i][0]) + ": " + str(results[i][-1]) + "\n")

    return to_display


def add_race_exp(results):
    for i in range(len(results)):
        current_snail = snails.get_snail_by_owner(results[i][0])
        current_snail.update_exp(len(results) - i - 1)
        snails.update_level(current_snail.update_exp(len(results) - i - 1) - current_snail.get_level())
        snails.update_exp(owner=results[i][0], new_exp=len(results) - i - 1)


# client.run(TOKEN)
bot.run(TOKEN)
