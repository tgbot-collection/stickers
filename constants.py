#!/usr/bin/env python3
# coding: utf-8

# stickers - constants.py
# 2022-10-20  23:26

start_text = ("Telegram sticker download bot. @BennyThink"
              "This bot supports all types of stickers, including animated stickers and even tgs format.")

help_text = \
    """
1⃣️ How to save stickers:
Just send your stickers.
Normal stickers: will send as png format.
Animated stickers: will send as gif format.
Emoji stickers: send custom emoji. You can send multiple emoji at once

2⃣️ What is batch mode?
Batch mode is a mode that allows you to download multiple stickers at once.
To start batch mode, send /batch_start, then send your stickers as many as you want.
When you are done, send /batch_stop, and the bot will send you a zip file containing all the stickers.

3⃣️ How to download an entire sticker pack?
Just send the sticker set link to the bot.
    """

batch_start = "Batch download started, please send your sticker!"
batch_save = "Sticker saved. Send /batch_stop if you're done."
