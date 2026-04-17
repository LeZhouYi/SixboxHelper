from io import BytesIO
from typing import Union, LiteralString, Tuple

import fitz
import pdfplumber
from PIL import Image, ImageDraw
from pymupdf import Document, Page


def pdf_to_images(file_io: BytesIO) -> list[bytes]:
    """
    将pdf转成图片
    :param file_io:
    :return:
    """
    with fitz.open(stream=file_io, filetype="pdf") as doc:
        image_bytes = []
        for i in range(doc.page_count):
            page = doc.load_page(i)
            pixmap = page.get_pixmap(dpi=300)
            image_bytes.append(pixmap.tobytes("png"))
    return image_bytes


def get_document_text(doc: Document):
    """
    获取PDF全文
    :param doc:
    :return:
    """
    text = ""
    for i in range(doc.page_count):
        text += doc.load_page(i).get_text()
    return text


def debug_pdf_blocks(document: Document):
    """
    打印pdf每一block的信息
    :param document:
    :return:
    """
    for i in range(document.page_count):
        page = document.load_page(i)
        print(f"--- 正在处理第{i + 1}页----")
        for block in page.get_text("blocks"):
            print(block)


def debug_pdf_rect(page: Page, rect: fitz.Rect):
    """
    绘制矩形框并展示
    :param page:
    :param rect:
    :return:
    """
    pix = page.get_pixmap()
    img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    draw = ImageDraw.Draw(img)
    draw.rectangle([rect.x0, rect.y0, rect.x1, rect.y1], outline="red", width=2)
    img.show()


def get_lines_in_rect(page: Page, rect: fitz.Rect) -> list[str]:
    """
    获取在范围的所有行的文本
    :param page:
    :param rect:
    :return:
    """
    lines = []
    for block in page.get_text("dict", flags=fitz.TEXTFLAGS_TEXT)["blocks"]:
        for line in block.get("lines", []):
            line_text = "".join(span["text"] for span in line["spans"])
            is_in = True
            bbox = line["bbox"]
            for point in [(bbox[0], bbox[1]), (bbox[2], bbox[1]), (bbox[0], bbox[3]), (bbox[2], bbox[3])]:
                if fitz.Point(point[0], point[1]) not in rect:
                    is_in = False
                    break
            if is_in:
                lines.append(line_text)
    return lines

def extract_structured_lines_text(page: pdfplumber.pdf.Page, y_threshold=5):
    """
    提取 PDF 页面的结构化行（按表格物理位置排序）。
    :param page:
    :param y_threshold: 同一行的垂直容差 (像素)，默认 5
    :return: 直接返回按物理位置排版好的纯文本（自动分行、空格）
    """
    # 先按 top (垂直坐标) 排序，方便聚类
    words_sorted = sorted(page.extract_words(), key=lambda k: k['top'])
    lines = []
    current_line = []
    last_top = None
    for w in words_sorted:
        # 按垂直坐标聚类成行，如果垂直距离超过阈值，视为新的一行
        if last_top is None or abs(w['top'] - last_top) > y_threshold:
            if current_line:
                # 对当前行内的单词按 x0 (水平坐标) 排序
                current_line.sort(key=lambda k: k['x0'])
                lines.append(current_line)
            current_line = []
        current_line.append(w)
        last_top = w['top']
    # 处理最后一行
    if current_line:
        current_line.sort(key=lambda k: k['x0'])
        lines.append(current_line)
    result_text = "\n".join([
        " ".join([w['text'] for w in line]).strip()
        for line in lines
    ])
    return result_text


def extract_pages(input_pdf: Union[LiteralString, str], output_pdf: Union[LiteralString, str], indexes: list):
    """
    使用 PyMuPDF 提取页面
    :param output_pdf:
    :param input_pdf:
    :param indexes: 索引列表（从0开始计数）
    """
    doc = fitz.open(input_pdf)
    # select() 方法会根据提供的索引列表重新排列或筛选页面
    doc.select(indexes)
    doc.save(output_pdf)
    doc.close()


def remove_spans_by_bbox(input_pdf: Union[LiteralString, str], output_pdf: Union[LiteralString, str], page_index: int,
                         bbox: Tuple):
    """
    移除指定页面、指定 bbox 范围内的文字内容
    :param page_index:
    :param output_pdf:
    :param input_pdf:
    :param bbox: 格式为 (x0, y0, x1, y1) 的元组或列表
    """
    doc = fitz.open(input_pdf)
    page = doc[page_index]

    page.add_redact_annot(bbox)

    # 应用编辑：永久删除区域内的所有文字/图像内容
    page.apply_redactions()

    # 使用 garbage=4 和 deflate=True 可以进一步清理文件并压缩空间
    doc.save(output_pdf, garbage=4, deflate=True)
    doc.close()
