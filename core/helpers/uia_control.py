import os.path
import re
import subprocess
import time
from typing import LiteralString, Union
from uuid import uuid4

import cv2
import numpy as np
import pywinauto.application
from PIL import ImageGrab
from PIL.Image import Image
from pywinauto import Application, WindowSpecification, Desktop
from pywinauto.controls.uiawrapper import UIAWrapper
from pywinauto.mouse import click

from core.log.logger import logger

def start_file(filepath: Union[LiteralString, str]):
    """通过文件路径启动应用"""
    if os.path.exists(filepath):
        subprocess.Popen(f'start "" "{filepath}"', shell=True, encoding="gbk")
    else:
        raise Exception(f"文件不存在：{filepath}")

def start_application(filepath: Union[LiteralString, str], backend: str = "uia", timeout: int = 30):
    """启动window应用"""
    logger.info(f"启动元素：{filepath}")
    if not os.path.exists(filepath):
        raise Exception(f"应用不存在：{filepath}")
    app = Application(backend=backend)
    try:
        return app.connect(path=filepath)
    except pywinauto.application.ProcessNotFoundError:
        logger.info(f"应用未启动，正在启动：{filepath}")
        subprocess.Popen(filepath, shell=True)
        return app.connect(path=filepath, timeout=timeout)


def focus_window(window: WindowSpecification):
    """聚焦窗口并最大化"""
    logger.info(f"聚焦元素：{window.window_text()}")
    window.set_focus()
    if isinstance(window, WindowSpecification) and not window.get_show_state() == 3:
        window.maximize()


def find_element(window: WindowSpecification, timeout: int = 10, **kwargs):
    """查找元素"""
    logger.info(f"查找元素：{kwargs}")
    element = window.child_window(**kwargs)
    if element.exists(timeout=timeout):
        return element
    raise Exception(f"查找元素失败：{kwargs}")


def debug_element(element: WindowSpecification):
    """调试元素"""
    logger.info(f"调试元素：{element}")
    if hasattr(element, "exists") and element.exists(timeout=3):
        element.draw_outline()  # 显示元素红框
    elif element is not None and hasattr(element, "draw_outline"):
        element.draw_outline()
    else:
        raise Exception("元素不存在")

def debug_element_image(element: WindowSpecification):
    """调试元素"""
    logger.info(f"调试元素：{element}")
    img = element.capture_as_image()
    img.show()

def debug_window(window: WindowSpecification):
    """调试窗口"""
    logger.info(f"调试窗口：{window}")
    if hasattr(window, "exists") and window.exists(timeout=3):
        window.print_control_identifiers()
        for element in window.descendants():
            print(f"元素：text:{element.window_text()}, type: {type(element).__name__}")
    elif window is not None:
        for element in window.descendants():
            print(f"元素：text:{element.window_text()}, type: {type(element).__name__}")
    else:
        raise Exception("窗口不存在")


def debug_app(app: Application):
    """调试应用"""
    logger.info(f"调试app:{app}")
    for window in app.windows():
        print(f"window: {window.window_text()} class:{type(window).__name__}")
    print(f"top_window: {app.top_window().window_text()}")


def find_desktop_window(desktop: Desktop, title_re: str, class_name: str):
    """查找桌面的窗口"""
    logger.info(f"查找桌面的窗口：title_re:{title_re}, class_name:{class_name}")
    for window in desktop.windows(visible_only=True):
        if re.search(title_re, window.window_text()) and type(window).__name__ == class_name:
            return window
    raise Exception(f"查找窗口失败：title_re:{title_re}, class_name: {class_name}")


def find_element_by_children(window: WindowSpecification, title_re: str, class_name: str):
    """通过children来遍历查找元素"""
    logger.info(f"通过children查找元素：title_re:{title_re}, class_name:{class_name}")
    for element in window.children():
        if re.search(title_re, element.window_text()) and type(element).__name__ == class_name:
            return element
    raise Exception(f"查找元素失败：title_re:{title_re}, class_name: {class_name}")


def find_element_by_descendants(window: WindowSpecification, title_re: str, class_name: str):
    """通过descendants来遍历查找元素"""
    logger.info(f"通过descendants查找元素：title_re:{title_re}, class_name:{class_name}")
    for element in window.descendants():
        if re.search(title_re, element.window_text()) and type(element).__name__ == class_name:
            return element
    raise Exception(f"查找元素失败：title_re:{title_re}, class_name: {class_name}")

