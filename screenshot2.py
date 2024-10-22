import pyautogui
from mss import mss
import mss.tools
#导入该模块用于图像处理（创建、修改、保存）
from PIL import Image
def main():
	#获取屏幕的宽度和高度
	width,height = pyautogui.size()
	#创建一个mss.mss()对象，
	with mss.mss() as rec:
		rect = {'top':0,'left':0,'width':width,'height':height}
		img = rec.grab(rect)
		
		pim = Image.new('RGB',img.size)
		pim.frombytes(img.rgb)
		pim.save('a.jpg',quality=95)
		del img,pim
		
		