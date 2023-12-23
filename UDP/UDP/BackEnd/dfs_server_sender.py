# Threading and buffer thing implemented
# Encryption done
# Parity done
# Hash done

import socket
import time
import sys
import threading
import os
import select
import hashlib

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

# Your packet as bytes
# packet = b'YourPacketToEncrypt'

def calculate_parity(data):
    return sum(1 for bit in data if bit) % 2

# Create a key or retrieve a pre-existing key
# Replace this with your actual key generation or retrieval process
key = b'YourSymmetricKey'  # Replace this with your actual symmetric key

# Use the key to create an encryption cipher
cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
# encryptor = cipher.encryptor()

# Pad the data to match the block size (16 bytes for AES)
# padder = padding.PKCS7(128).padder()


n_threads = 5  # Adjust the number of threads as needed
buf = 65400 # in bytes
packets_sent = 0
seq_limit = 32
def send_file_chunk(sock, file_name, start_idx, n_packets, UDP_IP, UDP_PORT):

    with open(file_name, "rb") as f:
        f.seek(start_idx)
        starting_idx = start_idx

        for i in range(n_packets):
            encryptor = cipher.encryptor()
            padder = padding.PKCS7(128).padder()
            data = f.read(buf)
            packet = (starting_idx.to_bytes(seq_limit, 'big') + data)
            padded_data = padder.update(packet) + padder.finalize()
            encrypted_packet = encryptor.update(padded_data) + encryptor.finalize()
            parity = calculate_parity(encrypted_packet)
            final_packet = encrypted_packet + bytes([parity])
            sock.sendto(final_packet, (UDP_IP, UDP_PORT))
            time.sleep(0.1)
            starting_idx += buf

# def send_data(val):
#     print(val)
#     return {"status": "Data processed successfully",'values_i_got':val}

