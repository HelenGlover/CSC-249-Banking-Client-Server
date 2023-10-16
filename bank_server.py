#!/usr/bin/env python3
#
# Bank Server application
# Jimmy da Geek

import socket
import selectors
import types


HOST = "127.0.0.1"      # Standard loopback interface address (localhost)
PORT = 65432            # Port to listen on (non-privileged ports are > 1023)
ALL_ACCOUNTS = dict()   # initialize an empty dictionary
ACCT_FILE = "accounts.txt"
ADDR = (HOST, PORT)
FORMAT = "utf-8"

##########################################################
#                                                        #
# Bank Server Core Functions                             #
#                                                        #
# No Changes Needed in This Section                      #
#                                                        #
##########################################################

#this is working, there is no code for the first two characters being alphabet but thats okay

def acctNumberIsValid(ac_num):
    """Return True if ac_num represents a valid account number. This does NOT test whether the account actually exists, only
    whether the value of ac_num is properly formatted to be used as an account number.  A valid account number must be a string,
    lenth = 8, and match the format AA-NNNNN where AA are two alphabetic characters and NNNNN are five numeric characters."""
    return isinstance(ac_num, str) and \
        len(ac_num) == 8 and \
        ac_num[2] == '-' and \
        ac_num[:2].isalpha() and \
        ac_num[3:8].isdigit()

def acctPinIsValid(pin):
    """Return True if pin represents a valid PIN number. A valid PIN number is a four-character string of only numeric characters."""
    return (isinstance(pin, str) and \
        len(pin) == 4 and \
        pin.isdigit())

def amountIsValid(amount):
    """Return True if amount represents a valid amount for banking transactins. For an amount to be valid it must be a positive float()
    value with at most two decimal places."""
    return isinstance(amount, float) and (round(amount, 2) == amount) and (amount >= 0)

class BankAccount:
    """BankAccount instances are used to encapsulate various details about individual bank accounts."""
    acct_number = ''        # a unique account number
    acct_pin = ''           # a four-digit PIN code represented as a string
    acct_balance = 0.0      # a float value of no more than two decimal places
    
    def __init__(self, ac_num = "zz-00000", ac_pin = "0000", bal = 0.0):
        """ Initialize the state variables of a new BankAccount instance. """
        if acctNumberIsValid(ac_num):
            self.acct_number = ac_num
        if acctPinIsValid(ac_pin):
            self.acct_pin = ac_pin
        if amountIsValid(bal):
            self.acct_balance = bal

    def deposit(self, amount):
        """ Make a deposit. The value of amount must be valid for bank transactions. If amount is valid, update the acct_balance.
        This method returns three values: self, success_code, current balance.
        Success codes are: 0: valid result; 1: invalid amount given. """
        result_code = 0
        if not amountIsValid(amount):
            result_code = 1
        else:
            # valid amount, so add it to balance and set succes_code 1
            self.acct_balance += amount
        return self, result_code, round(self.acct_balance,2)

    def withdraw(self, amount):
        """ Make a withdrawal. The value of amount must be valid for bank transactions. If amount is valid, update the acct_balance.
        This method returns three values: self, success_code, current balance.
        Success codes are: 0: valid result; 1: invalid amount given; 2: attempted overdraft. """
        result_code = 0
        if not amountIsValid(amount):
            # invalid amount, return error 
            result_code = 1
        elif amount > self.acct_balance:
            # attempted overdraft
            result_code = 2
        else:
            # all checks out, subtract amount from the balance
            self.acct_balance -= amount
        return self, result_code, round(self.acct_balance,2)

def get_acct(ac_num): 
    """ Lookup acct_num in the ALL_ACCOUNTS database and return the account object if it's found.
        Return False if the acct_num is invalid. """
    if acctNumberIsValid(ac_num) and (ac_num in ALL_ACCOUNTS):
        return ALL_ACCOUNTS[ac_num] 
    else:
        return False

