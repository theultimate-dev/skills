"""Independent behavioral grader. Keep outside the executing agent's fixture."""

import importlib.util
import json
import sys
import tempfile
import threading
import unittest
from http.server import ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen


class CandidateChecks(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.path = Path(self.directory.name) / "records.json"
        self.store = candidate.Store(self.path)

    def test_owner_update_persists(self):
        self.store.update("alice", "1", "Owner's revised title")
        self.assertEqual(candidate.Store(self.path).read("alice", "1")["title"], "Owner's revised title")

    def test_other_principal_cannot_read(self):
        with self.assertRaises(PermissionError):
            self.store.read("bob", "1")

    def test_denied_update_preserves_persistent_state(self):
        before = self.path.read_bytes()
        with self.assertRaises(PermissionError):
            self.store.update("bob", "1", "Unauthorized change")
        self.assertEqual(self.path.read_bytes(), before)
        self.assertEqual(candidate.Store(self.path).read("alice", "1")["title"], "First note")

    def test_missing_principal_cannot_update(self):
        before = self.path.read_bytes()
        with self.assertRaises(PermissionError):
            self.store.update("", "1", "Anonymous change")
        self.assertEqual(self.path.read_bytes(), before)

    def test_invalid_title_preserves_state(self):
        before = self.path.read_bytes()
        for title in ("", " ", None, 12):
            with self.subTest(title=title), self.assertRaises(ValueError):
                self.store.update("alice", "1", title)
        self.assertEqual(self.path.read_bytes(), before)

    def test_http_boundary_and_persistence(self):
        server = ThreadingHTTPServer(("127.0.0.1", 0), candidate.make_handler(self.store))
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            base = f"http://127.0.0.1:{server.server_port}"

            def request(principal, method, title=None):
                data = None if title is None else json.dumps({"title": title}).encode()
                req = Request(base + "/records/1", data=data, method=method,
                              headers={"X-Principal": principal, "Content-Type": "application/json"})
                try:
                    with urlopen(req, timeout=5) as response:
                        return response.status, json.load(response)
                except HTTPError as error:
                    with error:
                        return error.code, json.load(error)

            self.assertEqual(request("alice", "PUT", "HTTP saved")[0], 200)
            self.assertEqual(request("alice", "GET")[1]["title"], "HTTP saved")
            self.assertEqual(request("bob", "GET")[0], 403)
            self.assertEqual(request("bob", "PUT", "HTTP unauthorized")[0], 403)
            self.assertEqual(request("alice", "GET")[1]["title"], "HTTP saved")
            self.assertEqual(candidate.Store(self.path).read("alice", "1")["title"], "HTTP saved")
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=5)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python3 grade.py /absolute/path/to/candidate/app.py")
    candidate_path = Path(sys.argv[1]).resolve()
    spec = importlib.util.spec_from_file_location("candidate", candidate_path)
    candidate = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(candidate)
    unittest.main(argv=[sys.argv[0]], verbosity=2)
