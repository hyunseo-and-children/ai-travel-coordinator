import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ProjectContractTest(unittest.TestCase):
    def test_notion_base_files_exist(self):
        required_files = [
            "requirements.txt",
            "app/__init__.py",
            "app/main.py",
            "app/settings.py",
            "app/agent.py",
            "app/tools.py",
            "app/auth.py",
            "app/logging_config.py",
            "app/schemas.py",
        ]

        missing = [path for path in required_files if not (ROOT / path).is_file()]

        self.assertEqual(missing, [])

    def test_travel_agent_skeleton_files_exist(self):
        required_files = [
            "app/agents/__init__.py",
            "app/agents/accommodation.py",
            "app/agents/food_itinerary.py",
            "app/agents/route.py",
            "app/agents/final_schedule.py",
        ]

        missing = [path for path in required_files if not (ROOT / path).is_file()]

        self.assertEqual(missing, [])

    def test_agent_files_are_comment_only(self):
        agent_files = [
            ROOT / "app" / "agent.py",
            ROOT / "app" / "agents" / "accommodation.py",
            ROOT / "app" / "agents" / "food_itinerary.py",
            ROOT / "app" / "agents" / "route.py",
            ROOT / "app" / "agents" / "final_schedule.py",
        ]

        non_comment_lines = []
        for path in agent_files:
            with self.subTest(path=path):
                self.assertTrue(path.is_file(), f"missing {path.relative_to(ROOT)}")
            if not path.is_file():
                continue
            for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                stripped = line.strip()
                if stripped and not stripped.startswith("#"):
                    non_comment_lines.append(f"{path.relative_to(ROOT)}:{line_number}:{line}")

        self.assertEqual(non_comment_lines, [])

    def test_main_exposes_expected_operational_endpoints(self):
        main_path = ROOT / "app" / "main.py"
        self.assertTrue(main_path.is_file(), "missing app/main.py")
        if not main_path.is_file():
            return
        main_py = main_path.read_text(encoding="utf-8")

        for expected in ['"/healthz"', '"/chat"', '"/chat/stream"']:
            self.assertIn(expected, main_py)

        self.assertIn("require_api_key", main_py)
        self.assertIn("setup_logging", main_py)


if __name__ == "__main__":
    unittest.main()
