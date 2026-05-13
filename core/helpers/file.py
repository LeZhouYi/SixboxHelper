import json
import os.path
import zipfile
from io import BytesIO
from pathlib import Path
from typing import LiteralString, Union, Generator, Any, List, Dict

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


def download_file(url: str, save_path: str):
    """下载文件并保存到本地"""
    response = requests.get(url)
    response.raise_for_status()
    folder = os.path.dirname(save_path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(save_path, "wb") as file:
        file.write(response.content)


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


def write_text(filepath: Union[LiteralString, str], data: str):
    """
    写文本
    :param filepath: 文件路径
    :param data: 写入数据
    :return:
    """
    folder = os.path.dirname(filepath)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(data)


def get_filelist(folder: Union[LiteralString, str], extensions: List[str] = None) -> list[Union[LiteralString, str]]:
    """
    获取该路径对应的文件列表，未指定suffixes则返回所有
    :param extensions:
    :param folder:
    :return:
    """
    filelist = []
    for filename in os.listdir(folder):
        filepath = os.path.join(folder, filename)
        if os.path.isfile(filepath) and (extensions is None or os.path.splitext(filename)[-1].lower() in extensions):
            filelist.append(filename)
    return filelist


def write_json(filepath: Union[LiteralString, str], data: Union[Dict, List], ensure_ascii: bool = False,
               indent=4):
    """
    写json数据到本地文件，若文件不存在则新建
    :param filepath: 文件路径
    :param data: 写入数据
    :param ensure_ascii: 是否转码
    :param indent: 缩进
    :return:
    """
    folder = os.path.dirname(filepath)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=ensure_ascii, indent=indent)


def extract_file(filepath: Union[LiteralString, str], target_dir: Union[LiteralString, str]):
    """
    解压文件到特定文件夹
    :param filepath: 文件路径
    :param target_dir: 解压后要放置的文件夹，若不存在则会创建
    """
    if not os.path.exists(target_dir):
        os.makedirs(target_dir, exist_ok=True)
    with zipfile.ZipFile(filepath, "r") as zip_ref:
        zip_ref.extractall(target_dir)


def zip_file(source_folder: Union[LiteralString, str], output_path: Union[LiteralString, str]):
    """
    压缩文件夹内的所有内容到压缩包
    :param source_folder: 源文件夹
    :param output_path: 输出的文件路径
    :return:
    """
    folder_path = Path(source_folder)
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arc_name = os.path.relpath(file_path, folder_path)
                zipf.write(file_path, arc_name)


def read_text(filepath: Union[LiteralString, str]) -> str:
    """读取文本"""
    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()
    return content
