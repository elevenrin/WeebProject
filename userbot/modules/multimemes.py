# Copyright (C) 2020 MoveAngel and MinaProject
#
# Licensed under the Raphielscape Public License, Version 1.d (the "License");
# you may not use this file except in compliance with the License.
#
# Multifunction memes
#
# Based code + improve from AdekMaulana and aidilaryanto

import asyncio
import io
import os
import random
import re
import textwrap
import time
from asyncio.exceptions import TimeoutError
from random import randint, uniform

from glitch_this import ImageGlitcher
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps
from telethon import events, functions, types
from telethon.errors.rpcerrorlist import YouBlockedUserError
from telethon.tl.types import DocumentAttributeFilename

from userbot import CMD_HELP, TEMP_DOWNLOAD_DIRECTORY, bot
from userbot.events import register
from userbot.utils import progress

THUMB_IMAGE_PATH = "./thumb_image.jpg"

Glitched = TEMP_DOWNLOAD_DIRECTORY + "glitch.gif"

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


@register(outgoing=True, pattern=r"^\.glitch(?: |$)(.*)")
async def glitch(event):
    if not event.reply_to_msg_id:
        await event.edit("`Saya tidak akan membuat kesalahan pada hantu!`")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.media:
        await event.edit("`Balas gambar/stiker`")
        return
    await event.edit("`Mengunduh media...`")
    if reply_message.photo:
        glitch_file = await bot.download_media(
            reply_message,
            "glitch.png",
        )
    elif (
        DocumentAttributeFilename(file_name="AnimatedSticker.tgs")
        in reply_message.media.document.attributes
    ):
        await bot.download_media(
            reply_message,
            "anim.tgs",
        )
        os.system("lottie_convert.py anim.tgs anim.png")
        glitch_file = "anim.png"
    elif reply_message.video:
        video = await bot.download_media(
            reply_message,
            "glitch.mp4",
        )
        extractMetadata(createParser(video))
        os.system("ffmpeg -i glitch.mp4 -vframes 1 -an -s 480x360 -ss 1 glitch.png")
        glitch_file = "glitch.png"
    else:
        glitch_file = await bot.download_media(
            reply_message,
            "glitch.png",
        )
    try:
        value = int(event.pattern_match.group(1))
        if value > 8:
            raise ValueError
    except ValueError:
        value = 2
    await event.edit("`Mengacaukan media ini...`")
    await asyncio.sleep(2)
    glitcher = ImageGlitcher()
    img = Image.open(glitch_file)
    glitch_img = glitcher.glitch_image(img, value, color_offset=True, gif=True)
    DURATION = 200
    LOOP = 0
    glitch_img[0].save(
        Glitched,
        format="GIF",
        append_images=glitch_img[1:],
        save_all=True,
        duration=DURATION,
        loop=LOOP,
    )
    await event.edit("`Mengunggah media yang bermasalah...`")
    c_time = time.time()
    nosave = await event.client.send_file(
        event.chat_id,
        Glitched,
        force_document=False,
        reply_to=event.reply_to_msg_id,
        progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
            progress(d, t, event, c_time, "[UNGGAH]")
        ),
    )
    await event.delete()
    os.remove(Glitched)
    await bot(
        functions.messages.SaveGifRequest(
            id=types.InputDocument(
                id=nosave.media.document.id,
                access_hash=nosave.media.document.access_hash,
                file_reference=nosave.media.document.file_reference,
            ),
            unsave=True,
        )
    )
    os.remove(glitch_file)
    os.system("rm *.tgs *.mp4")


@register(outgoing=True, pattern=r"^\.mmf(?: |$)(.*)")
async def mim(event):
    if not event.reply_to_msg_id:
        await event.edit(
            "`Sintaksis : membalas gambar dengan .mmf “texttop” ; “textbottom” `"
        )
        return
    reply_message = await event.get_reply_message()
    if not reply_message.media:
        await event.edit("`Balas gambar/stiker/gif.`")
        return
    await event.edit("`Mengunduh media...`")
    if reply_message.photo:
        dls_loc = await bot.download_media(
            reply_message,
            "meme.png",
        )
    elif (
        DocumentAttributeFilename(file_name="AnimatedSticker.tgs")
        in reply_message.media.document.attributes
    ):
        await bot.download_media(
            reply_message,
            "meme.tgs",
        )
        os.system("lottie_convert.py meme.tgs meme.png")
        dls_loc = "meme.png"
    elif reply_message.video:
        video = await bot.download_media(
            reply_message,
            "meme.mp4",
        )
        extractMetadata(createParser(video))
        os.system("ffmpeg -i meme.mp4 -vframes 1 -an -s 480x360 -ss 1 meme.png")
        dls_loc = "meme.png"
    else:
        dls_loc = await bot.download_media(
            reply_message,
            "meme.png",
        )
    await event.edit(
        "`Waktunya Transfigurasi! Mwahaha Mengingat gambar ini! (」ﾟﾛﾟ)｣ `"
    )
    await asyncio.sleep(5)
    text = event.pattern_match.group(1)
    webp_file = await draw_meme_text(dls_loc, text)
    await event.client.send_file(
        event.chat_id, webp_file, reply_to=event.reply_to_msg_id
    )
    await event.delete()
    os.system("rm *.tgs *.mp4 *.png")
    os.remove(webp_file)


