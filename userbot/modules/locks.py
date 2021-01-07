# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.

from telethon.tl.functions.messages import EditChatDefaultBannedRightsRequest
from telethon.tl.types import ChatBannedRights

from userbot import CMD_HELP
from userbot.events import register


@register(outgoing=True, pattern=r"^\.lock ?(.*)")
async def locks(event):
    input_str = event.pattern_match.group(1).lower()
    peer_id = event.chat_id
    msg = None
    media = None
    sticker = None
    gif = None
    gamee = None
    ainline = None
    gpoll = None
    adduser = None
    cpin = None
    changeinfo = None
    if input_str == "msg":
        msg = True
        what = "Pesan"
    elif input_str == "media":
        media = True
        what = "Media"
    elif input_str == "sticker":
        sticker = True
        what = "Stiker"
    elif input_str == "gif":
        gif = True
        what = "GIF"
    elif input_str == "game":
        gamee = True
        what = "Game"
    elif input_str == "inline":
        ainline = True
        what = "Inline bots"
    elif input_str == "poll":
        gpoll = True
        what = "Jajak pendapat"
    elif input_str == "invite":
        adduser = True
        what = "Mengundang"
    elif input_str == "pin":
        cpin = True
        what = "Sematkan"
    elif input_str == "info":
        changeinfo = True
        what = "Info obrolan"
    elif input_str == "all":
        msg = True
        media = True
        sticker = True
        gif = True
        gamee = True
        ainline = True
        gpoll = True
        adduser = True
        cpin = True
        changeinfo = True
        what = "Semua"
    else:
        if not input_str:
            return await event.edit("`Saya tidak bisa mengunci apapun!`")
        else:
            return await event.edit(f"`Jenis kunci tidak valid :` {input_str}")

    lock_rights = ChatBannedRights(
        until_date=None,
        send_messages=msg,
        send_media=media,
        send_stickers=sticker,
        send_gifs=gif,
        send_games=gamee,
        send_inline=ainline,
        send_polls=gpoll,
        invite_users=adduser,
        pin_messages=cpin,
        change_info=changeinfo,
    )
    try:
        await event.client(
            EditChatDefaultBannedRightsRequest(peer=peer_id, banned_rights=lock_rights)
        )
        await event.edit(f"`Mengunci`  **{what}**  `untuk obrolan ini!`")
    except BaseException as e:
        return await event.edit(
            f"`Apakah saya memiliki hak yang layak untuk itu?`\n**Kesalahan** : {str(e)}"
        )


@register(outgoing=True, pattern=r"^\.unlock ?(.*)")
async def rem_locks(event):
    input_str = event.pattern_match.group(1).lower()
    peer_id = event.chat_id
    msg = None
    media = None
    sticker = None
    gif = None
    gamee = None
    ainline = None
    gpoll = None
    adduser = None
    cpin = None
    changeinfo = None
    if input_str == "msg":
        msg = False
        what = "Pesan"
    elif input_str == "media":
        media = False
        what = "Media"
    elif input_str == "sticker":
        sticker = False
        what = "Stiker"
    elif input_str == "gif":
        gif = False
        what = "GIF"
    elif input_str == "game":
        gamee = False
        what = "Game"
    elif input_str == "inline":
        ainline = False
        what = "Inline bots"
    elif input_str == "poll":
        gpoll = False
        what = "Jajak pendapat"
    elif input_str == "invite":
        adduser = False
        what = "Mengundang"
    elif input_str == "pin":
        cpin = False
        what = "Sematkan"
    elif input_str == "info":
        changeinfo = False
        what = "Info obrolan"
    elif input_str == "all":
        msg = False
        media = False
        sticker = False
        gif = False
        gamee = False
        ainline = False
        gpoll = False
        adduser = False
        cpin = False
        changeinfo = False
        what = "Semua"
    else:
        if not input_str:
            return await event.edit("`Saya tidak bisa membuka kunci apa pun!`")
        else:
            return await event.edit(f"`Jenis buka kunci tidak valid :` {input_str}")

    unlock_rights = ChatBannedRights(
        until_date=None,
        send_messages=msg,
        send_media=media,
        send_stickers=sticker,
        send_gifs=gif,
        send_games=gamee,
        send_inline=ainline,
        send_polls=gpoll,
        invite_users=adduser,
        pin_messages=cpin,
        change_info=changeinfo,
    )
    try:
        await event.client(
            EditChatDefaultBannedRightsRequest(
                peer=peer_id, banned_rights=unlock_rights
            )
        )
        await event.edit(f"**{what}**  `tidak lagi dikunci untuk obrolan ini!`")
    except BaseException as e:
        return await event.edit(
            f"`Apakah saya memiliki hak yang layak untuk itu?`\n**Kesalahan** : {str(e)}"
        )


CMD_HELP.update(
    {
        "locks": "`.lock [all/type(s)]`"
        "\n➥  Memungkinkan Anda mengunci beberapa jenis pesan umum dalam obrolan."
        "\n\n`.unlock [all/type(s)]`"
        "\n➥  Memungkinkan Anda membuka kunci beberapa jenis pesan umum dalam obrolan."
        "\n\n**CATATAN** : Membutuhkan hak admin yang tepat dalam obrolan!"
        "\n\n**Jenis pesan yang tersedia untuk dikunci / dibuka kuncinya adalah** : "
        "\n`all, msg, media, sticker, gif, game, inline, poll, invite, pin, info`"
    }
)
