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

class TestAuthorityGates(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        self.repo_root = self.test_dir
        
        # Mock repository structure
        (self.repo_root / "scripts" / "validators").mkdir(parents=True)
        (self.repo_root / "promotion-runs").mkdir()
        (self.repo_root / "skills" / "test-skill" / "references").mkdir(parents=True)
        
        # Copy scripts and validators
        shutil.copytree(REPO_ROOT / "scripts" / "validators", self.repo_root / "scripts" / "validators", dirs_exist_ok=True)
        for script in ["run_promotion_suite.py", "sync_reference_evidence.py", "enforce_promotion_lock.py", "verify_certification_authority.py"]:
            shutil.copy2(REPO_ROOT / "scripts" / script, self.repo_root / "scripts" / script)
            
        # Create dummy skills.json
        self.skills_json = self.repo_root / "skills.json"
        self.skills_data = {
            "skills": [
                {
                    "name": "test-skill",
                    "status": "stable",
                    "canonical_output_paths": ["output.md"]
                }
            ]
        }
        self.skills_json.write_text(json.dumps(self.skills_data, indent=2))

        # Create dummy promotion-plan.yaml
        self.plan_yaml = self.repo_root / "promotion-plan.yaml"
        self.plan_data = {
            "skills": {
                "test-skill": {
                    "fixtures": [],
                    "promotion_criteria": {"scope": "stable"},
                    "behavioral_criteria": {
                        "fixture_family": "test-family",
                        "minimum_behavioral_complexity": {"min_findings": 1},
                        "blocking_failure_modes": ["hallucination"]
                    }
                }
            }
        }
        (self.repo_root / "test-family").mkdir()
        self.plan_yaml.write_text(yaml.dump(self.plan_data))

        # Patch REPO_ROOT in scripts
        self.patch_repo_root(self.repo_root / "scripts" / "run_promotion_suite.py")
        self.patch_repo_root(self.repo_root / "scripts" / "sync_reference_evidence.py")
        self.patch_repo_root(self.repo_root / "scripts" / "enforce_promotion_lock.py")
        self.patch_repo_root(self.repo_root / "scripts" / "verify_certification_authority.py")

    def patch_repo_root(self, script_path):
        content = script_path.read_text(encoding="utf-8")
        # Replace the logic that finds REPO_ROOT with our temp dir
        patched = content.replace('REPO_ROOT = Path(__file__).parent.parent', f'REPO_ROOT = Path("{self.repo_root.as_posix()}")')
        patched = patched.replace('REPO_ROOT = Path(__file__).resolve().parent.parent', f'REPO_ROOT = Path("{self.repo_root.as_posix()}")')
        script_path.write_text(patched, encoding="utf-8")

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def create_workflow_run(self, run_id, decision="approved", scope="workflow_promotion_authorized"):
        run_dir = self.repo_root / "promotion-runs" / run_id
        run_dir.mkdir()
        
        # Create MANIFEST.json
        manifest = {
            "workflow_id": "test-workflow",
            "run_id": run_id,
            "timestamp": "2026-05-16",
            "status": "pass",
            "steps": [
                {
                    "skill": "test-skill",
                    "status": "pass",
                    "artifact": "promotion-runs/" + run_id + "/output.md"
                }
            ]
        }
        (run_dir / "MANIFEST.json").write_text(json.dumps(manifest, indent=2))
        (run_dir / "output.md").write_text("Test output content " * 100)
        (run_dir / "CONTINUITY-AUDIT.md").write_text("# Continuity Audit")
        
        # Create HUMAN-WORKFLOW-REVIEW.md
        review_content = f"""# Human Workflow Review
**Decision:** {decision}
**Scope:** {scope}
**Run ID:** {run_id}

- [x] **Real Handoff Confirmed**
- [x] **Zero Manual Repair Confirmed**
- [x] **Final Artifact Accepted**
"""
        (run_dir / "HUMAN-WORKFLOW-REVIEW.md").write_text(review_content)
        return run_dir

    def test_workflow_validation_passes_on_approved(self):
        run_id = "2026-05-16-workflow-test"
        run_dir = self.create_workflow_run(run_id, decision="approved")
        
        import subprocess
        res = subprocess.run([sys.executable, str(self.repo_root / "scripts" / "run_promotion_suite.py"), "--validate", str(run_dir)], 
                             capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, f"Validation should pass for approved review. Output: {res.stdout}\n{res.stderr}")

    def test_workflow_validation_fails_on_pending(self):
        run_id = "2026-05-16-workflow-pending"
        run_dir = self.create_workflow_run(run_id, decision="pending")
        
        import subprocess
        res = subprocess.run([sys.executable, str(self.repo_root / "scripts" / "run_promotion_suite.py"), "--validate", str(run_dir)], 
                             capture_output=True, text=True)
        self.assertNotEqual(res.returncode, 0, "Validation should fail for pending review.")

    def test_workflow_validation_fails_on_wrong_scope(self):
        run_id = "2026-05-16-workflow-wrong-scope"
        # Create a review with 'stable' scope instead of 'workflow'
        run_dir = self.create_workflow_run(run_id, decision="approved", scope="stable_promotion_authorized")
        
        import subprocess
        res = subprocess.run([sys.executable, str(self.repo_root / "scripts" / "run_promotion_suite.py"), "--validate", str(run_dir)], 
                             capture_output=True, text=True)
        self.assertNotEqual(res.returncode, 0, "Validation should fail for scope mismatch.")
        self.assertIn("Scope mismatch", res.stdout)

    def test_workflow_sync_works_on_approved(self):
        run_id = "2026-05-16-workflow-sync"
        run_dir = self.create_workflow_run(run_id, decision="approved")
        
        import subprocess
        res = subprocess.run([sys.executable, str(self.repo_root / "scripts" / "sync_reference_evidence.py")], 
                             capture_output=True, text=True)
        
        ref_record = self.repo_root / "skills" / "test-skill" / "references" / "reference_record.json"
        self.assertTrue(ref_record.exists(), "Reference record should be created after sync.")
        
        data = json.loads(ref_record.read_text())
        self.assertEqual(data["approval_metadata"]["authorizing_run_id"], run_id)

    def test_workflow_sync_skips_unapproved(self):
        run_id = "2026-05-16-workflow-skip"
        run_dir = self.create_workflow_run(run_id, decision="pending")
        
        import subprocess
        subprocess.run([sys.executable, str(self.repo_root / "scripts" / "sync_reference_evidence.py")], capture_output=True, text=True)
        
        ref_record = self.repo_root / "skills" / "test-skill" / "references" / "reference_record.json"
        self.assertFalse(ref_record.exists(), "Reference record should NOT be created for pending run.")

    def test_promotion_lock_blocks_on_drift(self):
        # 1. Create a certified state
        run_id = "2026-05-16-lock-test"
        run_dir = self.create_workflow_run(run_id, decision="approved")
        
        # Create SKILL.md
        skill_md = self.repo_root / "skills" / "test-skill" / "SKILL.md"
        skill_md.parent.mkdir(parents=True, exist_ok=True)
        skill_md.write_text("Original Skill Content")
        
        # Sync to create reference
        import subprocess
        subprocess.run([sys.executable, str(self.repo_root / "scripts" / "sync_reference_evidence.py")], capture_output=True, text=True)
        
        # Verify lock passes initially
        res = subprocess.run([sys.executable, str(self.repo_root / "scripts" / "enforce_promotion_lock.py")], capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, "Lock should pass initially.")
        
        # 2. Modify SKILL.md (Drift)
        skill_md.write_text("Modified Skill Content")
        
        # Verify lock fails
        res = subprocess.run([sys.executable, str(self.repo_root / "scripts" / "enforce_promotion_lock.py")], capture_output=True, text=True)
        self.assertNotEqual(res.returncode, 0, "Lock should fail after drift.")
        self.assertIn("REGISTRY PROMOTION LOCK ACTIVE", res.stdout)

    def test_full_authority_audit_path(self):
        # 1. Create an approved run
        run_id = "2026-05-16-audit-pass"
        self.create_workflow_run(run_id, decision="approved")
        
        # 2. Sync to references
        import subprocess
        subprocess.run([sys.executable, str(self.repo_root / "scripts" / "sync_reference_evidence.py")], capture_output=True, text=True)
        
        # 3. Create SKILL.md to match reference (synchronized during sync)
        skill_md = self.repo_root / "skills" / "test-skill" / "SKILL.md"
        skill_md.parent.mkdir(parents=True, exist_ok=True)
        skill_md.write_text("Original Skill Content") # Match what we "synced"
        
        # We need to ensure the sync actually used the current SKILL.md hash.
        # In our setUp, we didn't have SKILL.md before sync.
        # Let's recreate the flow properly.
        shutil.rmtree(self.repo_root / "skills" / "test-skill" / "references")
        (self.repo_root / "skills" / "test-skill" / "references").mkdir()
        skill_md.write_text("Gold Standard Content")
        subprocess.run([sys.executable, str(self.repo_root / "scripts" / "sync_reference_evidence.py")], capture_output=True, text=True)
        
        # 4. Run Certification Audit
        res = subprocess.run([sys.executable, str(self.repo_root / "scripts" / "verify_certification_authority.py")], capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, f"Audit should pass for fully certified repo. Output: {res.stdout}")
        self.assertIn("[CERTIFIED]", res.stdout)

    def test_authority_audit_fails_on_missing_reference(self):
        # Stable skill but no references
        res = subprocess.run([sys.executable, str(self.repo_root / "scripts" / "verify_certification_authority.py")], capture_output=True, text=True)
        self.assertNotEqual(res.returncode, 0, "Audit should fail if stable skill missing references.")
        self.assertIn("[FAIL]", res.stdout)
        self.assertIn("Missing reference_record.json", res.stdout)

if __name__ == "__main__":
    unittest.main()
