import base64
import logging
from enum import Enum
from typing import Optional, Union, Dict, List

import requests

from core.env import AI_API_KEY, AI_MODEL, AI_URL, AI_AUTH_TYPE, REQUEST_TIMEOUT
from core.helpers.data import extract_json


class Role(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


def generate_message(content: str, role: str):
    return {
        "role": role,
        "content": content
    }


def generate_headers(auth_type: str) -> dict:
    """生成对应类型的请求头"""
    if auth_type == "api-key":
        return {
            "Content-Type": "application/json",
            "api-key": AI_API_KEY
        }
    elif auth_type == "bearer":
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {AI_API_KEY}"
        }
    else:
        raise Exception(f"不支持的认证类型：{auth_type}")


def chat_with_image(image_url: str, message: str, ai_type: str = "silicon") -> str:
    """
    使用图片和文本与AI对话
    """
    json_body = {
        "model": AI_MODEL,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_url
                        }
                    },
                    {
                        "type": "text",
                        "text": message
                    }
                ]
            }
        ],
        "stream": False
    }
    if ai_type == "silicon":
        json_body.update({
            "enable_thinking": False
        })
    response = requests.post(
        url=AI_URL,
        headers=generate_headers(AI_AUTH_TYPE),
        json=json_body,
        timeout=REQUEST_TIMEOUT
    )
    if response.status_code != 200:
        raise Exception(f"请求失败：{response.status_code}, content:{response.content}")
    data = response.json()
    if "usage" in data:
        logging.info(f"token消耗：{data["usage"]}")
    return data["choices"][0]["message"]["content"]


def chat_with_images(images: list[bytes], message: str, ai_type: str = "silicon") -> str:
    """
    使用图片和文本与AI对话
    """
    image_content = []
    for item_bytes in images:
        base64_data = base64.b64encode(item_bytes).decode("utf-8")
        image_content.append({
            "type": "image_url",
            "image_url": {
                "url": f"data:image/png;base64,{base64_data}"
            }
        })
    image_content.append({
        "type": "text",
        "text": message
    })
    json_body = {
        "model": AI_MODEL,
        "messages": [
            {
                "role": "user",
                "content": image_content
            }
        ],
        "stream": False
    }
    if ai_type == "silicon":
        json_body.update({
            "enable_thinking": False
        })
    response = requests.post(
        url=AI_URL,
        headers=generate_headers(AI_AUTH_TYPE),
        json=json_body,
        timeout=REQUEST_TIMEOUT
    )
    if response.status_code != 200:
        raise Exception(f"请求失败：{response.status_code}, content:{response.content}")
    data = response.json()
    if "usage" in data:
        logging.info(f"token消耗：{data["usage"]}")
    return data["choices"][0]["message"]["content"]


def chat_with_api(messages: list, response_format: Optional[dict] = None, ai_type: str = "silicon") -> str:
    """
    与AI对话
    """
    logging.info(f"请求AI:{str(messages)[:100]}")
    json_body: dict = {
        "model": AI_MODEL,
        "messages": messages,
        "stream": False,
    }
    if format:
        json_body["response_format"] = response_format
    if ai_type == "silicon":
        json_body.update({
            "enable_thinking": False
        })
    response = requests.post(
        url=AI_URL,
        headers=generate_headers(AI_AUTH_TYPE),
        json=json_body,
        timeout=REQUEST_TIMEOUT
    )
    if response.status_code != 200:
        raise Exception(f"请求失败：{response.status_code}, content:{response.content}")
    data = response.json()
    if "usage" in data:
        logging.info(f"token消耗：{data["usage"]}")
    return data["choices"][0]["message"]["content"]


def chat_with_api_json(messages: list, response_format: Optional[dict] = None, ai_type: str = "silicon") -> Union[
    Dict, List]:
    """与AI对话并返回json"""
    logging.info(f"请求AI:{str(messages)[:100]}")
    json_body: dict = {
        "model": AI_MODEL,
        "messages": messages,
        "stream": False,
    }
    if format:
        json_body["response_format"] = response_format
    if ai_type == "silicon":
        json_body.update({
            "enable_thinking": False
        })
    response = requests.post(
        url=AI_URL,
        headers=generate_headers(AI_AUTH_TYPE),
        json=json_body,
        timeout=REQUEST_TIMEOUT
    )
    if response.status_code != 200:
        raise Exception(f"请求失败：{response.status_code}, content:{response.content}")
    data = response.json()
    content = data["choices"][0]["message"]["content"]
    if "usage" in data:
        logging.info(f"token消耗：{data["usage"]}")
    return extract_json(content)
