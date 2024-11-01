import os

def main():
	#定义要遍历的路径。注意：使用‘c:\abc’其中的‘\’表示转义字符，将a给转义了，不能表示文件路径，要么使用‘ c:\\abc ’，或者强调原始字符串‘ r“c:\abc” ’
	file_dir = 'c:\\abc'

	for roots,dirs,files in os.walk(file_dir):
		for file in files:
			if endswith(".txt")
			print(file)
			#使用os.psth.join()函数，通过文件路径和文件名拼接成完整的路径
			print("文件完整路径：",os.path.join(roots,file))
			#使用os.rename()函数批量修改文件名
			os.rename(os.path.join(roots,file),os.path.join(roots,"xx-"+file))