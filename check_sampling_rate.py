import threading

import time

def change_user():
    print('这是中断,切换账号')
    t = threading.Timer(3, change_user)
    t.start()

#每过3秒切换一次账号
t = threading.Timer(3, change_user)

t.start()
while True:
    print('我在爬数据')
    time.sleep(1)