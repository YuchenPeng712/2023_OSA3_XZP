import socket
import threading
import select
import sys

# define the Node
class Node:
  def __init__(self, label, content):
    self.label = label
    self.content = content
    self.next_node = None
    self.next_book = None
    self.next_frequent_search = None

# define the List
class Node_List:
    def __init__(self):
        self.head = None
        self.tail = None
        self.head_list = []
        self.tail_list = []
        self.id_index_dict = {}


# client connection handler
def handle_client(client_socket, client_ID):
    print("Connection established from client_ID:", client_ID)
    client_socket.send(bytes("Welcome to the server!", "utf-8"))
    # data = client_socket.recv(1024)
    # print(data)
    # client_socket.close()
    while True:
        # Use select to check for readable sockets
        readable, _, _ = select.select([client_socket], [], [], 1)
        if readable:
            data = client_socket.recv(1024)
            if not data:
                break  # No more data to read, client disconnected
            else:
                # Construct the Node, Lock the List, Add to the List, Unlock
                label = client_ID  # keep track of which book is it
                new_node = Node(label, data)
                # Acquire Lock Here
                while True:
                    print("Client : ", client_ID, "Got The Lock")
                    with lock:
                        # 1. Append to the list
                            # If this is the first node of the list
                            # If not the first node of this list
                        if shared_list.head is None:
                            shared_list.head = new_node
                            shared_list.tail = new_node
                        else:
                            shared_list.tail.next_node = new_node
                            shared_list.tail = new_node

                        # 2. Update for head&tail list
                            # if this is a new book
                            # if this book has been records
                        if client_ID not in shared_list.id_index_dict:
                            dict_index = len(shared_list.head_list) # the number of books in head/tail list is the index for the new book
                            shared_list.id_index_dict[client_ID] = dict_index
                            shared_list.head_list.append(new_node)
                            shared_list.tail_list.append(new_node)
                        else:
                            dict_index = shared_list.id_index_dict[client_ID]
                            shared_list.tail_list[dict_index].next_book = new_node
                            shared_list.tail_list[dict_index] = new_node
                    
                    # Unlock Here
                    break

    client_socket.close()
    content_to_write = []
    dict_index = shared_list.id_index_dict[client_ID]
    current_node = shared_list.head_list[dict_index]

    while current_node:
        content_to_write.append(current_node.content)
        current_node = current_node.next_book

    # Write the content to the book file
    with open(f'book_{client_ID:02d}.txt', 'wb') as book_file:
        for content in content_to_write:
            book_file.write(content)

# access command-line arguments
arguments = sys.argv
for i in range(len(arguments)):
    if arguments[i] == "-l":
        port_number = int(arguments[i+1])
    if arguments[i] == "-p":
        pattern = arguments[i+1]


# set up the socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', port_number))
server_socket.listen(10)

# variable definition 
client_ID = 1
shared_list = Node_List()
lock = threading.Lock()

# listen
while True:
    client_socket, address = server_socket.accept()
    # Create a new thread for each client connection
    client_handler = threading.Thread(target=handle_client, args=(client_socket, client_ID))
    client_handler.start()
    client_ID =  client_ID + 1 
