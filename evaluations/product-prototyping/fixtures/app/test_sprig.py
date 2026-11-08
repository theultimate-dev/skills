import contextlib
import io
import pathlib
import tempfile
import unittest

import sprig


class SprigTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.data = str(pathlib.Path(self.tmp.name) / "sprig.json")

    def run_sprig(self, *args, today="2026-03-01"):
        out = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
            code = sprig.main(["--data", self.data, "--today", today, *args])
        return code, out.getvalue()

    def test_due_after_interval(self):
        self.run_sprig("add", "fern", "--every", "7")
        self.assertEqual(self.run_sprig("due", today="2026-03-07")[1], "")
        self.assertEqual(self.run_sprig("due", today="2026-03-08")[1], "fern\n")

    def test_water_resets_interval(self):
        self.run_sprig("add", "fern", "--every", "7")
        self.run_sprig("water", "fern", today="2026-03-08")
        self.assertEqual(self.run_sprig("due", today="2026-03-14")[1], "")

    def test_names_are_case_insensitive(self):
        self.run_sprig("add", "Fern", "--every", "7")
        self.assertEqual(self.run_sprig("add", "fern", "--every", "3")[0], 2)

    def test_unknown_plant(self):
        self.assertEqual(self.run_sprig("water", "fern")[0], 3)

    def test_remove(self):
        self.run_sprig("add", "fern", "--every", "7")
        self.assertEqual(self.run_sprig("remove", "fern")[0], 0)
        self.assertEqual(self.run_sprig("list")[1], "")


if __name__ == "__main__":
    unittest.main()
