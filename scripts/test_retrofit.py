import os
import sys
import subprocess
import json

SKILL_PATH = "skills/ui-brief/SKILL.md"
VALIDATOR_SCRIPT = "scripts/validate-package.py"
TEST_PKG = "scratch/brief_retrofit_test"

def test_skill_instructions_mention_manifest():
    print("Checking if SKILL.md mentions 'Run Manifest'...")
    with open(SKILL_PATH, 'r', encoding='utf-8') as f:
        content = f.read()
    assert "Run Manifest" in content, "FAILED: SKILL.md does not mention 'Run Manifest'"
    print("SUCCESS: SKILL.md contains Run Manifest instructions.")

def test_validation_of_legacy_output():
    print("Verifying that legacy output (missing manifest) fails validation...")
    if os.path.exists(TEST_PKG):
        import shutil
        shutil.rmtree(TEST_PKG)
    os.makedirs(TEST_PKG)
    
    with open(os.path.join(TEST_PKG, "00-index.md"), "w") as f: f.write("# Index")
    with open(os.path.join(TEST_PKG, "brief.md"), "w") as f: f.write("# Brief")
    
    result = subprocess.run(["python", VALIDATOR_SCRIPT, TEST_PKG], capture_output=True, text=True)
    assert result.returncode != 0, "FAILED: Validator should reject package missing a manifest"
    print("SUCCESS: Legacy output correctly rejected.")

def test_validation_of_modern_output():
    print("Verifying that modern output (with manifest) passes validation...")
    if os.path.exists(TEST_PKG):
        import shutil
        shutil.rmtree(TEST_PKG)
    os.makedirs(TEST_PKG)
    
    with open(os.path.join(TEST_PKG, "00-index.md"), "w") as f: f.write("# Index")
    with open(os.path.join(TEST_PKG, "brief.md"), "w") as f: f.write("# Brief")
    
    manifest = {
        "skill_name": "ui-brief",
        "timestamp": "2026-05-13T10:00:00Z",
        "input_hashes": {},
        "artifact_outputs": ["00-index.md", "brief.md"]
    }
    with open(os.path.join(TEST_PKG, "run-manifest.json"), "w") as f:
        json.dump(manifest, f)
    
    result = subprocess.run(["python", VALIDATOR_SCRIPT, TEST_PKG], capture_output=True, text=True)
    assert result.returncode == 0, f"FAILED: Modern output rejected: {result.stdout}"
    print("SUCCESS: Modern output correctly accepted.")

if __name__ == "__main__":
    try:
        test_skill_instructions_mention_manifest()
        test_validation_of_legacy_output()
        test_validation_of_modern_output()
        print("\nALL TESTS PASSED - GREEN PHASE COMPLETE")
    except AssertionError as e:
        print(f"\n{e}")
        sys.exit(1)
