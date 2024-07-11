import socket
import threading
import sys
import os
import gzip

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
            header_dict[key] = value.strip()
    header_dict["data"] = headers[-1].strip()
    return header_dict

def handle_client(client):

    request = client.recv(1024).decode()
    parsed_request = parse_request(request)

    if len(sys.argv) >1  and sys.argv[1] == "--directory":
        directory = sys.argv[2]

    modified_path = parsed_request["path"].split('/',2)

    if modified_path[1] == "echo":
        if "Accept-Encoding" in parsed_request.keys():
            accepted_encodings = list(map(str.strip , parsed_request["Accept-Encoding"].split(",")))
            if "gzip" in accepted_encodings:
                compressed_data = gzip.compress(modified_path[2].encode())
                client.sendall(f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Encoding: gzip\r\nContent-Length: {len(compressed_data)}\r\n\r\n".encode())
                client.sendall(compressed_data)
            else:
                client.sendall(f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(modified_path[2])}\r\n\r\n{modified_path[2]}".encode())
        else:
            client.sendall(f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(modified_path[2])}\r\n\r\n{modified_path[2]}".encode())

    elif modified_path[1] == "files":
        filename = modified_path[2]
        filepath = os.path.join(directory,filename)

        if parsed_request["method"] == "GET":
            if(os.path.exists(filepath)):
                with open(filepath, "r") as f:
                    content = f.read()
                client.sendall(f"HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: {len(content)}\r\n\r\n{content}".encode())
            else:
                client.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")

        elif parsed_request["method"] == "POST":
            with open(filepath,"w") as f:
                f.write(parsed_request["data"])
            client.sendall(b"HTTP/1.1 201 Created\r\n\r\n")

    elif parsed_request["path"] == "/": 
        client.sendall(b"HTTP/1.1 200 OK\r\n\r\n")

    elif parsed_request['path'] == "/user-agent":
        user_agent = parsed_request["User-Agent"].strip()
        client.sendall(f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(user_agent)}\r\n\r\n{user_agent}".encode())

    else:
        client.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")


def main():

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    while True:
        client, address = server_socket.accept()
        thread = threading.Thread(target=handle_client,args=(client,))
        thread.start()



if __name__ == "__main__":
    main()
