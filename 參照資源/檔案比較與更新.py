import os, time, sys

##批量檔案內容更新

def fileExists(file1, file2):#確認兩檔案是否皆存在
    ### FileExistsError: [Errno 17] File exists:
    ### 確認版本號或路徑是否更新
    
    print(str(os.path.exists(file1)))
    print(str(os.path.exists(file2)))
    
    if os.path.exists(file1) and os.path.exists(file2):
        return True
    else:
        return False

def compare(file1, file2, lineSave, strS, strS2, look = False):#比較兩檔案內容差異並列出
     
    lineNum = 1
    
    print ('兩檔案皆存在...' + str(fileExists(file1, file2)) +'\n')
    if not fileExists(file1, file2):
        print ('不存在該檔案，將自動新增...\n')
        f2 = open(file2, 'x', encoding = 'utf-8')
        f2.close()
        
    f1 = open(file1, encoding = 'utf-8')
    f2 = open(file2, encoding = 'utf-8')

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
        print ('%s和%s比較結果:\n' % (file1, file2))
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
    file = open(fileO, 'r', encoding = 'utf-8')
    file2 = open(fileM, 'w', encoding = 'utf-8')
    
    lineN = 0

    for line in file:#修改內容回報
        if(lineN < len(lineSave)) and strS2[lineN] in line:
            sys.stdout.write('修正第%s行內容...' % lineSave[lineN])
            sys.stdout.flush()
            #print ('修正第%s行內容...' % lineSave[lineN])
            lineN += 1
            ##print(line)
            
        file2.write(line)
        
    #隨手關檔
    file2.close()    
    file.close()

    #回收空間
    lineSave.clear()
    strS.clear()
    strS2.clear()
    
def addNote(file, note, jum = True):#追加註記
    if not jum:
        return
    #開啟檔案
    f = open(file, 'a', encoding = 'utf-8')

    #寫入註記
    note = '\n##' + note + '\n##' + time.strftime("%Y-%m-%d %H:%M:%S",
                                                time.localtime()) + '秒 註\n'
    f.write(note)
    print ('完成註記\n')

    #隨手關檔
    f.close()

def update(new, files, li, note, strS, strS2, ju, look):
    compare(new, files, li, strS, strS2, look)
    print ('=====================開始更新======================')
    contentModify(new, files, li, strS, strS2)
    #print ('==============更新結束，比對更新結果===============')
    #compare(new, files, li, strS, strS2, look)
    addNote(files, note, ju)
    print ('完成該檔更新！\n')
    
##
li = []#行號
strS = []#對照檔
strS2 = []#待修正檔
ju = True #跳過註解

stdFile  = 'K:/tserver/server.py'
files = ['C:/Users/?/Desktop/server/server-4.py']

for j in files:
    print ('===================更新第%s個檔案===================' % str(files.index(j)))
    compare(stdFile, j, li, strS, strS2, True)

ans = input('進行批量更新?(y/n)')

if ans == 'y' or ans == '1':

    note = input('\n更新內容註記:')
    
    start_t = time.time()
    for i in range(len(files)):
        print ('===================更新第%s個檔案===================' % str(i+1))
        
        update(stdFile , files[i], li, note, strS, strS2, ju, False)
        
    print ('完成批次更新！')
        
    end_t = time.time()
    print ('\n花費時間為 %s 秒' % str(end_t - start_t))
    
elif ans == 'n' or ans == '0':
    print ('取消更新')
    pass

#暫停以檢視
print('按任一鍵結束...')
os.system('pause')
