import os
import sys
import json
import yaml
import shutil
import tempfile
import unittest
import subprocess
from pathlib import Path

# Add REPO_ROOT to sys.path
REPO_ROOT = Path(__file__).parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.append(str(REPO_ROOT))

class TestValidateAllRuns(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        self.repo_root = self.test_dir
        (self.repo_root / "scripts" / "validators").mkdir(parents=True)
        (self.repo_root / "promotion-runs").mkdir()
        shutil.copytree(REPO_ROOT / "scripts" / "validators", self.repo_root / "scripts" / "validators", dirs_exist_ok=True)
        shutil.copy2(REPO_ROOT / "scripts" / "run_promotion_suite.py", self.repo_root / "scripts" / "run_promotion_suite.py")
        
        self.plan_yaml = self.repo_root / "promotion-plan.yaml"
        self.plan_yaml.write_text("skills: {}") # Minimal valid plan

        self.skills_json = self.repo_root / "skills.json"
        self.skills_json.write_text(json.dumps({"skills": []}))
        
        self.patch_repo_root(self.repo_root / "scripts" / "run_promotion_suite.py")

    def patch_repo_root(self, script_path):
        content = script_path.read_text(encoding="utf-8")
        patched = content.replace('REPO_ROOT = Path(__file__).parent.parent', f'REPO_ROOT = Path("{self.repo_root.as_posix()}")')
        patched = patched.replace('REPO_ROOT = Path(__file__).resolve().parent.parent', f'REPO_ROOT = Path("{self.repo_root.as_posix()}")')
        script_path.write_text(patched, encoding="utf-8")

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def create_run(self, run_id, approved=True):
        run_dir = self.repo_root / "promotion-runs" / run_id
        run_dir.mkdir()
        
        artifact_path = run_dir / "output.md"
        artifact_path.write_text("A" * 105) # At least 100 bytes
        
        manifest = {
            "workflow_id": "test-workflow",
            "run_id": run_id,
            "status": "pass",
            "steps": [
                {
                    "skill": "test-skill",
                    "status": "pass",
                    "artifact": f"promotion-runs/{run_id}/output.md"
                }
            ]
        }
        (run_dir / "MANIFEST.json").write_text(json.dumps(manifest))
        (run_dir / "CONTINUITY-AUDIT.md").write_text("# Audit")
        
        review_content = f"""# Human Workflow Review
**Decision:** {'approved' if approved else 'pending'}
**Scope:** workflow_promotion_authorized
**Run ID:** {run_id}

- [x] **Real Handoff Confirmed**
- [x] **Zero Manual Repair Confirmed**
- [x] **Final Artifact Accepted**
"""
        (run_dir / "HUMAN-WORKFLOW-REVIEW.md").write_text(review_content)
        return run_dir

    def test_validate_all_runs_passes_when_all_approved(self):
        self.create_run("2026-05-16-run-1", approved=True)
        self.create_run("2026-05-16-run-2", approved=True)
        
        res = subprocess.run([sys.executable, str(self.repo_root / "scripts" / "run_promotion_suite.py"), "--validate-all-runs"], 
                             capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, f"Validate all runs should pass. Output: {res.stdout}")

    def test_validate_all_runs_fails_when_one_pending(self):
        self.create_run("2026-05-16-run-1", approved=True)
        self.create_run("2026-05-16-run-2", approved=False)
        
        res = subprocess.run([sys.executable, str(self.repo_root / "scripts" / "run_promotion_suite.py"), "--validate-all-runs"], 
                             capture_output=True, text=True)
        self.assertNotEqual(res.returncode, 0, "Validate all runs should fail if one run is pending.")
        self.assertIn("run-2", res.stdout)

if __name__ == "__main__":
    unittest.main()
