import io
import tempfile
import time
import unittest
import urllib.error
from pathlib import Path
from unittest.mock import patch

from mdcp_runtime.providers import Provider, ProviderRouter
from mdcp_runtime.tasks import TaskRunner, TaskStore
from mdcp_runtime.skills import discover_skills, skill_context


class FakeRouter:
    def complete(self, messages):
        return {"provider": "fake", "model": "fake-model", "content": "completed: " + messages[-1]["content"][:20], "failures": []}


class FakeResponse:
    def __enter__(self): return self
    def __exit__(self, *args): return False
    def read(self): return b'{"choices":[{"message":{"content":"fallback worked"}}]}'


class RuntimeTests(unittest.TestCase):
    def test_task_persists_and_completes(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = TaskStore(Path(tmp) / "tasks.sqlite3")
            runner = TaskRunner(store, FakeRouter(), poll_seconds=0.01)
            task_id = runner.submit("Build a small feature")
            deadline = time.time() + 2
            while time.time() < deadline:
                result = runner.status(task_id)
                if result["status"] == "completed": break
                time.sleep(0.01)
            runner.close()
            self.assertEqual(result["status"], "completed")
            self.assertEqual(result["provider"], "fake")
            self.assertIn("completed", result["result"])

    def test_task_input_is_bounded_and_secrets_redacted(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = TaskStore(Path(tmp) / "tasks.sqlite3")
            with self.assertRaises(ValueError): store.create("x" * 12001)
            task_id = store.create("use API_KEY=supersecret")
            self.assertNotIn("supersecret", store.get(task_id)["task"])

    def test_resume_only_failed_or_cancelled(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = TaskStore(Path(tmp) / "tasks.sqlite3")
            task_id = store.create("task")
            self.assertFalse(store.resume(task_id))
            self.assertIsNotNone(store.claim(task_id))
            store.fail(task_id, "test error")
            self.assertTrue(store.resume(task_id))

    def test_running_tasks_recover_after_restart(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "tasks.sqlite3"
            store = TaskStore(path)
            task_id = store.create("task")
            store.claim(task_id)
            recovered = TaskStore(path)
            self.assertEqual(recovered.get(task_id)["status"], "queued")
            self.assertIn(task_id, recovered.queued())

    def test_cancel_queued_task(self):
        with tempfile.TemporaryDirectory() as tmp:
            store = TaskStore(Path(tmp) / "tasks.sqlite3")
            task_id = store.create("task")
            self.assertTrue(store.cancel(task_id))
            self.assertEqual(store.get(task_id)["status"], "cancelled")

    def test_skill_search_and_context(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skill = root / "skills" / "python-testing"
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text('---\nname: python-testing\ndescription: Write reliable Python unit tests\n---\n# Tests\nUse unittest and assert behavior.\n', encoding="utf-8")
            rows = discover_skills(root, "python test")
            self.assertEqual(rows[0]["name"], "python-testing")
            self.assertIn("Use unittest", skill_context(root, "python test"))

    def test_provider_requires_https_config(self):
        with patch.dict("os.environ", {"MDCP_PROVIDERS": '[{"name":"x","base_url":"http://example.com/v1","model":"m","api_key_env":"X_KEY"}]'}):
            from mdcp_runtime.providers import configured_providers
            with self.assertRaises(ValueError): configured_providers()

    def test_provider_fallbacks_to_next_configured_key(self):
        providers = [Provider("first", "https://first.example/v1", "m1", "FIRST_KEY"), Provider("second", "https://second.example/v1", "m2", "SECOND_KEY")]
        calls = []
        def opener(request, timeout):
            calls.append(request.full_url)
            if "first.example" in request.full_url:
                raise urllib.error.HTTPError(request.full_url, 429, "rate limited", {"Retry-After": "2"}, io.BytesIO(b""))
            return FakeResponse()
        with patch.dict("os.environ", {"FIRST_KEY": "one", "SECOND_KEY": "two"}):
            router = ProviderRouter(providers, opener=opener)
            result = router.complete([{"role": "user", "content": "hello"}])
        self.assertEqual(result["provider"], "second")
        self.assertEqual(result["content"], "fallback worked")
        self.assertEqual(len(result["failures"]), 1)
        self.assertEqual(len(calls), 2)


if __name__ == "__main__": unittest.main()
