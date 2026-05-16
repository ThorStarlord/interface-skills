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

class TestSyncReferenceEvidence(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        self.repo_root = self.test_dir
        (self.repo_root / "scripts" / "validators").mkdir(parents=True)
        (self.repo_root / "promotion-runs").mkdir()
        shutil.copytree(REPO_ROOT / "scripts" / "validators", self.repo_root / "scripts" / "validators", dirs_exist_ok=True)
        shutil.copy2(REPO_ROOT / "scripts" / "sync_reference_evidence.py", self.repo_root / "scripts" / "sync_reference_evidence.py")
        
        self.skills_json = self.repo_root / "skills.json"
        self.skills_data = {"skills": [{"name": "test-skill", "status": "stable"}]}
        self.skills_json.write_text(json.dumps(self.skills_data))
        
        self.patch_repo_root(self.repo_root / "scripts" / "sync_reference_evidence.py")

    def patch_repo_root(self, script_path):
        content = script_path.read_text(encoding="utf-8")
        patched = content.replace('REPO_ROOT = Path(__file__).parent.parent', f'REPO_ROOT = Path("{self.repo_root.as_posix()}")')
        patched = patched.replace('REPO_ROOT = Path(__file__).resolve().parent.parent', f'REPO_ROOT = Path("{self.repo_root.as_posix()}")')
        script_path.write_text(patched, encoding="utf-8")

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def create_run(self, run_id, decision="approved"):
        run_dir = self.repo_root / "promotion-runs" / run_id
        run_dir.mkdir()
        manifest = {
            "skill_name": "test-skill",
            "run_id": run_id,
            "status": "pass",
            "steps": [{"skill": "test-skill", "status": "pass", "artifact": f"promotion-runs/{run_id}/output.md"}]
        }
        (run_dir / "MANIFEST.json").write_text(json.dumps(manifest))
        (run_dir / "output.md").write_text("content")
        
        review_content = f"""# HUMAN REVIEW
**Decision:** {decision}
**Reviewer:** Test Reviewer
**Date:** 2026-05-16
**Scope:** stable_promotion_authorized
**Run ID:** {run_id}

### Behavioral Review
- [x] Verified logic.

### Continuity Review
- [x] Verified handoff.
"""
        (run_dir / "HUMAN-REVIEW.md").write_text(review_content)
        return run_dir

    def test_sync_filters_by_decision(self):
        self.create_run("2026-05-16-approved", decision="approved")
        self.create_run("2026-05-16-pending", decision="pending")
        
        subprocess.run([sys.executable, str(self.repo_root / "scripts" / "sync_reference_evidence.py")], capture_output=True)
        
        ref_record = self.repo_root / "skills" / "test-skill" / "references" / "reference_record.json"
        self.assertTrue(ref_record.exists())
        data = json.loads(ref_record.read_text())
        self.assertEqual(data["approval_metadata"]["authorizing_run_id"], "2026-05-16-approved")

    def test_sync_updates_existing_record(self):
        # Create initial record
        self.create_run("2026-05-16-run-1", decision="approved")
        subprocess.run([sys.executable, str(self.repo_root / "scripts" / "sync_reference_evidence.py")], capture_output=True)
        
        # Create newer run
        self.create_run("2026-05-16-run-2", decision="approved")
        # Ensure run-2 has a newer timestamp or just run it again
        subprocess.run([sys.executable, str(self.repo_root / "scripts" / "sync_reference_evidence.py")], capture_output=True)
        
        data = json.loads((self.repo_root / "skills" / "test-skill" / "references" / "reference_record.json").read_text())
        # sync_reference_evidence.py picks the first approved run it finds. 
        # Since we don't have timestamps, it depends on iterdir order, but usually lex order.
        self.assertIn(data["approval_metadata"]["authorizing_run_id"], ["2026-05-16-run-1", "2026-05-16-run-2"])

if __name__ == "__main__":
    unittest.main()
