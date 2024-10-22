#！ /usr/bin/python
#! -*- coding: utf-8 -*-
import sys
import time
import logging
#观察文件系统变化的类
from watchdog.observers import Observer  
#用于定义文件操作行为的类
from watchdog.events import FileSystemEventHandler  
import os
#提供高级文件操作，包括删除、复制文件和目录
import shutil

#装饰器函数，捕获异常，忽略错误并继续执行函数（防止因某个文件操作失败而中止）
def add_try(f):
    def new_f(*args, **kwargs):
        try:
            f(*args, **kwargs)
        except:
            pass

    return new_f

#用于监控和备份文件，继承自FileSystemEventHandler
class MyDog(FileSystemEventHandler):
    """文件监控和备份
    """
    def __init__(self, **kwargs):
        super(MyDog, self).__init__(**kwargs)
        self.formats = ['.py']  #要监控的文件类型
        self.base_dest_path = './backup'  #备份路径
        self.period = 500   #文件备份周期，单位为秒

	#计算备份文件的路径和目标
    def get_dest_path(self, path=''):
        idx = int(time.time()) // self.period
        if path:
            return '%s/%s/%s' % (self.base_dest_path, idx, path)
        else:
            return '%s/%s' % (self.base_dest_path, idx)

    #检查拓展名，查看是否是需要监控的文件类型
    def check_format(self, path):
        f = os.path.splitext(path)[1]
        return (f in self.formats)

    #移动过文件或目录，复制到备份路径
    @add_try
    def move_it(self, source_path, dest_path, is_directory):
        if not self.check_format(source_path):
            return None
        dest_source_path = self.get_dest_path(source_path)
        dest_dest_path = self.get_dest_path(dest_path)
        if is_directory:
	        #复制整个目录
            shutil.copytree(dest_path, dest_dest_path)
            shutil.rmtree(dest_source_path)
        else:
            folder, filename = os.path.split(dest_dest_path)
            if not os.path.exists(folder):
                os.makedirs(folder)
            #复制文件
            shutil.copy(dest_path, dest_dest_path)
            os.remove(dest_source_path)

    #克隆文件或目录，同时复制到备份路径
    @add_try
    def clone_it(self, source_path, is_directory):
        if not self.check_format(source_path):
            return None
        dest_path = self.get_dest_path(source_path)
        if is_directory:
            if not os.path.exists(dest_path):
                os.makedirs(dest_path)
            else:
                folder, filename = os.path.split(dest_path)
                if not os.path.exists(folder):
                    os.makedirs(folder)
                    shutil.copy(source_path, dest_path)

    #删除文件或目录，复制到备份路径
    @add_try
    def remove_it(self, source_path, is_directory):
        if not self.check_format(source_path):
            return None
        dest_path = self.get_dest_path(source_path)
        if is_directory:
            shutil.rmtree(dest_path)
        else:
            os.remove(dest_path)

    #下面的所有方法是observe触发的方法重写
    ##################################################
    #监听文件或目录是否被移动，若被移动就调用move_it函数
    def on_moved(self, event):
        #重写方法
        super(MyDog, self).on_moved(event)
        #判断是目录还是文件
        what = 'directory' if event.is_directory else 'file'
        #使用自己的move_it方法操作
        self.move_it(event.src_path, event.dest_path, event.is_directory)
        logging.info('移动操作 %s: from %s to %s', what, event.src_path,event.dest_path)

	#监听文件或目录是否被创建，若被创建就调用clone_it函数
    def on_created(self, event):
        super(MyDog, self).on_created(event)
        what = 'directory' if event.is_directory else 'file'
        self.clone_it(event.src_path, event.is_directory)
        logging.info('创建操作 %s: %s', what, event.src_path)

	#监听文件或目录是否被删除，若被删除就调用remove_it函数
    def on_deleted(self, event):
        super(MyDog, self).on_deleted(event)
        what = 'directory' if event.is_directory else 'file'
        self.remove_it(event.src_path, event.is_directory)
        logging.info('删除操作 %s: %s', what, event.src_path)

	#监听文件或目录是否被修改，若被修改就调用clone_it函数
    def on_modified(self, event):
        super(MyDog, self).on_modified(event)
        what = 'directory' if event.is_directory else 'file'
        self.clone_it(event.src_path, event.is_directory)
        logging.info('修改操作 %s: %s', what, event.src_path)

if __name__ == '__main__':
    #弹出日志
    logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(message)s',datefmt='%Y-%m-%d %H:%M:%S')

    #判断第一个参数，如果默认就是当前目录
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    #new一个类
    event_handler = MyDog()
    #初始化Observe
    observer = Observer()
    #observe监控文件事件，路径，监控子目录文件修改
    observer.schedule(event_handler, path, recursive=True)
    #开始监控
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()


