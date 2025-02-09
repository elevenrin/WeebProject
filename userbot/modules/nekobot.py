import os
import re

import requests
from html_telegraph_poster.upload_images import upload_image
from PIL import Image
from validators.url import url

from userbot import CMD_HELP, bot
from userbot.events import register

EMOJI_PATTERN = re.compile(
    "["
    "\U0001F1E0-\U0001F1FF"  # flags (iOS)
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F680-\U0001F6FF"  # transport & map symbols
    "\U0001F700-\U0001F77F"  # alchemical symbols
    "\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
    "\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
    "\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
    "\U0001FA00-\U0001FA6F"  # Chess Symbols
    "\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
    "\U00002702-\U000027B0"  # Dingbats
    "]+"
)


def deEmojify(inputString: str) -> str:
    return re.sub(EMOJI_PATTERN, "", inputString)


# for nekobot
async def trumptweet(text):
    r = requests.get(
        f"https://nekobot.xyz/api/imagegen?type=trumptweet&text={text}"
    ).json()
    geng = r.get("message")
    kapak = url(geng)
    if not kapak:
        return "check syntax once more"
    with open("gpx.png", "wb") as f:
        f.write(requests.get(geng).content)
    img = Image.open("gpx.png").convert("RGB")
    img.save("gpx.webp", "webp")
    return "gpx.webp"


async def phss(uplded, input, name):
    web = requests.get(
        f"https://nekobot.xyz/api/imagegen?type=phcomment&image={uplded}&text={input}&username={name}"
    ).json()
    alf = web.get("message")
    uri = url(alf)
    if not uri:
        return "check syntax once more"
    with open("alf.png", "wb") as f:
        f.write(requests.get(alf).content)
    img = Image.open("alf.png").convert("RGB")
    img.save("alf.webp", "webp")
    return "alf.webp"


async def changemymind(text):
    r = requests.get(
        f"https://nekobot.xyz/api/imagegen?type=changemymind&text={text}"
    ).json()
    geng = r.get("message")
    kapak = url(geng)
    if not kapak:
        return "check syntax once more"
    with open("gpx.png", "wb") as f:
        f.write(requests.get(geng).content)
    img = Image.open("gpx.png").convert("RGB")
    img.save("gpx.webp", "webp")
    return "gpx.webp"


async def kannagen(text):
    r = requests.get(
        f"https://nekobot.xyz/api/imagegen?type=kannagen&text={text}"
    ).json()
    geng = r.get("message")
    kapak = url(geng)
    if not kapak:
        return "check syntax once more"
    with open("gpx.png", "wb") as f:
        f.write(requests.get(geng).content)
    img = Image.open("gpx.png").convert("RGB")
    img.save("gpx.webp", "webp")
    return "gpx.webp"


async def qorygore(text):
    r = requests.get(
        f"https://nekobot.xyz/api/imagegen?type=tweet&text={text}&username=QoryGore"
    ).json()
    geng = r.get("message")
    kapak = url(geng)
    if not kapak:
        return "check syntax once more"
    with open("gpx.png", "wb") as f:
        f.write(requests.get(geng).content)
    img = Image.open("gpx.png").convert("RGB")
    img.save("gpx.webp", "webp")
    return "gpx.webp"


async def tweets(text1, text2):
    r = requests.get(
        f"https://nekobot.xyz/api/imagegen?type=tweet&text={text1}&username={text2}"
    ).json()
    geng = r.get("message")
    kapak = url(geng)
    if not kapak:
        return "check syntax once more"
    with open("gpx.png", "wb") as f:
        f.write(requests.get(geng).content)
    img = Image.open("gpx.png").convert("RGB")
    img.save("gpx.webp", "webp")
    return "gpx.webp"


async def purge():
    try:
        os.system("rm *.png *.webp")
    except OSError:
        pass


async def get_user_from_event(event):
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        user_obj = await event.client.get_entity(previous_message.from_id)
    return user_obj


@register(outgoing=True, pattern=r"^\.trump(?: |$)(.*)")
async def trump(event):
    text = event.pattern_match.group(1)
    text = re.sub("&", "", text)
    reply_to_id = event.message
    if event.reply_to_msg_id:
        reply_to_id = await event.get_reply_message()
    if not text:
        if event.is_reply and not reply_to_id.media:
            text = reply_to_id.message
        else:
            await event.edit("`Kirim teks Anda ke trump sehingga dia bisa tweet.`")
            return
    await event.edit("`Meminta trump untuk menge-tweet...`")
    text = deEmojify(text)
    img = await trumptweet(text)
    await event.client.send_file(event.chat_id, img, reply_to=reply_to_id)
    await event.delete()
    await purge()


