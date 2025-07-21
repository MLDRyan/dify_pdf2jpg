import requests
from pdf2image import convert_from_bytes
import os
from uuid import uuid4
from typing import List

OUTPUT_FOLDER = "jpg_outputs"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def pdf_url_to_jpg(sys_files: list) -> List[str]:
    if not sys_files or "url" not in sys_files[0]:
        raise ValueError("無有效的 PDF URL")

    pdf_url = sys_files[0]["url"]
    response = requests.get(pdf_url)
    if response.status_code != 200:
        raise Exception(f"無法下載 PDF，狀態碼: {response.status_code}")

    images = convert_from_bytes(response.content, dpi=200)
    output_paths = []

    for i, image in enumerate(images):
        filename = f"{uuid4()}_page_{i+1}.jpg"
        filepath = os.path.join(OUTPUT_FOLDER, filename)
        image.save(filepath, "JPEG")
        output_paths.append(filepath)

    return output_paths