def send_data(val):
    # Step 1: I am gathering the required data to be sent to server which will further send it to the receiver
    # This data includes important details about my ip and the file and receiving requirements

    # a) Getting all the variables
    #__________________
    ip_file = val["ip_file"]
    f = open(ip_file, "r")
    # _ser means data for the server
    my_ip_ser = str(f.read()) # got the IP
    print(my_ip_ser)
    file_name_ser = val["file_name"]
    # file_name_ser = "190.mkv"
    file_size_ser  = str(os.path.getsize(file_name_ser))
    print("ser: ", file_size_ser)
    key_ser = str(key.decode('utf-8'))
    # n_packets = file_size // buf
    n_threads_ser = str(n_threads)
    print(n_threads_ser)
    buf_ser = str(buf)
    port_ser = str(50002)
    flag = val["flag"]
    # flag = 1
    password = val["password"]
    # password = "aa"
    room_cap = val["room_cap"]
    # room_cap = 2
    data_for_server = {
        "ip" : my_ip_ser,
        "file_size" : file_size_ser,
        "file_name" : file_name_ser,
        "key" : key_ser,
        "n_threads" : n_threads_ser,
        "buf" : buf_ser,
        "port" : port_ser,
        "flag":flag,
        "password":password,
        "room_cap":room_cap
    }
    
    # making a file where i will be storing all these info
    f = open("data_for_server.txt", "w")
    for data in data_for_server:
        # print(data)
        f.write(str(data_for_server[data]))
        f.write("\n")
    f.close()
    
    # b) sending this file created to the server

    SERVER_IP = "192.168.150.233" # this is universally known
    SERVER_PORT = 50000 # PORT of server is universally known
    data_for_server_file = "data_for_server.txt"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_file_bytes = data_for_server_file.encode('utf-8')
    sock.sendto(server_file_bytes, (SERVER_IP, SERVER_PORT))
    print ("Sending this file to server: ", data_for_server_file)
    time.sleep(0.1)

    with open(data_for_server_file, 'r') as file:
        line = file.readline()
        while line:
            sock.sendto(line.encode('utf-8'), (SERVER_IP, SERVER_PORT))
            time.sleep(0.01)
            line = file.readline()
    sock.close()

    # 3. Now i will be receiving receiver's data

    RECEIVING_IP = "0.0.0.0"
    SENDER_PORT = 50002 # Our port(from where we will be listening)
    timeout = 3
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((RECEIVING_IP, SENDER_PORT))


    while True:
        n = 0 # total (10*room_cap) details we are receiving
        receiver_data_file_name,addr = sock.recvfrom(1024)
        if receiver_data_file_name:
            print ("File name:", receiver_data_file_name)
            file_name = receiver_data_file_name.strip()
        else:
            print("error while getting file name")

        f = open("receiver_data.txt", 'wb')
        ready = select.select([sock], [], [], timeout)
        if ready[0]:
            data, addr = sock.recvfrom(1024)
            while data:
                n += 1
                # print(data)
                f.write(data)
                print(type(data))
                if n == (10*room_cap):
                    # f.close()
                    break
                data, addr = sock.recvfrom(1024)
            break
    f.close()
    sock.close()
    print("Got all the receiver's details")
    receiver_details = [] # this will be list of lists
    with open("receiver_data.txt", "rb") as file:
        n = 0
        one_receiver = []
        line = file.readline()
        print("here: ", line)
        while(line):
            line = line.strip()
            print(line)
            one_receiver.append(line.decode('utf-8'))
            n += 1
            if n % 10 == 0:
                n = 0
                receiver_details.append(one_receiver)
                one_receiver = []
            line = file.readline()
    # print(receiver_details[0])
    # print(receiver_details[1])
    
    # no_of_receivers = room_cap

    # Time to iterate through all the receivers and giving them what they need

    hasher = hashlib.sha256()
    with open(file_name_ser, 'rb') as file:
        buffer = file.read()
        hasher.update(buffer)
    file_hash = hasher.hexdigest()
    for i in range(room_cap):
        receiver_dict = {
            "ip"  : receiver_details[i][0],
            "port" : receiver_details[i][6]
        }


        time.sleep(2)
        start_time = time.time() # timer
        RECEIVER_IP = receiver_dict["ip"]
        RECEIVER_PORT = int(receiver_dict["port"])
        print(RECEIVER_IP, RECEIVER_PORT)

        # RECEIVER_IP = receiver_dict["ip"]
        # RECEIVER_PORT = int(receiver_dict["port"])
        # RECEIVING_IP = "0.0.0.0"
        SENDER_PORT = 50002

        file_name = val["file_name"]
        # file_name = "190.mkv"

        # creates a UDP socket named sock that can be used for sending and receiving datagrams over an IPv4 network.
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # AF_INET for IPv4 and SOOCK_DRAM for UDP
        file_name_bytes = file_name.encode('utf-8') # because for sending data bytes are the required format
        sock.sendto(file_name_bytes, (RECEIVER_IP, RECEIVER_PORT)) # sending the file name that we will be sending later
        print("Sending", file_name)


        
        sock.sendto(file_hash.encode(), (RECEIVER_IP, RECEIVER_PORT))  # Send the file hash
        print("This is your hash: ", file_hash)

        file_size  = os.path.getsize(file_name)
        print("Your file size is: ", file_size)
        n_packets = file_size // buf
        print("No of packets overall: ", n_packets)
        n_packets_one = n_packets // n_threads
        threads = []

        for i in range(n_threads):
            start_idx = n_packets_one*buf*i 
            thread = threading.Thread(target=send_file_chunk, args=(sock, file_name, start_idx, n_packets_one, RECEIVER_IP, RECEIVER_PORT))
            threads.append(thread)
            thread.start()
            # time.sleep(5)

        # It continues to loop until all threads have completed their execution
        for thread in threads:
            thread.join()
        print("loop is done")

        # Now for the last part
        idx_for_last = n_packets_one*buf*n_threads
        start_idx = idx_for_last
        n_packets_buf = (file_size-start_idx) // buf
        print("packets of buf size left are: ", n_packets_buf)

        thread = threading.Thread(target=send_file_chunk, args=(sock, file_name, start_idx, n_packets_buf, RECEIVER_IP, RECEIVER_PORT))
        thread.start()
        thread.join()

        start_idx = idx_for_last + (buf*n_packets_buf)
        end_idx = file_size
        print("apart from that size remaining would be: ", end_idx-start_idx)
        with open(file_name, "rb") as f:
            f.seek(start_idx) # getting to that point from where we need to start selecting
            encryptor = cipher.encryptor()
            padder = padding.PKCS7(128).padder()
            data = f.read(end_idx-start_idx)
            packet = (start_idx.to_bytes(seq_limit, 'big') + data)
            padded_data = padder.update(packet) + padder.finalize()
            encrypted_packet = encryptor.update(padded_data) + encryptor.finalize()
            parity = calculate_parity(encrypted_packet)
            final_packet = encrypted_packet + bytes([parity])
            sock.sendto(final_packet, (RECEIVER_IP, RECEIVER_PORT))
            time.sleep(0.1)
        print("Done with sending the entire file")
        # f.close()
        sock.close()

        # Now i will be receiving if any packets were missing
        print("Now time to see if any packet was missing")
        # RECEIVING_IP = "0.0.0.0"
        # SENDER_PORT = 50002
        receiving_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        receiving_sock.bind((RECEIVING_IP, SENDER_PORT))
        print("Became a receiver")
        data, addr = receiving_sock.recvfrom(buf)
        time.sleep(0.05)
        if data.decode('utf-8') == "missing":
            # so now i will receive the size of array of missing packets
            print("Some packets were missing")
            quantity, addr = receiving_sock.recvfrom(buf)
            quantity = int(quantity.decode('utf-8'))
            print("Packets missing: ", quantity)
            missing_seq_list = []
            for _ in range(quantity):
                # print(_, end=" ")
                packet_number, addr = receiving_sock.recvfrom(1024)
                missing_seq_list.append(int(packet_number.decode('utf-8')))
            print()
            print(len(missing_seq_list))

            receiving_sock.close()
            # so as i have got the list of the packets not received i will send them again
            # RECEIVER_IP = "192.168.150.233"
            # RECEIVER_PORT = 50001
            sender_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # AF_INET for IPv4 and SOOCK_DRAM for UDP
            time.sleep(2)
            with open(file_name, "rb") as f:
                for seq in missing_seq_list:
                    print(seq, " this is the seq I am sending")
                    f.seek(seq)
                    encryptor = cipher.encryptor()
                    padder = padding.PKCS7(128).padder()
                    data = f.read(buf)
                    packet = (seq.to_bytes(seq_limit, 'big') + data)
                    padded_data = padder.update(packet) + padder.finalize()
                    encrypted_packet = encryptor.update(padded_data) + encryptor.finalize()
                    parity = calculate_parity(encrypted_packet)
                    final_packet = encrypted_packet + bytes([parity])
                    sender_sock.sendto(final_packet, (RECEIVER_IP, RECEIVER_PORT))
                    time.sleep(0.1)

            sender_sock.close()
            end_time = time.time()
            print("Total time taken for sending: ", end_time - start_time)
            # return {"status": "Data processed successfully"}

        else:
            # sock.close()
            end_time = time.time()
            print("No missing packets reported")
            print("Total time taken for sending: ", end_time - start_time)
            # return {"status": "Data processed successfully"}

# send_data()