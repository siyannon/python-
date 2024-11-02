import base64
import qrcode
from io import BytesIO

def main():
	#创建变量，存储生成二维码的链接
	code_url = 'https://www.baidu.com'
	#生成二维码图像对象
	qrcode_img = qrcode.make(data = code_url)
	#创建一个BytesIO对象，用于在内存中存储图像的二进制数据
	output_buffer = BytesIO()
	#将 qrcode_img 图像对象保存到 output_buffer 中，指定为‘JPEG’格式
	qrcode_img.save(output_buffer,format = 'JPEG')
	#获取图像的二进制数据
	byte_data = output_buffer.getvalue()
	#将二进制数据编码
	base64_str = base64.b64encode(byte_data).decode('utf-8')

	print(base64_str)