def find_elements_by_descendants(window: WindowSpecification, title_re: str, class_name: str, limit:int = 0):
    """通过descendants来遍历查找多个元素"""
    logger.info(f"通过descendants查找多个元素：title_re:{title_re}, class_name:{class_name}")
    elements = []
    for element in window.descendants():
        if re.search(title_re, element.window_text()) and type(element).__name__ == class_name:
            elements.append(element)
        if 0 < limit == len(elements):
            break
    if len(elements) == 0 or (0 < limit != len(elements)):
        raise Exception(f"查找多个元素时未预期：{len(elements)}, expect: {limit}(零代表任意正整数)")
    return elements

def click_element(element: WindowSpecification, timeout: int = 10, rx: float = 0.5, ry: float = 0.5, **kwargs):
    """点击元素"""
    logger.info(f"点击元素：element:{element}, timeout:{timeout}, rx:{rx}, ry:{ry}, args:{kwargs}")
    if rx == 0.5 and ry == 0.5 and len(kwargs) == 0:
        if hasattr(element, "wait") and element.wait('ready', timeout=timeout):
            element.click_input()
            return
        elif hasattr(element, "click_input"):
            element.click_input()
            return
    rect = element.rectangle()
    x = int((rect.right - rect.left) * rx)
    y = int((rect.bottom - rect.top) * ry)
    element.click_input(coords=(x, y), **kwargs)


def exist_element_by_descendants(window: WindowSpecification, title_re: str, class_name: str):
    """通过descendants来遍历查找元素"""
    logger.info(f"通过descendants判断元素是否存在：title_re:{title_re} class_name:{class_name}")
    for element in window.descendants():
        if re.search(title_re, element.window_text()) and type(element).__name__ == class_name:
            return element
    return None


def click_by_template(parent: UIAWrapper, template_path: Union[os.PathLike, str], relative_x: float = 0.5,
                      relative_y: float = 0.5, match_val: float = 0.8):
    """图片模板匹配点击"""
    logger.info(
        f"通过模块匹配元素：parent:{parent}, template:{template_path}, rx:{relative_x}, ry:{relative_y}, match_val:{match_val}")
    template_path = os.path.abspath(template_path)

    rect = parent.rectangle()
    left, top, right, bottom = rect.left, rect.top, rect.right, rect.bottom

    screen = parent.capture_as_image()
    screen = cv2.cvtColor(np.array(screen, dtype=np.uint8), cv2.COLOR_RGB2GRAY)
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)

    # 模板匹配
    result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    logger.info(f"min_val:{min_val}, max_val: {max_val}, min_loc: {min_loc}, max_loc: {max_loc}")
    if max_val < match_val:
        raise Exception("未找到匹配控件：%s" % template_path)

    # 计算坐标
    template_h, template_w = template.shape[:2]
    top_left_x, top_left_y = max_loc
    x = int(left + top_left_x + template_w * relative_x)
    y = int(top + top_left_y + template_h * relative_y)

    # 点击
    click(coords=(x, y))


def match_template(parent: UIAWrapper, template_path: Union[os.PathLike, str], match_val: float = 0.8):
    """匹配模板"""
    logger.info(
        f"判断元素是否符合模板：parent:{parent}, template:{template_path}, match_val:{match_val}")
    template_path = os.path.abspath(template_path)

    screen = parent.capture_as_image()
    screen = cv2.cvtColor(np.array(screen, dtype=np.uint8), cv2.COLOR_RGB2GRAY)
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)

    # 模板匹配
    result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    logger.info(f"min_val:{min_val}, max_val: {max_val}, min_loc: {min_loc}, max_loc: {max_loc}")
    return max_val > match_val


def debug_capture(image: Image):
    """测试截图"""
    file = f"data/temp/{str(uuid4())}.png"
    logger.info(f"测试截图：{file}")
    image.save(file)

def save_desktop_shot(out_path: Union[os.PathLike, str], filename: str = None) -> Union[LiteralString | str]:
    """
        保存元素所属窗口的截图，MenuItemWrapper的父窗口可能没有，会报错
        pip install Pillow
    """
    try:
        if not os.path.exists(out_path):
            os.makedirs(out_path, exist_ok=True)
        if filename is None:
            filename = "%s.png" % (int(time.time()))
            time.sleep(1)
        image_path = os.path.join(out_path, filename)
        ImageGrab.grab().save(image_path)
        return image_path
    except Exception as e:
        raise Exception("截图失败：%s" % e)