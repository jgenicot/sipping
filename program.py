import socket
import time
from argparse import ArgumentParser
import numpy as np

def print_time():
    pass

def open_connection(s):
    # create an INET, STREAMing socket
    #print("Socket Created")
    s.connect((args.dst, 5060))
    #print("Connection established")

def close_connection(s):
    s.close()
    #print("Connection Closed")

def send_recv(s, sipmsg):
    # everytime open and close connection otherwise the python timing is incorrect (too low with factor 100)
    open_connection(s)
    BUFFER_SIZE = 4096
    sent_time = time.perf_counter_ns()
    s.sendall(sipmsg)
    #print("Message Sent")
    siprsp = s.recv(BUFFER_SIZE)
    #print("received data:", siprsp)
    #received_time = time.perf_counter_ns()
    #print(str(siprsp))    
    time_difference = time.perf_counter_ns() - sent_time
    #print("{} {} {}".format(sent_time,received_time,time_difference))
    # return converts to ms
    close_connection(s)
    return int(time_difference/1000000)
    


def replace_words(base_text, device_values):
    for key, val in device_values.items():
        base_text = base_text.replace(key, val)
    return base_text


def craft_message(addresses):
    # time format Thu, 27 Aug 2018 14:30:39 CET
    t = open("testtemplate.txt", "r")
    tempstr = t.read()
    t.close()
    current_time = time.strftime("%a, %d %b %Y %H:%M:%S %Z", time.localtime())
    addresses["!!TIME!!"] = current_time
    data = str.encode(replace_words(tempstr,addresses))
    #print(str(data))
    return data


def main():
    # parameter parser
    parser = ArgumentParser()
    parser.add_argument("-s", "--source", dest="src", help="Source IP Address")
    parser.add_argument("-d", "--destination", dest="dst",  help="Destination IP Address")
    global args
    args = parser.parse_args()
    addresses = {}
    addresses["!!SRC!!"] = args.src
    addresses["!!DST!!"] = args.dst
    print("add the following configuration to the router:\nvoice service voip\nip address trusted list\nipv4 {} 255.255.255.255".format(args.src))
    #print("{} {}".format(args.src, args.dst))
    #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # loop
    #open_connection(s)
    filename = time.strftime("./logs/%Y%M%d-%H%M%S-", time.localtime())+args.dst
    stats = open(filename, "w")
    results = []
    print("Writing results to: {}".format(filename))
    print("Connection Opened press CTRL+C to exit")
    while True:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        msg = craft_message(addresses)
        time_difference = send_recv(s,msg)
        results.append(time_difference)
        st = np.array(results) 
        print("SIP Ping {} ms Maximum: {} ms Minimum: {} ms Means {} ms 99 percentile {} ms ".format(time_difference,np.amax(st),np.amin(st),int(np.mean(st)),int(np.percentile(st,99))))
        stats.write("{};{}\n".format(time.strftime("%Y%M%d-%H%M%S", time.localtime()),time_difference))
        time.sleep(1)
    stats.close()

main()
