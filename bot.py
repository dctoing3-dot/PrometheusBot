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
    # Mode baru yang lebih ringan
    modes = {
        "0": ("Minify", "--preset Minify"),
        "1": ("Light (1x VM)", "--config light_config.lua"),
        "2": ("Medium (1x VM+)", "--config medium_config.lua"),
        "3": ("Strong (2x VM)", "--preset Strong"),
    }
    
    if mode not in modes:
        await ctx.send(
            "❌ **Mode tidak valid!**\n\n"
            "**Mode tersedia:**\n"
            "`!obf 0` → Minify (tercepat, proteksi minimal)\n"
            "`!obf 1` → Light (cepat, 1x VM) ⭐\n"
            "`!obf 2` → Medium (seimbang)\n"
            "`!obf 3` → Strong (2x VM, untuk file kecil)\n\n"
            "**Tips:** Untuk file >10KB, gunakan mode 0-2"
        )
        return
    
    if not ctx.message.attachments:
        await ctx.send("❌ Lampirkan file `.lua` lalu ketik `!obf 1`")
        return
    
    attachment = ctx.message.attachments[0]
    if not attachment.filename.endswith(".lua"):
        await ctx.send("❌ File harus `.lua`!")
        return
    
    # Batasi ukuran file
    file_size_kb = attachment.size / 1024
    if file_size_kb > 100:
        await ctx.send(f"❌ File terlalu besar ({file_size_kb:.1f}KB)! Max 100KB")
        return
    
    # Warning untuk file besar + mode berat
    if file_size_kb > 20 and mode in ["3"]:
        await ctx.send(f"⚠️ File {file_size_kb:.1f}KB + Mode Strong = Lambat! Disarankan pakai `!obf 1` atau `!obf 2`")
    
    mode_name, mode_arg = modes[mode]
    msg = await ctx.send(f"🔄 **Processing** `{attachment.filename}`\n📦 Mode: **{mode_name}**\n⏳ Mohon tunggu...")

    input_file = f"input_{ctx.author.id}.lua"
    output_file = f"output_{ctx.author.id}.lua"

    try:
        await attachment.save(input_file)
        
        cmd = f"lua5.1 cli.lua {input_file} {mode_arg} --out {output_file}"
        
        process = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        
        # Timeout lebih pendek untuk mode ringan
        timeout = 30 if mode in ["0", "1"] else 60 if mode == "2" else 120
        stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=timeout)

        if os.path.exists(output_file):
            orig_size = os.path.getsize(input_file)
            obf_size = os.path.getsize(output_file)
            ratio = int((obf_size / orig_size) * 100)
            
            await msg.delete()
            
            embed = discord.Embed(title="✅ Obfuscation Berhasil!", color=0x00ff00)
            embed.add_field(name="📄 File", value=attachment.filename, inline=True)
            embed.add_field(name="🔒 Mode", value=mode_name, inline=True)
            embed.add_field(name="📊 Ukuran", value=f"{orig_size}B → {obf_size}B ({ratio}%)", inline=False)
            
            await ctx.send(embed=embed, file=discord.File(output_file, f"obf_{attachment.filename}"))
        else:
            error_text = stderr.decode()[:500] if stderr else "Unknown error"
            await msg.edit(content=f"❌ Gagal!\n```{error_text}```")

    except asyncio.TimeoutError:
        await msg.edit(content=f"❌ **Timeout!** File terlalu besar untuk mode {mode_name}.\nCoba mode lebih ringan: `!obf 0` atau `!obf 1`")
    except Exception as e:
        await msg.edit(content=f"❌ Error: {str(e)[:200]}")
    finally:
        if os.path.exists(input_file): os.remove(input_file)
        if os.path.exists(output_file): os.remove(output_file)

@bot.command(name="help")
async def help_cmd(ctx):
    embed = discord.Embed(
        title="🔒 Prometheus Obfuscator Bot",
        description="Obfuscate script Lua dengan berbagai level proteksi",
        color=0x5865F2
    )
    embed.add_field(
        name="📖 Cara Pakai",
        value="Upload file `.lua` + ketik `!obf [mode]`",
        inline=False
    )
    embed.add_field(
        name="🎚️ Mode Tersedia",
        value=(
            "`!obf 0` → **Minify** (tercepat, file kecil)\n"
            "`!obf 1` → **Light** (cepat, 1x VM) ⭐ Recommended\n"
            "`!obf 2` → **Medium** (seimbang)\n"
            "`!obf 3` → **Strong** (2x VM, file <10KB saja)"
        ),
        inline=False
    )
    embed.add_field(
        name="⚠️ Tips",
        value=(
            "• File >20KB → Gunakan mode 0-2\n"
            "• File <10KB → Bisa pakai mode 3\n"
            "• Max file size: 100KB"
        ),
        inline=False
    )
    await ctx.send(embed=embed)

if TOKEN:
    keep_alive()
    bot.run(TOKEN)
else:
    print("Token not found!")