@register(outgoing=True, pattern=r"^\.ph(?: |$)(.*)")
async def phcomment(event):
    try:
        await event.edit("`Sedang memproses...`")
        text = event.pattern_match.group(1)
        reply = await event.get_reply_message()
        if reply:
            user = await get_user_from_event(event)
            if user.last_name:
                name = user.first_name + " " + user.last_name
            else:
                name = user.first_name
            if text:
                text = text
            else:
                text = str(reply.message)
        elif text:
            user = await bot.get_me()
            if user.last_name:
                name = user.first_name + " " + user.last_name
            else:
                name = user.first_name
            text = text
        else:
            return await event.edit("`Berikan teks...`")
        try:
            photo = await event.client.download_profile_photo(
                user.id,
                str(user.id) + ".png",
                download_big=False,
            )
            uplded = upload_image(photo)
        except BaseException:
            uplded = "https://telegra.ph/file/7d110cd944d54f72bcc84.jpg"
    except BaseException as e:
        await purge()
        return await event.edit(f"**Kesalahan** : `{e}`")
    img = await phss(uplded, text, name)
    try:
        await event.client.send_file(
            event.chat_id,
            img,
            reply_to=event.reply_to_msg_id,
        )
    except BaseException:
        await purge()
        return await event.edit("`Pesan balasan tidak memiliki teks!`")
    await event.delete()
    await purge()


@register(outgoing=True, pattern=r"^\.qg(?: |$)(.*)")
async def qg(event):
    text = event.pattern_match.group(1)
    text = re.sub("&", "", text)
    reply_to_id = event.message
    if event.reply_to_msg_id:
        reply_to_id = await event.get_reply_message()
    if not text:
        if event.is_reply and not reply_to_id.media:
            text = reply_to_id.message
        else:
            await event.edit("`Kirim teks Anda ke`  **@QoryGore**  `agar dia bisa tweet.`")
            return
    await event.edit("`Meminta QoryGore untuk menge-tweet...`")
    text = deEmojify(text)
    img = await qorygore(text)
    await event.client.send_file(event.chat_id, img, reply_to=reply_to_id)
    await event.delete()
    await purge()


@register(outgoing=True, pattern=r"^\.cmm(?: |$)(.*)")
async def cmm(event):
    text = event.pattern_match.group(1)
    text = re.sub("&", "", text)
    reply_to_id = event.message
    if event.reply_to_msg_id:
        reply_to_id = await event.get_reply_message()
    if not text:
        if event.is_reply and not reply_to_id.media:
            text = reply_to_id.message
        else:
            await event.edit("`Berikan teks untuk ditulis di spanduk!`")
            return
    await event.edit("`Spanduk Anda sedang dalam pembuatan\nTunggu sebentar...`")
    text = deEmojify(text)
    img = await changemymind(text)
    await event.client.send_file(event.chat_id, img, reply_to=reply_to_id)
    await event.delete()
    await purge()


@register(outgoing=True, pattern=r"^\.kanna(?: |$)(.*)")
async def kanna(event):
    text = event.pattern_match.group(1)
    text = re.sub("&", "", text)
    reply_to_id = event.message
    if event.reply_to_msg_id:
        reply_to_id = await event.get_reply_message()
    if not text:
        if event.is_reply and not reply_to_id.media:
            text = reply_to_id.message
        else:
            await event.edit("`Apa yang harus`  **kanna**  `tulis?`\n`Berikan teks!`")
            return
    await event.edit("`Kanna sedang menulis teks...`")
    text = deEmojify(text)
    img = await kannagen(text)
    await event.client.send_file(event.chat_id, img, reply_to=reply_to_id)
    await event.delete()
    await purge()


@register(outgoing=True, pattern=r"\.tweet(?: |$)(.*)")
async def tweet(event):
    text = event.pattern_match.group(1)
    text = re.sub("&", "", text)
    reply_to_id = event.message
    if event.reply_to_msg_id:
        reply_to_id = await event.get_reply_message()
    if not text:
        if event.is_reply:
            if not reply_to_id.media:
                text = reply_to_id.message
            else:
                await event.edit("`Apa yang harus saya tweet?`\n`Berikan nama pengguna dan tweet Anda!`")
                return
        else:
            await event.edit("`Apa yang harus saya tweet?`\n`Berikan nama pengguna dan tweet Anda!`")
            return
    if "." in text:
        username, text = text.split(".")
    else:
        await event.edit("`Apa yang harus saya tweet?`\n`Berikan nama pengguna dan tweet Anda!`")
    await event.edit(f"`Meminta {username} untuk menge-tweet...`")
    text = deEmojify(text)
    img = await tweets(text, username)
    await event.client.send_file(event.chat_id, img, reply_to=reply_to_id)
    await event.delete()
    await purge()


CMD_HELP.update(
    {
        "nekobot": "`.tweet [nama pengguna].[tweet]`"
        "\n➥  Buat tweet dengan nama pengguna khusus."
        "\n\n`.trump [tweet]`"
        "\n➥  Buat tweet untuk Donald Trump."
        "\n\n`.qg [tweet]`"
        "\n➥  Buat tweet untuk **@QoryGore**."
        "\n\n`.cmm [teks]`"
        "\n➥  Buat spanduk untuk “Change My Mind”."
        "\n\n`.kanna [teks]`"
        "\n➥  Kanna sedang menulis teks Anda."
        "\n\n`.ph [balas dengan teks/tanpa teks]`"
        "\n➥  Menulis komentar di p*rnhub XD."
    }
)
