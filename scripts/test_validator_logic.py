import subprocess
import os
import shutil
import json

TEST_DIR = "scratch/test_package"
VALIDATOR_SCRIPT = "scripts/validate-package.py"

def setup_package(has_index=True, has_manifest=True, manifest_valid=True, missing_artifact=False):
    if os.path.exists(TEST_DIR):
        shutil.rmtree(TEST_DIR)
    os.makedirs(TEST_DIR)
    
    if has_index:
        with open(os.path.join(TEST_DIR, "00-index.md"), "w") as f:
            f.write("# Test Index")
            
    if has_manifest:
        manifest = {
            "skill_name": "test-skill",
            "timestamp": "2026-05-13T10:00:00Z",
            "input_hashes": {},
            "artifact_outputs": ["00-index.md"]
        }
        if missing_artifact:
            manifest["artifact_outputs"].append("missing.md")
            
        if not manifest_valid:
            del manifest["skill_name"] # Break the schema
            
        with open(os.path.join(TEST_DIR, "run-manifest.json"), "w") as f:
            json.dump(manifest, f)

def run_validator(path):
    result = subprocess.run(
        ["python", VALIDATOR_SCRIPT, path],
        capture_output=True,
        text=True
    )
    return result

def test_valid_package():
    print("Testing valid package...")
    setup_package()
    res = run_validator(TEST_DIR)
    assert res.returncode == 0, f"FAILED: Valid package rejected: {res.stdout}"
    print("SUCCESS: Valid package accepted.")

def test_missing_index():
    print("Testing missing index...")
    setup_package(has_index=False)
    res = run_validator(TEST_DIR)
    assert res.returncode != 0, "FAILED: Missing index not caught"
    assert "[CRITICAL] Missing `00-index.md`" in res.stdout
    print("SUCCESS: Missing index caught.")

def test_invalid_manifest():
    print("Testing invalid manifest...")
    setup_package(manifest_valid=False)
    res = run_validator(TEST_DIR)
    assert res.returncode != 0, "FAILED: Invalid manifest schema not caught"
    assert "Manifest missing required field: `skill_name`" in res.stdout
    print("SUCCESS: Invalid manifest caught.")

def test_missing_artifact():
    print("Testing missing artifact...")
    setup_package(missing_artifact=True)
    res = run_validator(TEST_DIR)
    assert res.returncode != 0, "FAILED: Missing artifact not caught"
    assert "listed in manifest but missing on disk" in res.stdout
    print("SUCCESS: Missing artifact caught.")

if __name__ == "__main__":
    try:
        test_valid_package()
        test_missing_index()
        test_invalid_manifest()
        test_missing_artifact()
        print("\nALL TESTS PASSED - GREEN PHASE COMPLETE")
    except AssertionError as e:
        print(f"\n{e}")
        exit(1)
    except Exception as e:
        print(f"\nUNEXPECTED ERROR: {e}")
        exit(1)
