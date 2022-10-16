# python C:\Users\?\Desktop\server\server.py #? = 本機帳號名稱

#coding:utf-8
import socket
import time
import os

HOST = "163.24.XXX.XXX"#同網域的本機 IP，通常是私網形式
PORT = 20
txtData = []
c = ''

sockfd = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sockfd.bind((HOST,PORT,))
sockfd.listen(1)

print ("等待任何連線")
conn,addr = sockfd.accept()
print ("與 ",addr," 連線")

def send():
    # 開始傳輸
    print ("接獲下載請求")
    print ("start send file")
    txtFile = open("save.txt", "r")
    while True:
        txtData = txtFile.read(1024)
        txtData = txtData.encode()
        print("傳輸中...")
        if not txtData:
            print("完成傳輸")
            break  # 讀完檔案結束迴圈
        conn.sendall(txtData)
    txtFile.close()
    print("傳送結束")

def sendback():  
    numData = '成功寫入紀錄'
    Cbyt = numData.encode()
    conn.send(Cbyt)
    print('已送出成功寫入訊息')
    
def recv():
    # 開始接收
    print ("開始接收並存在 'save'")
    txtFile = open('save.txt', 'a')  
    while True:
        txtData = conn.recv(1024)
        txtData = txtData.decode()
        print ("傳輸中...",txtData)
        #if not txtData:
        txtFile.write("\n#############"+ time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime())+ str(addr) +"\n")
        txtFile.write(txtData)
        print ("完成打卡")
        txtFile.close()
        break
    # 讀完檔案結束迴圈
    
#主介面
#while True:
c = conn.recv(1024)
c = c.decode()
print(c)
if c == '1':
    #傳送文件
    send()
elif c == '2':
    #接收文件
    recv()
    sendback()
        
sockfd.close()
print ("成功與 ",addr," 結束連線")
    #break
os.system('python C:/Users/?/Desktop/server/server.py') #? = 本機帳號名稱

#臨時停止
