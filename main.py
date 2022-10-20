#!/usr/bin/env python3
# coding: utf-8

# stickers - main.py
# 2022-10-20  19:49

import logging
import os
import shutil
import tempfile
from pathlib import Path

from pyrogram import Client, enums, filters, types
from pyrogram.raw import functions
from pyrogram.raw import types as raw_types

import constants
from helpers import converter, get_ext_from_mime, get_file_id, zip_dir

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

app = Client("sticker", API_ID, API_HASH, bot_token=BOT_TOKEN, in_memory=True)

batch = {}  # uid - temp dir


@app.on_message(filters.command(["start"]))
async def start_handler(client: "Client", message: "types.Message"):
    await message.reply_text(constants.start_text)


@app.on_message(filters.command(["help"]))
async def help_handler(client: "Client", message: "types.Message"):
    await message.reply_text(constants.help_text)


@app.on_message(filters.command(["batch_start", "batch_stop"]))
async def batch_start(client: "Client", message: "types.Message"):
    if message.text == "/batch_start":
        batch[message.from_user.id] = tempfile.mkdtemp()
        await message.reply_text(constants.batch_start)
    else:
        target_dir = batch.pop(message.from_user.id)
        with tempfile.NamedTemporaryFile(suffix=".zip") as zip_filepath:
            zip_dir(target_dir, zip_filepath)
            await message.reply_chat_action(enums.ChatAction.UPLOAD_DOCUMENT)
            await message.reply_document(zip_filepath.name)
            shutil.rmtree(target_dir)


@app.on_message(filters.text & filters.incoming & filters.regex(r"https://t.me/addstickers/.*"))
async def entire_set(client: "Client", message: "types.Message"):
    short_name = message.text.replace("https://t.me/addstickers/", "")
    s = raw_types.InputStickerSetShortName(short_name=short_name)

    packs: raw_types.messages.StickerSet = await client.invoke(functions.messages.GetStickerSet(stickerset=s, hash=0))
    tempdir = tempfile.mkdtemp()
    for doc in packs.documents:
        file_id = get_file_id(doc, packs.set.id, packs.set.access_hash)

        ext = get_ext_from_mime(doc.mime_type)
        with open(Path(tempdir).joinpath(f"{doc.id}{ext}"), "wb") as file:
            async for chunk in client.get_file(file_id):
                file.write(chunk)

    with tempfile.NamedTemporaryFile(suffix=".zip") as zip_filepath:
        zip_dir(tempdir, zip_filepath)
        await message.reply_chat_action(enums.ChatAction.UPLOAD_DOCUMENT)
        await message.reply_document(zip_filepath.name)
        shutil.rmtree(tempdir)


@app.on_message(filters.text & filters.incoming)
async def emoji_sticker_handler(client: "Client", message: "types.Message"):
    stickers = await app.get_custom_emoji_stickers(
        [i.custom_emoji_id for i in message.entities if i.type.name == 'CUSTOM_EMOJI' if i]
    )
    for sticker in stickers:
        await message.reply_chat_action(enums.ChatAction.UPLOAD_DOCUMENT)
        with tempfile.NamedTemporaryFile(suffix=sticker.file_name) as temp:
            await client.download_media(sticker.file_id, file_name=temp.name)
            target_file = converter(temp.name)
            await client.send_document(message.chat.id, target_file)


@app.on_message(filters.sticker & filters.incoming)
async def sticker_handler(client: "Client", message: "types.Message"):
    await message.reply_chat_action(enums.ChatAction.TYPING)
    if temp := batch.get(message.from_user.id):
        file_id = message.sticker.file_id
        ext = message.sticker.file_name.split(".")[-1]
        filepath: "Path" = Path(temp).joinpath(f"{file_id}.{ext}")
        await client.download_media(message, file_name=filepath.as_posix())
        converter(filepath)
        filepath.unlink()
        await message.reply_text(constants.batch_save)
    else:
        with tempfile.NamedTemporaryFile(suffix=message.sticker.file_name) as temp:
            await client.download_media(message, file_name=temp.name)
            target_file = converter(temp.name)
            await client.send_document(message.chat.id, target_file)


if __name__ == '__main__':
    app.run()
