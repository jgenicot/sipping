import time
import socket

while True:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM )
    start = time.perf_counter_ns()
    s.connect(('216.58.198.100',80))
    print('time taken {} ms'.format((time.perf_counter_ns()-start)/1000000))
    s.close()
    time.sleep(0.5)
