# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
# Credits to @aryanvikash for zippyshare
#
""" Userbot module containing various sites direct links generators"""

import asyncio
import json
import re
import urllib.parse
from asyncio import create_subprocess_shell as asyncSubprocess
from asyncio.subprocess import PIPE as asyncPIPE
from random import choice

import aiohttp
import requests
from bs4 import BeautifulSoup
from humanize import naturalsize

from userbot import CMD_HELP, USR_TOKEN
from userbot.events import register
from userbot.utils import time_formatter

_REGEX_LINK = r"https://www(\d{1,3}).zippyshare.com/v/(\w{8})/file.html"
_REGEX_RESULT = (
    r'document.getElementById\(\'dlbutton\'\).href = "/d/[a-zA-Z\d]{8}/" '
    r'\+ \((\d+) % (\d+) \+ (\d+) % (\d+)\) \+ "\/(.+)";'
)
_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome"
    "/75.0.3770.100 Safari/537.36"
}


async def subprocess_run(cmd):
    reply = ""
    subproc = await asyncSubprocess(cmd, stdout=asyncPIPE, stderr=asyncPIPE)
    result = await subproc.communicate()
    exitCode = subproc.returncode
    if exitCode != 0:
        reply += (
            "**Kesalahan terdeteksi saat menjalankan subproses**\n"
            f"exitCode : `{exitCode}`\n"
            f"stdout : `{result[0].decode().strip()}`\n"
            f"stderr : `{result[1].decode().strip()}`"
        )
        return reply
    return result


@register(outgoing=True, pattern=r"^\.direct(?: |$)([\s\S]*)")
async def direct_link_generator(request):
    """ direct links generator """
    await request.edit("`Sedang memproses...`")
    textx = await request.get_reply_message()
    message = request.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await request.edit("`Gunakan .direct [url]`")
        return
    reply = ""
    links = re.findall(r"\bhttps?://.*\.\S+", message)
    if not links:
        reply = "`Tautan tidak ditemukan!`"
        await request.edit(reply)
    for link in links:
        if "zippyshare.com" in link:
            reply += await zippy_share(link)
        elif "yadi.sk" in link:
            reply += await yandex_disk(link)
        elif "cloud.mail.ru" in link:
            reply += await cm_ru(link)
        elif "mediafire.com" in link:
            reply += await mediafire(link)
        elif "sourceforge.net" in link:
            reply += await sourceforge(link)
        elif "osdn.net" in link:
            reply += await osdn(link)
        elif "github.com" in link:
            reply += await github(link)
        elif "androidfilehost.com" in link:
            reply += await androidfilehost(link)
        elif "uptobox.com" in link:
            await uptobox(request, link)
            return None
        else:
            reply += re.findall(r"\bhttps?://(.*?[^/]+)", link)[0] + " tidak didukung!"
    await request.edit(reply)


async def zippy_share(url: str) -> str:
    reply = ""
    try:
        session = requests.Session()
        session.headers.update(_HEADERS)
        with session as ses:
            match = re.match(_REGEX_LINK, url)
            if not match:
                raise ValueError("**URL tidak valid** : " + str(url))
            server, id_ = match.group(1), match.group(2)
            res = ses.get(url)
            res.raise_for_status()
            match = re.search(_REGEX_RESULT, res.text)
            if not match:
                raise ValueError("`Respon tidak valid!`")
            val_1 = int(match.group(1))
            val_2 = int(match.group(2))
            val_3 = int(match.group(3))
            val_4 = int(match.group(4))
            val = val_1 % val_2 + val_3 % val_4
            name = match.group(5)
            d_l = "https://www{}.zippyshare.com/d/{}/{}/{}".format(
                server, id_, val, name
            )
        name = urllib.parse.unquote(d_l.split("/")[-1])
        reply += f"[{name}]({d_l})\n"
    except Exception as err:
        reply += f"{err}"
    return reply


async def yandex_disk(url: str) -> str:
    """Yandex.Disk direct links generator
    Based on https://github.com/wldhx/yadisk-direct"""
    reply = ""
    try:
        link = re.findall(r"\bhttps?://.*yadi\.sk\S+", url)[0]
    except IndexError:
        reply = "`Tautan Yandex.Disk tidak ditemukan`\n"
        return reply
    api = "https://cloud-api.yandex.net/v1/disk/public/resources/download?public_key={}"
    try:
        dl_url = requests.get(api.format(link)).json()["href"]
        name = dl_url.split("filename=")[1].split("&disposition")[0]
        reply += f"[{name}]({dl_url})\n"
    except KeyError:
        reply += "**Kesalahan** : `File tidak ditemukan / batas unduhan telah tercapai.`\n"
        return reply
    return reply


