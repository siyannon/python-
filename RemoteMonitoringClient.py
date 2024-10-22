import mss      #用于截图
import socket   #用于网络连接
import io       #用于处理数据流
from PIL import Image  #从Pillow图像库中导入Image库用于图像处理

#定义一个用于发送数据的函数
def send_data(sock,data):
	#获得data的字节长度，用于告诉服务端接收的数据长度
    data_length = len(data)
    #将数据长度转化为4字节的大端序格式，并通过sock发送出去
    sock.sendall(data_length.to_bytes(4,'big'))
    #通过sock发送实际的图像数据
    sock.sendall(data)

#创建客户端套接字（IPV4、TCP）
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#指定要连接的服务器IP和端口，并进行连接
host = '192.168.9.138'
port = 6666
client_socket.connect((host,port))

#创建截图对象sct
with mss.mss() as sct:
	#获取主显示器的监视器信息
    monitor = sct.monitors[1]
    #持续捕捉屏幕，并发送
    while True:
	    #抓取截图，返回对象
        sct_img = sct.grab(monitor)
	    #创建一个BytesIO对象，用于图像存储为字节流。ing_bytes类似于一个虚拟文件，可以向个里面写入字节流
        img_bytes = io.BytesIO()
#使用PIL库将从sct_img捕获的截屏图像数据转化为Image对象，最终生成的图像模式是RGB，原始数据raw（截屏图像）是img_bgra,原始数据的颜色通道和格式是BGRX（忽略透明通道）。将图像保存到img_bytes对象中，格式设置为PNG
Image.frombytes('RGB',sct_img.size,sct_img.bgra,'raw','BGRX').save(img_bytes,format='PNG')

		#调用函数，获取img_bytes中的图像数据，通过套接字将PNG格式的图像数据发送给服务端
        send_data(client_socket,img_bytes.getvalue())

#关闭客户端套接字，结束网络连接（在这个代码中用不到）
client_socket.close()




	