async def draw_meme_text(image_path, text):
    img = Image.open(image_path)
    os.remove(image_path)
    i_width, i_height = img.size
    m_font = ImageFont.truetype(
        "resources/MutantAcademyStyle.ttf", int((70 / 640) * i_width)
    )
    if ";" in text:
        upper_text, lower_text = text.split(";")
    else:
        upper_text = text
        lower_text = ""
    draw = ImageDraw.Draw(img)
    current_h, pad = 10, 5
    if upper_text:
        for u_text in textwrap.wrap(upper_text, width=15):
            u_width, u_height = draw.textsize(u_text, font=m_font)

            draw.text(
                xy=(((i_width - u_width) / 2) - 1, int((current_h / 640) * i_width)),
                text=u_text,
                font=m_font,
                fill=(0, 0, 0),
            )
            draw.text(
                xy=(((i_width - u_width) / 2) + 1, int((current_h / 640) * i_width)),
                text=u_text,
                font=m_font,
                fill=(0, 0, 0),
            )
            draw.text(
                xy=((i_width - u_width) / 2, int(((current_h / 640) * i_width)) - 1),
                text=u_text,
                font=m_font,
                fill=(0, 0, 0),
            )
            draw.text(
                xy=(((i_width - u_width) / 2), int(((current_h / 640) * i_width)) + 1),
                text=u_text,
                font=m_font,
                fill=(0, 0, 0),
            )

            draw.text(
                xy=((i_width - u_width) / 2, int((current_h / 640) * i_width)),
                text=u_text,
                font=m_font,
                fill=(255, 255, 255),
            )
            current_h += u_height + pad
    if lower_text:
        for l_text in textwrap.wrap(lower_text, width=15):
            u_width, u_height = draw.textsize(l_text, font=m_font)

            draw.text(
                xy=(
                    ((i_width - u_width) / 2) - 1,
                    i_height - u_height - int((20 / 640) * i_width),
                ),
                text=l_text,
                font=m_font,
                fill=(0, 0, 0),
            )
            draw.text(
                xy=(
                    ((i_width - u_width) / 2) + 1,
                    i_height - u_height - int((20 / 640) * i_width),
                ),
                text=l_text,
                font=m_font,
                fill=(0, 0, 0),
            )
            draw.text(
                xy=(
                    (i_width - u_width) / 2,
                    (i_height - u_height - int((20 / 640) * i_width)) - 1,
                ),
                text=l_text,
                font=m_font,
                fill=(0, 0, 0),
            )
            draw.text(
                xy=(
                    (i_width - u_width) / 2,
                    (i_height - u_height - int((20 / 640) * i_width)) + 1,
                ),
                text=l_text,
                font=m_font,
                fill=(0, 0, 0),
            )

            draw.text(
                xy=(
                    (i_width - u_width) / 2,
                    i_height - u_height - int((20 / 640) * i_width),
                ),
                text=l_text,
                font=m_font,
                fill=(255, 255, 255),
            )
            current_h += u_height + pad

    image_name = "memify.webp"
    webp_file = os.path.join(TEMP_DOWNLOAD_DIRECTORY, image_name)
    img.save(webp_file, "WebP")
    return webp_file


