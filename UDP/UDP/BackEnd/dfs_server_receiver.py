# Threading and missing packets handled
# Decryption done
# Padding done
# Parity done
# Hash done

import socket
import time
import hashlib
import os
import select

from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

key = b'YourSymmetricKey'
cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())

def calculate_parity(data):
    # Calculate the parity by counting the number of set bits (1s) in the data
    return sum(1 for bit in data if bit) % 2

def verify_parity(encrypted_data):
    encrypted_packet = encrypted_data[:-1]  # Remove the last byte (parity byte)
    received_parity = encrypted_data[-1]  # Last byte is the received parity

    # Calculate parity for the received packet
    parity = calculate_parity(encrypted_packet)

    return parity == received_parity

seq_limit = 32

def receive_data(val):

    # 2. Receiver will send his IP to server

    # a) Getting all the variables
    print("Receiver has started")
    ip_file = "my_ip.txt"
    f = open(ip_file, "r")
    my_ip_ser = str(f.read())
    # print(my_ip_ser)
    password=val["password"]
    # password = "aa"
    flag=val["flag"]
    # flag = 2
    port_ser = str(50001)
    # data_for_server = {
    #     "ip" : my_ip_rec,
    #     "port" : "50002",
    #     "password":password,
    #     "flag":flag
    # }
    data_for_server = {
        "ip" : my_ip_ser,
        "file_size" :"NA",
        "file_name" : "NA",
        "key" : "NA",
        "n_threads" : "NA",
        "buf" : "NA",
        "port" : port_ser,
        "flag":flag,
        "password":password,
        "room_cap":"NA"
    }
    f = open("data_for_server_receiver.txt", "w")
    for data in data_for_server:
        # print(data)
        f.write(str(data_for_server[data]))
        f.write("\n")
    f.close()

    # b) sending this file created to the server

    SERVER_IP = "192.168.150.233" # this is universally known
    SERVER_PORT = 50000 # PORT of server is universally known
    data_for_server_file = "data_for_server_receiver.txt"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_file_bytes = data_for_server_file.encode('utf-8')
    sock.sendto(server_file_bytes, (SERVER_IP, SERVER_PORT))
    print ("Sending this file to server: ", data_for_server_file)
    time.sleep(0.1)

    with open(data_for_server_file, 'r') as file:
        line = file.readline()
        while line:
            # print(line)
            sock.sendto(line.encode('utf-8'), (SERVER_IP, SERVER_PORT))
            time.sleep(0.01)
            line = file.readline()
    sock.close()

    # 4. Now i will be receiving sender's data

    RECEIVING_IP = "0.0.0.0"
    RECEIVER_PORT = 50001 # Receiver's port(i.e. sender initallly mujhe kya kkya values bhej rha hai)
    timeout = 3
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((RECEIVING_IP, RECEIVER_PORT))


    while True:
        n = 0 # total 10 details we are receiving
        sender_data_file_name,addr = sock.recvfrom(1024)
        if sender_data_file_name:
            print ("File name:", sender_data_file_name)
            file_name = sender_data_file_name.strip()
        else:
            print("error while getting file name")
        f = open("sender_data.txt", 'wb')
        ready = select.select([sock], [], [], timeout)
        if ready[0]:
            data, addr = sock.recvfrom(1024)
            while data:
                n += 1
                # print(data)
                f.write(data)
                if n == 9:
                    # f.close()
                    break
                data, addr = sock.recvfrom(1024)
            break
    f.close()
    sock.close()
    # Now I will be extracting details from both
    print("Now I will be extracting details of the sender")
    sender_details = []
    with open("sender_data.txt", "rb") as file:
        line = file.readline()
        while(line):
            line = line.strip()
            # print(line)
            sender_details.append(line.decode('utf-8'))
            line = file.readline()

    sender_dict = {
        "ip" : sender_details[2],
        "file_size" : sender_details[3],
        "file_name" : sender_details[4],
        "key" : sender_details[5],
        "n_threads" : sender_details[6],
        "buf" : sender_details[7],
        "port" : sender_details[8]
    }

    time.sleep(0.5)
    # start_time = time.time()





    RECEIVING_IP = "0.0.0.0"
    RECEIVER_PORT = 50001
    SENDER_IP = sender_dict["ip"]
    SENDER_PORT = int(sender_dict["port"])



    start_time = time.time() # for timer

    buf = int(sender_dict["buf"]) + 60 # 33 is just to incorporate the sequence number and parity size
    # 1515360846
    file_size = int(sender_dict["file_size"]) # to be received earlier
    n_threads = int(sender_dict["n_threads"]) # to be received earlier
    stopper = (file_size // (buf-60)) + 1 # Max no of packets I will receive
    print("Total number of packets that I will be receiving: ", stopper)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((RECEIVING_IP, RECEIVER_PORT))

    # Receiving the name of the file
    data, addr = sock.recvfrom(buf)
    file_name = data.decode('utf-8')
    # print("Receiving ", file_name) 

    # Calculating the hash
    data, addr = sock.recvfrom(buf)
    received_hash = data.decode('utf-8')
    # print("Received hash: ", received_hash)

    received_data = {}
    no_received_packets = 0
    failed = False # Has the parity failed
    sock.settimeout(5) # if some packet got lost it will wait for 5 seconds and then cut it out to check all the missing packets
    repeat = 0 # is there any un received packets
    seq_list = []
    percent = (no_received_packets/stopper)*100
    try:
        # print("Planning to receive")
        while True:
            # print("Planning to receive")
            encrypted_packet, addr = sock.recvfrom(buf)  # 8 bytes for the sequence number
            # print(encrypted_packet)
            if not verify_parity(encrypted_packet):
                failed = True
                print("Parity check failed. Packet corrupted.")
                break  # Discard the corrupted packet
            decryptor = cipher.decryptor()
            encrypted_packet = encrypted_packet[:-1]
            decrypted_padded_data = decryptor.update(encrypted_packet) + decryptor.finalize()
            # Unpad the decrypted data
            unpadder = padding.PKCS7(128).unpadder()
            unpadded_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()

            no_received_packets += 1
            if no_received_packets%20 == 0:
                percent = 100*(no_received_packets/stopper)
                print("Percentage of file received: ", percent)
            # print(no_received_packets)
            seq_number = int.from_bytes(unpadded_data[:seq_limit], 'big')
            seq_list.append(seq_number)
            file_data = unpadded_data[seq_limit:]

            # I have got a new packet
            if seq_number not in received_data:
                received_data[seq_number] = file_data
            # print("Number of packets received: ", no_received_packets)

            # Received all the packets with no loss
            if no_received_packets == stopper:
                break

    # 5 seconds over some packets were therefore missing
    except Exception:
        repeat = 1
        print("Now we will try to get the missing packets")
    # sock.close()
    sock.close()


    if repeat == 1:
        # Now i will send the missng packet's sequence number to the sender to receive them again
        # SENDER_IP = "192.168.150.55"
        # SENDER_PORT = 50002
        time.sleep(1)
        sender_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Sending the info to the sender that some packets were missing
        sender_sock.sendto("missing".encode('utf-8'), (SENDER_IP, SENDER_PORT))
        time.sleep(0.05)

        # Getting the missing sequence numbers from the sequences that i received
        # I know what all the sequence number would be since the sequence number are in from 0 to buf(-33) size difference till file size
        seq_list.sort()
        # print("Seq list received length: ", len(seq_list))
        # print(seq_list[0], seq_list[1], seq_list[2])

        all_seq_list = []
        for i in range(0, file_size, buf-60):
            all_seq_list.append(i)
        # print("All seq list: ", len(all_seq_list))
        missing_seq_set = set(all_seq_list) - set(seq_list)
        missing_seq_set = list(missing_seq_set)
        print("No. of missing packets: ", len(missing_seq_set))

        # Sending the missing sequence list to the sender
        sender_sock.sendto(str(len(missing_seq_set)).encode('utf-8'), (SENDER_IP, SENDER_PORT))
        time.sleep(0.05)
        for _ in range(len(missing_seq_set)):
            sender_sock.sendto(str(missing_seq_set[_]).encode('utf-8'), (SENDER_IP, SENDER_PORT))
            time.sleep(0.05)
        sender_sock.close()


        # Getting those missng packets now
        print("Now we will receive the missing packets")
        # RECEIVING_IP = "0.0.0.0"
        # RECEIVER_PORT = 50001
        receiving_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        receiving_sock.bind((RECEIVING_IP, RECEIVER_PORT))
        print("Became the receiver")

        for _ in range(len(missing_seq_set)):
            encrypted_packet, addr = receiving_sock.recvfrom(buf)
            if not verify_parity(encrypted_packet):
                failed = True
                print("Parity check failed. Packet corrupted.")
                break  # Discard the corrupted packet
            decryptor = cipher.decryptor()
            encrypted_packet = encrypted_packet[:-1]
            # Decrypt the received encrypted data
            decrypted_padded_data = decryptor.update(encrypted_packet) + decryptor.finalize()

            # Unpad the decrypted data
            unpadder = padding.PKCS7(128).unpadder()
            unpadded_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()

            seq_number = int.from_bytes(unpadded_data[:seq_limit], 'big')
            file_data = unpadded_data[seq_limit:]

            # Adding those missing packets here
            if seq_number not in received_data:
                received_data[seq_number] = file_data
        # print("Received packets: ", len(received_data))
        receiving_sock.close()

        end_time = time.time()
        packet_receive_time = end_time - start_time
        # print("Time taken for receiving all the packets including the missing ones: ", packet_receive_time)

        # Now i will be sorting the packets and adding them to a file
        start_time_a = time.time()
        # print("I am out now sorting")
        received_data_hash = b''
        with open(f"received_{file_name}", "wb") as f:
            # print("Now sorting will start")
            sorted_packets = sorted(received_data.keys())
            # print("It has been sorted")
            for i in sorted_packets:
                # print(i)
                f.write(received_data[i])
                received_data_hash += received_data[i]
            print("Percentage of file received: 100")


        # Checking the hash
        print("Time to check for hash")
        hasher = hashlib.sha256()
        hasher.update(received_data_hash)
        calculated_hash = hasher.hexdigest()
        print("Hash calculated is: ", calculated_hash)

        end_time_a = time.time()

        sort_hash_time = end_time_a - start_time_a
        print("Sort and hash time: ", sort_hash_time)
        print("Time taken overall: ", sort_hash_time + packet_receive_time)
        if received_hash == calculated_hash:
            print("File integrity verified. Hashes match.")
            return {"status": "Data received successfully"}
        
        else:
            print("Hash does not match! File may be corrupt.")
            os.remove(f"received_{file_name}") # Since its corrupted we remove the file
            return {"status": "File received is corrupted"}
        
        


    else:
        # No missing packets

        # print("The socket has been closed")
        end_time = time.time()
        packet_receive_time = end_time - start_time
        print("Time taken for receiving all the packets before hash and sort: ", packet_receive_time)
        start_time_a = time.time()

        # Confirmation to the sender that no missing packets reported
        # SENDER_IP = "192.168.150.55"
        # SENDER_PORT = 50002
        time.sleep(1)
        sender_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sender_sock.sendto("Done".encode('utf-8'), (SENDER_IP, SENDER_PORT))
        sender_sock.close()

        # Sort and hash
        print("I am out now sorting")
        if failed == False:
            received_data_hash = b''
            with open(f"received_{file_name}", "wb") as f:
                sorted_packets = sorted(received_data.keys())
                print("Packets have been sorted")
                for i in sorted_packets:
                    f.write(received_data[i])
                    received_data_hash += received_data[i]
            
            hasher = hashlib.sha256()
            hasher.update(received_data_hash)
            calculated_hash = hasher.hexdigest()

            end_time_a = time.time()
            sort_hash_time = end_time_a - start_time_a
            print("Sort and hash time: ", sort_hash_time)
            print("Overall time taken: ", sort_hash_time + packet_receive_time)
            print("Calculated hash: ", calculated_hash)
            if received_hash == calculated_hash:
                print("File integrity verified. Hashes match.")
                return {"status": "Data received successfully"}
            else:
                print("Hash does not match! File may be corrupt.")
                os.remove(f"received_{file_name}")
                return {"status": "File received is corrupted"}
        else:
            return {"status": "Parity failed"}
        
# receive_data()