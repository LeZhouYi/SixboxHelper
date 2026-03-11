def is_key_str_empty(data: dict, key: str) -> bool:
    """
    判断字典是否存在某数据且非空
    :param data:
    :param key:
    :return: true 表示 不存在或空
    """
    return key not in data or data[key] is None or str(data[key]).strip() == ""

def is_str_empty(value: str) -> bool:
    """
    判断字典是否存在某数据且非空
    :param value:
    :return: true 表示 不存在或空
    """
    return value is None or str(value).strip() == ""