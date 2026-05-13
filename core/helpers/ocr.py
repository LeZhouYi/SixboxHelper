import logging
from io import BytesIO

import requests

from core.env import OCR_URL, OCR_TYPE


def get_ocr_text(image_io: BytesIO):
    """提取图片中的文本"""
    logging.info("提取图片文本")
    image_io.seek(0)
    response = requests.post(
        url=OCR_URL,
        files={
            "file": ("page.png", image_io, "image/png")
        },
        data={
            "ocr_type": OCR_TYPE
        }
    )
    if response.status_code != 200:
        raise Exception(f"请求失败：{response.status_code}, content:{response.content[:300]}")
    return response.json()["text"]