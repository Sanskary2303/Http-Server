# Uncomment this to pass the first stage
import socket
import threading

def parse_request(request:str):
    header_dict = {}
    headers = request.split("\r\n")
    request_line = headers[0].split()
    header_dict["method"] = request_line[0]
    header_dict["path"] = request_line[1]
    header_dict["protocol"] = request_line[2]
    for header in headers[1:]:
        if header == '':
            break
        else:
            key , value = header.split(':',1)
            header_dict[key] = value
    return header_dict

def handle_client(client):
    request = client.recv(1024).decode()
    parsed_request = parse_request(request)

    modified_path = parsed_request["path"].split('/')

    if modified_path[1] == "echo":
        client.sendall(f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(modified_path[2])}\r\n\r\n{modified_path[2]}".encode())
    elif parsed_request["path"] == "/": 
        client.sendall(b"HTTP/1.1 200 OK\r\n\r\n")
    elif parsed_request['path'] == "/user-agent":
        user_agent = parsed_request["User-Agent"].strip()
        client.sendall(f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(user_agent)}\r\n\r\n{user_agent}".encode())
    else:
        client.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    while True:
        client, address = server_socket.accept()
        thread = threading.Thread(target=handle_client,args=(client,))
        thread.start()



if __name__ == "__main__":
    main()
