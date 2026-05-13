import json
import os
import sys

SCHEMA_PATH = "shared/references/run-manifest.schema.json"

def test_schema_exists():
    print(f"Checking if {SCHEMA_PATH} exists...")
    assert os.path.exists(SCHEMA_PATH), f"FAILED: {SCHEMA_PATH} does not exist"
    print("SUCCESS: Schema file found.")

def test_required_fields():
    with open(SCHEMA_PATH, 'r') as f:
        schema = json.load(f)
    
    required = schema.get("required", [])
    expected = ["skill_name", "timestamp", "input_hashes", "artifact_outputs"]
    
    for field in expected:
        assert field in required, f"FAILED: Schema missing required field: {field}"
    print(f"SUCCESS: Schema contains all required fields: {expected}")

if __name__ == "__main__":
    try:
        test_schema_exists()
        test_required_fields()
        print("\nALL TESTS PASSED")
    except AssertionError as e:
        print(f"\n{e}")
        sys.exit(1)
    except Exception as e:
        print(f"\nUNEXPECTED ERROR: {e}")
        sys.exit(1)
