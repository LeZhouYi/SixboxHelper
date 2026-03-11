import json
import os.path
from io import BytesIO
from typing import LiteralString, Union, Generator, Any

import requests


def get_file_extension(filename: Union[LiteralString, str]) -> str:
    """
    提取文件名的后缀
    :param filename:
    :return:
    """
    return os.path.splitext(filename)[-1].lower()


def download_file_on_load(url: str) -> BytesIO:
    """
    下载文件并载入内存
    :param url:
    :return:
    """
    response = requests.get(url)
    response.raise_for_status()
    file = BytesIO(response.content)
    return file

def load_json(filepath: Union[LiteralString, str]):
    """
    加载本地的JSON数据
    :param filepath: 文件路径
    :return:
    """
    if not os.path.exists(filepath) or not os.path.isfile(filepath):
        raise FileNotFoundError(str(filepath))
    with open(filepath, encoding="utf-8") as file:
        return json.load(file)

def get_stream_io(filepath: str, chunk_size: int = None) -> Generator[bytes, Any, None]:
    """
    获取文件流式传输流
    :param filepath:
    :param chunk_size:
    :return:
    """
    chunk_size = chunk_size or 1024
    with open(filepath, "rb") as file:
        while True:
            data = file.read(chunk_size)
            if not data:
                break
            yield data