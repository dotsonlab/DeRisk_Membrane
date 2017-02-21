
import time, sys
import os.path

start_time1 = time.strftime('%S', time.localtime())

elapsed_time = time.strftime('%S', time.localtime())
print start_time1
print elapsed_time
i = float(elapsed_time) - float(start_time1)
print i
