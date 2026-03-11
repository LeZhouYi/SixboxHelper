from datetime import datetime


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
