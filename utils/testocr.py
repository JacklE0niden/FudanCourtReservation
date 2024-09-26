from PIL import Image
import base64
import io
import numpy as np
from ocr import get_captcha_results_nn

# 将本地图片转换为 PIL 图像对象
def load_local_image(image_path):
    """
    加载本地图片为 PIL 图像对象
    :param image_path: 本地图片的路径
    :return: PIL 图像对象
    """
    try:
        image = Image.open(image_path)
        print("Successfully loaded image from local file.")
        return image
    except Exception as e:
        print(f"Failed to load image: {e}")
        return None

# 将 PIL 图像对象转换为 base64 字符串
def pil_to_base64(pil_image):
    """
    将 PIL 图像对象转换为 base64 字符串
    :param pil_image: PIL 图像对象
    :return: base64 字符串
    """
    buffered = io.BytesIO()
    pil_image.save(buffered, format="PNG")
    base64_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return base64_str

# 将 base64 字符串转换为 PIL 图像对象
def base64_to_image(base64_str):
    """
    将 base64 字符串转换为 PIL 图像对象
    :param base64_str: base64 字符串
    :return: PIL 图像对象
    """
    image_data = base64.b64decode(base64_str)
    pil_image = Image.open(io.BytesIO(image_data))
    return pil_image

# 将 PIL 图像对象转换为字节流
def pil_to_bytes(pil_image):
    """
    将 PIL 图像对象转换为字节流
    :param pil_image: PIL 图像对象
    :return: 字节流
    """
    buffered = io.BytesIO()
    pil_image.save(buffered, format="PNG")
    return buffered.getvalue()

# 示例用法
image_path = "../pic/captcha2.png"  # 替换为你本地图片的路径
pil_image = load_local_image(image_path)

# 将 PIL 图像转换为 base64 编码格式
if pil_image:
    base64_str = pil_to_base64(pil_image)
    print(f"Base64 string: {base64_str[:100]}...")  # 只打印前100个字符

    # 将 base64 字符串转换为 PIL 图像对象
    pil_image_converted = base64_to_image(base64_str)
    if pil_image_converted:
        print("Successfully converted base64 back to PIL image.")

    # 将 PIL 图像对象转换为字节流
    image_bytes = pil_to_bytes(pil_image)

    # 调用 get_captcha_results_nn 进行验证码识别
    captcha_results = get_captcha_results_nn(image_bytes)
    print(f"Captcha results: {captcha_results}")
else:
    print("Failed to load and process the image.")

if __name__ == '__main__':
    # 读取本地图片并获取字节流
    with open('../pic/captcha2.png', 'rb') as f:
        image_bytes = f.read()
    # 调用识别函数，打印结果
    captcha_results = get_captcha_results_nn(image_bytes)
    print(f"Recognized captcha results: {captcha_results}")