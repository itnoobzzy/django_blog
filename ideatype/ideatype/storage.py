#!/usr/bin/env python
# _*_ coding: utf-8 _*_
# @Time : 2020/7/28 16:28
# @Author : zhouzy_a
# @Version：V 0.1
# @File : storage.py
# @desc :保存图片
from io import BytesIO

from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import InMemoryUploadedFile

from PIL import Image, ImageDraw, ImageFont


class WatermarkStorage(FileSystemStorage):
    """重写django存储文件方法保存图片"""
    def save(self, name, content, max_length=None):
        # 处理逻辑
        if 'image' in content.content_type:
            # 加水印
            image = self.watermark_with_text(content, 'zzy.com', 'red')
            content = self.convert_image_to_file(image, name)

        return super(WatermarkStorage, self).save(name, content, max_length=max_length)

    def convert_image_to_file(self, image, name):
        temp = BytesIO()
        image.save(temp, format='PNG')
        file_size = temp.tell()
        return InMemoryUploadedFile(temp, None, name, 'image/png', file_size, None)

    def watermark_with_text(self, file_obj, text, color, fontfamily=None):
        image = Image.open(file_obj).convert('RGBA')
        draw = ImageDraw.Draw(image)
        width, height = image.size
        margin = 10
        # 计算文字大小和放置位置
        if fontfamily:
            font = ImageFont.truetype(fontfamily, int(height / 20))
        else:
            font = None
        textWidth, textHeight = draw.textsize(text, font)
        x = (width - textHeight - margin) / 2
        y = height - textHeight - margin
        draw.text((x, y), text, color, font)
        return image


if __name__ == '__main__':
    pass