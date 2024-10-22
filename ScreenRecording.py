import mss  #用于截图
import numpy  #支持高效数组运算，方便处理数据
import cv2  #用于图像的处理和显示

def main():
	#定义一个字典，规定截图的大小
	rect = {'top':0,'left':0,'width':640,'height':480}
	#创建对象sct，用于进行截图操作
	with mss.mss() as sct:
		while True:
	#使用sct进行截图，并将截图结果转化为NumPy数组，方便OpenCV进行图像显示何处理
			img = numpy.array(sct.grab(rect))
			#显示图像，并将其命名为“mss window”
			cv2.imshow('mss window',img)

			#每25毫秒检查一次键盘上输入，如果是‘q’就关闭窗口，并退出监控循环
			if cv2.waitKey(25) & 0xFF == ord('q'):
				cv2.destroyWindow('mss window')
				break
			