
import socket
from threading import Thread

#########################################################################################################################
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #create socket connection 
host = "localhost"  #establish local host
port = 18000    #port
MAX_USERS = 3   #create max users
server_socket.bind((host, port))    
server_socket.listen(MAX_USERS)  #max 3 clients in the listen queue
clients = {}  #stores client socket, username, IP, and port
msgList = []  #stores the message list
usernameList = []
########################################################################################################################



#############################################   handle_client    #######################################################
def handle_client(client_socket, client_address):
    username = None #create username variable
    

    while True:
        message = client_socket.recv(1024).decode()     #recieve message
        print(f"Received message from {client_address}: {message}")

############################   if the user enters a 1    #############################
        if message == "1":      #look for report
            user_list = "Users in chatroom:"
            for socket, (username, ip, port) in clients.items():
                user_list += f"\n{username} at IP: {ip} and port: {port}"       #add elements to a message
            client_socket.send(user_list.encode())          #send message
#########################################################################################

###########################if the user enters their username (JOIN:"username")#########
        elif message.startswith("JOIN:"):  
            username = message.split(":")[1]        #save username split from leading part
            ############################################################
            if username in usernameList:
                taken_msg = "username is taken"
                client_socket.send(taken_msg.encode())
            elif len(usernameList) > 2:
                full_msg = "full"
                client_socket.send(full_msg.encode())
            else:
                good_msg = "good"
                client_socket.send(good_msg.encode())


            ############################################################
                usernameList.append(username)
                print(f"{username} is trying to join the chatroom.")
            
                clients[client_socket] = (username, client_address[0], client_address[1])  #store client address
                send_all(f"{username} has joined the chatroom.", client_socket)

                client_socket.send(("----------Chatlog----------").encode())
                for msg in msgList:
                    client_socket.send((msg + "\n").encode())           #send each message in the array
                client_socket.send(("\n----------EndLog----------").encode())
#########################################################################################

##########################   if the user wanted to quit       ##################################
        elif message.lower() == "q": 
            if client_socket in clients:
                username = clients[client_socket][0]        #username is empty
                print(f"{username} is leaving the chatroom.")
                clients.pop(client_socket, None)        #remove client from clients
            send_all(f"{username} has left the chatroom.")
            client_socket.close()       #close socket
            break
##################################################################################################3


##############################    normal message         #############################################3
        else:  #sending general messages
            msgList.append(message)  # store the message
            send_all(message, client_socket)
###########################################################################################################


##########################################################################################################################


#################################################  broadcast  ############################################################
def send_all(message, sender_socket=None):     #function so user can send message to everyone other than themselves
    for client_socket in clients:
        if client_socket != sender_socket:
            client_socket.send(message.encode())        #send message to all
            
##############################################################################################################################


###############################################   accept_clients      ########################################################
def server_start():
    print("Server is running...")     #print start of server output
    while True:
        
        client_socket, client_address = server_socket.accept()  #get the client socket address
        
        if len(clients) > MAX_USERS:        #check for chatroom size
            print("Chatroom is full. Rejecting connection...")
            client_socket.send("Sorry, the chatroom is full. Try again later.".encode())        #error message
            client_socket.close()
            continue

        
        client_socket.send("Connected to the server.".encode())     #connect client
        Thread(target=handle_client, args=(client_socket, client_address)).start()

        
#####################################################################################################################################


server_start()  #call function to start server