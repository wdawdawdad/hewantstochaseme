import discord
import os
import time
from discord.ext import commands
from discord.ext.commands import has_permissions
import pyarmor  # Importing pyarmor for obfuscation

# Allowed user IDs (replace with your own list)
allowed_users = [980024916235661352, 987654321012345678]

# Define bot intents
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.reactions = True  # Make sure to enable reactions

# Create the bot
bot = commands.Bot(command_prefix='!', intents=intents)

# Obfuscation function using pyarmor
def obfuscate_file(file_path):
    obfuscated_file_path = f"obfuscated_{file_path}"

    # Using pyarmor to obfuscate the file
    os.system(f"pyarmor obfuscate --output . {file_path}")

    # The obfuscated file is saved in a directory named 'dist'
    obfuscated_file_path = f"dist/{file_path}"

    return obfuscated_file_path

@bot.event
async def on_ready():
    print(f'Bot is online as {bot.user}')

@bot.command(name='obfuscate')
async def obfuscate(ctx):
    # Check if the user is allowed
    if ctx.author.id not in allowed_users:
        await ctx.send("You do not have permission to use this command.")
        return

    # Ask for confirmation to proceed
    msg = await ctx.send("Would you like to obfuscate? ✅ or ❌")
    await msg.add_reaction("✅")
    await msg.add_reaction("❌")

    # This function will check if the reaction is from the user and is one of the specified emojis
    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ["✅", "❌"]

    try:
        # Wait for a reaction for up to 30 seconds
        reaction, user = await bot.wait_for("reaction_add", timeout=30.0, check=check)

        # If the user clicked ✅
        if str(reaction.emoji) == "✅":
            await ctx.send("Please upload the DLL file to be obfuscated.")
            
            # Wait for the user to upload a message with the DLL file attached
            msg = await bot.wait_for(
                "message",
                check=lambda m: m.author == ctx.author and m.attachments,
                timeout=60.0)

            # Check if the uploaded file is a DLL
            attachment = msg.attachments[0]
            if not attachment.filename.endswith(".dll"):
                await ctx.send("Please upload a valid DLL file.")
                return

            # Download the DLL file
            file_path = f'./{attachment.filename}'
            await attachment.save(file_path)
            await ctx.send("Obfuscating the file, please wait...")

            # Call obfuscate_file and send back the result
            obfuscated_file_path = obfuscate_file(file_path)

            # Send the obfuscated file back
            await ctx.send("File obfuscation complete! Here is your obfuscated DLL:", file=discord.File(obfuscated_file_path))

            # Clean up files after sending
            os.remove(file_path)
            os.remove(obfuscated_file_path)

        else:
            await ctx.send("Obfuscation cancelled.")

    except Exception as e:
        await ctx.send("Obfuscation request timed out or failed.")
        print(f"Error: {e}")


# Run the bot with your token (make sure to securely replace this in your environment)
bot.run("YOUR_DISCORD_BOT_TOKEN")
