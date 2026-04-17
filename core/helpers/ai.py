import base64
import json
import logging
from typing import Optional

import requests

from core.env import AI_HOST, AI_MODEL, AI_URL, AI_API_KEY


def chat_with_image(image_url: str, message: str) -> str:
    """
    使用图片和文本与AI对话
    :param image_url:
    :param message:
    :return:
    """
    response = requests.post(
        url=f"{AI_HOST}/chat/completions",
        headers={
            "Content-Type": "application/json"
        },
        json={
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
    )
    if response.status_code != 200:
        raise Exception(f"请求失败：{response.status_code}, content:{response.content}")
    return response.json()["choices"][0]["message"]["content"]

def chat_with_images(images: list[bytes], message: str) -> str:
    """
    使用图片和文本与AI对话
    :param images:
    :param message:
    :return:
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
    response = requests.post(
        url=f"{AI_HOST}/chat/completions",
        headers={
            "Content-Type": "application/json"
        },
        json={
            "model": AI_MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": image_content
                }
            ],
            "stream": False
        }
    )
    if response.status_code != 200:
        raise Exception(f"请求失败：{response.status_code}, content:{response.content}")
    return response.json()["choices"][0]["message"]["content"]

def chat_with_api(messages: list, response_format: Optional[dict] = None) -> str:
    """
    与AI对话
    :param response_format:
    :param messages:
    :return:
    """
    logging.info(f"请求AI:{str(messages)[:100]}")
    json_body:dict = {
        "messages":messages
    }
    if format:
        json_body["response_format"]=response_format
    response = requests.post(
        url=AI_URL,
        headers={
            "Content-Type": "application/json",
            "api-key": AI_API_KEY
        },
        json={
            "messages": messages
        }
    )
    if response.status_code != 200:
        raise Exception(f"请求失败：{response.status_code}, content:{response.content}")
    return response.json()["choices"][0]["message"]["content"]

def chat_with_api_json(messages: list, response_format: Optional[dict] = None) -> str:
    """
    与AI对话
    :param response_format:
    :param messages:
    :return:
    """
    logging.info(f"请求AI:{str(messages)[:100]}")
    json_body:dict = {
        "messages":messages
    }
    if format:
        json_body["response_format"]=response_format
    response = requests.post(
        url=AI_URL,
        headers={
            "Content-Type": "application/json",
            "api-key": AI_API_KEY
        },
        json={
            "messages": messages
        }
    )
    if response.status_code != 200:
        raise Exception(f"请求失败：{response.status_code}, content:{response.content}")
    return json.loads(response.json()["choices"][0]["message"]["content"])

