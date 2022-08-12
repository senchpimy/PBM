import os 
import hashlib
import sys
import time 
#t = time.localtime()
#current_time = time.strftime("%H:%M:%S", t)
#print(current_time)
if os.path.exists(".pbm"):
    print("Database already exists")
database=open(".pbm","a")
files=os.listdir(".")
BUF_SIZE = 65536
directories= []
files_list=[]
files_to_open=[]
for i in files:
    try:
        file=open(i,"rb")
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
        files_list.append(i)
        files_to_open.append(file)
    except:
        directories.append(i)

for i in files_to_open:
    hashlib.sha512(i.read()).hexdigest()
#t2 = time.localtime()
#current_time2 = time.strftime("%H:%M:%S", t2)
#print(current_time2)
