from functools import reduce
from dateutil import parser
import threading
import datetime
import socket
import time

servers = []
def initiateClockServer(port):
    server = socket.socket()
    server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
    print(f"Socket at node created successfully at {port} \n")
    server.bind(('', port))
    servers.append([server,port])
    servers.sort(key=lambda x:x[1])
    # Start listening to requests
    server.listen(10)
    print("Clock server started...\n")

# the shared knowledge repository where a node knows the ids of other nodes and hence priority
def process_Pool(id,message_case=0):
    nodes_list = [server[1] for server in servers if not
    server[0]._closed] # id of the nodes in the networks
    if message_case==1: # sending the election request, message=election
        new_list=[]
        for x in nodes_list:
            if id<x:
                new_list.append(x) # create a list of nodes with an id higher

            #than the current node denoted by the parameter id
            if nodes_list.index(id)+1==len(nodes_list): # last node in the list
                return None # there's no higher priority node
        return new_list # return list of higher priority nodes
    if message_case==2 and id!=servers[0][1]:#sending an ok message within the time limit

        return [nodes_list[nodes_list.index(id) - 1]]# return id of predecessor node in priority hierarchy
    if message_case==3: #sending an Ive won message to other nodes
        del nodes_list[len(nodes_list)-1] # pop the highest id and form a list of recipients which is
    #everyone else
    return nodes_list # updated list with recipients being everyone minus the winner

#simulate communication of nodes
def sending_data(myId,recepients,message): # recipients list and message to be sent
    if recepients is not None:# no empty list
        for node in recepients:
            print(message+" sent to Node"+str(node)) # emulate send message via print
    return

# Construct a node
def node(myId):
    sending_list=process_Pool(myId,1)
    if sending_list is None: # meaning no node is higher and thus, this node has won

        sending_data(myId,process_Pool(myId,3),"I've won") # when the highest node wins

        print(f'Server on port {myId} elected as master server')
    else:
        sending_data(myId,sending_list,"Election") # forward an election message to your successor in the priority list
        sending_data(myId,process_Pool(myId,2),"OK") #send data to your predecessor in the priority list

# #Initialize program by simulating the starting of nodes
# # by calling the node function
def start_servers():
    l = list(map(int,input().split()))
    for port in l:
        initiateClockServer(port)
    i = 0
    while(True):
        print("----------------------")
        for server in servers:
            if not server[0]._closed:
                node(server[1])

        time.sleep(10)
        i += 1
        if i == 1:
            servers[-1][0].close()

start_servers()