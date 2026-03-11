import base64

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
    response.raise_for_status()
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
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

def chat_with_api(messages: list) -> str:
    """
    与AI对话
    :param messages:
    :return:
    """
    response = requests.post(
        url=AI_URL,
        headers={
            "Content-Type": "application/json",
            "api-key": AI_API_KEY
        },
        json={
            "model": AI_MODEL,
            "messages": messages
        }
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]
