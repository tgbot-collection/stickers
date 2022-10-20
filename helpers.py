#!/usr/bin/env python3
# coding: utf-8
import logging
import os
import subprocess
import zipfile
from pathlib import Path

from pyrogram.file_id import FileId, FileType


# stickers - helpers.py
# 2022-10-20  23:27
def get_target_file(src: Path):
    old_ext = src.suffix
    if old_ext in [".jpeg", ".jpg", ".png", ".webp"]:
        return src.with_suffix(".png")
    elif old_ext in [".mp4", ".webm", ".tgs"]:
        return src.with_suffix(".gif")
    else:
        return src.with_suffix(".mp4")


def converter(src_file):
    src_file = Path(src_file)
    target_file = get_target_file(src_file)
    logging.info(f"converting %s to %s", src_file, target_file)
    if src_file.suffix == ".tgs":
        subprocess.check_output(["lottie_convert.py", src_file, target_file])
    else:
        subprocess.check_output(["ffmpeg", "-i", src_file, target_file])
    return target_file.as_posix()


def get_file_id(doc, set_id, set_hash):
    return FileId(file_type=FileType.STICKER,
                  dc_id=doc.dc_id,
                  file_reference=doc.file_reference,
                  media_id=doc.id,
                  access_hash=doc.access_hash,
                  sticker_set_id=set_id,
                  sticker_set_access_hash=set_hash)


def get_ext_from_mime(mime):
    if mime == "image/jpeg":
        return ".jpg"
    elif mime == "image/png":
        return ".png"
    elif mime == "image/webp":
        return ".webp"
    elif mime == "video/mp4":
        return ".mp4"
    elif mime == "video/webm":
        return ".webm"
    elif mime == "application/x-tgsticker":
        return ".tgs"
    else:
        return ""


def zip_dir(dir_path, zip_filepath):
    logging.info("zipping %s to %s", dir_path, zip_filepath)
    zipf = zipfile.ZipFile(zip_filepath, 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            file_path = Path(root).joinpath(file)
            file_name = file_path.relative_to(dir_path)
            zipf.write(file_path, file_name)
    zipf.close()