async def cm_ru(url: str) -> str:
    """cloud.mail.ru direct links generator
    Using https://github.com/JrMasterModelBuilder/cmrudl.py"""
    reply = ""
    try:
        link = re.findall(r"\bhttps?://.*cloud\.mail\.ru\S+", url)[0]
    except IndexError:
        reply = "`Tautan cloud.mail.ru tidak ditemukan`\n"
        return reply
    cmd = f"bin/cmrudl -s {link}"
    result = subprocess_run(cmd)
    try:
        result = result[0].splitlines()[-1]
        data = json.loads(result)
    except json.decoder.JSONDecodeError:
        reply += "**Kesalahan** : `Tidak dapat mengekstrak tautan`\n"
        return reply
    except IndexError:
        return reply
    dl_url = data["download"]
    name = data["file_name"]
    size = naturalsize(int(data["file_size"]))
    reply += f"[{name} ({size})]({dl_url})\n"
    return reply


async def mediafire(url: str) -> str:
    """ MediaFire direct links generator """
    try:
        link = re.findall(r"\bhttps?://.*mediafire\.com\S+", url)[0]
    except IndexError:
        reply = "`Tautan MediaFire tidak ditemukan`\n"
        return reply
    reply = ""
    page = BeautifulSoup(requests.get(link).content, "lxml")
    info = page.find("a", {"aria-label": "Download file"})
    dl_url = info.get("href")
    size = re.findall(r"\(.*\)", info.text)[0]
    name = page.find("div", {"class": "filename"}).text
    reply += f"[{name} {size}]({dl_url})\n"
    return reply


async def sourceforge(url: str) -> str:
    """ SourceForge direct links generator """
    try:
        link = re.findall(r"\bhttps?://.*sourceforge\.net\S+", url)[0]
    except IndexError:
        reply = "`Tautan SourceForge tidak ditemukan`\n"
        return reply
    file_path = re.findall(r"files(.*)/download", link)[0]
    reply = f"Mirror untuk __{file_path.split('/')[-1]}__\n"
    project = re.findall(r"projects?/(.*?)/files", link)[0]
    mirrors = (
        f"https://sourceforge.net/settings/mirror_choices?"
        f"projectname={project}&filename={file_path}"
    )
    page = BeautifulSoup(requests.get(mirrors).content, "html.parser")
    info = page.find("ul", {"id": "mirrorList"}).findAll("li")
    for mirror in info[1:]:
        name = re.findall(r"\((.*)\)", mirror.text.strip())[0]
        dl_url = (
            f'https://{mirror["id"]}.dl.sourceforge.net/project/{project}/{file_path}'
        )
        reply += f"[{name}]({dl_url}) "
    return reply


async def osdn(url: str) -> str:
    """ OSDN direct links generator """
    osdn_link = "https://osdn.net"
    try:
        link = re.findall(r"\bhttps?://.*osdn\.net\S+", url)[0]
    except IndexError:
        reply = "`Tautan OSDN tidak ditemukan`\n"
        return reply
    page = BeautifulSoup(requests.get(link, allow_redirects=True).content, "lxml")
    info = page.find("a", {"class": "mirror_link"})
    link = urllib.parse.unquote(osdn_link + info["href"])
    reply = f"Mirror untuk __{link.split('/')[-1]}__\n"
    mirrors = page.find("form", {"id": "mirror-select-form"}).findAll("tr")
    for data in mirrors[1:]:
        mirror = data.find("input")["value"]
        name = re.findall(r"\((.*)\)", data.findAll("td")[-1].text.strip())[0]
        dl_url = re.sub(r"m=(.*)&f", f"m={mirror}&f", link)
        reply += f"[{name}]({dl_url}) "
    return reply


async def github(url: str) -> str:
    """ GitHub direct links generator """
    try:
        link = re.findall(r"\bhttps?://.*github\.com.*releases\S+", url)[0]
    except IndexError:
        reply = "`Tautan Rilis GitHub tidak ditemukan`\n"
        return reply
    reply = ""
    dl_url = ""
    download = requests.get(url, stream=True, allow_redirects=False)
    try:
        dl_url = download.headers["location"]
    except KeyError:
        reply += "**Kesalahan** : `Tidak dapat mengekstrak tautan`\n"
    name = link.split("/")[-1]
    reply += f"[{name}]({dl_url}) "
    return reply


