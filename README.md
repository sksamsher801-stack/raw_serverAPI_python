# Q1: Raw HTTP Notes Server

A small REST-style notes server built with Python's built-in http.server module. Notes are stored in memory while the server is running.

## Requirements

- Python 3
- No third-party packages are required.
- See requirements.txt.

## Run the server

Open Command Prompt in this folder and run:

~~~cmd
python server.py
~~~

Leave this terminal running. Use a second Command Prompt window for the curl commands below.

## Endpoints

### List all notes

~~~cmd
curl.exe -i http://127.0.0.1:8080/notes
~~~

### Add a note

~~~cmd
curl.exe -i -X POST http://127.0.0.1:8080/notes -H "Content-Type: application/json" -d "{\"text\":\"Learn REST\"}"
~~~

The request body must be JSON and contain a text field.

### Get one note

~~~cmd
curl.exe -i http://127.0.0.1:8080/notes/1
~~~

Change 1 to the note ID you want to retrieve.

### Delete one note

~~~cmd
curl.exe -i -X DELETE http://127.0.0.1:8080/notes/1
~~~

Change 1 to the note ID you want to delete.

## Responses and request logs

The server returns JSON responses. It uses status codes such as 200 for successful reads, 201 when a note is created, 204 when a note is deleted, 400 for invalid input, and 404 when a path or note is not found. Each request is logged in the server terminal with its method, path, status code, and duration.

Notes are kept in memory, so they are erased when the server stops.

## Submission

Include server.py, this README, and screenshots showing the endpoint tests and their responses.
