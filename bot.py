import discord
from discord.ext import commands
import json
from datetime import datetime, timedelta
import os
import random
import string

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="/", intents=intents)

# Load database
def load_data():
    try:
        with open("database.json", "r") as f:
            return json.load(f)
    except:
        return {"keys": {}}

def save_data(data):
    with open("database.json", "w") as f:
        json.dump(data, f, indent=4)

data = load_data()

# Helper function to generate random key
def generate_key(length=10):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

# /key command
@bot.command()
async def key(ctx):
    user_id = str(ctx.author.id)
    key = generate_key()
    hwid = generate_key(16)  # Random HWID

    expiry = (datetime.utcnow() + timedelta(hours=24)).timestamp()

    data["keys"][key] = {
        "user_id": user_id,
        "hwid": hwid,
        "expiry": expiry
    }
    save_data(data)

    await ctx.author.send(f"Your key: `{key}`\nYour HWID: `{hwid}`\nValid for 24 hours.")
    await ctx.send("✅ Check your DM for key & HWID.")

# /set command
@bot.command()
async def set(ctx):
    user_id = str(ctx.author.id)
    # Find key by user_id
    user_key = None
    for k, v in data["keys"].items():
        if v["user_id"] == user_id:
            user_key = k
            break

    if user_key:
        await ctx.send(f"✅ Your HWID is already set: {data['keys'][user_key]['hwid']}")
    else:
        await ctx.send("❌ You don't have a key yet. Use `/key` first.")

# Run bot using environment variable
bot.run(os.environ.get("DISCORD_BOT_TOKEN"))
