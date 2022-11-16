#!/usr/bin/env python3
import socket
import argparse
import json

parser = argparse.ArgumentParser()
parser.add_argument("--ip", type=str, help="Enter IP address of server",default="127.0.0.1")
parser.add_argument("port", type=int, help="Enter Port number")
args = parser.parse_args()
HOST = args.ip
PORT = args.port
prices = {'Medicine1': 250, 'Medicine2': 200, 'Medicine3': 300, 'Medicine4': 150, 'Medicine5': 400}

def getCartInfoFromUser():
    items = {}
    for i, key in enumerate(prices):
        items[i + 1] = key
    print("Enter your choices")
    cart = {}
    while(True):
        for i, (k, v) in enumerate(prices.items()):
            print(i + 1, k + ": ", v)
        print(i + 2, "exit")
        choice = int(input())
        if choice == i + 2:
            break
        print("Enter the quantity")
        quantity = int(input())
        cart[items[choice]] = quantity
    return json.dumps({"cart": cart})

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    data = bytes(getCartInfoFromUser(), 'utf-8')
    print(data)
    s.sendall(data)
    print(f"Cart details Sent !!")