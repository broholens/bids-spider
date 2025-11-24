"""Utilities for interacting with Baidu OCR (AipOcr)."""

from __future__ import annotations

import io
import os
from dataclasses import dataclass
from typing import List
import uuid

from PIL import Image, ImageFilter
from aip import AipOcr
import pytesseract
import requests
import cv2
import numpy as np

from utils.log import logger

DEFAULT_THRESHOLD = 25


def _ensure_credentials(app_id: str, api_key: str, secret_key: str) -> None:
    missing = [name for name, value in {
        "app_id": app_id,
        "api_key": api_key,
        "secret_key": secret_key,
    }.items() if not value]
    if missing:
        raise ValueError(f"Missing Baidu OCR credential(s): {', '.join(missing)}")


@dataclass
class OCRResult:
    words: List[str]

    @classmethod
    def from_response(cls, response: dict) -> "OCRResult":
        words = []
        for item in response.get("words_result", []):
            text = item.get("words")
            if text:
                words.append(text.strip())
        return cls(words=words)


class BaiduOCR:
    """Wrapper around Baidu AipOcr with simple image preprocessing."""

    def __init__(self, app_id: str, api_key: str, secret_key: str, *, threshold: int = DEFAULT_THRESHOLD):
        _ensure_credentials(app_id, api_key, secret_key)
        self.client = AipOcr(app_id, api_key, secret_key)
        self.threshold = threshold

    @classmethod
    def from_env(cls, prefix: str = "BAIDU_OCR_", *, threshold: int = DEFAULT_THRESHOLD) -> "BaiduOCR":
        """Create client using environment variables such as BAIDU_OCR_APP_ID."""
        app_id = os.getenv(f"{prefix}APP_ID")
        api_key = os.getenv(f"{prefix}API_KEY")
        secret_key = os.getenv(f"{prefix}SECRET_KEY")
        return cls(app_id or "", api_key or "", secret_key or "", threshold=threshold)

    def preprocess_image(self, image_path: str, *, save_processed: bool = False) -> Image.Image:
        """Convert captcha to a high-contrast, black-and-white image."""
        logger.debug(f"Preprocessing captcha image: {image_path}")
        image = Image.open(image_path).convert("L")
        processed = Image.new("L", image.size, 255)
        for y in range(image.size[1]):
            for x in range(image.size[0]):
                pix = image.getpixel((x, y))
                processed.putpixel((x, y), 255 if int(pix) > self.threshold else 0)
        processed = processed.filter(ImageFilter.MedianFilter())
        if save_processed:
            processed.save(image_path)
        return processed

    @staticmethod
    def _image_to_bytes(image: Image.Image, *, fmt: str = "PNG") -> bytes:
        buffer = io.BytesIO()
        image.save(buffer, format=fmt)
        return buffer.getvalue()

    def recognize(self, image_path: str, *, preprocess: bool = True, save_processed: bool = False, delete_cache: bool = True) -> OCRResult:
        """Recognize text from captcha and return OCRResult."""
        logger.info(f"Recognizing captcha text from {image_path}")
        image = self.preprocess_image(image_path, save_processed=save_processed) if preprocess else Image.open(image_path)
        image_bytes = self._image_to_bytes(image)
        response = self.client.basicGeneral(image_bytes)
        logger.info(f"OCR raw response: {response}")
        if delete_cache:
            os.remove(image_path)
        return OCRResult.from_response(response)

    def recognize_url(self, url, delete_cache=True):
        filename = str(uuid.uuid4()) + '.png'
        self.download_img(filename, url)
        return self.recognize(filename, delete_cache=delete_cache)
    
    def download_img(self, filename, url):
        with open(filename, 'wb')as f:
            f.write(requests.get(url, verify=False).content)
        logger.info(f'download {url} to {filename} success')
