import discord
from discord.ext import commands
import subprocess
import os
import asyncio
from flask import Flask
from threading import Thread

# --- WEB SERVER HACK ---
app = Flask('')
@app.route('/')
def home():
    return "Bot is alive!"

def run_web():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_web)
    t.start()
# -----------------------

TOKEN = os.environ.get("DISCORD_TOKEN")
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'✅ Bot {bot.user} sudah online!')

@bot.command(name="obf")
async def obfuscate(ctx, mode: str = "2"):
    if mode not in ["1", "2", "3"]:
        await ctx.send("❌ Mode: 1, 2, atau 3")
        return
    if not ctx.message.attachments:
        await ctx.send("❌ Lampirkan file .lua!")
        return
    
    attachment = ctx.message.attachments[0]
    input_file = f"input_{ctx.author.id}.lua"
    output_file = f"output_{ctx.author.id}.lua"
    
    await attachment.save(input_file)
    msg = await ctx.send("🔄 Processing...")

    try:
        if mode == "1":
            cmd = f"lua5.1 cli.lua {input_file} --preset Weak --out {output_file}"
        elif mode == "2":
            cmd = f"lua5.1 cli.lua {input_file} --config luraph_config.lua --out {output_file}"
        else:
            cmd = f"lua5.1 cli.lua {input_file} --config ultimate_config.lua --out {output_file}"

        process = await asyncio.create_subprocess_shell(cmd)
        await asyncio.wait_for(process.communicate(), timeout=120)

        if os.path.exists(output_file):
            await msg.delete()
            await ctx.send(f"✅ Success!", file=discord.File(output_file, f"obf_{attachment.filename}"))
        else:
            await msg.edit(content="❌ Obfuscation Failed!")
    except Exception as e:
        await msg.edit(content=f"❌ Error: {e}")
    finally:
        if os.path.exists(input_file): os.remove(input_file)
        if os.path.exists(output_file): os.remove(output_file)

if TOKEN:
    keep_alive() # Jalankan web server sebelum bot
    bot.run(TOKEN)
else:
    print("Token not found!")
