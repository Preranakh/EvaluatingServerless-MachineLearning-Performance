import os
import uuid
import shutil
import requests

from loguru import logger


def download_img_from_url(img_url: str) -> str:
    logger.info("Downloading image...")
    filename = uuid.uuid4().hex
    ext = img_url.split("/")[-1].split(".")[-1]
    file_path = os.path.join(
        os.path.dirname(__file__), "../", "tmp", filename + "." + ext
    )
    r = requests.get(img_url, stream=True)
    if r.status_code == 200:
        r.raw.decode_content = True

        with open(file_path, "wb") as f:
            shutil.copyfileobj(r.raw, f)
        logger.info("Download successful...")
        return file_path
    else:
        logger.error("Download failed...")
        return "DOWNLOAD_ERROR"
