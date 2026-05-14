import subprocess
import sys
import os

def run_command(command):
    print(f"Running: {' '.join(command)}")
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[FAIL] {result.stderr}")
        return False
    print(f"[PASS] {result.stdout.strip().splitlines()[-1] if result.stdout.strip() else 'Success'}")
    return True

def main():
    stable_skills = ["ui-spec-linter", "ui-orchestrator", "ui-surface-inventory"]
    all_passed = True

    print("=== Stable Skill Regression Guard ===\n")

    for skill in stable_skills:
        print(f"Checking {skill}...")
        
        # 1. Structural validation
        if not run_command(["python", "scripts/validate-skill.py", "--skill", skill]):
            all_passed = False
            
        # 2. Promotion suite pass (validation mode)
        if not run_command(["python", "scripts/run-promotion-suite.py", "--skill", skill]):
            all_passed = False
        
        print("-" * 40)

    if all_passed:
        print("\n[SUCCESS] All stable skills passed regression.")
        sys.exit(0)
    else:
        print("\n[FAIL] Some stable skills failed regression.")
        sys.exit(1)

if __name__ == "__main__":
    main()