#helper function for load_all_accounts
#client creates a new account, loads it into the file, new deposit  
def load_account(num_str, pin_str, bal_str):
    """ Load a presumably new account into the in-memory database. All supplied arguments are expected to be strings. """
    try:
        # it is possible that bal_str does not represent a float, so be sure to catch that error.
        bal = float(bal_str)
        if acctNumberIsValid(num_str):
            if get_acct(num_str):
                print(f"Duplicate account detected: {num_str} - ignored")
                return False
            # We have a valid new account number not previously loaded
            new_acct = BankAccount(num_str, pin_str, bal)
            # Add the new account instance to the in-memory database
            ALL_ACCOUNTS[num_str] = new_acct
            print(f"loaded account '{num_str}'")
            return True
    except ValueError:
        print(f"error loading acct '{num_str}': balance value not a float")
    return False
    
def load_all_accounts(acct_file = "accounts.txt"):
    print('g')
    """ Load all accounts into the in-memory database, reading from a file in the same directory as the server application. """
    print(f"loading account data from file: {acct_file}")
    with open(acct_file, "r") as f:
        while True:
            line = f.readline()
            if not line:
                # we're done
                break
            if line[0] == "#":
                # comment line, no error, ignore
                continue
            # convert all alpha characters to lowercase and remove whitespace, then split on comma
            acct_data = line.lower().replace(" ", "").split(',')
            if len(acct_data) != 3:
                print(f"ERROR: invalid entry in account file: '{line}' - IGNORED")
                continue
            load_account(acct_data[0], acct_data[1], acct_data[2])
    print("finished loading account data")
    return True

# ##########################################################
# #                                                        #
# # Bank Server Network Operations                         #
# #                                                        #
# # TODO: THIS SECTION NEEDS TO BE WRITTEN!!               #
# #                                                        #
# ##########################################################

    #######################################
    # Implementing the selectors - NEED TO FIGURE OUT MESSAGE ENCODING BEFOREHAND 
    #######################################
def run_network_server():

#     sel = selectors.DefaultSelector()

#     lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) ##calls to this socket will not block
#     lsock.bind((HOST, PORT))
#     lsock.listen()
#     print(f"Listening on {(HOST, PORT)}")
#     lsock.setblocking(False) ##calls will no longer block
#     sel.register(lsock, selectors.EVENT_READ, data=None) ##registers socket with select(), event read allows it to read 
    
#     try:
#         while True:
#             events = sel.select(timeout=None) ##returns a list of tuples, each with a key and mask
#             for key, mask in events:
#                 if key.data is None:
#                     accept_wrapper(sel, key.fileobj) ##get new socket and register it 
#                 else: ##if key data is not none, then the socket is already accepted - just need to service it
#                     service_connection(sel, key, mask)
#     except KeyboardInterrupt:
#         print("Caught keyboard interrupt, exiting")
#     finally:
#         sel.close()

# def accept_wrapper(sel, sock):
#     conn, addr = sock.accept()  ## Should be ready to read
#     print(f"Accepted connection from {addr}")
#     conn.setblocking(False) ##puts socket in a non-blocking mode
#     data = {} ##object to hold the data you want in !!@331212
#     events = selectors.EVENT_READ | selectors.EVENT_WRITE ##uses bitwise OR - used for manipulating bits - now client connection is ready for writing and reading 
#     sel.register(conn, events, data=data)


# def service_connection(sel, key, mask):
#     sock = key.fileobj ##tuple from .select with the socket object
#     data = key.data
#     if mask & selectors.EVENT_READ: ##evaluates to true, data is append to data.outb
#         recv_data = sock.recv(1024)  
#         if recv_data:
#             print("the recieving data" + str(recv_data))
#             data.outb += recv_data
#         else: ##client closed socket and SERVER should too!
#             print(f"Closing connection to {data.addr}")
#             sel.unregister(sock)
#             sock.close()
#     if mask & selectors.EVENT_WRITE: ##data also stored in data.outb
#         if data.outb:
#             print(f"Echoing {data.outb!r} to {data.addr}")
#             sent = sock.send(data.outb)  ## Should be ready to write
#             data.outb = data.outb[sent:]

