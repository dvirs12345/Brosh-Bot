# Author - Dvir Sadon & Stav Byevsky (At least 1 line)
import discord
from discord.ext import commands
import re
import os
from dotenv import load_dotenv
from exceptions import NoRegexMatchException, RoleNotFoundException, NewcomerRoleNotFoundException

load_dotenv()

TOKEN = os.environ.get('DISCORD_TOKEN')
WELCOME_CHANNEL_NAME = "הרשמה"
NEWCOMER_ROLE_NAME = "מחוסר צוות"

intents = discord.Intents.default()
intents.message_content = True
intents.presences = True
intents.members = True
bot = commands.Bot(intents=intents, command_prefix='!')


@bot.event
async def on_message(message):
    if not message.author.bot \
            or not isinstance(message.channel, discord.TextChannel):
        if "קאדר" in message.content:
            await message.channel.send("קאדרים עושים ביחד")
    await startswith_commands(message)

    await bot.process_commands(message)


@bot.event
async def on_member_join(member: discord.Member):
    newcomer_role = discord.utils.get(member.guild.roles, name=NEWCOMER_ROLE_NAME)
    if newcomer_role is None:
        print("Bruh where newcomer role")
        return
    await member.add_roles(newcomer_role)
    await member.send("היי, {} :)\n"
                      "ברוכים הבאים לשרת דיסקורד של גדוד ברוש!\n"
                      "כדי להירשם, כנסו לשרת וכתבו בערוץ \"{}\" את שמכם המלא ואת מספר הצוות שלכם כך \"<שם מלא> <מספר צוות>\", למשל:"
                      "\n דביר סעדונוביץ' 22"
                      "\n\nתודה ❤️"
                      .format(member.name, WELCOME_CHANNEL_NAME))


@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))


# @bot.command(name="קאדר")
# async def kader(ctx):
#     await ctx.send("קאדרים עושים ביחד")


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
        if not str(ctx.message.author).split("#")[0] == "":
            voice = await ctx.message.author.voice.channel.connect()
            source = discord.FFmpegPCMAudio('yada_eghh.wav')
            player = voice.play(source)


async def startswith_commands(message: discord.Message):
    if message.author.bot \
            or not isinstance(message.channel, discord.TextChannel) \
            or message.channel.name != WELCOME_CHANNEL_NAME \
            or len(message.author.roles) > 2:
        return

    try:
        name, team = get_credentials_from_message(message.content)

        author = message.author
        team_role = discord.utils.get(author.guild.roles, name="צוות" + " " + str(team))
        newcomer_role = discord.utils.get(author.guild.roles, name=NEWCOMER_ROLE_NAME)
        if team_role is None:
            raise RoleNotFoundException
        if newcomer_role is None:
            raise NewcomerRoleNotFoundException

        await author.edit(nick=name)
        await author.add_roles(team_role)
        if newcomer_role in author.roles:
            await author.remove_roles(newcomer_role)

        messages_to_delete = []
        channel = message.channel
        async for message_in_channel in channel.history(limit=200):
            if message_in_channel.reference is None or message_in_channel.reference.message_id is None:
                continue
            referenced_message = None
            try:
                referenced_message = await channel.fetch_message(message_in_channel.reference.message_id)
            except Exception as exception:
                print("Message fetch error (id: {}) - {}".format(message_in_channel.reference.message_id, exception))
                continue

            is_message_reply_to_author = referenced_message.author.id == author.id
            if message_in_channel.author.id == author.id \
                    or is_message_reply_to_author:
                messages_to_delete.append(message_in_channel)
        await channel.delete_messages(messages_to_delete)

        await author.send("היי {}, נרשמת בהצלחה לשרת, כעת יש לך גישה לכלל הערוצים של הפלוגה ושל צוות {}!"
                          .format(name, team))
    except NoRegexMatchException:
        await message.reply("הודעה לא תקינה")
    except RoleNotFoundException:
        await message.reply("צוות לא תקין")
    except NewcomerRoleNotFoundException:
        print("Bruh where newcomer role")
        await message.reply("תקלה, אנא נסו שנית")


def get_credentials_from_message(str1):
    match = re.match("(.+ .+) ([0-9]+)", str1)
    if match is None or len(match.groups()) != 2:
        raise NoRegexMatchException

    name = match.group(1)
    team = match.group(2)
    name = name.replace("צוות ", "")
    return name, team


bot.run(TOKEN)
