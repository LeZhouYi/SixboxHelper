import logging
from uuid import uuid4

import requests

from core.env import CODE_INTERPRETER_URL


def exec_code(code:str):
    """执行代码"""
    logging.info("执行代码")
    response = requests.post(
        url=CODE_INTERPRETER_URL,
        headers={
            "Content-Type": "application/json",
        },
        json={
            "code": code,
            "thread_id": str(uuid4())
        }
    )
    if response.status_code != 200:
        raise Exception(f"请求失败：{response.status_code}, content:{response.content[:300]}")
    return response.json()