async def androidfilehost(url: str) -> str:
    """ AFH direct links generator """
    try:
        link = re.findall(r"\bhttps?://.*androidfilehost.*fid.*\S+", url)[0]
    except IndexError:
        reply = "`Tautan AFH tidak ditemukan`\n"
        return reply
    fid = re.findall(r"\?fid=(.*)", link)[0]
    session = requests.Session()
    user_agent = await useragent()
    headers = {"user-agent": user_agent}
    res = session.get(link, headers=headers, allow_redirects=True)
    headers = {
        "origin": "https://androidfilehost.com",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9",
        "user-agent": user_agent,
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "x-mod-sbb-ctype": "xhr",
        "accept": "*/*",
        "referer": f"https://androidfilehost.com/?fid={fid}",
        "authority": "androidfilehost.com",
        "x-requested-with": "XMLHttpRequest",
    }
    data = {"submit": "submit", "action": "getdownloadmirrors", "fid": f"{fid}"}
    mirrors = None
    reply = ""
    error = "**Kesalahan** : `Tidak dapat menemukan tautan untuk Mirror`\n"
    try:
        req = session.post(
            "https://androidfilehost.com/libs/otf/mirrors.otf.php",
            headers=headers,
            data=data,
            cookies=res.cookies,
        )
        mirrors = req.json()["MIRRORS"]
    except (json.decoder.JSONDecodeError, TypeError):
        reply += error
    if not mirrors:
        reply += error
        return reply
    for item in mirrors:
        name = item["name"]
        dl_url = item["url"]
        reply += f"[{name}]({dl_url}) "
    return reply


async def uptobox(request, url: str) -> str:
    """ Uptobox direct links generator """
    try:
        link = re.findall(r"\bhttps?://.*uptobox\.com\S+", url)[0]
    except IndexError:
        await request.edit("`Tautan Uptobox tidak ditemukan`")
        return
    if USR_TOKEN is None:
        await request.edit("`Setel dahulu`  **USR_TOKEN_UPTOBOX!**")
        return
    if link.endswith("/"):
        index = -2
    else:
        index = -1
    FILE_CODE = link.split("/")[index]
    origin = "https://uptobox.com/api/link"
    """ Retrieve file informations """
    uri = f"{origin}/info?fileCodes={FILE_CODE}"
    await request.edit("`Mengambil informasi file...`")
    async with aiohttp.ClientSession() as session:
        async with session.get(uri) as response:
            result = json.loads(await response.text())
            data = result.get("data").get("list")[0]
            if "error" in data:
                await request.edit(
                    "`[KESALAHAN]`\n"
                    f"`statusCode :` **{data.get('error').get('code')}**\n"
                    f"`alasan :` **{data.get('error').get('message')}**"
                )
                return
            file_name = data.get("file_name")
            file_size = naturalsize(data.get("file_size"))
    """ Get waiting token and direct download link """
    uri = f"{origin}?token={USR_TOKEN}&file_code={FILE_CODE}"
    async with aiohttp.ClientSession() as session:
        async with session.get(uri) as response:
            result = json.loads(await response.text())
            status = result.get("message")
            if status == "Menunggu dibutuhkan":
                wait = result.get("data").get("waiting")
                waitingToken = result.get("data").get("waitingToken")
                await request.edit(f"`Menunggu tentang {time_formatter(wait)}.`")
                # for some reason it doesn't go as i planned
                # so make it 1 minute just to be save enough
                await asyncio.sleep(wait + 60)
                uri += f"&waitingToken={waitingToken}"
                async with session.get(uri) as response:
                    await request.edit("`Menghasilkan tautan unduhan langsung...`")
                    result = json.loads(await response.text())
                    status = result.get("message")
                    if status == "Berhasil":
                        webLink = result.get("data").get("dlLink")
                        await request.edit(f"[{file_name} ({file_size})]({webLink})")
                        return
                    else:
                        await request.edit(
                            "`[KESALAHAN]`\n"
                            f"`statusCode :` **{result.get('statusCode')}**\n"
                            f"`alasan :` **{result.get('data')}**\n"
                            f"`status :` **{status}**"
                        )
                        return
            elif status == "Berhasil":
                webLink = result.get("data").get("dlLink")
                await request.edit(f"[{file_name} ({file_size})]({webLink})")
                return
            else:
                await request.edit(
                    "`[KESALAHAN]`\n"
                    f"`statusCode :` **{result.get('statusCode')}**\n"
                    f"`alasan :` **{result.get('data')}**\n"
                    f"`status :` **{status}**"
                )
                return


async def useragent():
    """
    useragent random setter
    """
    useragents = BeautifulSoup(
        requests.get(
            "https://developers.whatismybrowser.com/"
            "useragents/explore/operating_system_name/android/"
        ).content,
        "lxml",
    ).findAll("td", {"class": "useragent"})
    user_agent = choice(useragents)
    return user_agent.text


CMD_HELP.update(
    {
        "direct": "`.direct [url]`"
        "\n➥  Balas tautan atau tempel URL untuk "
        "menghasilkan tautan unduhan langsung.\n\n"
        "**Daftar URL yang didukung** :\n"
        "`Google Drive - Cloud Mail - Yandex.Disk - AFH - "
        "ZippyShare - MediaFire - SourceForge - OSDN - GitHub`"
    }
)
