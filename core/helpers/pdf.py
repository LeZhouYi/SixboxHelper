from io import BytesIO

import fitz
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
