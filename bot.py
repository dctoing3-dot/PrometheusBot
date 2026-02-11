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

def safe_oneline(code):
    """Ubah ke 1 baris dengan AMAN - hanya hapus newline, jaga spasi"""
    # Hanya ganti newline jadi spasi (AMAN)
    code = code.replace('\n', ' ')
    code = code.replace('\r', '')
    
    # Hapus multiple spaces jadi 1 spasi (AMAN)
    import re
    code = re.sub(r' +', ' ', code)
    
    # Hapus spasi di awal/akhir
    code = code.strip()
    
    return code

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
        await ctx.send("❌ Mode: `0` `1` `2` `3`")
        return
    
    if not ctx.message.attachments:
        await ctx.send("❌ Upload `.lua` + `!obf 1`")
        return
    
    attachment = ctx.message.attachments[0]
    if not attachment.filename.endswith(".lua"):
        await ctx.send("❌ File harus `.lua`!")
        return
    
    mode_name, mode_arg, max_kb = modes[mode]
    file_kb = attachment.size / 1024
    
    if file_kb > max_kb:
        await ctx.send(f"❌ {file_kb:.1f}KB > {max_kb}KB\nCoba `!obf 0` atau `!obf 1`")
        return

    msg = await ctx.send(f"🔄 `{attachment.filename}` [{mode_name}]...")

    input_file = f"input_{ctx.author.id}.lua"
    output_file = f"output_{ctx.author.id}.lua"
    final_file = f"final_{ctx.author.id}.lua"

    try:
        await attachment.save(input_file)
        cmd = f"lua5.1 cli.lua {input_file} {mode_arg} --out {output_file}"
        
        process = await asyncio.create_subprocess_shell(
            cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        
        timeout = 30 if mode in ["0", "1"] else 60
        await asyncio.wait_for(process.communicate(), timeout=timeout)

        if os.path.exists(output_file):
            with open(output_file, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # AMAN: Hanya jadikan 1 baris, jaga spasi
            content = safe_oneline(content)
            
            with open(final_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            orig = os.path.getsize(input_file)
            obf = os.path.getsize(final_file)
            
            await msg.delete()
            embed = discord.Embed(title="✅ Berhasil!", color=0x00ff00)
            embed.add_field(name="File", value=attachment.filename, inline=True)
            embed.add_field(name="Mode", value=mode_name, inline=True)
            embed.add_field(name="Size", value=f"{orig}B → {obf}B", inline=False)
            
            await ctx.send(embed=embed, file=discord.File(final_file, f"obf_{attachment.filename}"))
        else:
            await msg.edit(content="❌ Gagal!")

    except asyncio.TimeoutError:
        await msg.edit(content="❌ Timeout!")
    except Exception as e:
        await msg.edit(content=f"❌ {e}")
    finally:
        for f in [input_file, output_file, final_file]:
            if os.path.exists(f): os.remove(f)

@bot.command(name="obfhelp")
async def obfhelp_cmd(ctx):
    embed = discord.Embed(title="🔒 Prometheus Bot", color=0x5865F2)
    embed.add_field(name="Cara", value="Upload `.lua` + `!obf [0-3]`", inline=False)
    embed.add_field(name="Mode", value="`0`Minify `1`Light⭐ `2`Medium `3`Strong", inline=False)
    await ctx.send(embed=embed)

if TOKEN:
    keep_alive()
    bot.run(TOKEN)
else:
    print("Token not found!")
