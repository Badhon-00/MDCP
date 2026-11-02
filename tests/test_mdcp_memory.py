import tempfile
import unittest
from pathlib import Path

from tools.mdcp_memory import pack, remember, search


class MemoryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "MDCP_CONTEXT.md").write_text("# Demo\nShort project brief.", encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    def test_deduplicates_identical_memory(self):
        first = remember(self.root, "API decision", "Use versioned routes.")
        second = remember(self.root, "API decision", "Use versioned routes.")
        self.assertEqual(first, second)
        self.assertEqual(len(search(self.root, "versioned")), 1)

    def test_pack_is_bounded_and_contains_context(self):
        remember(self.root, "Database", "SQLite for local project memory.")
        result = pack(self.root, max_chars=1500)
        self.assertLessEqual(len(result), 1500)
        self.assertIn("Demo", result)
        self.assertIn("Database", result)


if __name__ == "__main__":
    unittest.main()
