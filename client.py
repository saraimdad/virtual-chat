import socket
import threading
import argparse
from threading import Timer

parser = argparse.ArgumentParser(description="Client for virtual chat")

parser.add_argument('-n', '--name', help="Name of client" )
parser.add_argument('-p', '--port', help="Port Number", type=int, default=5050)
args = parser.parse_args()

name = args.name
port = args.port


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', port))
client.send(name.encode('ascii'))
while (client.recv(1024).decode('ascii') != "1"):
    print("Name already chosen")
    name = input("Enter new name :")
    client.send(name.encode('ascii'))


def sleepSender(client):
    client.send('/unsleep 0'.encode('ascii'))
# Listening to Server and Sending Nickname
def receive():
    while True:
        try:
            # Receive Message From Server
            # If 'NICK' Send Nickname
            message = client.recv(1024).decode('ascii')
            if str(message)=='DISCONNECT':
                client.close()
                print("Disconnected from server")
            elif message.split()[0]=='sleep':
                print(f'Gone to sleep for {message.split()[1]} seconds')
                t=Timer(int(message.split()[1]),sleepSender,[client])
                t.start()
            else:
                print(message)
        except:
            client.close()
            break


# Sending Messages To Server
def write():
    while True:
        
        message = '{}'.format(input(''))
        try:
            client.send(message.encode('ascii'))
        except:
            client.close()
            break

# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()

