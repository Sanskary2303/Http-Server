# HTTP Server Project

## Overview

This project is a simple HTTP server implemented in Python using the `socket` and `threading` modules. It includes functionality for handling echo requests, serving files, processing user-agent requests, and handling different HTTP methods (GET and POST).

## Features

1. **Echo Service**: 
   - Responds with the message sent in the request path. Supports gzip compression if specified in the `Accept-Encoding` header.

2. **File Service**:
   - **GET**: Serves files from a specified directory.
   - **POST**: Allows uploading files to a specified directory.

3. **User-Agent Service**:
   - Responds with the `User-Agent` header sent in the request.

4. **Root Path**:
   - Responds with a simple `200 OK` status.

## Usage

### Starting the Server

To start the server, run the following command in your terminal:

```bash
python server.py [--directory <path_to_directory>]

```
   - The `--directory` argument is optional. If provided, it specifies the directory from which files will be served.

## Handling Requests
1. **Echo Requests:**

   - Send a request to /echo/<message>.
   - Example: http://localhost:4221/echo/HelloWorld

2. **File Requests:**

   - **GET**: Request a file from the specified directory.
      - Example: http://localhost:4221/files/filename.txt
   - **POST**: Upload a file to the specified directory.
      - Include the file content in the request body.

3. **User-Agent Requests:**

   - Send a request to /user-agent to get the User-Agent header from the request.
   - Example: http://localhost:4221/user-agent

## Example Commands
1. **Start Server with Directory:**

```bash
python server.py --directory /path/to/directory
```

2. **Send Echo Request:**

```bash
curl -H "Accept-Encoding: gzip" http://localhost:4221/echo/HelloWorld
```

3. **Get a File:**

```bash
curl http://localhost:4221/files/filename.txt
```

4. **Post a File:**

```bash
curl -X POST -d "File content" http://localhost:4221/files/newfile.txt
```

5. **Get User-Agent:**

```bash
curl http://localhost:4221/user-agent
```

## Code Overview

### `parse_request` Function
Parses the incoming HTTP request and returns a dictionary containing the method, path, protocol, headers, and data.

### `handle_client` Function
Handles client requests based on the parsed request:

   - Echoes the message for /echo.
   - Serves or uploads files for /files.
   - Returns the User-Agent for /user-agent.
   - Returns 200 OK for the root path.
   - Returns 404 Not Found for invalid paths.

### `main` Function
Creates and starts the server, accepting incoming client connections and spawning a new thread to handle each client.

## Dependencies
   - Python 3.x

## Notes
   - Ensure the specified directory exists and is accessible for file operations.
   - The server listens on `localhost` at port `4221`.