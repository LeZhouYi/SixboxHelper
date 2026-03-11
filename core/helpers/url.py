import posixpath
from urllib.parse import urlsplit, unquote


def parse_filename(url: str) -> str:
    """
    从链接中解析出文件名
    :param url:
    :return:
    """
    path = urlsplit(url).path
    filename = posixpath.basename(path)
    return unquote(filename)
