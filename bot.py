import discord
from discord.ext import commands
import subprocess
import os
import asyncio
from flask import Flask
from threading import Thread

app = Flask('')
@app.route('/')
def home():
    return "Bot is alive!"

def run_web():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_web)
    t.start()

TOKEN = os.environ.get("DISCORD_TOKEN")
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'✅ Bot {bot.user} sudah online!')

@bot.command(name="obf")
async def obfuscate(ctx, mode: str = "1"):
    modes = {
        "0": ("Minify", "--preset Minify", 100),
        "1": ("Light 1x VM", "--config light_config.lua", 80),
        "2": ("Medium", "--config medium_config.lua", 50),
        "3": ("Strong 2x VM", "--preset Strong", 15),
    }
    
    if mode not in modes:
        await ctx.send(
            "❌ **Mode tidak valid!**\n\n"
            "**Pilih mode:**\n"
            "`!obf 0` → Minify (tercepat)\n"
            "`!obf 1` → Light ⭐ Recommended\n"
            "`!obf 2` → Medium\n"
            "`!obf 3` → Strong (file kecil saja)\n"
        )
        return
    
    if not ctx.message.attachments:
        await ctx.send("❌ Upload file `.lua` lalu ketik `!obf 1`")
        return
    
    attachment = ctx.message.attachments[0]
    if not attachment.filename.endswith(".lua"):
        await ctx.send("❌ File harus `.lua`!")
        return
    
    mode_name, mode_arg, max_kb = modes[mode]
    file_kb = attachment.size / 1024
    
    if file_kb > max_kb:
        await ctx.send(
            f"❌ **File terlalu besar untuk mode {mode_name}!**\n"
            f"📁 File kamu: {file_kb:.1f}KB\n"
            f"📏 Max untuk mode ini: {max_kb}KB\n\n"
            f"**Saran:** Gunakan `!obf 0` atau `!obf 1`"
        )
        return

    msg = await ctx.send(f"🔄 **Processing** `{attachment.filename}`\n📦 Mode: **{mode_name}**")

    input_file = f"input_{ctx.author.id}.lua"
    output_file = f"output_{ctx.author.id}.lua"

    try:
        await attachment.save(input_file)
        cmd = f"lua5.1 cli.lua {input_file} {mode_arg} --out {output_file}"
        
        process = await asyncio.create_subprocess_shell(
            cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        
        timeout = 30 if mode in ["0", "1"] else 60
        stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=timeout)

        if os.path.exists(output_file):
            orig = os.path.getsize(input_file)
            obf = os.path.getsize(output_file)
            
            await msg.delete()
            embed = discord.Embed(title="✅ Berhasil!", color=0x00ff00)
            embed.add_field(name="File", value=attachment.filename, inline=True)
            embed.add_field(name="Mode", value=mode_name, inline=True)
            embed.add_field(name="Size", value=f"{orig}B → {obf}B", inline=False)
            
            await ctx.send(embed=embed, file=discord.File(output_file, f"obf_{attachment.filename}"))
        else:
            await msg.edit(content="❌ Gagal! Coba mode lebih ringan.")

    except asyncio.TimeoutError:
        await msg.edit(content="❌ Timeout! Coba `!obf 0` atau `!obf 1`")
    except Exception as e:
        await msg.edit(content=f"❌ Error: {e}")
    finally:
        if os.path.exists(input_file): os.remove(input_file)
        if os.path.exists(output_file): os.remove(output_file)

@bot.command(name="obfhelp")
async def obfhelp_cmd(ctx):
    embed = discord.Embed(title="🔒 Prometheus Bot", color=0x5865F2)
    embed.add_field(
        name="📖 Cara Pakai",
        value="Upload file `.lua` + ketik `!obf [mode]`",
        inline=False
    )
    embed.add_field(
        name="🎚️ Mode",
        value=(
            "`!obf 0` → Minify (max 100KB)\n"
            "`!obf 1` → Light ⭐ (max 80KB)\n"
            "`!obf 2` → Medium (max 50KB)\n"
            "`!obf 3` → Strong (max 15KB)"
        ),
        inline=False
    )
    await ctx.send(embed=embed)

if TOKEN:
    keep_alive()
    bot.run(TOKEN)
else:
    print("Token not found!")
