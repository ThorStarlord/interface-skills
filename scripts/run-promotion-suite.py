#!/usr/bin/env python3
"""
scripts/run-promotion-suite.py

The Skill Promotion Harness runner.
Automates the execution of skills against fixtures, validates outputs,
checks against rubrics, and collects evidence for promotion.

Usage:
  python scripts/run-promotion-suite.py --skill ui-spec-linter
  python scripts/run-promotion-suite.py --all
"""

import argparse
import os
import sys
import yaml
import json
import time
import shutil
from pathlib import Path
import re
import subprocess

REPO_ROOT = Path(__file__).parent.parent
PROMOTION_RUNS_DIR = REPO_ROOT / "promotion-runs"
PLAN_FILE = REPO_ROOT / "promotion-plan.yaml"

def parse_rubric(rubric_path):
    """
    Parses a markdown rubric with checkboxes.
    Returns a list of dicts: {text: str, passed: bool, section: str}
    """
    if not rubric_path.exists():
        return []
    
    rubric_text = rubric_path.read_text(encoding="utf-8")
    items = []
    current_section = "General"
    
    for line in rubric_text.splitlines():
        if line.startswith("## "):
            current_section = line[3:].strip()
        
        match = re.search(r"^\s*-\s*\[([ xX])\]\s*(.*)", line)
        if match:
            state = match.group(1).strip().lower() == "x"
            text = match.group(2).strip()
            items.append({
                "text": text,
                "expected": state, # Actually, rubrics usually list what SHOULD pass
                "section": current_section
            })
    return items

def run_validator(script_name, target_path):
    """Runs a validator script and returns (passed, output)."""
    script_path = REPO_ROOT / "scripts" / script_name
    if not script_path.exists():
        return False, f"Validator {script_name} not found"
    
    try:
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        result = subprocess.run(
            [sys.executable, str(script_path), str(target_path)],
            capture_output=True,
            text=True,
            encoding='utf-8',
            check=False,
            env=env
        )
        return result.returncode == 0, result.stdout + result.stderr
    except Exception as e:
        return False, str(e)

def evaluate_output_against_rubric(output_content, rubric_items):
    """
    Very simple heuristic: check if the rubric text exists or is satisfied in the output.
    In a real scenario, this might need more sophisticated NLP or LLM evaluation.
    For this harness, we look for 'pass' markers or keyword presence.
    """
    results = []
    for item in rubric_items:
        # Heuristic: if the rubric item text is in the output, or if it's a structural check
        # that we can verify.
        # For now, we'll mark them as 'manual_review_required' if we can't automate.
        found = False
        if item["text"].lower() in output_content.lower():
            found = True
        
        results.append({
            "item": item["text"],
            "section": item["section"],
            "passed": found,
            "automation": "keyword_match" if found else "pending_manual"
        })
    return results

