import numpy as np  #用于处理数据图像数组数据
import cv2          #用于显示和处理图像
import socket       #用于网络连接

#用于从套接字sock接收来自客户端的图像数据
def receive_data(sock):
    #使用套接字接收前4个字节，并将其转化为整数，表示即将传输的数据长度，big表示大端字节序
    data_length = int.from_bytes(sock.recv(4),'big')
    #创建空字节串接收数据
    data = b''
    #当接收到的数据长度小于声明的数据长度时，持续接收数据
    while len(data) < data_length:
	    #根据还需要接收的字节数从套接字处接收数据
        packet = sock.recv(data_length - len(data))
        #如果接收到的数据包为空，表示连接已关闭
        if not packet:
            return None
        #将接收到的包追加到data字节中，逐步接收完整数据
        data += packet
	#接收完所有的数据后，返回data
    return data


#创建套接字，并且设置服务器的IP地址和端口，并且绑定套接字，设置最大连接数
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host = '192.168.9.138'
port = 6666
server_socket.bind((host,port))
server_socket.listen(5)

print("server is listening on %s %s"%(host,port))

#保持服务器持续运行，等待客户端连接
while True:
	#接收到连接后，返回新的套接字和客户端地址
    client_socket,addr = server_socket.accept()
    print("get a connection from %s"%str(addr))

    try:
	    #持续接收客户端发送数据
        while True:
	        #从客户端套接字接收数据，并且将数据存储在data中
            data = receive_data(client_socket)
            #如果连接关闭，跳出循环
            if not data:
                break
            #将接收到的字节数据转化为NumPy数组，数据类型是无符号8位整数
            nparr = np.frombuffer(data,np.uint8)
			#使用OpenCV将NumPy数组解码为图像
            img_np = cv2.imdecode(nparr,cv2.IMREAD_COLOR)
            #检查解码后的图像是否有效
            if img_np is not None:
	            #将有效图像放到‘screen’的窗口中显示
                cv2.imshow('screen',img_np)
                #每1ms检查一次按键，如果按下‘q’键就退出循环
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

	#捕获连接重置错误，如果客户端关闭连接，忽略错误，并等待新的客户端连接
    except ConnectionResetError:
        pass

    client_socket.close()
cv2.destroyAllWindows()
