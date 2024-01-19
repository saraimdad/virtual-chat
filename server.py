import socket
import threading
import argparse
parser = argparse.ArgumentParser(description="Server for virtual chat")
args = parser.parse_args()

# Connection Data
host = '127.0.0.1'
port = 5050

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()


allClients={}

class createClient:
    def __init__(self, name):
        self.name=name
        self.blockedList=[]
        self.sleeping=False
        self.queuedMessages=[]
    
    



def broadcast(message,client):
    for someClient in allClients:
        if client not in allClients[someClient].blockedList:
            if allClients[someClient].sleeping==False:
                someClient.send(message)
            else:
                allClients[someClient].queuedMessages.append(message)
        #if someClient not in allClients[client].blockedList:
         #   someClient.send(message)

def errorCompensate(client,clientToUnblock):
    for someClient in allClients:
        if someClient!=client:
            if clientToUnblock in allClients[someClient].blockedList:
                print(f'{allClients[someClient].name} unblocked {allClients[clientToUnblock].name}')
                allClients[someClient].blockedList.remove(clientToUnblock)
def handle(client):
    while True:
        try:
           
            message = client.recv(1024)
            decodedMessage=message.decode('utf-8')
            if decodedMessage[0]=='/':
                splittedMessage=decodedMessage[1:].split()
                command=splittedMessage[0]
                if len(splittedMessage)<2 and command!='quit':
                        client.send('Invalid argument'.encode('ascii'))
                        continue
                
                if command=='block':
                    nameToBeBlocked=splittedMessage[1]
                    
                    if nameToBeBlocked==allClients[client].name:
                        client.send('Cannot block yourself'.encode('ascii'))
                        continue
                    nameFound=0
                    for someClient in allClients:
                        if allClients[someClient].name==nameToBeBlocked:
                            allClients[client].blockedList.append(someClient)
                            client.send(f'{nameToBeBlocked} has been blocked'.encode('ascii'))
                            nameFound=1
                            break
                    for someClient in allClients:
                        for k in allClients[someClient].blockedList:
                            print(f'{allClients[someClient].name} has {allClients[k].name} blocked')
                    if nameFound==0:
                        client.send(f'{nameToBeBlocked} not found'.encode('ascii')) 
                elif command=='unblock':
                    nameToBeUnblocked=splittedMessage[1]
                    nameFound=0
                    for k in allClients[client].blockedList:
                        if nameToBeUnblocked==allClients[k].name:
                            allClients[client].blockedList.remove(k)
                            client.send(f'{allClients[k].name} has been unblocked'.encode('ascii'))
                            nameFound=1
                 
                    if nameFound==0:
                        client.send('Name not found'.encode('ascii'))
                    
                elif command == 'quit':
                    print('in here')
                    client.send('DISCONNECT'.encode('ascii'))
                    encodedMessage=(str(allClients[client].name+' left the chat.')).encode('ascii')
                    broadcast(encodedMessage,client)
                    del allClients[client]
                    client.close()
                        
                    break
                elif command == 'getlist':
                    if len(allClients[client].blockedList)==0:
                        print('None blocked')
                        continue
                    else:
                        for k in allClients[client].blockedList:
                            print(allClients[k].name + '\n')
                elif command=='getall':
                    for someClient in allClients:
                        for k in allClients[someClient].blockedList:
                            print(f'{allClients[someClient].name} has {allClients[k].name} blocked'.encode('ascii'))
                elif command=='name':
                    nameToBeChanged=splittedMessage[1]
                    nameFound=0
                    for someClient in allClients:
                        if allClients[someClient].name==nameToBeChanged:
                            nameFound=1
                            client.send('That name is already taken'.encode('ascii'))
                            break
                    if nameFound==0:
                        allClients[client].name=nameToBeChanged
                        client.send('Name Changed'.encode('ascii'))
                elif command=='sleep':
                    allClients[client].sleeping=True
                    splittedMessage=str(decodedMessage).split()
                    timeToSleep=splittedMessage[1]
                    client.send(f'sleep {timeToSleep}'.encode('ascii'))

                elif command=='unsleep':
                    allClients[client].sleeping=False
                    client.send('Brought back to life'.encode('ascii'))
                    client.send('Here is what you missed\n'.encode('ascii'))
                    for mm in allClients[client].queuedMessages:
                        spacedMessage=mm.decode('ascii') + '\n'
                        encodedMessage=spacedMessage.encode('ascii')
                        client.send(encodedMessage)
                    allClients[client].queuedMessages=[]
                        
                        
                    
            else:
                encodedMessage=((allClients[client].name)+'>'+str(decodedMessage)).encode('ascii')
                broadcast(encodedMessage,client)
            
        except Exception as e:
        
            print(e)
            try:           
                client.send('DISCONNECT'.encode('ascii'))
                client.close()
            except:
                client.close()
            name=allClients[client].name
            
            del allClients[client]
            
            broadcast(f'{name} left!'.encode('ascii'),client)
            
            break



def receive():
    while True:
        
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        
        name = client.recv(1024).decode('ascii')
        nameTaken=0
        while nameTaken==0:
            nameTaken=0
            for someClient in allClients:
                if allClients[someClient].name==name:
                    client.send('0'.encode('ascii'))
                    name=client.recv(1024).decode('ascii')
                    nameTaken=1
            if nameTaken==0:
                break
                
        
       
        clientObject=createClient(name)
        allClients[client]=clientObject
        client.send("1".encode('ascii'))
        


        
        print("Name is {}".format(allClients[client].name))
        broadcast("{} joined!".format(allClients[client].name).encode('ascii'),client)
        client.send('Connected to server!'.encode('ascii'))

        
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


receive()