@register(outgoing=True, pattern=r"^\.q(?: |$)(.*)")
async def quotess(qotli):
    if qotli.fwd_from:
        return
    if not qotli.reply_to_msg_id:
        await qotli.edit("`Balas pesan pengguna mana pun.`")
        return
    reply_message = await qotli.get_reply_message()
    if not reply_message.text:
        await qotli.edit("`Balas pesan teks.`")
        return
    chat = "@QuotLyBot"
    reply_message.sender
    if reply_message.sender.bot:
        await qotli.edit("`Balas pesan pengguna sebenarnya.`")
        return
    try:
        await qotli.edit("`Sedang memproses...`")
        async with bot.conversation(chat) as conv:
            try:
                response = conv.wait_event(
                    events.NewMessage(incoming=True, from_users=1031952739)
                )
                msg = await bot.forward_messages(chat, reply_message)
                response = await response
                await bot.send_read_acknowledge(conv.chat_id)
            except YouBlockedUserError:
                await qotli.reply("`Harap buka blokir`  **@QuotLyBot**  `dan coba lagi.`")
                return
            if response.text.startswith("Hi!"):
                await qotli.edit(
                    "`Bisakah Anda dengan ramah menonaktifkan pengaturan privasi penerusan untuk selamanya?`"
                )
            else:
                downloaded_file_name = await qotli.client.download_media(
                    response.media, TEMP_DOWNLOAD_DIRECTORY
                )
                await qotli.client.send_file(
                    qotli.chat_id, downloaded_file_name, reply_to=qotli.reply_to_msg_id
                )
                await qotli.delete()
                await bot.send_read_acknowledge(qotli.chat_id)
                await qotli.client.delete_messages(conv.chat_id, [msg.id, response.id])
                os.remove(downloaded_file_name)
    except TimeoutError:
        await qotli.edit("**@QuotLyBot**  `tidak menanggapi!`")
        await qotli.client.delete_messages(conv.chat_id, [msg.id])


@register(outgoing=True, pattern=r"^\.hz(:? |$)(.*)?")
async def hazz(hazmat):
    await hazmat.edit("`Mengirim informasi...`")
    level = hazmat.pattern_match.group(2)
    if hazmat.fwd_from:
        return
    if not hazmat.reply_to_msg_id:
        await hazmat.edit("`WoWoWo Kapten!, kita tidak akan cocok dengan hantu!`")
        return
    reply_message = await hazmat.get_reply_message()
    if not reply_message.media:
        await hazmat.edit("`Kata bisa menghancurkan apapun, Kapten!`")
        return
    if reply_message.sender.bot:
        await hazmat.edit("`Balas ke pengguna sebenarnya...`")
        return
    chat = "@hazmat_suit_bot"
    await hazmat.edit("`Siapkan Kapten!, Kami akan membersihkan beberapa virus...`")
    message_id_to_reply = hazmat.message.reply_to_msg_id
    msg_reply = None
    async with hazmat.client.conversation(chat) as conv:
        try:
            msg = await conv.send_message(reply_message)
            if level:
                m = f"/hazmat {level}"
                msg_reply = await conv.send_message(m, reply_to=msg.id)
                r = await conv.get_response()
                response = await conv.get_response()
            elif reply_message.gif:
                m = f"/hazmat"
                msg_reply = await conv.send_message(m, reply_to=msg.id)
                r = await conv.get_response()
                response = await conv.get_response()
            else:
                response = await conv.get_response()
            """don't spam notif"""
            await bot.send_read_acknowledge(conv.chat_id)
        except YouBlockedUserError:
            await hazmat.reply("`Harap buka blokir`  **@hazmat_suit_bot**`...`")
            return
        if response.text.startswith("I can't"):
            await hazmat.edit("`Tidak dapat menangani GIF ini...`")
            await hazmat.client.delete_messages(
                conv.chat_id, [msg.id, response.id, r.id, msg_reply.id]
            )
            return
        else:
            downloaded_file_name = await hazmat.client.download_media(
                response.media, TEMP_DOWNLOAD_DIRECTORY
            )
            await hazmat.client.send_file(
                hazmat.chat_id,
                downloaded_file_name,
                force_document=False,
                reply_to=message_id_to_reply,
            )
            """cleanup chat after completed"""
            if msg_reply is not None:
                await hazmat.client.delete_messages(
                    conv.chat_id, [msg.id, msg_reply.id, r.id, response.id]
                )
            else:
                await hazmat.client.delete_messages(conv.chat_id, [msg.id, response.id])
    await hazmat.delete()
    return os.remove(downloaded_file_name)


