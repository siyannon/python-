import os

def main():
	#指定要遍历的目录（起始位置）
	file_dir = './'
	#使用os.walk()函数遍历指定目录，返回遍历到的路径、子目录、文件
	for roots,dirs,files in os.walk(file_dir):
		print("roots:",roots)
		print("dirs:",dirs)
		print("files",files)

		#遍历当前目录下的每个文件，并且输出以“.exe”结尾的文件
		for file in files:
			if file.endswith('.exe'):
				print(file)