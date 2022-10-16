# python C:\Users\?\Desktop\server\server1.py

#coding:utf-8
import socket, struct, time, os, sys, threading, shutil

HOST = "163.24.XXX.XXX"#同網域的本機 IP，通常是私網形式
PORT = 20
txtData = []
c = ''
file = 'save.txt'
recoder = 'C:/Users/?/Desktop/server/save.txt' #? = 本機帳號名稱
'''
li = []#行號
strS = []#對照檔
strS2 = []#待修正檔
files = ['file2.txt', 'file3.txt']
'''
'''
p = 'file-2.txt'
'''
##

def send():   
    #filepath = input('檔案路徑:')
    filepath = recoder
    if os.path.isfile(filepath):
        print ('找到檔案...')
            
        # 定義定義檔案資訊。128s表示檔名為128bytes長，l表示一個
        #int或log檔案型別，在此為檔案大小
            
        fileinfo_size = struct.calcsize('128sl')
        # 定義檔案頭資訊，包含檔名和檔案大小

        print ('打包檔案...')
        fhead = struct.pack('128sl', bytes(os.path.basename(filepath).encode('utf-8')), os.stat(filepath).st_size)

        print ('傳送檔案...')
        conn.send(fhead)
        print ('接收端路徑: {0}'.format(filepath))

        fp = open(filepath, 'rb')
        while True:
            data = fp.read(1024)
            if not data:
                print ('傳送中...')
                break
            conn.send(data)
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

def fileExists(file1, file2):#確認兩檔案是否皆存在
    if os.path.exists(file1) and os.path.exists(file2):
        return True
    else:
        return False

def compare(file1, file2, lineSave, strS, strS2, look = False):#比較兩檔案內容差異並列出
     
    lineNum = 1
    
    if fileExists(file1, file2):#確認檔案存在
        print ('該檔案存在...')
    else:
        print ('不存在該檔案，將自動新增...')
        f2 = open(file2,'w')
        f2.close()
        
    f1 = open(file1,encoding = 'utf-8')
    f2 = open(file2,encoding = 'utf-8')

    #讀入各自變數
    flist1 = [x for x in f1]
    flist2 = [y for y in f2]

    #得出資料長度
    flines1 = len(flist1)
    flines2 = len(flist2)

    #對兩串列作等長處理以比較
    if flines1 < flines2:
        flist1[flines1:flines2+1] = ' ' * (flines2 - flines1)
    elif flines1 > flines2:
        flist2[flines2:flines1+1] = ' ' * (flines1 - flines2)

    #輸出比較結果
    if look:
        print ('%s和%s比較結果:' % (file1, file2))
    for y in zip(flist1, flist2):#字典化合併處理
        if y[0] == y[1]:
            lineNum +=1
            continue
        if y[0] != y[1] :#發現相異內容就呈現
            if look:    
                print('第%s行: %s <--> %s\n' % (lineNum, y[0].strip(),
                                              y[1].strip()))
            lineNum +=1
            
            lineSave.append(lineNum-1)#保留相異資訊的行號
            strS.append(y[0])
            strS2.append(y[1])

    #未有內容呈現，回報兩檔案相同
    if len(lineSave) == 0:
        print ('\n%s和%s內容和排版完全相同！' % (file1, file2))

def contentModify(fileO, fileM, lineSave, strS, strS2):#進行內容修改(以fileO為準修正fileM)
    #確認有內容要更新
    if len(lineSave) == 0:
        print ('\n沒有要更新的內容！')
        return        
    
    #開啟兩檔案，一個讀取，一個寫入
    file = open(fileO, 'r')
    file2 = open(fileM, 'w')
    lineN = 0

    for line in file:#修改內容回報
        if(lineN < len(lineSave)) and strS2[lineN] in line:
            print ('修正第%s行內容...' % lineSave[lineN])
            line = line.replace(strS2[lineN],strS[lineN])
            lineN += 1
        file2.write(line)
        

    #隨手關檔
    file2.close()    
    file.close()

    #回收空間
    lineSave.clear()
    strS.clear()
    strS2.clear()
    
def addNote(file, note):#追加註記   
    #開啟檔案
    f = open(file, 'a')

    #寫入註記
    note = '\n##' + note + '\n##' + time.strftime("%Y-%m-%d %H:%M:%S",
                                                time.localtime()) + '秒 註\n'
    f.write(note)
    print ('完成註記\n')

    #隨手關檔
    f.close()

def update(new, files, li, note, strS, strS2, look):
    compare(new, files, li, strS, strS2, look)
    print ('=====================開始更新======================')
    contentModify(new, files, li, strS, strS2)
    print ('==============更新結束，比對更新結果===============')
    compare(new, files, li, strS, strS2, look)
    addNote(files, note)
    print ('完成該檔更新！\n')
    
def backup(oriPath, newdir):#移動舊版本至備份區(backup/)並更新檔名
    if not os.path.isdir(newdir):#如果指定目錄不存在就建立目錄
        os.mkdir(newdir)
        print ('建立新目錄' + newdir)
        
    if os.path.isfile(oriPath):#確認待更新檔案存在
        #複製至指定路徑下
        shutil.copyfile(oriPath, newdir + oriPath)
        
        #擷取路徑各個位置
        '''
        p = 'F:/tserver/file.txt'
        print(p.split('/')[-1])
        print('')
        print(p.split('/')[-1].split('.')[0].split('-')[0])
        print(p.split('/')[-1].split('.')[0])
        print(str(int(p.split('/')[-1].split('.')[0].split('-')[1]) + 1))
        print(p.split('/')[-1].split('.')[1])
        print('')
        print(os.path.isfile(p))
        '''
        #修改檔名
        os.rename(oriPath.split('/')[-1],
              oriPath.split('/')[-1].split('.')[0].split('-')[0] + '-' +
              str(int(p.split('/')[-1].split('.')[0].split('-')[1]) + 1) +
              '.' + oriPath.split('/')[-1].split('.')[1])
    else:
        print ('待更新的檔案不存在！')
        
#主介面
while True:
    print ('==============================' + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    sockfd = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sockfd.bind((HOST,PORT))
    sockfd.listen(1)

    print ("等待任何連線")
    
    ##該函數會回傳兩個值
    conn, addr = sockfd.accept()    
    print ("與 ",addr," 連線", '\n')
    
    while True:
        try:         
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
            #os.system('python C:/Users/?/Desktop/server/server-1.py') #? = 本機帳號名稱
        
#####待更新內容
'''
for j in files:
    compare('file.txt', j, li, strS, strS2, True)

ans = input('進行批量更新?(y/n)')

if ans == 'y' or ans == '1':

    note = input('\n更新內容註記:')
    
    start_t = time.time()
    for i in range(len(files)):
        print ('===================更新第%s個檔案===================' % i)
        thread_Update = threading.Thread(target = update,
                                         args = ('file.txt', files[i],
                                                 li, note, strS, strS2, False))
        thread_Update.start()
        thread_Update.join()
    print ('完成批次更新！')
        
    end_t = time.time()
    print ('\n花費時間為 %s 秒' % str(end_t - start_t))
    
elif ans == 'n' or ans == '0':
    print ('取消更新')
    pass
'''
'''
backup (p, 'backup/')
'''
