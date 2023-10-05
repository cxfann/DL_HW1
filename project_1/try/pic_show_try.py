from PIL import Image
import requests
from io import BytesIO

from PIL import Image
import requests
from io import BytesIO

# 指定图像的URL
image_url = "https://www.hfgdjt.com/1ywuKELSO2ahQuWZ/pr/0/r/e00a0e273cb8/YagM72orAMwIpLDWIOTB4jBGDK2z4ophe9Wx8RaBwYpCGDkU3knr4UdAk_nH0VPtuE7UeY75Lw7rYCxe1s01KKNac2XsIcI0ps8KYDL2Hvk%3D/020230407152933_712480.jpg"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

response = requests.get(image_url, headers=headers, allow_redirects=True)

# 检查是否成功获取图像数据
if response.status_code == 200:
    try:
        # 将图像数据读取为PIL图像对象
        image = Image.open(BytesIO(response.content))

        # 显示图像
        image.show()
    except Exception as e:
        print(f"Error: {e}")
else:
    print(f"Failed to fetch image, status code: {response.status_code}")
