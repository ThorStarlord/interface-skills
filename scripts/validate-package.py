import os
import json
import sys
import argparse

def validate_package(package_path):
    issues = []
    
    # 1. Check existence of 00-index.md
    index_path = os.path.join(package_path, "00-index.md")
    if not os.path.exists(index_path):
        issues.append("- [CRITICAL] Missing `00-index.md` (Entry point)")
    
    # 2. Check existence of run-manifest.json
    manifest_path = os.path.join(package_path, "run-manifest.json")
    if not os.path.exists(manifest_path):
        issues.append("- [CRITICAL] Missing `run-manifest.json` (Run History)")
    else:
        # 3. Validate Manifest Content (Basic Schema Check)
        try:
            with open(manifest_path, 'r') as f:
                manifest = json.load(f)
            
            required = ["skill_name", "timestamp", "input_hashes", "artifact_outputs"]
            for field in required:
                if field not in manifest:
                    issues.append(f"- [ERROR] Manifest missing required field: `{field}`")
            
            # 4. Naming Conventions & Existence
            outputs = manifest.get("artifact_outputs", [])
            for artifact in outputs:
                art_path = os.path.join(package_path, artifact)
                if not os.path.exists(art_path):
                    issues.append(f"- [ERROR] Artifact `{artifact}` listed in manifest but missing on disk")
                    
        except json.JSONDecodeError:
            issues.append("- [CRITICAL] `run-manifest.json` is not valid JSON")

    # Final Report
    if not issues:
        print("# Package Validation Report: SUCCESS")
        print("Package conforms to the Canonical Package Format.")
        return 0
    else:
        print("# Package Validation Report: FAILED")
        for issue in issues:
            print(issue)
        return 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="Path to the spec package")
    args = parser.parse_args()
    
    if not os.path.isdir(args.path):
        print(f"Error: {args.path} is not a directory")
        sys.exit(2)
        
    sys.exit(validate_package(args.path))
