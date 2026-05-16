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

class TestCertificationAuthority(unittest.TestCase):
    """
    End-to-end lifecycle test for the Skill Certification Authority.
    Covers the 'Golden Path': run_promotion_suite -> sync_reference_evidence -> verify_certification_authority.
    """
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        self.repo_root = self.test_dir
        
        # Mock repository structure
        (self.repo_root / "scripts" / "validators").mkdir(parents=True)
        (self.repo_root / "promotion-runs").mkdir()
        (self.repo_root / "skills" / "test-skill" / "references").mkdir(parents=True)
        (self.repo_root / "skills" / "workflow-orchestrator" / "references").mkdir(parents=True)
        
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
                    "fixtures": ["examples/fixtures/test-family/test-fixture"],
                    "promotion_criteria": {"scope": "stable"},
                    "behavioral_criteria": {
                        "fixture_family": "test-family",
                        "minimum_behavioral_complexity": {"min_findings": 1},
                        "blocking_failure_modes": ["hallucination"]
                    }
                }
            }
        }
        (self.repo_root / "examples" / "fixtures" / "test-family" / "test-fixture").mkdir(parents=True)
        (self.repo_root / "examples" / "fixtures" / "test-family" / "test-fixture" / "output.md").write_text("Valid content")
        self.plan_yaml.write_text(yaml.dump(self.plan_data))

        # Create dummy workflow registry
        self.wf_registry_path = self.repo_root / "skills" / "workflow-orchestrator" / "references" / "workflow-registry.yaml"
        self.wf_data = {
            "workflows": [
                {
                    "id": "test-workflow",
                    "status": "stable",
                    "steps": [{"skill": "test-skill"}]
                }
            ]
        }
        self.wf_registry_path.write_text(yaml.dump(self.wf_data))

        # Patch REPO_ROOT in scripts
        for script in ["run_promotion_suite.py", "sync_reference_evidence.py", "enforce_promotion_lock.py", "verify_certification_authority.py"]:
            self.patch_repo_root(self.repo_root / "scripts" / script)

    def patch_repo_root(self, script_path):
        content = script_path.read_text(encoding="utf-8")
        patched = content.replace('REPO_ROOT = Path(__file__).parent.parent', f'REPO_ROOT = Path("{self.repo_root.as_posix()}")')
        patched = patched.replace('REPO_ROOT = Path(__file__).resolve().parent.parent', f'REPO_ROOT = Path("{self.repo_root.as_posix()}")')
        script_path.write_text(patched, encoding="utf-8")

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_full_certification_lifecycle(self):
        """Tests the complete path from execution to certification approval."""
        # 1. Run Promotion Suite
        # We'll mock the execution by creating a run dir manually to avoid complex subprocess mocks
        run_id = "2026-05-16-test-run"
        run_dir = self.repo_root / "promotion-runs" / run_id
        run_dir.mkdir()
        
        manifest = {
            "workflow_id": "test-workflow",
            "run_id": run_id,
            "status": "pass",
            "steps": [{"skill": "test-skill", "status": "pass", "artifact": f"promotion-runs/{run_id}/output.md"}],
            "fixture": "examples/fixtures/test-family/test-fixture"
        }
        (run_dir / "MANIFEST.json").write_text(json.dumps(manifest, indent=2))
        (run_dir / "output.md").write_text("A" * 105) # >= 100 bytes for final_artifact validator
        
        # Create approved HUMAN-WORKFLOW-REVIEW.md
        review_content = f"""# Human Workflow Review
**Decision:** approved
**Scope:** workflow_promotion_authorized
**Run ID:** {run_id}

- [x] **Real Handoff Confirmed**
- [x] **Zero Manual Repair Confirmed**
- [x] **Final Artifact Accepted**
"""
        (run_dir / "HUMAN-WORKFLOW-REVIEW.md").write_text(review_content)
        (run_dir / "CONTINUITY-AUDIT.md").write_text("# Audit")
        
        # Create SKILL.md to be certified
        skill_md = self.repo_root / "skills" / "test-skill" / "SKILL.md"
        skill_md.write_text("Gold Standard Skill Logic")

        # 2. Sync Reference Evidence
        env = os.environ.copy()
        env["SKIP_AUTHORITY_VALIDATION"] = "1"
        sync_res = subprocess.run([sys.executable, str(self.repo_root / "scripts" / "sync_reference_evidence.py")], 
                                  capture_output=True, text=True, env=env)
        self.assertEqual(sync_res.returncode, 0, f"Sync should succeed. Output: {sync_res.stdout}\n{sync_res.stderr}")
        
        # Verify reference created
        ref_record = self.repo_root / "skills" / "test-skill" / "references" / "reference_record.json"
        self.assertTrue(ref_record.exists(), "reference_record.json should have been created by sync")
        
        # 3. Verify Certification Authority
        audit_res = subprocess.run([sys.executable, str(self.repo_root / "scripts" / "verify_certification_authority.py")], 
                                   capture_output=True, text=True, env=env)
        self.assertEqual(audit_res.returncode, 0, f"Audit should pass. Output: {audit_res.stdout}\n{audit_res.stderr}")
        self.assertIn("[CERTIFIED]", audit_res.stdout)

if __name__ == "__main__":
    unittest.main()