def run_promotion_for_skill(skill_name, plan, dry_run=False):
    skill_config = plan.get("skills", {}).get(skill_name)
    if not skill_config:
        print(f"Error: Skill {skill_name} not found in promotion-plan.yaml")
        return False

    print(f"\n>>> Running Promotion Suite for: {skill_name}")
    
    timestamp = time.strftime("%Y-%m-%d-%H-%M-%S")
    run_id = f"{timestamp}-{skill_name}"
    run_dir = PROMOTION_RUNS_DIR / run_id
    
    if not dry_run:
        run_dir.mkdir(parents=True, exist_ok=True)

    fixtures = skill_config.get("fixtures", [])
    messy_fixture = skill_config.get("messy_fixture")
    if messy_fixture:
        fixtures.append(messy_fixture)

    all_results = []

    for fixture_rel_path in fixtures:
        fixture_path = REPO_ROOT / fixture_rel_path
        fixture_name = fixture_path.name
        print(f"  - Testing fixture: {fixture_name}")
        
        fixture_run_dir = run_dir / fixture_name
        if not dry_run:
            fixture_run_dir.mkdir(exist_ok=True)
        
        # 1. Setup Environment
        # (In a real runner, we might copy the fixture to a temp worktree of the target repo)
        
        # 2. Execution Task
        # Since we are an AI repo, the "execution" is the output of the skill.
        # If the output already exists in the fixture (as an expected result), we validate it.
        # If not, the harness should ideally "call" the skill.
        
        # Look for existing output in the fixture to validate
        output_file = None
        # Heuristic for output file name based on skill
        if skill_name == "ui-spec-linter":
            output_file = fixture_path / "reports" / "SPEC-LINT-REPORT.md"
            if not output_file.exists():
                output_file = fixture_path / "spec-linter-report.md" # Fallback for some fixtures

        if not output_file or not output_file.exists():
            print(f"    [WARN] No output file found for {skill_name} in {fixture_name}. Skipping rubric check.")
            output_content = ""
        else:
            output_content = output_file.read_text(encoding="utf-8")

        # 3. Structural Validation
        skill_valid, skill_log = run_validator("validate-skill.py", REPO_ROOT / "skills" / skill_name)
        
        # If the output is a spec package (or part of one), validate it
        pkg_valid = True
        pkg_log = "N/A"
        if output_file and output_file.exists():
            pkg_valid, pkg_log = run_validator("validate-spec-package.py", fixture_path)

        # 4. Rubric Evaluation
        rubric_path = fixture_path / "expected" / "rubric.md"
        rubric_results = []
        if rubric_path.exists():
            rubric_items = parse_rubric(rubric_path)
            # Filter rubric items for this specific skill
            skill_rubric_items = [item for item in rubric_items if item["section"].lower() in (skill_name.lower(), "general")]
            if skill_rubric_items:
                rubric_results = evaluate_output_against_rubric(output_content, skill_rubric_items)
            else:
                 print(f"    [INFO] No rubric section found for {skill_name} in {fixture_name}")
        else:
            print(f"    [INFO] No rubric.md found for {fixture_name}")

        # 5. Record Result
        fixture_result = {
            "fixture": fixture_name,
            "skill_structural_valid": skill_valid,
            "package_structural_valid": pkg_valid,
            "rubric_passed": all(r["passed"] for r in rubric_results) if rubric_results else "N/A",
            "rubric_details": rubric_results,
            "logs": {
                "skill_validation": skill_log,
                "package_validation": pkg_log
            }
        }
        all_results.append(fixture_result)
        
        if not dry_run:
            with open(fixture_run_dir / "result.json", "w", encoding="utf-8") as f:
                json.dump(fixture_result, f, indent=2)
            
            # Write human-readable review
            with open(fixture_run_dir / "review.md", "w", encoding="utf-8") as f:
                f.write(f"# Review: {skill_name} on {fixture_name}\n\n")
                f.write(f"- **Skill Valid:** {'✅' if skill_valid else '❌'}\n")
                f.write(f"- **Package Valid:** {'✅' if pkg_valid else '❌'}\n")
                f.write(f"- **Rubric Pass:** {fixture_result['rubric_passed']}\n\n")
                f.write("## Rubric Details\n\n")
                if rubric_results:
                    for r in rubric_results:
                        f.write(f"- [{'x' if r['passed'] else ' '}] {r['item']} ({r['automation']})\n")
                else:
                    f.write("No rubric items found.\n")

    # 6. Generate Improvement Brief if needed
    total_failures = sum(1 for r in all_results if not r["skill_structural_valid"] or not r["package_structural_valid"] or r["rubric_passed"] is False)
    
    if total_failures > 0 and not dry_run:
        brief_path = run_dir / "improvement-brief.md"
        with open(brief_path, "w", encoding="utf-8") as f:
            f.write(f"# Skill Improvement Brief: {skill_name}\n\n")
            f.write(f"Detected {total_failures} failures across fixtures.\n\n")
            f.write("## Recommended Edits\n\n")
            f.write("- [ ] Check why rubric items failed (see review.md in each fixture folder).\n")
            if any(not r["skill_structural_valid"] for r in all_results):
                f.write("- [ ] Resolve structural issues in SKILL.md (missing sections or TODOs).\n")
            f.write("\n## Do Not Change\n\n")
            f.write("- Output template (unless explicitly required)\n")
            f.write("- Core workflow steps\n")

    print(f"\n>>> Run complete. ID: {run_id}")
    print(f"    Results saved to promotion-runs/{run_id}/")
    return total_failures == 0

def main():
    parser = argparse.ArgumentParser(description="Skill Promotion Harness Runner")
    parser.add_argument("--skill", help="Run promotion suite for a specific skill")
    parser.add_argument("--all", action="store_true", help="Run promotion suite for all skills in plan")
    parser.add_argument("--dry-run", action="store_true", help="Don't write any files")
    args = parser.parse_args()

    if not PLAN_FILE.exists():
        print(f"Error: {PLAN_FILE} not found")
        sys.exit(1)

    with open(PLAN_FILE, "r") as f:
        plan = yaml.safe_load(f)

    if args.all:
        skills_to_run = plan.get("skills", {}).keys()
    elif args.skill:
        skills_to_run = [args.skill]
    else:
        parser.print_help()
        sys.exit(0)

    success = True
    for skill in skills_to_run:
        if not run_promotion_for_skill(skill, plan, dry_run=args.dry_run):
            success = False
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
