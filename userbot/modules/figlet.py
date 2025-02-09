import asyncio
import pyfiglet

from telethon import events, functions
from userbot import CMD_HELP
from userbot.events import register
import sys
 
@register(outgoing=True, pattern="^\.figlet(?: |$)(.*)")
async def figlet(event):
    if event.fwd_from:
        return
    CMD_FIG = {"slant": "slant", "3D": "3-d", "5line": "5lineoblique", "alpha": "alphabet", "banner": "banner3-D", "doh": "doh", "iso": "isometric1", "letter": "letters", "allig": "alligator", "dotm": "dotmatrix", "bubble": "bubble", "bulb": "bulbhead", "digi": "digital"}
    input_str = event.pattern_match.group(1)
    if "|" in input_str:
        text, cmd = input_str.split("|", maxsplit=1)
    elif input_str is not None:
        cmd = None
        text = input_str
    else:
        await event.edit("`Harap tambahkan beberapa teks ke figlet.`")
        return
    if cmd is not None:
        try:
            font = CMD_FIG[cmd]
        except KeyError:
            await event.edit("`Font yang dipilih tidak valid.`")
            return
        result = pyfiglet.figlet_format(text, font=font)
    else:
        result = pyfiglet.figlet_format(text)
    await event.respond("‌‌‎`{}`".format(result))
    await event.delete()

CMD_HELP.update(
    {
        "figlet": "`.figlet [teks]`"
        "\n➥  Tingkatkan teks Anda menjadi garis strip dengan landasan."
    }
)
