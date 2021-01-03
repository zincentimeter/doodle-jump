import time
import os
while True:
    with open("log.txt", "r") as f:  # 打开文件
            data = f.read()  # 读取文件
            print(data)
    i = os.system("cls")
