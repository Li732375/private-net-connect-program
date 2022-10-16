import socket, time, os, struct

##連線程式client端
'''

'''
HOST = "163.24.XXX.XXX"#同網域的本機 IP，通常是私網形式
PORT = 20
choose = ''
keyname = 'test1'

def DownLoad(choose):
    sockfd = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sockfd.connect_ex((HOST,PORT))
    print (HOST,"建立連線")
    b = choose.encode()
    sockfd.sendall(b)
    
    fileinfo_size = struct.calcsize('128sl')
    buf = sockfd.recv(fileinfo_size)
    if buf:
        filename, filesize = struct.unpack('128sl', buf)
        fn = filename.strip(b'\00')
        new_filename = os.path.join(b'./'+ fn)
        print ('檔案名稱為 {0}, 大小 {1}'.format(new_filename,filesize))
            
        recvd_size = 0  # 定義已接收檔案的大小
        fp = open(new_filename, 'wb')
        print ('開始接收')

        while not recvd_size == filesize:
            if filesize - recvd_size > 1024:
                data = sockfd.recv(1024)
                recvd_size += len(data)
            else:
                data = sockfd.recv(filesize - recvd_size)
                recvd_size = filesize
            fp.write(data)
            print ('下載中...')
        fp.close()
        print ('下載完成')

    print ("與",HOST,"結束連線")
    sockfd.close()
        
def punch(name, choose):
    sockfd = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sockfd.connect_ex((HOST,PORT))
    print (HOST,"建立連線")
    b = choose.encode()
    sockfd.send(b)

    time.sleep(0.5)
    #送出名稱
    print ('你好! ',name,' 歡迎來到網路實驗室!')
    txtData = name
    Cbyt = txtData.encode()
    sockfd.send(Cbyt)
    print ('送出打卡訊息')
    
    #等待回覆
    response  = sockfd.recv(1024).decode()
    print(response)

    print ("與",HOST,"結束連線")
    sockfd.close()

###主介面
#sockfd = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

try:
    #連線
    #sockfd.connect_ex((HOST,PORT))
    #print (HOST,"建立連線")

    while True:
        print ('----------------------------------------' +
               time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        #主畫面
        print ("(1)download       -下載記錄檔")
        print ("(2)punch          -打卡")
        choose = input("請輸入想操作的內容: ")

        #需要連線伺服器的功能才要這兩行
        #byt = choose.encode()

        #sockfd.sendall(byt)

        if choose == '1':            
            DownLoad(choose)
            
        elif choose == '2':            
            punch(keyname, choose)
            
    #暫停以檢視
    print ('按任一鍵結束...')
    os.system('pause')
    
except socket.error as msg :
    print (msg)
    print ("連線中斷or失敗，倘若仍有操作尚未完成，洽相關人員~~:)")
            
    #暫停以檢視
    print ('按任一鍵結束...')
    os.system('pause')
