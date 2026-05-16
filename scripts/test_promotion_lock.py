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

class TestPromotionLock(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        self.repo_root = self.test_dir
        (self.repo_root / "scripts" / "validators").mkdir(parents=True)
        shutil.copytree(REPO_ROOT / "scripts" / "validators", self.repo_root / "scripts" / "validators", dirs_exist_ok=True)
        shutil.copy2(REPO_ROOT / "scripts" / "enforce_promotion_lock.py", self.repo_root / "scripts" / "enforce_promotion_lock.py")
        
        self.skills_json = self.repo_root / "skills.json"
        self.skills_data = {"skills": [{"name": "test-skill", "status": "stable"}]}
        self.skills_json.write_text(json.dumps(self.skills_data))
        
        self.patch_repo_root(self.repo_root / "scripts" / "enforce_promotion_lock.py")

    def patch_repo_root(self, script_path):
        content = script_path.read_text(encoding="utf-8")
        patched = content.replace('REPO_ROOT = Path(__file__).parent.parent', f'REPO_ROOT = Path("{self.repo_root.as_posix()}")')
        patched = patched.replace('REPO_ROOT = Path(__file__).resolve().parent.parent', f'REPO_ROOT = Path("{self.repo_root.as_posix()}")')
        script_path.write_text(patched, encoding="utf-8")

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def create_reference(self, content_hash):
        ref_dir = self.repo_root / "skills" / "test-skill" / "references"
        ref_dir.mkdir(parents=True, exist_ok=True)
        record = {
            "metadata": {
                "skill_hash": content_hash
            }
        }
        (ref_dir / "reference_record.json").write_text(json.dumps(record))

    def test_lock_passes_when_hashes_match(self):
        skill_md = self.repo_root / "skills" / "test-skill" / "SKILL.md"
        skill_md.parent.mkdir(parents=True, exist_ok=True)
        skill_md.write_text("Gold standard logic")
        
        # Calculate SHA256 of the content to match enforce_promotion_lock.py logic
        import hashlib
        h = hashlib.sha256()
        h.update("Gold standard logic".encode("utf-8"))
        self.create_reference(h.hexdigest())
        
        res = subprocess.run([sys.executable, str(self.repo_root / "scripts" / "enforce_promotion_lock.py")], capture_output=True, text=True)
        self.assertEqual(res.returncode, 0, f"Lock should pass when hashes match. Output: {res.stdout}\n{res.stderr}")

    def test_lock_blocks_when_hashes_drift(self):
        skill_md = self.repo_root / "skills" / "test-skill" / "SKILL.md"
        skill_md.parent.mkdir(parents=True, exist_ok=True)
        skill_md.write_text("Drifted logic")
        
        self.create_reference("some-old-hash")
        
        res = subprocess.run([sys.executable, str(self.repo_root / "scripts" / "enforce_promotion_lock.py")], capture_output=True, text=True)
        self.assertNotEqual(res.returncode, 0, "Lock should block when hashes drift.")
        self.assertIn("REGISTRY PROMOTION LOCK ACTIVE", res.stdout)

if __name__ == "__main__":
    unittest.main()
