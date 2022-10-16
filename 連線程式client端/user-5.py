#coding:utf-8 
import socket, struct, time, os, requests
from bs4 import BeautifulSoup

HOST = "163.24.XXX.XXX"#同網域的本機 IP，通常是私網形式
PORT = 20
choose = ''
keyname = 'test'

url = "https://XXXXX.XXXX.edu.tw/aes/aes/aee0010.aspx"

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
    
def adjust(infList, aP, bP, add = False):#調整串列內容
    if add:
        infList[aP] += ' ' + infList[bP]
    else:
        infList[aP] += infList[bP]
        
    infList.remove(infList[bP])

def spicalSet(adList, num):
    #自行定義調整後的串列，參數的串列不會被更改，會由另一個串列回傳
    backList = adList

    #進行次數
    i = len(backList) - 1
    
    while(i):
        adjust(backList, 0, 1, True)
        i -= 1
            
    return backList

def check(p, tarStr, clist):#核對統計結果並輸出
    #預設不寫入
    w = False
    afterList = []

    for i in range(len(clist)):
        if i % 7 == 0:#找到資料組(7個一組)的頭並核對欄位
            if clist[i + p] == tarStr:
                w = True
            else:
                w = False
        ##print(str(i) + ' ' + str(w) + ' ' + clist[i + p])    
        if not w:#不符則跳過不繼續寫入
            continue
        afterList.append(clist[i])

    return afterList

def crawlbug(url, appoint = False):#預設將不能報名的淘汰，但會一併呈現'未開始'的    
    #取得網頁資料
    r = requests.get(url) 
    #將網頁資料以html.parser
    soup = BeautifulSoup(r.text,"html.parser")
    #找到各欄位資料
    allData = soup.select('table#GridView1 td')

    '''
    各欄位資料如下:
    每 7 個為一筆資料循環，記得加.text.split()保留純文字，不然會連html都跑出來
    '''
    '''
    開啟布林參數(appoint)並設定數字參數(point)，將對資料進行單一過濾
    '''
    allresult = []#首輪輸出結果，未調整
    result = []#最終輸出結果
    sta = []#儲存統計值

    jump = True #決定跳過該輪資料寫入
    point = 7 #指定欄位指標
    allDis = False #是否全顯示

    #指定欄位顯示
    if appoint:       
        print('0 -活動名稱')
        print('1 -報名對象')
        print('2 -主辦單位')
        print('3 -錄(備)取人數')
        print('4 -活動起迄日期')
        print('5 -報名起迄日期')
        print('6 -報名狀態')
        point = input('輸入指定報名狀態(數字):')
        point = int(point)
        if point < 0 or point > 7:
            point = 7

        default = input('\n是否完全顯示所有報名狀態(涵蓋\'已截止\'、\'已額滿\'，預設自動排除)？(y/n)')
        if default == 'y' or default == '1':
            allDis = True
        elif default == 'n' or default == '0':
            allDis = False
        else:
            print('\n例外選項，自動回歸預設處理...\n')
            
    #進行預設(排除'已截止'、'已額滿')整理
    for i in range(len(allData)):
        if i % 7 == 0:
            if appoint == True and i < len(allData) and allDis == False:
                if allData[i + 6].text.split() == ['已截止'] or allData[i + 6].text.split() == ['已額滿']:
                    jump = False
                else:
                    jump = True
                        
        if not jump:#決定是否寫入
            continue
        
        data = allData[i].text.split()
        ##print ('%s %s' % (i, data))
        adData = spicalSet(data, i % 7)        
        ##print (str(i) + ' ' + adData[0])
        allresult.append(adData[0])

        
        #寫入過濾條件
        if point != 7 and i % 7 == 6:
            if i < 7:
                if sta.count(allresult[point]) == 0:
                    sta.append(allresult[point])
            else:
                long = len(allresult)
                if sta.count(allresult[long - 1 - (6 - point)]) == 0:
                    sta.append(allresult[long - 1 - (6 - point)])
                     
    if point != 7:#列出指定欄位下的選項
        print('\n目標代號如下:')
        for j in range(len(sta)):
            if j < 10:
                print(str(j) + '   ' + sta[j])
            else:
                print(str(j) + '  ' + sta[j])
        #選擇該選項
        numP = int(input('\n輸入代號:'))
        #進行核對輸出
        result = check(point, sta[numP], allresult)
    else:
        result = allresult

    #確認無資料顯示
    if len(result) == 0:
        return print ('\n沒有可顯示的資料！\n')

    #為顯示資料組間作分隔
    for i in range(len(result)):
        if i % 7 == 0 :
            print ('\n<===================第%s筆資料===================>\n' % str(int(i/7) + 1))
        print (result[i])

    #資源回收
    result.clear()
    print('\n<<---------------------------顯示完畢----------------------------->>')
    print('\n https://webap.nptu.edu.tw/aes/aes/aee0010.aspx \n')
        
#主介面

print('載入中...')
try:
    
    while True:
        print ('----------------------------------------' +
               time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        #主畫面
        print ("(1)download       -下載記錄檔")
        print ("(2)punch          -打卡")
        print ("(3)exit           -離開程式")
        print ("(4)pachon         -最新活動查詢")
        choose = input("請輸入想操作的內容: ")
        
        if choose == '1':            
            DownLoad(choose)
            
        elif choose == '2':            
            punch(keyname, choose)
            
        elif choose == '3':
            break
        
        elif choose == '4':
            ans = input('是否有指定欄位與內容？(y/n)')
            if ans == 'y' or ans == '1':
                crawlbug(url, True)
            elif ans == 'n' or ans == '0':
                crawlbug(url)
            else:
                print ('\n例外選項，自動回歸預設處理...\n')
            print ('')
            
    #暫停以檢視
    print ('按任一鍵結束...')
    os.system('pause')
    
except socket.error as msg :
    print (msg)
    print ("連線中斷or失敗，倘若仍有操作尚未完成，洽相關人員~~:)")
            
    #暫停以檢視
    print ('按任一鍵結束...')
    os.system('pause')


##確認爬蟲估能不能添加超連結文字，打包功能完成
##2019-10-23 17:10:12秒 註