@register(outgoing=True, pattern=r"^\.df(:? |$)([1-8])?")
async def fryerrr(fry):
    await fry.edit("`Mengirim informasi...`")
    level = fry.pattern_match.group(2)
    if fry.fwd_from:
        return
    if not fry.reply_to_msg_id:
        await fry.edit("`Balas pesan foto pengguna mana pun...`")
        return
    reply_message = await fry.get_reply_message()
    if not reply_message.media:
        await fry.edit("`Tidak ada gambar untuk digoreng...`")
        return
    if reply_message.sender.bot:
        await fry.edit("`Balas ke pengguna sebenarnya...`")
        return
    chat = "@image_deepfrybot"
    message_id_to_reply = fry.message.reply_to_msg_id
    try:
        async with fry.client.conversation(chat) as conv:
            try:
                msg = await conv.send_message(reply_message)
                if level:
                    m = f"/deepfry {level}"
                    msg_level = await conv.send_message(m, reply_to=msg.id)
                    r = await conv.get_response()
                response = await conv.get_response()
                await bot.send_read_acknowledge(conv.chat_id)
            except YouBlockedUserError:
                await fry.reply("`Harap buka blokir`  **@image_deepfrybot**`...`")
                return
            if response.text.startswith("Forward"):
                await fry.edit("`Nonaktifkan setelan privasi penerusan Anda...`")
            else:
                downloaded_file_name = await fry.client.download_media(
                    response.media, TEMP_DOWNLOAD_DIRECTORY
                )
                await fry.client.send_file(
                    fry.chat_id,
                    downloaded_file_name,
                    force_document=False,
                    reply_to=message_id_to_reply,
                )
                try:
                    msg_level
                except NameError:
                    await fry.client.delete_messages(
                        conv.chat_id, [msg.id, response.id]
                    )
                else:
                    await fry.client.delete_messages(
                        conv.chat_id, [msg.id, response.id, r.id, msg_level.id]
                    )
        await fry.delete()
        return os.remove(downloaded_file_name)
    except TimeoutError:
        await fry.edit("**@image_deepfrybot**  `tidak menanggapi!`")
        await fry.client.delete_messages(conv.chat_id, [msg.id])


@register(pattern=r"^\.deepfry(?: |$)(.*)", outgoing=True)
async def deepfryer(event):
    try:
        frycount = int(event.pattern_match.group(1))
        if frycount < 1:
            raise ValueError
    except ValueError:
        frycount = 1
    reply_message = await event.get_reply_message()
    image = io.BytesIO()
    await event.edit("`Mengunduh media...`")
    if reply_message.photo:
        image = await bot.download_media(
            reply_message,
            "df.png",
        )
    elif (
        DocumentAttributeFilename(file_name="AnimatedSticker.tgs")
        in reply_message.media.document.attributes
    ):
        await bot.download_media(
            reply_message,
            "df.tgs",
        )
        os.system("lottie_convert.py df.tgs df.png")
        image = "df.png"
    elif reply_message.video:
        video = await bot.download_media(
            reply_message,
            "df.mp4",
        )
        extractMetadata(createParser(video))
        os.system("ffmpeg -i df.mp4 -vframes 1 -an -s 480x360 -ss 1 df.png")
        image = "df.png"
    else:
        image = await bot.download_media(
            reply_message,
            "df.png",
        )
    image = Image.open(image)

    # fry the image
    await event.edit("`Menggoreng media...`")
    for _ in range(frycount):
        image = await deepfry(image)

    fried_io = io.BytesIO()
    fried_io.name = "image.jpeg"
    image.save(fried_io, "JPEG")
    fried_io.seek(0)

    await event.reply(file=fried_io)
    os.system("rm *.mp4 *.tgs *.png")


async def deepfry(img: Image) -> Image:
    colours = (
        (randint(50, 200), randint(40, 170), randint(40, 190)),
        (randint(190, 255), randint(170, 240), randint(180, 250)),
    )

    img = img.copy().convert("RGB")

    # Crush image to hell and back
    img = img.convert("RGB")
    width, height = img.width, img.height
    img = img.resize(
        (int(width ** uniform(0.8, 0.9)), int(height ** uniform(0.8, 0.9))),
        resample=Image.LANCZOS,
    )
    img = img.resize(
        (int(width ** uniform(0.85, 0.95)), int(height ** uniform(0.85, 0.95))),
        resample=Image.BILINEAR,
    )
    img = img.resize(
        (int(width ** uniform(0.89, 0.98)), int(height ** uniform(0.89, 0.98))),
        resample=Image.BICUBIC,
    )
    img = img.resize((width, height), resample=Image.BICUBIC)
    img = ImageOps.posterize(img, randint(3, 7))

    # Generate colour overlay
    overlay = img.split()[0]
    overlay = ImageEnhance.Contrast(overlay).enhance(uniform(1.0, 2.0))
    overlay = ImageEnhance.Brightness(overlay).enhance(uniform(1.0, 2.0))

    overlay = ImageOps.colorize(overlay, colours[0], colours[1])

    # Overlay red and yellow onto main image and sharpen the hell out of it
    img = Image.blend(img, overlay, uniform(0.5, 0.9))
    img = ImageEnhance.Sharpness(img).enhance(randint(5, 300))

    return img


