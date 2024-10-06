# CSC 249 – ATM client with multi-client back-end banking server

Build a distributed ATM banking application. This application consists of two separate software programs: (1) a bank server, which holds all bank account records and handles all financial transactions; and (2) an Automated Teller Machine client, which obtains needed inputs from the customer but otherwise relies on the server to perform transaction processing.

Enable the banking server to handle simultaneous connections from different ATM client instances, and then process transaction requests correctly. 

## The bank_server:

* MUST run in its own computing process (i.e., in a dedicated terminal window).
* MUST allow multiple simultaneous ATM client connections.
* MUST communicate with ATM clients exclusively by sending and receiving messages over the network using an application-layer message protocol of your own design.
* MUST allow multiple ATM clients to send messages to the server and receive timely responses from the server. One client should never be blocked until other client(s) have completed all their transactions.
* MUST validate an account's PIN code before allowing any other transactions to be performed on that account.
* MUST prevent more than one ATM client at a time from accessing a bank account and performing transactions on it.
* MUST transmit error results to the client using numeric codes rather than literal message strings.
* After a customer "logs in" to their account from an ATM client, the server MUST allow any number of transactions to be performed during that client banking session. During the session, access to the account from other ATM clients MUST be rejected.
* MUST prevent malicious client applications (i.e., other than the implemented atm_client application) from being able to send messages the the server which cause the server to crash, behave incorrectly, and/or provide unauthorized access to customer bank accounts.
* The bank_server MAY generate console output for tracing and debugging purposes.
* The bank_server MUST NOT assume that any customer has access to the server's console.

## ATM Client 

* MUST run in its own computing process (i.e., in a dedicated terminal window).
* MUST obtain all needed user inputs through keyboard interaction.
* MUST connect to only one bank_server at a time.
* MUST communicate with the bank_server exclusively by sending and receiving messages over the network using an application-layer message protocol of your own design.
* MUST require each banking session to being with a customer "log in" step, where the customer provides an account number and PIN which are then validated by the bank_server.
* MUST NOT allow a customer to perform any banking transactions unless their account number and PIN are first validated by the bank_server.
* MUST allow a customer to perform any sequence of deposits, withdrawals, and balance checks after they have validated their account number and PIN.
* MUST NOT allow a customer to overdraw their bank account.
