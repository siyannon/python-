import pyautogui
from mss import mss
import mss.tools

def main():
	#获取屏幕的宽度和高度
	width,height = pyautogui.size()
	#创建一个mss.mss()对象，用于屏幕捕获，使用with语句确保能自动释放资源
	with mss.mss() as rec:
		#定义一个字典，指定截图区域
		rect = {'top':0,'left':0,'width':width,'height':height}
		#截图并保存在img中
		img = rec.grab(rect)
		#调用函数将截图保存为png文件
		mss.tools.to_png(img.rgb,img.size,6,'a_png')