@register(outgoing=True, pattern=r"^\.sg(?: |$)(.*)")
async def lastname(steal):
    if steal.fwd_from:
        return
    if not steal.reply_to_msg_id:
        await steal.edit("`Balas pesan pengguna mana pun.`")
        return
    message = await steal.get_reply_message()
    chat = "@SangMataInfo_bot"
    user_id = message.sender.id
    id = f"/search_id {user_id}"
    if message.sender.bot:
        await steal.edit("`Balas pesan pengguna sebenarnya.`")
        return
    await steal.edit("`Tunggu sebentar sementara saya mengambil beberapa data dari NASA.`")
    try:
        async with bot.conversation(chat) as conv:
            try:
                msg = await conv.send_message(id)
                r = await conv.get_response()
                response = await conv.get_response()
            except YouBlockedUserError:
                await steal.reply("`Harap buka blokir`  **@sangmatainfo_bot**  `dan coba lagi.`")
                return
            if r.text.startswith("Name"):
                respond = await conv.get_response()
                await steal.edit(f"`{r.message}`")
                await steal.client.delete_messages(
                    conv.chat_id, [msg.id, r.id, response.id, respond.id]
                )
                return
            if response.text.startswith("No records") or r.text.startswith(
                "No records"
            ):
                await steal.edit("`Tidak ada catatan yang ditemukan untuk pengguna ini`")
                await steal.client.delete_messages(
                    conv.chat_id, [msg.id, r.id, response.id]
                )
                return
            else:
                respond = await conv.get_response()
                await steal.edit(f"`{response.message}`")
            await steal.client.delete_messages(
                conv.chat_id, [msg.id, r.id, response.id, respond.id]
            )
    except TimeoutError:
        return await steal.edit("**Kesalahan** : **@SangMataInfo_bot** `tidak menanggapi!`")


@register(outgoing=True, pattern=r"^\.waifu(?: |$)(.*)")
async def waifu(animu):
    text = animu.pattern_match.group(1)
    await animu.edit("`Menemukan waifu Anda...`")
    if not text:
        if animu.is_reply:
            text = (await animu.get_reply_message()).message
        else:
            await animu.answer("`Tidak ada teks yang diberikan, maka waifu tersebut lari.`")
            return
    animus = [20, 32, 33, 40, 41, 42, 58]
    sticcers = await bot.inline_query(
        "stickerizerbot", f"#{random.choice(animus)}{(deEmojify(text))}"
    )
    await sticcers[0].click(
        animu.chat_id,
        reply_to=animu.reply_to_msg_id,
        silent=bool(animu.is_reply),
        hide_via=True,
    )
    await animu.delete()


def deEmojify(inputString: str) -> str:
    return re.sub(EMOJI_PATTERN, "", inputString)


CMD_HELP.update(
    {
        "glitch": "`.glitch [1-8]`"
        "\n➥  Balas stiker/gambar dan kirim dengan cmd(perintah).\nNilainya berkisar 1-8 jika tidak maka akan memberikan nilai default yaitu 2."
    }
)

CMD_HELP.update(
    {
        "memify": "`.mmf texttop ; textbottom`"
        "\n➥  Balas stiker/gambar/gif dan kirim dengan cmd(perintah)."
    }
)

CMD_HELP.update(
    {
        "quotly": "`.q`"
          "\n➥  Sempurnakan teks Anda menjadi stiker."
    }
)

CMD_HELP.update(
    {
        "hazmat": "`.hz / .hz [flip, x2, rotate (degree), background (number), black]`"
        "\n➥  Balas gambar/stiker yang sesuai!"
        "\n**@hazmat_suit_bot**"
    }
)

CMD_HELP.update(
    {
        "deepfry": "`.df / .df [level(1-8)]`"
        "\n➥  Goreng gambar/stiker dari balasan."
        "\n**@image_deepfrybot**"
        "\n\n`.deepfry`"
        "\n➥  Gambar krispi."
    }
)


CMD_HELP.update({"sangmata": "`.sg`" "\n➥  Menampilkan info nama Anda atau seseorang."})


CMD_HELP.update(
    {
        "waifu": "`.waifu`"
        "\n➥  Tingkatkan teks Anda dengan templat gadis anime cantik."
        "\n**@StickerizerBot**"
    }
)
