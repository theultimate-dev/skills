import tempfile
import unittest
from pathlib import Path

from app import Store


class HappyPathTests(unittest.TestCase):
    def test_owner_update_survives_reopen(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "records.json"
            store = Store(path)
            store.update("alice", "1", "Updated note")
            self.assertEqual(Store(path).read("alice", "1")["title"], "Updated note")


if __name__ == "__main__":
    unittest.main()
