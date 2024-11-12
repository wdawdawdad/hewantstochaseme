import discord
import os
import time
from discord.ext import commands
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
    print(f"Obfuscating file: {file_path}")  # Debugging print
    obfuscated_file_path = f"obfuscated_{file_path}"

    # Using pyarmor to obfuscate the file
    os.system(f"pyarmor obfuscate --output . {file_path}")

    # The obfuscated file is saved in a directory named 'dist'
    obfuscated_file_path = f"dist/{file_path}"

    return obfuscated_file_path

# UI for the obfuscation panel
class ObfuscationView(discord.ui.View):
    def __init__(self, ctx):
        super().__init__()
        self.ctx = ctx

    @discord.ui.button(label="✅ Proceed with Obfuscation", style=discord.ButtonStyle.green)
    async def proceed_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message("Please upload the DLL file to be obfuscated.")  # Acknowledge the button press
        
        try:
            # Wait for the file upload from the user
            msg = await bot.wait_for(
                "message",
                check=lambda m: m.author == self.ctx.author and m.attachments,
                timeout=60.0  # 60 seconds to upload the file
            )

            # Download the DLL file
            attachment = msg.attachments[0]
            if not attachment.filename.endswith(".dll"):
                await self.ctx.send("Please upload a valid DLL file.")
                return

            # Save the file
            file_path = f'./{attachment.filename}'
            await attachment.save(file_path)
            await self.ctx.send("Obfuscating the file, please wait...")

            # Obfuscate the file
            obfuscated_file_path = obfuscate_file(file_path)

            # Send the obfuscated file back
            await self.ctx.send("File obfuscation complete! Here is your obfuscated DLL:", file=discord.File(obfuscated_file_path))

            # Clean up files after sending
            os.remove(file_path)
            os.remove(obfuscated_file_path)

        except Exception as e:
            await self.ctx.send(f"Error: {e}")
            print(e)

    @discord.ui.button(label="❌ Cancel", style=discord.ButtonStyle.red)
    async def cancel_button(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message("Obfuscation process has been cancelled.")
        self.stop()

@bot.event
async def on_ready():
    print(f'Bot is online as {bot.user}')

@bot.command(name='obfuscate')
async def obfuscate(ctx):
    # Check if the user is allowed
    if ctx.author.id not in allowed_users:
        await ctx.send("You do not have permission to use this command.")
        return

    # Ask for confirmation to proceed with buttons
    view = ObfuscationView(ctx)
    await ctx.send("Would you like to obfuscate? Choose an option below.", view=view)

# Run the bot with your token (make sure to securely replace this in your environment)
bot.run("YOUR_DISCORD_BOT_TOKEN")
