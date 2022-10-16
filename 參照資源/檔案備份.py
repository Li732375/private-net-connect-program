import shutil, os

##檔案備份

##
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
        print ('備份檔案完成！')
    else:
        print ('待更新的檔案不存在！')

p = 'user.py'
'''
print(p.split('/')[-1])
print('')
print(p.split('/')[-1].split('.')[0].split('-')[0])
print(p.split('/')[-1].split('.')[0])
print(str(int(p.split('/')[-1].split('.')[0].split('-')[1]) + 1))
print(p.split('/')[-1].split('.')[1])
print('')
print(os.path.isfile(p))
'''
backup (p, 'backup/')
##
