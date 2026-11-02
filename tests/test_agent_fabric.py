import tempfile, unittest
from pathlib import Path
from mdcp_fabric.core import context_pack, inventory, MAX_WORKERS

class FabricTests(unittest.TestCase):
    def test_worker_ceiling(self):
        self.assertEqual(MAX_WORKERS,64)
    def test_skips_secrets_and_build_folders(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); (root/"main.py").write_text("print('ok')")
            (root/".env").write_text("SECRET=never")
            (root/"node_modules").mkdir(); (root/"node_modules"/"x.js").write_text("vendor")
            files=inventory(root)
            self.assertEqual([x["path"] for x in files],["main.py"])
    def test_context_is_bounded(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); (root/"a.py").write_text("x"*10000)
            text,manifest=context_pack(root,max_chars=500)
            self.assertLessEqual(len(text),500)
            self.assertTrue(manifest)
if __name__=="__main__": unittest.main()
