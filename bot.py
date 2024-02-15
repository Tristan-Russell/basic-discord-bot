# Imports
import json
import os
import requests
import discord
from discord import app_commands
from discord.ext import tasks
from dotenv import load_dotenv

# Load Environment
load_dotenv()

# Initialize Discord
intents = discord.Intents.all()
client = discord.Client(intents=intents)
intents.message_content = True
intents.members=True
tree = app_commands.CommandTree(client)

#Initialize global vars
GUILD_ID = os.environ.get('GUILD_ID')
MAIN_CHANNEL_ID = os.environ.get('MAIN_CHANNEL_ID')
TOKEN = os.environ.get('TOKEN')

# Commands

# # Hi Command
@tree.command(
    name="hi",
    description="I say hello",
    guild=discord.Object(id=GUILD_ID)
)
async def hi_command(interaction):
    await interaction.response.send_message("Hello!")

# # Ping Command
@tree.command(
    name="ping",
    description="Check bot's latency",
    guild=discord.Object(id=GUILD_ID)
)
async def ping_command(interaction):
    latency = round(client.latency * 1000)  # Convert to milliseconds
    await interaction.response.send_message(f"Pong! Latency: {latency}ms")
    
# # View Server Info Command    
@tree.command(
    name="serverinfo",
    description="Get information about the server",
    guild=discord.Object(id=GUILD_ID)
)
async def serverinfo_command(interaction):
    server = interaction.guild
    server_info = f'Server Icon: {server.icon}\nServer Name: {server.name}\nMembers: {server.member_count}'
    await interaction.response.send_message(server_info)

# # View users avatar Info Command 
@tree.command(
    name="avatar",
    description="Get the avatar of a user",
    guild=discord.Object(id=GUILD_ID)
)
async def avatar_command(interaction, user: discord.User = None):
    if not user:
        user = interaction.user
    avatar_url = user.avatar
    await interaction.response.send_message(f"{user.name}'s Avatar: {avatar_url}")

# # View Help Command 
@tree.command(
    name="help",
    description="Lists all help commands",
    guild=discord.Object(id=GUILD_ID)
)
async def help_command(interaction):
    message = "Available Commands:\n/hi - Say hello\n/ping - Check bot's latency\n/userinfo - Get user information\n/stream - Announce stream\n/schedule - Display stream schedule\n/social - Get social media links"
    await interaction.response.send_message(message)

#Event Hooks
# # Bot startup event
@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=GUILD_ID))

# # Bot on message sent event
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
# Run bot
print("BOT is starting . . .")
client.run(TOKEN)
