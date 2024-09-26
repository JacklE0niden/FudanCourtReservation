import base64
import os
import io  # 导入 io 模块
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from typing import Tuple
import easyocr
import torch
from torchvision import transforms

# 初始化 EasyOCR 读者
reader = easyocr.Reader(['ch_sim'], gpu=False)


# 定义图像预处理步骤
transform = transforms.Compose([
    transforms.Resize((224, 224)),  # 调整图像大小
    transforms.ToTensor(),          # 转换为张量
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])  # 标准化
])

def get_captcha_results_nn(captcha_image: bytes):
    """
    自定义图像文字识别方法
    :param captcha_image: 验证码图片的字节流
    :return: 识别的坐标和文字结果
    """
    # 将字节流转为 PIL 图像
    image = Image.open(io.BytesIO(captcha_image)).convert('RGB')

    # 图像预处理
    gray_image = image.convert('L')  # 转换为灰度图
    image_np = np.array(gray_image)

    
    # 使用 EasyOCR 识别图像中的汉字，确保传入的格式是 numpy 数组
    from concurrent.futures import ThreadPoolExecutor, TimeoutError

    def ocr_task(image):
        print("Start recognizing text in the image...")
        return reader.readtext(image)

    # 创建线程池
    executor = ThreadPoolExecutor(max_workers=1)
    future = executor.submit(ocr_task, image_np)
    
    try:
        # 等待结果，设置超时为10秒
        print("use ocr to recognize the image")
        result = future.result(timeout=10)
    except TimeoutError:
        print("OCR operation timed out. Skipping this image.")
        future.cancel()  # 尝试取消任务
        result = None
    except Exception as e:
        print(f"An error occurred: {e}")
        result = None

    if result is not None:
        print(f"Successfully extracted text: {result}")
    else:
        print("Failed to extract text from the image.")


    # 提取坐标和文字信息
    captcha_dic = {}
    for (bbox, text, prob) in result:
        # 如果置信度太低，可以忽略这个结果
        if prob < 0.1:
            continue
        
        # bbox 是一个包含四个坐标的列表：[(x0, y0), (x1, y1), (x2, y2), (x3, y3)]
        # 计算汉字的中心坐标（取四个坐标的平均值）
        x_coordinates = [point[0] for point in bbox]
        y_coordinates = [point[1] for point in bbox]
        left = int(sum(x_coordinates) / 4)
        top = int(sum(y_coordinates) / 4)

        # 也可以使用边界框的左上角和右下角坐标来表示
        # left, top, right, bottom = bbox[0][0], bbox[0][1], bbox[2][0], bbox[2][1]
        
        # 将结果存入字典
        captcha_dic[text] = {'left': left, 'top': top}

    print(f"Successfully extracted coordinates: {captcha_dic}")
    return captcha_dic

# 示例：将图片的字节流传递给函数
# 假设 image_bytes 是你的图片字节流
# image_bytes = open('your_image.jpg', 'rb').read()
# result = get_captcha_results(image_bytes)