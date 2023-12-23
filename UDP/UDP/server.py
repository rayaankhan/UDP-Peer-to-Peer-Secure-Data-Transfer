import socket
import time
import select
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
# flaggy=0
# cases=-1
# roomname=""
def server():
    flaggy=0
    cases=-1
    roomname=""
    
    # Getting  file details(will determine if it's sender or receiver based on the flag value)
    while True:
        print("Getting details")
        RECEIVING_IP = "0.0.0.0"
        SERVER_PORT = 50000 # Server's port
        timeout = 3
        server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_sock.bind((RECEIVING_IP, SERVER_PORT))
        n = 0 # total 10 detatils we are receiving
        sender_data_file_name,addr = server_sock.recvfrom(1024)
        if sender_data_file_name:
            print ("File name:", sender_data_file_name)
            # file_name = sender_data_file_name.strip()
        else:
            print("error while getting file name")
        f = open("someone_data.txt", 'wb')
        ready = select.select([server_sock], [], [], timeout)
        if ready[0]:
            data, addr = server_sock.recvfrom(1024)
            while data:
                n += 1
                f.write(data)
                if n == 10:
                    f.close()
                    break
                data, addr = server_sock.recvfrom(1024)
            # break
        print("Received the files with someone's details")

        # Now i will extract that someone's details
        someone_details = []
        with open("someone_data.txt", "r") as file:
            line = file.readline()
            while(line):
                line = line.strip()
                someone_details.append(line)
                line = file.readline()

        someone_dict = {
            "ip" : someone_details[0],
            "file_size" : someone_details[1],
            "file_name" : someone_details[2],
            "key" : someone_details[3],
            "n_threads" : someone_details[4],
            "buf" : someone_details[5],
            "port" : someone_details[6],
            "flag" : someone_details[7],
            "password": someone_details[8],
            "room_cap" : someone_details[9]

        }
        print("1")
        print("flaggy: ", flaggy)
        if flaggy == 0: # No sender yet
            if someone_dict["flag"] == "1":
                cases = 1 # The first sender has arrived
            elif someone_dict["flag"] == "2":
                cases = 2 # receiver without any sender
        elif flaggy == 1: # There is a sender
            if someone_dict["flag"] == "1":
                cases = 3 # another sender can't come
            elif someone_dict["flag"] == "2":
                cases = 4 # a receiver add him or let him wait in the queue
        print("cases: ", cases)
        # switch(cases)
        # def switch(cases):
        if cases == 1:
            print("Inside case 1")
            # create new server room with the name as password, set its limit, and set flaggy as 1
            sender_ip = someone_dict["ip"]
            file_size=someone_dict["file_size"]
            file_name=someone_dict["file_name"]
            key = someone_dict["key"]
            n_threads = int(someone_dict["n_threads"])
            buf = int(someone_dict["buf"])
            port = int(someone_dict["port"])
            roomname = someone_dict["password"]
            capacity = int(someone_dict["room_cap"])
            room={
                "roomname":roomname,
                "capacity":capacity,
                "sender_ip":sender_ip,
                "file_size":file_size,
                "file_name":file_name,
                "key":key,
                "n_threads":n_threads,
                "buf":buf,
                "port":port,
                "rec_arr":[],
            }
            flaggy=1
            print("Case 1")
        elif cases == 2:
            # no room has been created yet, and hence there's no use of the receiver yet, hence kick him out
            print("Case 2")
        elif cases == 3:
            # the room already exists, hence the server is already busy, kick him out
            print("Case 3")
        elif cases == 4:
            print("Case 4")
            # the room already exists, verify the password and based on it put his info in room or kick him out
            if someone_dict["password"] == roomname:
                print("Password is same as sender")
                room["rec_arr"].append(someone_dict)
                print("Capacity is: ", room["capacity"])
                print(len(room["rec_arr"]))
                if len(room["rec_arr"]) == room["capacity"]:
                    flaggy = 0
                    # Now i will be sending the details of all the receivers to the sender
                    with open("sender_data.txt", "w") as sender_file:
                        for key, value in room.items():
                            if key != "rec_arr":
                                sender_file.write(f"{value}\n")
                    with open("receivers_data.txt", "w") as receivers_file:
                        # receivers_file.write("rec_arr:\n")
                        for receiver in room["rec_arr"]:
                            # receivers_file.write("-\n")
                            for key, value in receiver.items():
                                receivers_file.write(f"{value}\n")
                    SENDER_IP = room["sender_ip"]
                    SENDER_PORT = int(room["port"])                    
                    print(SENDER_IP,SENDER_PORT)
                    receiver_data_to_sender="receivers_data.txt"
                    sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
                    server_file_bytes = receiver_data_to_sender.encode('utf-8')
                    sock.sendto(server_file_bytes,(SENDER_IP,SENDER_PORT))
                    print ("Sending this file to sender: ", receiver_data_to_sender)
                    time.sleep(0.1)
                    with open(receiver_data_to_sender, 'r') as file:
                        line = file.readline()
                        while line:
                            print(line)
                            sock.sendto(line.encode('utf-8'), (SENDER_IP, SENDER_PORT))
                            time.sleep(0.01)
                            line = file.readline()
                    sock.close()
                    # now comes the case for all receivers..
                    for receiver in room["rec_arr"]:
                        RECEIVER_IP = receiver["ip"]
                        RECEIVER_PORT = int(receiver["port"])
                        print(RECEIVER_IP,RECEIVER_PORT)
                        sender_data_to_receiver = "sender_data.txt"
                        sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
                        server_file_bytes = sender_data_to_receiver.encode('utf-8')
                        sock.sendto(server_file_bytes,(RECEIVER_IP,RECEIVER_PORT))
                        print("Sending file to respective receivers:",sender_data_to_receiver)
                        time.sleep(0.1)
                        with open(sender_data_to_receiver,'r') as file:
                            line = file.readline()
                            while line:
                                print(line)
                                sock.sendto(line.encode('utf-8'),(RECEIVER_IP,RECEIVER_PORT))
                                time.sleep(0.01)
                                line=file.readline()
                        sock.close()
                    flaggy=0
                    cases=-1
                    roomname=""
            # room={}
            # roomname=""22       
        server_sock.close()
server()
