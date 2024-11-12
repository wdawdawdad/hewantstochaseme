import discord
import os
import time
from discord.ext import commands
from discord.ext.commands import has_permissions

# Allowed user IDs for commands
allowed_users = [123456789012345678, 987654321012345678]  # Replace with actual IDs

# Initialize the bot
bot = commands.Bot(command_prefix="!")

# Function to obfuscate the file (dummy implementation)
def obfuscate_file(file_path):
    obfuscated_path = file_path.replace(".dll", "_obfuscated.dll")
    # Simulate obfuscation delay
    time.sleep(3)
    with open(file_path, "rb") as f:
        data = f.read()
    with open(obfuscated_path, "wb") as f:
        f.write(data[::-1])  # Just a dummy operation to simulate "obfuscation"
    return obfuscated_path

@bot.event
async def on_ready():
    print(f'Bot connected as {bot.user}')

@bot.command()
async def obfuscate(ctx):
    # Check if user is in allowed list
    if ctx.author.id not in allowed_users:
        await ctx.send("You do not have permission to use this command.")
        return

    # Ask user to upload the DLL file
    await ctx.send("Please upload the DLL file to obfuscate.")

    # Wait for file upload
    def check(msg):
        return msg.author == ctx.author and len(msg.attachments) > 0

    try:
        msg = await bot.wait_for("message", check=check, timeout=60)
        attachment = msg.attachments[0]

        # Download the file
        file_path = f"./{attachment.filename}"
        await attachment.save(file_path)

        # Obfuscate the file
        await ctx.send("Obfuscating... Please wait.")
        obfuscated_file_path = obfuscate_file(file_path)

        # Send the obfuscated file back to the user
        await ctx.send(file=discord.File(obfuscated_file_path))
        await ctx.send("File obfuscation complete.")

        # Cleanup
        os.remove(file_path)
        os.remove(obfuscated_file_path)

    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

@bot.command()
async def ping(ctx):
    await ctx.send("Pong!")

# Start the bot (token will be read from environment variable)
bot.run(os.getenv("DISCORD_BOT_TOKEN"))
