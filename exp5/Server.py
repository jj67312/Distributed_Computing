import socket
import argparse

import json
parser = argparse.ArgumentParser()
parser.add_argument("--ip", type=str, help="Enter IP address of server", default="127.0.0.1")
parser.add_argument("port", type=int, help="Enter Port number")
args = parser.parse_args()
HOST = args.ip # Standard loopback interface address (localhost)
PORT = args.port # Port to listen on (non-privileged ports are >
# 1023)
prices = {'Medicine1': 250, 'Medicine2': 200, 'Medicine3': 300, 'Medicine4': 150, 'Medicine5': 400}
while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        all_data = ""
        total_bill_amount = 0
        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(4096)
                print(data)
                if not data:
                    break
                all_data += data.decode('utf-8')

        cart = json.loads(all_data)['cart']
        for k,v in cart.items():
            total_bill_amount += prices[k]*v
            print(f"Received Cart details from Client : ", json.loads(all_data))

        print(f'Total bill amount {total_bill_amount}')