#     print("server starting - listening for connections at IP", HOST, "and port", PORT)

    #######################################
    # Part A: Connecting to socket 
    #######################################
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
        server_sock.bind((HOST,PORT))
        server_sock.listen()
        conn, addr = server_sock.accept()

        with conn:  #new connection - new socket object is returned from accept() (different socket from the listening socket)
            print(f"Connection was established, {addr}")
    # #######################################
    # # Part B: decoding the message 
    # #######################################      
        #while True: #we want while to loop through processes?

            msg = conn.recv(1024)
            print('The decoded message', msg.decode(FORMAT)) #this worked, prints out the code
            print(f"Received client message '{msg!r}' [{len(msg)} bytes] \n") # print client message
            print(type(msg))

    #######################################
    # Part C: Split and get validation from acct_num 
    #######################################  

            new_login = str(msg) #Might want to keep as byte but for now keep as this - dont need to split (1. bytes, and 2. the acct_num from client was send over)
            print(type(new_login)) #just want to see if its
            new_login = [x.strip() for x in new_login.split(',')]
            ac_num = new_login[0] #does have b attached as byte
            ac_num = ac_num[2:]
            print(ac_num, "new account")
            pin = new_login[1][:-1]
            print(pin, "new pin")

            if acctNumberIsValid(ac_num) and acctPinIsValid(pin):    
                msg1 ='The account number and pin are correct'
                print(msg1)
                conn.sendall(msg1.encode(FORMAT))
                
            elif acctNumberIsValid(ac_num) and not acctPinIsValid(pin):  
                msg1 ='The account number is correct, the PIN is not'
                conn.sendall(msg1.encode(FORMAT))

            elif not acctNumberIsValid(ac_num) and acctPinIsValid(pin):  
                msg1 ='The pin is correct, the ACCOUNT NUMBER is not'
                conn.sendall(msg1.encode(FORMAT))

            else: 
                msg ="The PIN and ACCOUNT NUMBER are both wrong"
                print(msg1)
                conn.sendall(msg1.encode(FORMAT))
    return 
####################################################

        #####################################
        #transactions - hopefully implement them with the selectors soon
        #####################################
        
        #####################################
        #deposit
        #####################################

        #process_customer_transactions comes after validation

        #need to get balance  (get_acct_balance) - DEPOSIT

            #if process_deposit(sock, acct_num)

                # call amountIsValid
                # class BankAccount(input)
                # send back to server

        #adding new balance commands
    
        #####################################
        #withdraw
        #####################################

        #process_customer_transactions comes after validation

        #need to get balance  (get_acct_balance) - DEPOSIT

            #if withdraw(self, amount)
                # call amountIsValid
                # check - amountIsValid is not positive float() with at most two decimal places.
                # send back to client

                # class BankAccount(input)
                # send back to server
        
        #####################################
        #check balance is part of "withdraw" and "deposit", but not something ppl can do
    

##########################################################
#                                                        #
# Bank Server Demonstration                              #
#                                                        #
# Demonstrate basic server functions.                    #
# No changes needed in this section.                     #
#                                                        #
##########################################################

def demo_bank_server():
    """ A function that exercises basic server functions and prints out the results. """
    # get the demo account from the database
    acct = get_acct("zz-99999")
    print(f"Test account '{acct.acct_number}' has PIN {acct.acct_pin}")
    print(f"Current account balance: {acct.acct_balance}")
    print(f"Attempting to deposit 123.45...")
    _, code, new_balance = acct.deposit(123.45)
    if not code:
        print(f"Successful deposit, new balance: {new_balance}")
    else:
        print(f"Deposit failed!")
    print(f"Attempting to withdraw 123.45 (same as last deposit)...")
    _, code, new_balance = acct.withdraw(123.45)
    if not code:
        print(f"Successful withdrawal, new balance: {new_balance}")
    else:
        print("Withdrawal failed!")
    print(f"Attempting to deposit 123.4567...")
    _, code, new_balance = acct.deposit(123.4567)
    if not code:
        print(f"Successful deposit (oops), new balance: {new_balance}")
    else:
        print(f"Deposit failed as expected, code {code}") 
    print(f"Attempting to withdraw 12345.45 (too much!)...")
    _, code, new_balance = acct.withdraw(12345.45)
    if not code:
        print(f"Successful withdrawal (oops), new balance: {new_balance}")
    else:
        print(f"Withdrawal failed as expected, code {code}")
    print("End of demo!")

##########################################################
#                                                        #
# Bank Server Startup Operations                         #
#                                                        #
# No changes needed in this section.                     #
#                                                        #
##########################################################

if __name__ == "__main__":
    # on startup, load all the accounts from the account file
    load_all_accounts(ACCT_FILE)
    # uncomment the next line in order to run a simple demo of the server in action
    #demo_bank_server()
    run_network_server()
    print("bank server exiting...")
