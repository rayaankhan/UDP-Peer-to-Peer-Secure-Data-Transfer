import socket
import time
import sys
import select


# UDP_IP = "127.0.0.1"
# UDP_IP = "172.21.127.207"


def receive():
    UDP_IP = '192.168.148.55'
    UDP_PORT = 5000
    buf = 1024
    ip_file = "my_ip.txt"

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ip_name_bytes = ip_file.encode('utf-8')
    sock.sendto(ip_name_bytes, (UDP_IP, UDP_PORT))
    print ("Sending my ip file: ", ip_file)

    f = open("my_ip.txt", "rb")
    my_ip = f.read()
    print(my_ip)
    # while(data):
        # data_bytes = data.encode('utf-8')
    if(sock.sendto(my_ip, (UDP_IP, UDP_PORT))):
        time.sleep(0.02) # Give receiver a bit time to save
        print("sent")
    else:
        print("Error while sending the ip")
    sock.close()
    f.close()

    print("1")

    # UDP_IP="0.0.0.0"
    # IN_PORT = 5000
    # timeout = 3


    # sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # sock.bind((UDP_IP, IN_PORT))

    # while True:
    #     data, addr = sock.recvfrom(1024)
    #     if data:
    #         print ("File name:", data)
    #         file_name = data.strip()

    #     f = open("your_ip.txt", 'wb')
    #     ready = select.select([sock], [], [], timeout)
    #     if ready[0]:
    #         data, addr = sock.recvfrom(1024)
    #         f.write(data)
    #     # else:
    #     #     print ("Finish!", file_name)
    #     #     f.close()
    #         break


    # f = open("your_ip.txt", "r")
    # your_ip = f.read()


    time.sleep(1)
    UDP_IP="0.0.0.0"
    IN_PORT = 5000
    timeout = 3



    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, IN_PORT))
    print("2")
    while True:
        data, addr = sock.recvfrom(1024)
        print(data)
        if data:
            print ("File name:", data)
            file_name = data.strip()

        f = open(file_name, 'wb')

        while True:
            ready = select.select([sock], [], [], timeout)
            if ready[0]:
                data, addr = sock.recvfrom(1024)
                print(data)
                f.write(data)
            else:
                print ("Finish!", file_name)
                f.close()
                break
        break

receive()