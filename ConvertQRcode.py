import base64
import re  #处理正则表达式
from io import BytesIO
from PIL import Image

#将 base64 字符串转化为图像，并将其保存至指定的路径下
def base64_to_image(base64_str,image_path):
	#使用正则表达式替换函数，只筛选出 base64 编码部分
	base64_data = re.sub('^data:image/.+;base64','',base64_str)
	#解码获得字节流数据
	byte_data = base64.b64decode(base64_data)
	#创建字节流对象
	image_data = BytesIO(byte_data)
	#使用Image.open() 函数创建图片对象
	img = Image.open(image_data)
	#如果传入路径，就将图片保存到路径底下
	if image_path:
		img.save(image_path)

def main():
	src_str = '【base64编码的图像字符串】'
	base64_to_image(src_str,'./a.png')