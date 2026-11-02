import tempfile, unittest
from pathlib import Path
from tools.mdcp_memory import remember, pack

class MemoryTests(unittest.TestCase):
    def test_dedup_and_bounded_pack(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); (root/"MDCP_CONTEXT.md").write_text("# Demo")
            a=remember(root,"API","Use versioned routes")
            b=remember(root,"API","Use versioned routes")
            self.assertEqual(a,b)
            result=pack(root,1000)
            self.assertLessEqual(len(result),1000)
            self.assertIn("Demo",result)
if __name__=="__main__": unittest.main()
