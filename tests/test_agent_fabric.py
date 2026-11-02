import tempfile, unittest
from pathlib import Path
from mdcp_fabric.core import context_pack, inventory, MAX_WORKERS, redact_secrets, _check_base_url
class FabricTests(unittest.TestCase):
 def test_worker_ceiling(self): self.assertEqual(MAX_WORKERS,64)
 def test_skips_secrets_and_vendor(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d); (root/"main.py").write_text("print('ok')"); (root/".env").write_text("API_KEY=private")
   (root/"node_modules").mkdir(); (root/"node_modules"/"x.js").write_text("vendor")
   self.assertEqual([x["path"] for x in inventory(root)],["main.py"])
 def test_context_bounded(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d); (root/"a.py").write_text("x"*10000)
   text,manifest=context_pack(root,max_chars=500); self.assertLessEqual(len(text),500); self.assertTrue(manifest)
 def test_secret_redaction(self):
  v=redact_secrets("API_KEY=supersecret Bearer abcdefghijklmnopqrstuvwxyz")
  self.assertNotIn("supersecret",v); self.assertNotIn("abcdefghijklmnopqrstuvwxyz",v)
 def test_base_url_requires_https(self):
  _check_base_url("https://api.example.com/v1"); _check_base_url("http://localhost:11434/v1")
  for bad in ("http://api.example.com/v1","ftp://x","api.example.com"):
   with self.assertRaises(ValueError): _check_base_url(bad)
if __name__=="__main__": unittest.main()
