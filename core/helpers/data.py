import json
import re
from datetime import datetime
from typing import Any


def format_date_str(source: str, source_format: str, des_format: str):
    """
    将原日期字符串转换为目标格式的字符串
    :param des_format:
    :param source_format:
    :param source:
    :return:
    """
    date_obj = datetime.strptime(source, source_format)
    return date_obj.strftime(des_format)


def replace_date_placeholders(text: str) -> str:
    """检测日期占位字符串并替换为当前实际日期"""
    pattern = r"{{date:(.*?)}}"

    def replacer(match):
        # 获取匹配到的格式，例如 %Y%m%d
        date_format = match.group(1)
        # 返回当前时间的格式化字符串
        return datetime.now().strftime(date_format)

    # 执行替换
    return re.sub(pattern, replacer, text)

def get_data_by_path(data:dict, path:str) -> Any:
    """获取字符串路径对应位置的数据"""
    keys = re.findall(r'[^.\[\]]+', path)
    current = data
    for key in keys:
        if isinstance(current, list):
            current = current[int(key)]  # 如果当前是列表，转为整数索引
        else:
            current = current[key]  # 如果当前是字典，直接用键名
    return current

def extract_json(text):
    # 匹配从第一个 { 到最后一个 } 的内容
    match = re.search(r'\{.*}', text, re.DOTALL)
    if match:
        json_str = match.group()
        return json.loads(json_str)
    else:
        raise ValueError("未在字符串中找到 JSON 内容")