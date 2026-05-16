import os
import json
import hashlib
from pathlib import Path
from scripts.validators.common import ValidatorResult

def get_file_hash(file_path):
    """Calculates the SHA-256 hash of a file."""
    if not file_path.exists():
        return None
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def validate_reference_integrity(skill_path):
    """
    Verifies that the reference artifacts for a skill match the reference_record.json.
    Detects 'Dirty References' (manual edits to Gold Standard evidence).
    """
    findings = []
    failure_modes = []
    
    ref_dir = Path(skill_path) / "references"
    record_path = ref_dir / "reference_record.json"
    
    if not record_path.exists():
        return ValidatorResult(
            status="pass",
            validator_name="reference_integrity",
            findings=["No reference record found. skipping integrity check."]
        )

    try:
        record = json.loads(record_path.read_text(encoding="utf-8"))
        for artifact_name, meta in record.items():
            artifact_path = ref_dir / artifact_name
            expected_hash = meta.get("sha256")
            
            if not artifact_path.exists():
                findings.append(f"Missing Reference: '{artifact_name}' defined in record but missing on disk.")
                failure_modes.append("missing_reference_file")
                continue
                
            if expected_hash:
                actual_hash = get_file_hash(artifact_path)
                if actual_hash != expected_hash:
                    findings.append(f"Dirty Reference Detected: '{artifact_name}' hash mismatch. Manual edit suspected.")
                    failure_modes.append("dirty_reference")
                else:
                    findings.append(f"Reference OK: '{artifact_name}' integrity verified.")
            else:
                findings.append(f"Reference WARNING: '{artifact_name}' has no hash in record.")
                
    except Exception as e:
        return ValidatorResult(
            status="error",
            validator_name="reference_integrity",
            findings=[f"Error parsing reference record: {str(e)}"]
        )

    status = "fail" if any("Dirty" in f or "Missing" in f for f in findings) else "pass"
    return ValidatorResult(
        status=status,
        validator_name="reference_integrity",
        findings=findings,
        failure_modes=failure_modes
    )

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        res = validate_reference_integrity(sys.argv[1])
        print(json.dumps(res.__dict__, indent=2))
