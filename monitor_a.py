#-*- encoding: utf-8 -*-
#@author Bulel

'''@function: monitor system: if create a file ,it will delete it after 30s;
              and write all events added time in the head in log file;
'''

import re
import os
import sys
import time
import logging
import win32gui, win32con
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

def mlog(log):       
        m=open('monitorlog.txt','a')
        print("-"*64)
        print("Writing log in monitorlog.txt")
        date=time.strftime('%Y/%m/%d %H:%M:%S',time.localtime(time.time()))
        date=str(date)
        msg=date+" - "+log
        m.write(msg+"\n\n")
        m.close()


class MyHandler(FileSystemEventHandler):
    
    def on_created(self, event):
            what = 'directory' if event.is_directory else 'file'
            action="Creadted a file: "+ str(event.src_path)


    def on_modified(self,event):
            what = 'directory' if event.is_directory else 'file'

            reg=re.search(r'(.+?).txt.(.+?)|(.+?)tmp',str(event.src_path))
            if(reg):
                print("-"*64)
                print("Will not del it: ",event.src_path)
            else:
                print("-"*64)
                print("Will del it: ",event.src_path)
                action="Creadted a file: "+ str(event.src_path)      
                mlog(action) 
                time.sleep(1)
                file=str(event.src_path)
                os.popen('del '+'"'+file+'"')

    def on_deleted(self, event):
            what = 'directory' if event.is_directory else 'file'
            action="Deleted : "+ str(event.src_path)
            print("-"*64)
            print(action)
            mlog(action)

        
if __name__ == "__main__":
    
    #path=input("Please input path to be monitored:\n")
    path="D:\\0chmd"
    print("Will monitor: "+str(path)+"\r\n")

    print("Will minimize the window\r\n")    
    window = win32gui.FindWindow(None,"monitor_a.py")           #get the window whose title is monitor_a.py(itself)
    print("Handle num of the window : %d \r\n"%window)

    title=win32gui.GetWindowText(window)
    if title=="monitor_a.py":
            print("Got correct window\r\nThe title of the window is: %s \r\n"%title)
            win32gui.ShowWindow(window, win32con.SW_MINIMIZE)
            print("Minimizing...\r\n")
    else:
            print("Got wrong window, please check")
    
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)

    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
   
    observer.join()
