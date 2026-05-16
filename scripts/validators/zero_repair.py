import os
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

def validate_zero_repair(fixture_path, artifact_path, run_manifest=None, requested_scope="stable"):
    """
    Verifies that the artifact has not been manually repaired.
    Mechanical proof:
    1. If a .zero-repair-hashes.json exists in the fixture, verify the hash.
    2. Missing hashes or markers results in failure for stable/workflow promotion.
    """
    findings = []
    failure_modes = []
    
    # 1. Hash Verification
    hash_manifest_path = fixture_path / ".zero-repair-hashes.json"
    if hash_manifest_path.exists():
        import json
        try:
            hashes = json.loads(hash_manifest_path.read_text(encoding="utf-8"))
            # Try both relative to fixture and relative to run_dir if possible
            # For simplicity, we check if artifact_path ends with any key in hashes
            rel_path = None
            try:
                rel_path = str(artifact_path.relative_to(fixture_path))
            except ValueError:
                # Artifact might be outside fixture (e.g. in run directory)
                # Check for filename match
                rel_path = artifact_path.name
            
            expected_hash = hashes.get(rel_path)
            
            if expected_hash:
                actual_hash = get_file_hash(artifact_path)
                if actual_hash != expected_hash:
                    findings.append(f"Hash Mismatch: Artifact '{rel_path}' has been modified since generation.")
                    failure_modes.append("manual_repair_detected")
                else:
                    findings.append(f"Hash Verified: Artifact '{rel_path}' matches generation-time snapshot.")
            else:
                findings.append(f"Hash Missing: No recorded hash for '{rel_path}' in .zero-repair-hashes.json.")
                failure_modes.append("missing_hash_proof")
        except Exception as e:
            findings.append(f"Error reading hash manifest: {str(e)}")
            failure_modes.append("manifest_error")
    else:
        # Fallback: Check for a simple .zero-repair marker file (ADR 0008 Hardening)
        marker_path = fixture_path / ".zero-repair"
        if marker_path.exists():
            if requested_scope in ["stable", "workflow"]:
                findings.append("Soft Proof Violation: Marker-based proof (.zero-repair) is insufficient for stable/workflow promotion. Hash proof required.")
                failure_modes.append("insufficient_proof_type")
            else:
                findings.append("Zero-repair marker found (soft verification - allowed for draft scope).")
        else:
            findings.append("No zero-repair proof found (.zero-repair-hashes.json missing).")
            failure_modes.append("missing_zero_repair_proof")


    status = "fail" if failure_modes else "pass"
    
    if not findings and not failure_modes:
        status = "fail"
        findings.append("No zero-repair constraints defined for this fixture.")
        failure_modes.append("missing_zero_repair_proof")

    return ValidatorResult(
        validator_name="zero_repair",
        status=status,
        findings=findings,
        failure_modes=failure_modes
    )
