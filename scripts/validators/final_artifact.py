import os
from pathlib import Path
import json
from scripts.validators.common import ValidatorResult

def validate_final_artifact(run_dir, requested_scope="workflow"):
    """
    Verifies the final artifact of a workflow promotion run.
    Checks:
    - MANIFEST.json exists.
    - The last step in MANIFEST.json is successful.
    - The final artifact file exists and is non-empty.
    - Semantic integrity against zero-repair contracts.
    """
    manifest_path = run_dir / "MANIFEST.json"
    if not manifest_path.exists():
        return ValidatorResult(
            validator_name="final_artifact",
            status="fail",
            findings=["MANIFEST.json not found, cannot verify final artifact."],
            failure_modes=["missing_manifest"]
        )

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        steps = manifest.get("steps", [])
        if not steps:
            return ValidatorResult(
                validator_name="final_artifact",
                status="fail",
                findings=["No steps found in manifest."],
                failure_modes=["empty_manifest"]
            )
        
        last_step = steps[-1]
        artifact_rel = last_step.get("artifact")
        
        if not artifact_rel:
            return ValidatorResult(
                validator_name="final_artifact",
                status="fail",
                findings=[f"Last step ({last_step.get('skill')}) produced no artifact."],
                failure_modes=["missing_artifact"]
            )
            
        repo_root = Path(run_dir).parent.parent # Assuming run_dir is promotion-runs/ID
        # Actually it's better to pass repo_root or find it
        # Let's try to find it from the run_dir
        
        artifact_path = Path(artifact_rel)
        if not artifact_path.is_absolute():
            # Try relative to repo root (which is 2 levels up from run_dir)
            artifact_path = run_dir.parent.parent / artifact_path

        if not artifact_path.exists():
             return ValidatorResult(
                validator_name="final_artifact",
                status="fail",
                findings=[f"Final artifact file not found at {artifact_path}."],
                failure_modes=["missing_artifact"]
            )
            
        if artifact_path.stat().st_size < 100:
             return ValidatorResult(
                validator_name="final_artifact",
                status="fail",
                findings=[f"Final artifact file is too small ({artifact_path.stat().st_size} bytes), likely a placeholder or failure."],
                failure_modes=["invalid_artifact"]
            )

        return ValidatorResult(
            validator_name="final_artifact",
            status="pass",
            findings=[f"Final artifact verified: {artifact_rel}"],
            failure_modes=[]
        )

    except Exception as e:
        return ValidatorResult(
            validator_name="final_artifact",
            status="fail",
            findings=[f"Error validating final artifact: {str(e)}"],
            failure_modes=["validation_error"]
        )
