#!/usr/bin/env python3
# Automated Teller Machine (ATM) client application.

import socket
import selectors #needed for handling multiple connections at once, calls send and recv as many times
import types 

HOST = "127.0.0.1"      # The bank server's IP address
PORT = 65432            # The port used by the bank server
FORMAT = "utf-8"
ADDR = (HOST, PORT)

##########################################################
#                                                        #
# ATM Client Network Operations                          #
#                                                        #
# NEEDS REVIEW. Changes may be needed in this section.   #
#                                                        #
##########################################################

##multi-connection client on the client side

# sel = selectors.DefaultSelector()
# messages = [b"Message 1 from client.", b"Message 2 from client."]

# def start_connections(host, port, num_conns): ##num_comms read from cmd line, # of connections to create
#     server_addr = (host, port)
#     for i in range(0, num_conns):
#         connid = i + 1
#         print(f"Starting connection {connid} to {server_addr}")
#         sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         sock.setblocking(False)
#         sock.connect_ex(server_addr) ##avoid blocking error with connect()
#         events = selectors.EVENT_READ | selectors.EVENT_WRITE
#         data = types.SimpleNamespace( ##data to store with client uses simplenamespaces
#             connid=connid,
#             msg_total=sum(len(m) for m in messages),
#             recv_total=0,
#             messages=messages.copy(), ##copy the messages client sends and keeps track in object data
#             outb=b"",
#         )
#         sel.register(sock, events, data=data)



## sending messages to the server given a open socket connection
def send_to_server(sock, msg):
    """ Given an open socket connection (sock) and a string msg, send the string to the server. """
    sock.sendall(msg.encode('utf-8'))
    get_from_server(sock)

## recieving message from server 
def get_from_server(sock):
    """ Attempt to receive a message from the active connection. Block until message is received. """
    msg1 = sock.recv(1024)
    msg1.decode("utf-8")
    print(msg1) #should be "The account number and pin are correct"
    return


def login_to_server(sock, acct_num, pin):
    """ Attempt to login to the bank server. Pass acct_num and pin, get response, parse and check whether login was successful. """
    msg = acct_num + ',' + pin #concatenate into a string to be converted into bytes
    send_to_server(sock, msg)

    #we want validated to remain as 0 so it passes the factors forward
    validated = 0
    msg1 = get_from_server(sock)
    print('The message is printing on the terminal:', msg1)

    #possible for loop
    if msg1 is True:
        print("Sending message to transactions")
        validated = 1

    if msg is False: 
        send_to_server(sock, msg) 
        msg1 = get_from_server(sock)
        if msg == "1":
            validated = 1
    return validated


def get_login_info(): 
    """ Get info from customer. TODO: Validate inputs, ask again if given invalid input. """
    acct_num = input("Please enter your account number: ")
    pin = input("Please input your four digital PIN ")
    return acct_num, pin

def process_deposit(sock, acct_num):
    """ TODO: Write this code. """
    bal = get_acct_balance(sock, acct_num)
    amt = input("How much would you like to deposit? (You have '${bal}' available)")
    # TODO communicate with the server to request the deposit, check response for success or failure.
    
    send_to_server("d" + amt)
    deposit_success = get_from_server(sock)

    if deposit_success == 1:
        print("Deposit transaction completed.")
    else:
        print("Something is wrong")
    return


def get_acct_balance(sock, acct_num):
    """ TODO: Ask the server for current account balance. """
    bal = 0.0
    # TODO code needed here, to get balance from server then return it
    send_to_server(sock, acct_num)
    bal = get_from_server(sock)
    bal = bal.decode('utf-8')
    return bal

def process_withdrawal(sock, acct_num):
    """ TODO: Write this code. """
    bal = get_acct_balance(sock, acct_num)
    amt = input(f"How much would you like to withdraw? (You have ${bal} available)")
    # TODO communicate with the server to request the withdrawal, check response for success or failure.
    send_to_server(bal, amt)
    get_from_server(bal, amt)
        
    print("Withdrawal transaction completed.")
    return

def process_customer_transactions(sock, acct_num):
    """ Ask customer for a transaction, communicate with server. TODO: Revise as needed. """
    while True:
        print("Select a transaction. Enter 'd' to deposit, 'w' to withdraw, or 'x' to exit.")
        req = input("Your choice? ").lower()
        if req not in ('d', 'w', 'x'):
            print("Unrecognized choice, please try again.")
            continue
        if req == 'x':
            # if customer wants to exit, break out of the loop
            break
        elif req == 'd':
            process_deposit(sock, acct_num)
        else:
            process_withdrawal(sock, acct_num)

def run_atm_core_loop(sock):
    """ Given an active network connection to the bank server, run the core business loop. """
    acct_num, pin = get_login_info()
    validated = login_to_server(sock, acct_num, pin)
    if validated == 1:
        print("Thank you, your credentials have been validated.")
    else:
        print("Account number and PIN do not match. Terminating ATM session.")
        return False
    process_customer_transactions(sock, acct_num)
    print("ATM session terminating.")
    return True    

##########################################################
#                                                        #
# ATM Client Startup Operations                          #
#                                                        #
# No changes needed in this section.                     #
#                                                        #
##########################################################

def run_network_client():
    """ This function connects the client to the server and runs the main loop. """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            run_atm_core_loop(s)
    except Exception as e:
        print(f"Unable to connect to the banking server - exiting...")

if __name__ == "__main__":
    print("Welcome to the ACME ATM Client, where customer satisfaction is our goal!")
    run_network_client()
    print("Thanks for banking with us! Come again soon!!")
