import socket
import time
import sys
import select

def send(file_name):
    UDP_IP="0.0.0.0"
    IN_PORT = 5000
    timeout = 3


    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, IN_PORT))
    print("binded")

    while True:
        print("1")
        data, addr = sock.recvfrom(1024)
        print(data)
        if data:
            print ("File name:", data)
            your_ip_file = data.strip()
        else:
            print("error")

        f = open("your_ip.txt", 'wb')
        ready = select.select([sock], [], [], timeout)
        if ready[0]:
            data, addr = sock.recvfrom(1024)
            f.write(data)
        # else:
        #     print ("Finish!", file_name)
        #     f.close()
            break


        
    f = open("your_ip.txt", "r")
    your_ip = f.read()
    print(your_ip)



    time.sleep(1.5)
    UDP_IP = your_ip
    UDP_PORT = 5000
    buf = 1024
    file_name = file_name


    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    file_name_bytes = file_name.encode('utf-8')
    sock.sendto(file_name_bytes, (UDP_IP, UDP_PORT))
    print ("Sending ", file_name)

    f = open(file_name, "rb")
    data = f.read(buf)
    print(data)
    while(data):
        # data_bytes = data.encode('utf-8')

        if(sock.sendto(data, (UDP_IP, UDP_PORT))):
            data = f.read(buf)
            print(data)
            # data_bytes = data.encode('utf-8')
            time.sleep(0.02) # Give receiver a bit time to save

    sock.close()
    f.close()

send("ip_finder.js")