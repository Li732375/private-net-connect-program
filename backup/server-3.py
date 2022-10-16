# python C:\Users\?\Desktop\server\server1.py

#coding:utf-8
import socket, struct, time, os, sys

HOST = "163.24.XXX.XXX"#同網域的本機 IP，通常是私網形式
PORT = 20
txtData = []
c = ''
file = 'save.txt'
recoder = 'C:/Users/?/Desktop/server/save.txt' #? = 本機帳號名稱

##

def send():   
    #filepath = input('檔案路徑:')
    filepath = recoder
    if os.path.isfile(filepath):
        print ('找到檔案...')
            
        # 定義定義檔案資訊。128s表示檔名為128bytes長，l表示一個
        #int或log檔案型別，在此為檔案大小

        # 定義檔案頭資訊，包含檔名和檔案大小    
        fileinfo_size = struct.calcsize('128sl')

        print ('打包檔案...')
        fhead = struct.pack('128sl', bytes(os.path.basename(filepath).encode('utf-8')), os.stat(filepath).st_size)

        print ('傳送檔案...')
        conn.send(fhead)
        print ('接收端路徑: {0}'.format(filepath))

        fp = open(filepath, 'rb')
        
        while True:
            data = fp.read(1024)
            if not data:
                break
            conn.send(data)
            print ('傳送中...')
            
    print("傳送結束")

def sendback():  
    numData = '成功寫入紀錄'
    Cbyt = numData.encode()
    conn.send(Cbyt)
    print('已送出成功寫入訊息')
    
def recv():
    # 開始接收
    print ("開始接收並存在 'save'")
    txtFile = open(file, 'a')  
    
    txtData = conn.recv(1024)
    txtData = txtData.decode()
    print ("傳輸中...",txtData)
    txtFile.write("\n#############"+ time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + str(addr) + '\n')
    txtFile.write(txtData)
    print (txtData + " 打卡完成")
    txtFile.close()
        
#主介面
while True:
    print ('==============================' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    sockfd = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    
    while True:
        try:
            sockfd.bind((HOST,PORT))
            sockfd.listen(1)

            print ("等待任何連線")
    
            ##該函數會回傳兩個值
            conn, addr = sockfd.accept()    
            print ("與 ",addr," 連線", '\n')
    
            c = conn.recv(1024).decode()
            print(c)
            if c == '1':#傳送文件            
                send()
            elif c == '2':#接收文件 
                recv()
                sendback()
            elif c == '3':#斷線
                sockfd.close()
                print ("與 ",addr," 結束連線")
                break
            #elif c == '數字':
            else:
                print ('接獲非介面指示操作' + c)
            print ('------------------------------' + str(addr) + ' ' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        except socket.error :
            sockfd.close()
            break
            #os.system('python C:/Users/?/Desktop/server/server1.py') #? = 本機帳號名稱
        
#####待更新內容

##主介面架構修正
##2019-10-18 16:08:02秒 註
