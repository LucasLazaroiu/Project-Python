
import socket
from threading import Thread
from datetime import datetime

client_socket = None 

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)                   #Connects client to socket
client_socket.connect(("localhost", 18000))



def messages():                                                          #constantly checks for messages in the server      
    while True:
            message = client_socket.recv(1024).decode()
            if message:
                print("\n" + message)
        
#########################################################################################################################################


def chatroom():                                                               # Function that can allow us to join chatroom
    username = input("Enter your username to join: ")
    client_socket.send(f"JOIN:{username}".encode())
    ####################################################################
    status = client_socket.recv(1024).decode()

    if status == "taken":
        print("taken")
        displayMenu()
    elif status == "full":
        print("full")
        displayMenu()
    else:




    ####################################################################
        print(f"You have joined the chatroom as {username}")
    
    
        while True:                                                                     # Enter chat mode for sending messages
            message = input()                       
            if message.lower() == "q":                                                  #checks if user types in 1 to return back into the menu
                client_socket.send("q".encode())
                print("You have left the chatroom.")
                break  
            else:
                # Send the message to the server with a timestamp
                timestamp = datetime.now().strftime("[%H:%M]")  # Add timestamp           #creates timestamp for when user types in a message
                client_socket.send(f"{timestamp} {username}: {message}".encode())

##########################################################################################################################################
def displayMenu():                                                                 # Function to handle the menu and user input
    while True:
        print("\nMenu:")
        print("1. Get a report of the chatroom from the server")
        print("2. Request to join the chatroom")
        print("3. Quit the program")
        choice = input("Select an option: ")

        # Option 1: View users in the chatroom
        if choice == "1":
            client_socket.send("1".encode())                                       #if choice is option 1 then it sends the message to to server to return report
        
        # Option 2: Join chatroom
        elif choice == "2":
                                                                   #actually join the chatroom by going through the chatroom function
            chatroom()
        
        # Option 3: Quit
        elif choice == "3":                                                         #ends the program
            print("You have disconnected from the server.")
            client_socket.close()
            break
        else:
            print("Invalid option. Please choose 1, 2, or 3.")
########################################################################################################################################
# Main execution
def main():
    global client_socket                                    


    listen_thread = Thread(target=messages)
    listen_thread.daemon = True                                                         # Will create athread for the server
    listen_thread.start()


    displayMenu()                                                                      # Display the menu for interacting with the server

    client_socket.close()
    print("Client disconnected.")

if __name__ == "__main__":
    main()                                  