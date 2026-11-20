# Q1 raw HTTP notes server.

from http.server import BaseHTTPRequestHandler, HTTPServer  # Use Python built-ins to create the HTTP server.
import json  # Convert JSON request and response data.
import time  # Measure how long each request takes.
from urllib.parse import urlparse  # Extract the path from a request URL.

HOST = "127.0.0.1"
PORT = 8080
notes = {}  # Keep notes in memory while the server is running.
next_id = 1  # Assign a unique ID to each new note.

class NotesHandler(BaseHTTPRequestHandler):
    def send_json(self, status_code, data):
        """sending JSON response."""
        body = json.dumps(data).encode("utf-8")  # Convert response data to JSON bytes.
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        if status_code != 204:
            self.wfile.write(body)

    def do_GET(self):  # Handle requests that read notes.
        started_at = time.perf_counter()
        status_code = 200
        path = urlparse(self.path).path  # Get the request path without query parameters.
        parts = path.strip("/").split("/")
        try:
            if path == "/notes":
                self.send_json(200, list(notes.values()))
            elif len(parts) == 2 and parts[0] == "notes":
                try:
                    note_id = int(parts[1])
                except ValueError:
                    self.send_json(400, {"error": "Note ID must be a number"})
                    status_code = 400
                else:
                    note = notes.get(note_id)
                    if note is None:
                        self.send_json(404, {"error": f"Note {note_id} not found"})
                        status_code = 404
                    else:
                        self.send_json(200, note)
            else:
                self.send_json(404, {"error": "Endpoint not found"})
                status_code = 404
        finally:
            self.log_request_details(started_at, status_code)

    def do_POST(self):  # Handle requests that add a note.
        started_at = time.perf_counter()
        status_code = 201
        global next_id  # Allow this method to update the shared ID counter.
        if self.path != "/notes":
            self.send_json(404, {"error": "Endpoint not found"})
            status_code = 404
            self.log_request_details(started_at, status_code)
            return
        try:
            content_length = int(self.headers.get("Content-Length", "0"))
            body = self.rfile.read(content_length)  # Read the JSON body sent by the client.
            data = json.loads(body.decode("utf-8"))  # Decode and parse the submitted JSON.
            if not isinstance(data, dict) or not isinstance(data.get("text"), str):
                self.send_json(400, {"error": "JSON body must contain a text field"})
                status_code = 400
            else:
                note = {"id": next_id, "text": data["text"]}  # Build the new note.
                notes[next_id] = note  # Store the note in memory.
                next_id += 1
                self.send_json(201, note)
        except (json.JSONDecodeError, UnicodeDecodeError, ValueError):
            self.send_json(400, {"error": "Invalid JSON body"})
            status_code = 400
        finally:
            self.log_request_details(started_at, status_code)

    def do_DELETE(self):  # Handle requests that delete a note.
        started_at = time.perf_counter()
        status_code = 204
        path = urlparse(self.path).path  # Get the request path without query parameters.
        parts = path.strip("/").split("/")
        if len(parts) != 2 or parts[0] != "notes":
            self.send_json(404, {"error": "Endpoint not found"})
            status_code = 404
        else:
            try:
                note_id = int(parts[1])
            except ValueError:
                self.send_json(400, {"error": "Note ID must be a number"})
                status_code = 400
            else:
                if note_id not in notes:
                    self.send_json(404, {"error": f"Note {note_id} not found"})
                    status_code = 404
                else:
                    del notes[note_id]  # Remove the selected note from memory.
                    self.send_response(204)
                    self.end_headers()
        self.log_request_details(started_at, status_code)

    def log_request_details(self, started_at, status_code):
        elapsed = time.perf_counter() - started_at  # Calculate the request duration.
        print(
            f"{self.command} {self.path} "
            f"{status_code} {elapsed:.4f}s"
        )

    def send_error(self, code, message=None, explain=None):
        """with 405 HTTP error's return as JSON."""
        messages = {
            405: "Method not allowed",
            501: "Method not implemented",
        }
        self.send_json(code, {"error": messages.get(code, message or "Error")})

def run_server():
    server = HTTPServer((HOST, PORT), NotesHandler)  # Create the server using the chosen host and port.
    print(f"Server is running: http://{HOST}:{PORT}")
    print("for close the server press: Ctrl+C")
    try:
        server.serve_forever()  # Keep accepting requests until stopped.
    except KeyboardInterrupt:
        print("\nServer is closing.....")
    finally:
        server.server_close()

if __name__ == "__main__":  # Run the server only when this file is started directly.
    run_server()
