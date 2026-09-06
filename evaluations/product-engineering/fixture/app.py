"""Deliberately incomplete local evaluation fixture, not production software."""

import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Lock


class Store:
    def __init__(self, path):
        self.path = Path(path)
        self.lock = Lock()
        if not self.path.exists():
            self.path.write_text(json.dumps({"1": {"owner": "alice", "title": "First note"}}))

    def read(self, principal, record_id):
        with self.lock:
            record = json.loads(self.path.read_text()).get(record_id)
            if record is None or record["owner"] != principal:
                raise PermissionError("Record unavailable")
            return dict(record)

    def update(self, principal, record_id, title):
        if not isinstance(title, str) or not title.strip():
            raise ValueError("Title is required")
        with self.lock:
            records = json.loads(self.path.read_text())
            record = records.get(record_id)
            if record is None:
                raise PermissionError("Record unavailable")
            record["title"] = title
            self.path.write_text(json.dumps(records))
            return dict(record)


HTML = b'''<!doctype html>
<html lang="en"><meta charset="utf-8"><title>Saved record fixture</title>
<style>body{font:18px system-ui;max-width:40rem;margin:3rem auto;padding:1rem}label,button{display:block;margin:1rem 0}input,select,button{font:inherit}</style>
<h1>Saved record</h1>
<label>Principal <select id="principal"><option value="alice">Alice</option><option value="bob">Bob</option></select></label>
<button id="load">Load record</button>
<label>Title <input id="title" value=""></label>
<button id="save">Save record</button>
<p role="status" id="status">Choose a principal and load the record.</p>
<script>
const principal = document.getElementById('principal');
const title = document.getElementById('title');
const status = document.getElementById('status');
async function request(method) {
  const options = {method, headers: {'X-Principal': principal.value, 'Content-Type':'application/json'}};
  if (method === 'PUT') options.body = JSON.stringify({title:title.value});
  try {
    const response = await fetch('/records/1', options);
    const body = await response.json();
    if (!response.ok) throw new Error(body.error);
    title.value = body.title;
    status.textContent = method === 'PUT' ? 'Saved' : 'Loaded';
  } catch (error) { status.textContent = error.message; }
}
document.getElementById('load').onclick = () => request('GET');
document.getElementById('save').onclick = () => request('PUT');
</script></html>'''


def make_handler(store):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, format, *args):
            pass

        def reply(self, status, body):
            data = json.dumps(body).encode()
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def do_GET(self):
            if self.path == "/":
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(HTML)))
                self.end_headers()
                self.wfile.write(HTML)
                return
            if self.path != "/records/1":
                self.reply(404, {"error": "Not found"})
                return
            try:
                self.reply(200, store.read(self.headers.get("X-Principal", ""), "1"))
            except PermissionError as error:
                self.reply(403, {"error": str(error)})

        def do_PUT(self):
            if self.path != "/records/1":
                self.reply(404, {"error": "Not found"})
                return
            try:
                body = json.loads(self.rfile.read(int(self.headers.get("Content-Length", "0"))))
                result = store.update(self.headers.get("X-Principal", ""), "1", body.get("title"))
                self.reply(200, result)
            except PermissionError as error:
                self.reply(403, {"error": str(error)})
            except (ValueError, TypeError, AttributeError) as error:
                self.reply(400, {"error": str(error)})

    return Handler


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--data", required=True)
    args = parser.parse_args()
    server = ThreadingHTTPServer(("127.0.0.1", args.port), make_handler(Store(args.data)))
    print(f"Fixture listening on http://127.0.0.1:{server.server_port}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
