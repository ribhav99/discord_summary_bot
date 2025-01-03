import discord
import os
import openai
from datetime import datetime
from openAI_wrapper import OpenAISummariser
import logging
logging.basicConfig(level=logging.DEBUG)


with open("bot_token.txt", 'r') as f:   
    DISCORD_BOT_TOKEN = f.read().strip()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI
openai.api_key = OPENAI_API_KEY

# Set up Discord client
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
client = discord.Client(intents=intents)

messages = []

async def fetch_messages(channel, date):
    """Fetch messages from a channel on a specific date."""
    async for message in channel.history(limit=10000):
        if message.created_at.date() >= date:
            m = {"role": "user", "content": f"{message.author.name}: {message.content}"} 
            messages.append(m)
    return messages

def summarize_messages(messages):
    """Summarize messages using OpenAI."""
    summmariser = OpenAISummariser(messages)
    return summmariser.summarise()

@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("!summarize") or message.content.startswith("!summarise"):
        try:
            # Extract date from command
            _, date_str = message.content.split(" ", 1)
            date = datetime.strptime(date_str, "%Y-%m-%d").date()

            # Fetch messages from the same channel
            messages = await fetch_messages(message.channel, date)
            if not messages:
                await message.channel.send("No messages found for that date.")
                return

            # Summarize messages
            summary = summarize_messages(messages)
            await message.channel.send(f"Summary for {date}:\n{summary}")
        except ValueError:
            await message.channel.send("Invalid date format. Use YYYY-MM-DD.")
        except Exception as e:
            await message.channel.send(f"An error occurred: {e}")

# Run the bot
client.run(DISCORD_BOT_TOKEN)