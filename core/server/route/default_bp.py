import mimetypes
import os
from urllib.parse import quote

from flask import Blueprint, Response, jsonify

from core.helpers.file import get_stream_io
from core.helpers.validate import is_str_empty

DEFAULT_BP = Blueprint("default", __name__)
API_VERSION = "/api/v1"


@DEFAULT_BP.route(API_VERSION + "/files/<filename>", methods=["GET"])
def download_file(filename: str):
    """下载文件"""
    try:
        if is_str_empty(filename):
            raise Exception("File name cannot be empty")
        if filename.find("/") > -1:
            raise Exception("File name error")
        filepath = os.path.normpath(os.path.join(os.getcwd(), "/data/download", filename))
        if not os.path.exists(filepath):
            raise Exception("The file does not exist.")
        mime_type, _ = mimetypes.guess_type(filepath)
        return Response(get_stream_io(filepath), mimetype=mime_type, headers={
            "Content-Disposition": "attachment;filename=%s" % quote(filename)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400
