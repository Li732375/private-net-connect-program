import time
import sys

##動態進度點
'''
該效果限在 cmd 時才看的到喔！
'''
for i in range(100):
    time.sleep(0.1)
    sys.stdout.write("\r%d%%" % i)
    sys.stdout.flush()
