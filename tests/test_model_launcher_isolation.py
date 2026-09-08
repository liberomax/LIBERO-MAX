import unittest
from pathlib import Path


ROOT = Path(__file__).parents[1]


class ModelLauncherIsolationTest(unittest.TestCase):


    def test_openpi_server_prefers_its_own_venv(self):
        source = (ROOT / "scripts" / "run_openpi_persistent_benchmark.sh").read_text(
            encoding="utf-8"
        )
        self.assertIn("OPENPI_FALLBACK_PYTHON", source)
        self.assertIn("openpi_runtime_ready", source)
        self.assertIn('"python": sys.executable', source)
        self.assertIn('mujoco.__version__ != "3.2.6"', source)
        self.assertIn('hasattr(mujoco.MjModel, "mesh_scale")', source)
        self.assertIn('"simulator_client": json.loads(sys.argv[7])', source)
        self.assertIn("OPENPI_SITE_PACKAGES", source)
        self.assertIn("OPENPI_SERVER_PYTHONPATH", source)
        self.assertIn('PYTHONPATH="$OPENPI_SERVER_PYTHONPATH"', source)
        declaration = source.index('OPENPI_SERVER_PYTHONPATH="')
        self.assertNotIn(
            "${PYTHONPATH:+:$PYTHONPATH}",
            source[declaration : source.index("CLIENT_PYTHON=", declaration)],
        )
        self.assertIn("os.kill(server_pid, 0)", source)
        self.assertIn("exited before port", source)


if __name__ == "__main__":
    unittest.main()
