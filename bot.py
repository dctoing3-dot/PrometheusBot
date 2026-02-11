import discord
from discord.ext import commands
import subprocess
import os
import asyncio

TOKEN = os.environ.get("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f'Bot {bot.user} sudah online!')

@bot.command(name="obf")
async def obfuscate(ctx, mode: str = "2"):
    if mode not in ["1", "2", "3"]:
        await ctx.send("❌ Mode harus 1, 2, atau 3!\n• `!obf 1` = Weak\n• `!obf 2` = Luraph 2x VM\n• `!obf 3` = Maximum 3x VM")
        return

    if not ctx.message.attachments:
        await ctx.send("❌ Upload file `.lua` lalu ketik `!obf 2`")
        return

    attachment = ctx.message.attachments[0]
    if not attachment.filename.endswith(".lua"):
        await ctx.send("❌ File harus `.lua`!")
        return

    if attachment.size > 100000:
        await ctx.send("❌ File terlalu besar! Max 100KB")
        return

    mode_names = {"1": "Weak", "2": "Luraph 2x VM", "3": "Maximum 3x VM"}
    msg = await ctx.send(f"🔄 Memproses dengan **{mode_names[mode]}**...")

    input_file = f"input_{ctx.author.id}.lua"
    output_file = f"output_{ctx.author.id}.lua"

    try:
        await attachment.save(input_file)

        if mode == "1":
            cmd = f"lua5.1 cli.lua {input_file} --preset Weak --out {output_file}"
        elif mode == "2":
            cmd = f"lua5.1 cli.lua {input_file} --config luraph_config.lua --out {output_file}"
        else:
            cmd = f"lua5.1 cli.lua {input_file} --config ultimate_config.lua --out {output_file}"

        process = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        await asyncio.wait_for(process.communicate(), timeout=120)

        if os.path.exists(output_file):
            orig = os.path.getsize(input_file)
            obf = os.path.getsize(output_file)
            await msg.delete()
            await ctx.send(
                f"✅ **Berhasil!**\n📄 `{attachment.filename}`\n🔒 Mode: {mode_names[mode]}\n📊 {orig}B → {obf}B",
                file=discord.File(output_file, f"obf_{attachment.filename}")
            )
        else:
            await msg.edit(content="❌ Gagal memproses file!")

    except asyncio.TimeoutError:
        await msg.edit(content="❌ Timeout! File terlalu besar.")
    except Exception as e:
        await msg.edit(content=f"❌ Error: {e}")
    finally:
        if os.path.exists(input_file): os.remove(input_file)
        if os.path.exists(output_file): os.remove(output_file)

if TOKEN:
    bot.run(TOKEN)
else:
    print("DISCORD_TOKEN tidak ditemukan!")
