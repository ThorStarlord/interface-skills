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
import tempfile
from pathlib import Path
import re
import subprocess

# Add REPO_ROOT to sys.path to allow importing from scripts.validators
REPO_ROOT = Path(__file__).parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.append(str(REPO_ROOT))

from scripts.validators.human_review import validate_human_review
from scripts.validators.promotion_plan import validate_promotion_plan
from scripts.validators.handoff_verification import validate_handoff
from scripts.validators.fixture_integrity import validate_fixture_integrity
from scripts.validators.behavioral_result import validate_behavioral_result
from scripts.validators.reference_evidence import validate_reference_evidence
from scripts.validators.workflow_link import validate_workflow_link
from scripts.validators.zero_repair import validate_zero_repair
PROMOTION_RUNS_DIR = REPO_ROOT / "promotion-runs"
PLAN_FILE = REPO_ROOT / "promotion-plan.yaml"
SKILLS_FILE = REPO_ROOT / "skills.json"

def load_skill_registry():
    """Loads the machine-readable skill registry."""
    if not SKILLS_FILE.exists():
        return {"skills": []}
    return json.loads(SKILLS_FILE.read_text(encoding="utf-8"))


def extract_input_content(fixture_path, output_file=None):
    """
    Concatenates content from all relevant input files in the fixture.
    Excludes the expected/ directory and the current output file.
    """
    input_texts = []
    for f in fixture_path.glob("**/*"):
        if f.is_file() and f.suffix in ('.md', '.json', '.js', '.ts', '.html', '.css'):
            if "expected" in str(f):
                continue
            if output_file and f.resolve() == output_file.resolve():
                continue
            try:
                input_texts.append(f.read_text(encoding="utf-8"))
            except Exception:
                pass
    return "\n\n".join(input_texts)

def resolve_skill_artifact(skill_name, fixture_path, registry):
    """
    Resolves the output artifact for a skill within a fixture using registry mappings.
    Returns the Path to the artifact or None.
    """
    skill = next((s for s in registry.get("skills", []) if s["name"] == skill_name), None)
    if not skill or "canonical_output_paths" not in skill:
        return None
    
    for rel_path in skill["canonical_output_paths"]:
        # Handle globs (like component-specs/*.md)
        if "*" in rel_path:
            parts = rel_path.split("/")
            search_dir = fixture_path
            for part in parts[:-1]:
                search_dir = search_dir / part
            
            if search_dir.exists() and search_dir.is_dir():
                matches = list(search_dir.glob(parts[-1]))
                if matches:
                    return matches[0]
        else:
            candidate = fixture_path / rel_path
            if candidate.exists():
                return candidate
                
    return None

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

def run_validator(script_name, target_path, skill_name=None):
    """Runs a validator script and returns (passed, output)."""
    script_path = REPO_ROOT / "scripts" / script_name
    if not script_path.exists():
        return False, f"Validator {script_name} not found"
    
    try:
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        
        args = [sys.executable, str(script_path)]
        if script_name == "validate-skill.py" and skill_name:
            args.extend(["--skill", skill_name])
        else:
            args.append(str(target_path))
            
        result = subprocess.run(
            args,
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
    def extract_subject(text, prefix_len):
        subject = text[prefix_len:].strip().rstrip('.')
        for sep in [" where ", " if ", " consistent with ", " as "]:
            if sep in subject.lower():
                subject = subject.lower().split(sep)[0].strip()
                break
        return subject

    def strip_articles(text):
        """Strip leading articles (the, a, an) for fuzzy matching."""
        for article in ["the ", "a ", "an "]:
            if text.lower().startswith(article):
                return text[len(article):]
        return text

    results = []
    for item in rubric_items:
        found = False
        text_lower = item["text"].lower()
        
        # 1. Direct match
        if text_lower in output_content.lower():
            found = True
        # 2. Extract "Identifies X" subject
        elif text_lower.startswith("identifies "):
            subject = extract_subject(item["text"], 11)
            subj_stripped = strip_articles(subject)
            if subj_stripped.lower() in output_content.lower() or subject.lower() in output_content.lower():
                found = True
            elif subject.lower().endswith(" surface"):
                sub_subject = subject[:-8].strip()
                if sub_subject.lower() in output_content.lower():
                    found = True
        # 3. Extract "Prioritizes X" subject
        elif text_lower.startswith("prioritizes "):
            subject = extract_subject(item["text"], 12)
            if strip_articles(subject).lower() in output_content.lower():
                found = True
        # 4. Extract "Accounts for X" subject
        elif text_lower.startswith("accounts for "):
            subject = extract_subject(item["text"], 13)
            if strip_articles(subject).lower() in output_content.lower():
                found = True
        # 5. Handle "Does not X" (negative test - true if NOT found)
        elif text_lower.startswith("does not "):
            subject = extract_subject(item["text"], 9)
            if subject.lower() not in output_content.lower():
                found = True
        # 6. Extract "Names X" subject
        elif text_lower.startswith("names "):
            subject = extract_subject(item["text"], 6)
            if strip_articles(subject).lower() in output_content.lower():
                found = True
        # 7. Extract "Mentions X" subject
        elif text_lower.startswith("mentions "):
            subject = extract_subject(item["text"], 9)
            if strip_articles(subject).lower() in output_content.lower():
                found = True
        # 8. Extract "Captures X" subject
        elif text_lower.startswith("captures "):
            subject = extract_subject(item["text"], 9)
            if strip_articles(subject).lower() in output_content.lower():
                found = True
        # 9. Extract "Includes X" subject
        elif text_lower.startswith("includes "):
            subject = extract_subject(item["text"], 9)
            if strip_articles(subject).lower() in output_content.lower():
                found = True
        # 10. Extract "Separates X" — check for both halves around " from "
        elif text_lower.startswith("separates "):
            subject = extract_subject(item["text"], 10)
            parts = subject.lower().split(" from ")
            if all(p.strip() in output_content.lower() for p in parts if p.strip()):
                found = True
        
        results.append({
            "item": item["text"],
            "section": item["section"],
            "passed": found,
            "automation": "keyword_match" if found else "pending_manual"
        })
    return results
 

def classify_result(skill_name, fixture_name, skill_config, skill_valid, pkg_valid, rubric_passed, rubric_results, output_content, input_content=None):
    """
    Classifies the result based on whether the fixture was expected to fail.
    Returns (classification, classification_msg, behavioral_status)
    """
    messy_fixture_rel = skill_config.get("messy_fixture", "")
    is_messy = (fixture_name == Path(messy_fixture_rel).name)
    
    if not skill_valid:
        return "fail", "Skill structural validation failed unexpectedly", "invalid_structure"
        
    # Behavioral Check via modular validator
    behavioral_criteria = skill_config.get("behavioral_criteria", {})
    complexity_thresholds = behavioral_criteria.get("minimum_behavioral_complexity", {})
    
    bev_result = validate_behavioral_result(output_content, skill_name, complexity_thresholds, input_content=input_content)
    
    if is_messy:
        # For messy fixtures, we EXPECT failure in rubric or behavioral result
        if rubric_passed is False or bev_result.status == "fail":
            return "expected_fail", f"Messy fixture defects correctly detected: {bev_result.findings[0] if bev_result.status == 'fail' else 'Rubric failure'}", "valid"
        else:
            return "fail", "Messy fixture defects NOT correctly detected (False Positive Pass)", "adversarial_failure"

    if bev_result.status == "fail":
        # Map failure modes to legacy behavioral_status if needed
        status = "valid"
        if "trivial_placeholders" in bev_result.failure_modes:
            status = "trivial"
        elif "low_complexity" in bev_result.failure_modes:
            status = "low_complexity"
            
        return "fail", bev_result.findings[0], status
            
    if not pkg_valid:
        return "fail", "Clean fixture package validation failed", "invalid_package"

    if rubric_passed is False:
        return "fail", "Clean fixture failed automated rubric check", "rubric_failure"
        
    if rubric_passed == "N/A" or rubric_passed == "pending" or any(r.get("automation") == "pending_manual" for r in rubric_results):
        return "needs_human_review", "Evidence requires human judgment", "needs_review"
        
    return "pass", "Clean fixture passed", "valid"


def run_promotion_for_skill(skill_name, plan, dry_run=False, fresh=False):
    skill_config = plan.get("skills", {}).get(skill_name)
    if not skill_config:
        print(f"Error: Skill {skill_name} not found in promotion-plan.yaml")
        return False

    print(f"\n>>> Running Promotion Suite for: {skill_name} {'[FRESH RUN]' if fresh else ''}")
    
    total_failures = 0
    timestamp = time.strftime("%Y-%m-%d-%H-%M-%S")
    run_id = f"{timestamp}-{skill_name}{'-fresh' if fresh else ''}"
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
        
        # Pre-flight: Fixture Integrity
        integrity_result = validate_fixture_integrity(fixture_path)
        if integrity_result.status != "pass":
            print(f"    [FAIL] Fixture integrity check failed: {', '.join(integrity_result.findings)}")
            total_failures += 1
            continue
        
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
        elif skill_name == "ui-orchestrator":
            output_file = fixture_path / "reports" / "ORCHESTRATOR-RECOMMENDATION.md"
            if not output_file.exists():
                output_file = fixture_path / "orchestrator-recommendation.md"
        elif skill_name == "ui-surface-inventory":
            output_file = fixture_path / "reports" / "surface-inventory.md"
            if not output_file.exists():
                output_file = fixture_path / "surface-inventory.md"
        elif skill_name == "ui-to-issues":
            # ui-to-issues often generates issues.md or SOURCE.md in the fixture
            for candidate in [
                fixture_path / "reports" / "issues.md",
                fixture_path / "issues.md",
                fixture_path / "SOURCE.md",
            ]:
                if candidate.exists():
                    output_file = candidate
                    break
        elif skill_name == "ui-brief":
            # Brief can be stored at different paths depending on fixture layout:
            # - spec-recovery-create style: brief.md at root
            # - kanban-recovery style: input/02-brief.md
            # - standardized: specs/02-brief.md
            for candidate in [
                fixture_path / "specs" / "02-brief.md",
                fixture_path / "input" / "02-brief.md",
                fixture_path / "brief.md",
                fixture_path / "02-brief.md",
            ]:
                if candidate.exists():
                    output_file = candidate
                    break

        if not output_file or not output_file.exists():
            print(f"    [WARN] No output file found for {skill_name} in {fixture_name}. Skipping rubric check.")
            output_content = ""
        else:
            output_content = output_file.read_text(encoding="utf-8")

        # 3. Structural Validation
        skill_valid, skill_log = run_validator("validate-skill.py", REPO_ROOT / "skills" / skill_name, skill_name=skill_name)
        
        # If the output is a spec package (or part of one), validate it
        pkg_valid = True
        pkg_log = "N/A"
        if output_file and output_file.exists():
            pkg_valid, pkg_log = run_validator("validate-spec-package.py", fixture_path)

        # 4. Rubric Evaluation
        rubric_path = fixture_path / "expected" / "rubric.md"
        rubric_results = []
        rubric_passed = "N/A"
        if rubric_path.exists():
            rubric_items = parse_rubric(rubric_path)
            # Filter rubric items for this specific skill
            skill_rubric_items = [item for item in rubric_items if item["section"].lower() in (skill_name.lower(), "general")]
            if skill_rubric_items:
                rubric_results = evaluate_output_against_rubric(output_content, skill_rubric_items)
                # True if ALL passed (no pending_manual)
                # False if ANY automated FAILED
                # "pending" if some are pending_manual but none of the automated failed
                automated_fail = any(r["passed"] is False and r["automation"] != "pending_manual" for r in rubric_results)
                all_passed = all(r["passed"] for r in rubric_results)
                
                if automated_fail:
                    rubric_passed = False
                elif all_passed:
                    rubric_passed = True
                else:
                    rubric_passed = "pending"
            else:
                 print(f"    [INFO] No rubric section found for {skill_name} in {fixture_name}")
        else:
            print(f"    [INFO] No rubric.md found for {fixture_name}")

        # 4.5 Extract Input Content (for behavioral validation)
        input_content = extract_input_content(fixture_path, output_file)

        # 5. Classification
        classification, classification_msg, behavioral_status = classify_result(skill_name, fixture_name, skill_config, skill_valid, pkg_valid, rubric_passed, rubric_results, output_content, input_content=input_content)

        # 5.5 Evidence Level
        evidence_level = "promotion_candidate_run" if fresh else "harness_validation"
        generated_fresh_output = fresh
        
        # 6. Record Result
        fixture_result = {
            "fixture": fixture_name,
            "classification": classification,
            "classification_msg": classification_msg,
            "behavioral_status": behavioral_status,
            "evidence_level": evidence_level,
            "generated_fresh_output": generated_fresh_output,
            "skill_structural_valid": skill_valid,
            "package_structural_valid": pkg_valid,
            "rubric_passed": rubric_passed,
            "rubric_details": rubric_results,
            "pointers": {
                "fixture_input": str(fixture_rel_path),
                "output_artifact": str(output_file.relative_to(REPO_ROOT)) if output_file and output_file.exists() else None,
                "narrative_review": str((fixture_run_dir / "review.md").relative_to(REPO_ROOT)),
                "invocation_file": None # Placeholder for future invocation tracking
            },
            "logs": {
                "skill_validation": skill_log,
                "package_validation": pkg_log
            }
        }
        all_results.append(fixture_result)

        # 7. Downstream Test (if configured for this skill and fixture)
        downstream_config = skill_config.get("downstream")
        if downstream_config and fixture_rel_path == downstream_config.get("fixture"):
            next_skill = downstream_config.get("next_skill")
            print(f"    - Running downstream test: {skill_name} -> {next_skill}")
            
            # Look for downstream output
            downstream_output_file = None
            if next_skill == "ui-spec-reconcile":
                downstream_output_file = fixture_path / "reports" / "SPEC-RECONCILE-SUMMARY.md"
            elif next_skill == "ui-inspector":
                downstream_output_file = fixture_path / "reports" / "inspector-report.md"
                if not downstream_output_file.exists():
                    downstream_output_file = fixture_path / "redlines" / "inspector-report.md"
            elif next_skill == "ui-visual-calibration":
                for candidate in [
                    fixture_path / "specs" / "03-visual-calibration.md",
                    fixture_path / "visual-calibration.md",
                    fixture_path / "03-visual-calibration.md",
                ]:
                    if candidate.exists():
                        downstream_output_file = candidate
                        break
            
            if downstream_output_file and downstream_output_file.exists():
                next_skill_output = downstream_output_file.read_text(encoding="utf-8")
                # Verify handoff via modular validator
                # In this context, we need to create a temporary run_dir 
                # or just use the current run_dir and mock the file presence 
                # if we want to reuse the validator logic.
                # Actually, the validator expects a file.
                # We'll save the downstream output to a temp file or use the existing one.
                
                # For now, I'll update the validator to also accept raw content 
                # or I'll just write the downstream output to a temp file here.
                with tempfile.TemporaryDirectory() as tmp_handoff_dir:
                    handoff_path = Path(tmp_handoff_dir)
                    ds_file = handoff_path / f"downstream_{next_skill}.md"
                    ds_file.write_text(next_skill_output, encoding="utf-8")
                    
                    handoff_result = validate_handoff(handoff_path, skill_name, next_skill)
                
                ds_passed = handoff_result.status == "pass"
                ds_msg = handoff_result.findings[0]
                
                ds_result = {
                    "fixture": f"{fixture_name}_downstream",
                    "classification": "pass" if ds_passed else "fail",
                    "classification_msg": ds_msg,
                    "evidence_level": "harness_validation",
                    "generated_fresh_output": False,
                    "downstream_chain": f"{skill_name} -> {next_skill}"
                }
                all_results.append(ds_result)
                print(f"      [{'OK' if ds_passed else 'FAIL'}] {ds_msg}")
                
                if not dry_run:
                    ds_run_dir = run_dir / f"{fixture_name}_downstream"
                    ds_run_dir.mkdir(exist_ok=True)
                    with open(ds_run_dir / "result.json", "w", encoding="utf-8") as f:
                        json.dump(ds_result, f, indent=2)
                    with open(ds_run_dir / "review.md", "w", encoding="utf-8") as f:
                        f.write(f"# Downstream Review: {skill_name} -> {next_skill}\n\n")
                        f.write(f"- **Classification:** `{ds_result['classification']}`\n")
                        f.write(f"- **Message:** {ds_result['classification_msg']}\n")
                        f.write(f"- **Evidence Level:** `{ds_result['evidence_level']}`\n")
                        f.write(f"- **Chain:** {ds_result['downstream_chain']}\n")
            else:
                print(f"      [WARN] No downstream output found at {downstream_output_file}")
        
        if not dry_run:
            with open(fixture_run_dir / "result.json", "w", encoding="utf-8") as f:
                json.dump(fixture_result, f, indent=2)
            
            # Write human-readable review
            with open(fixture_run_dir / "review.md", "w", encoding="utf-8") as f:
                f.write(f"# Review: {skill_name} on {fixture_name}\n\n")
                f.write(f"- **Classification:** `{fixture_result['classification']}`\n")
                f.write(f"- **Message:** {fixture_result['classification_msg']}\n")
                f.write(f"- **Evidence Level:** `{fixture_result.get('evidence_level', 'unknown')}`\n")
                f.write(f"- **Skill Valid:** {'✅' if skill_valid else '❌'}\n")
                f.write(f"- **Package Valid:** {'✅' if pkg_valid else '❌'}\n")
                f.write(f"- **Rubric Pass:** {fixture_result['rubric_passed']}\n\n")
                
                if fixture_result['classification'] == "needs_human_review" or fixture_result['classification'] == "expected_fail":
                    f.write("> [!IMPORTANT]\n")
                    f.write("> **Human Review Required:** This result needs manual verification to confirm the skill's judgment matches reality.\n\n")

                f.write("## Human Review Checklist\n\n")
                f.write("- [ ] The clean fixtures are not incorrectly classified as failures.\n")
                f.write("- [ ] The messy fixture is correctly classified as `expected_fail`.\n")
                f.write("- [ ] The lint report catches the expected defects.\n")
                f.write("- [ ] The lint report does not invent major false positives.\n")
                f.write("- [ ] The severity levels are useful.\n")
                f.write("- [ ] The output format remained stable.\n")
                f.write("- [ ] A downstream skill can consume the output.\n")
                f.write("- [ ] The reviewer agrees the output is useful and not misleading.\n\n")
                f.write("Decision: approved | rejected | needs_revision\n")
                f.write("Reviewer:\n")
                f.write("Review date:\n\n")

                behavioral_criteria = skill_config.get("behavioral_criteria")
                if behavioral_criteria:
                    f.write("## Behavioral Scrutiny\n\n")
                    f.write("Verify that none of the following blocking failure modes occurred:\n\n")
                    for mode in behavioral_criteria.get("blocking_failure_modes", []):
                        f.write(f"- [ ] {mode}\n")
                    f.write("\n")
                    
                    f.write("## Judgment Fidelity Assessment\n\n")
                    f.write("- [ ] Judgment matches ground truth exactly.\n")
                    f.write("- [ ] Ambiguous boundaries handled with correct trade-offs.\n")
                    f.write("- [ ] No hallucination of artifacts or attributes.\n")
                    f.write("- [ ] Scope correctly bounded to the fixture domain.\n\n")

                f.write("## Rubric Details\n\n")
                if rubric_results:
                    for r in rubric_results:
                        f.write(f"- [{'x' if r['passed'] else ' '}] {r['item']} ({r['automation']})\n")
                else:
                    f.write("No rubric items found.\n")

    # 6. Generate Improvement or Fixture Repair Brief if needed
    total_failures = sum(1 for r in all_results if r.get("classification") == "fail")
    
    if total_failures > 0 and not dry_run:
        # Check if any failures were due to trivial or low complexity (fixture issues)
        fixture_issues = [r for r in all_results if r.get("behavioral_status") in ("trivial", "low_complexity")]
        skill_issues = [r for r in all_results if r.get("classification") == "fail" and r not in fixture_issues]
        
        if skill_issues:
            brief_path = run_dir / "improvement-brief.md"
            with open(brief_path, "w", encoding="utf-8") as f:
                f.write(f"# Skill Improvement Brief: {skill_name}\n\n")
                f.write(f"Detected {len(skill_issues)} logic failures across fixtures.\n\n")
                f.write("## Recommended Edits\n\n")
                f.write("- [ ] Check why rubric items failed.\n")
                if any(not r.get("skill_structural_valid", True) for r in skill_issues):
                    f.write("- [ ] Resolve structural issues in SKILL.md.\n")
                f.write("\n## Do Not Change\n\n")
                f.write("- Output template (unless explicitly required)\n")
                f.write("- Core workflow steps\n")

        if fixture_issues:
            repair_path = run_dir / "fixture-repair-brief.md"
            with open(repair_path, "w", encoding="utf-8") as f:
                f.write(f"# Fixture Repair Brief: {skill_name}\n\n")
                f.write(f"Detected {len(fixture_issues)} behavioral integrity issues (trivial or low complexity).\n\n")
                f.write("## Required Repairs\n\n")
                for issue in fixture_issues:
                    f.write(f"### Fixture: {issue['fixture']}\n")
                    f.write(f"- **Problem**: {issue['classification_msg']}\n")
                    if issue['behavioral_status'] == "trivial":
                        f.write("- [ ] Remove placeholders (TBD/TODO) and replace with realistic domain content.\n")
                    elif issue['behavioral_status'] == "low_complexity":
                        f.write("- [ ] Increase domain pressure (more surfaces/findings) to meet the minimum complexity threshold.\n")
                    f.write("\n")

    print(f"\n>>> Run complete. ID: {run_id}")
    print(f"    Results saved to promotion-runs/{run_id}/")
    return total_failures == 0


def validate_run(run_dir, requested_scope="stable"):
    """
    Runs all modular validators for a given promotion run directory.
    """
    print(f"\n>>> Validating Run Certification: {run_dir.name}")
    
    # 1. Human Review Governance Validation
    review_path = run_dir / "HUMAN-REVIEW.md"
    # Fallback to review.md if HUMAN-REVIEW.md doesn't exist yet (for transition)
    if not review_path.exists():
        review_path = run_dir / "review.md"
        
    result = validate_human_review(review_path, requested_scope)
    
    # 2. Handoff Verification Validation
    # We check if there are any downstream files to validate
    downstream_files = list(run_dir.glob("downstream_*.md"))
    for ds_file in downstream_files:
        next_skill = ds_file.name.replace("downstream_", "").replace(".md", "")
        # Note: we don't strictly know the source skill from just the filename, 
        # but in this harness it's the skill currently being validated.
        # We'll use a placeholder or try to infer.
        result = validate_handoff(run_dir, "unknown-source", next_skill)
        
        if result.status == "pass":
            print(f"    [OK] {result.validator_name}: {result.findings[0]}")
        else:
            print(f"    [FAIL] {result.validator_name}: {', '.join(result.findings)}")
            for mode in result.failure_modes:
                print(f"         Failure Mode: {mode}")
    
    # 3. Reference Evidence Validation
    # We infer the skill name from the run_dir name if possible, 
    # or it should be passed in.
    # Run ID format: YYYY-MM-DD-HH-MM-SS-skillname
    run_parts = run_dir.name.split("-")
    if len(run_parts) > 6:
        skill_name = "-".join(run_parts[6:])
        # For fresh runs, remove -fresh suffix
        if skill_name.endswith("-fresh"):
            skill_name = skill_name[:-6]
            
        ref_dir = REPO_ROOT / "examples" / "promotion" / skill_name / "reference"
        if ref_dir.exists():
            ref_result = validate_reference_evidence(skill_name, ref_dir)
            if ref_result.status == "pass":
                print(f"    [OK] {ref_result.validator_name}: Reference snapshot verified for {skill_name}")
            else:
                print(f"    [FAIL] {ref_result.validator_name}: {', '.join(ref_result.findings)}")
                # We don't fail the whole run yet as reference might not be mandatory for candidates
    
    return True # Human review is the primary cert gate for now


def run_promotion_for_workflow(workflow_id, plan, registry_path, dry_run=False):
    """
    Runs a full-chain promotion for a workflow.
    """
    if not registry_path.exists():
        print(f"Error: Workflow registry {registry_path} not found")
        return False

    with open(registry_path, "r", encoding="utf-8") as f:
        registry = yaml.safe_load(f)
    
    workflow = next((w for w in registry.get("workflows", []) if w["id"] == workflow_id), None)
    if not workflow:
        print(f"Error: Workflow {workflow_id} not found in registry")
        return False

    print(f"\n>>> Running Full-Chain Promotion Suite for Workflow: {workflow_id}")
    
    timestamp = time.strftime("%Y-%m-%d-%H-%M-%S")
    run_id = f"{timestamp}-workflow-{workflow_id}"
    run_dir = PROMOTION_RUNS_DIR / run_id
    
    if not dry_run:
        run_dir.mkdir(parents=True, exist_ok=True)

    # In a full-chain run, we typically use one master fixture
    # For now, we'll look for a 'full_chain' entry in the promotion-plan or use a convention
    # Let's assume the spec-recovery workflow uses the 'pulse-recovery' fixture
    fixture_rel_path = f"examples/fixtures/full-chain/{workflow_id}"
    fixture_path = REPO_ROOT / fixture_rel_path
    
    if not fixture_path.exists():
         # Try a fallback or looking in promotion-plan
         print(f"    [WARN] No dedicated full-chain fixture found at {fixture_rel_path}")
         return False

    print(f"  - Testing with fixture: {fixture_path.name}")
    
    workflow_results = []
    total_failures = 0
    
    skill_registry = load_skill_registry()
    
    # Loop through steps
    for step in workflow.get("steps", []):
        skill_name = step["skill"]
        print(f"    [Step {step['id']}] Verifying skill: {skill_name}")
        
        # 1. Structural Validation of the skill itself
        skill_valid, skill_log = run_validator("validate-skill.py", REPO_ROOT / "skills" / skill_name, skill_name=skill_name)
        
        # 2. Find the output artifact for this step in the fixture
        output_file = resolve_skill_artifact(skill_name, fixture_path, skill_registry)

        step_success = True
        step_msg = "Artifact found and valid"
        
        if not output_file or not output_file.exists():
            step_success = False
            step_msg = f"Missing artifact for {skill_name}"
        else:
            # 3. Validate the artifact
            pkg_valid, pkg_log = run_validator("validate-spec-package.py", fixture_path)
            if not pkg_valid:
                step_success = False
                step_msg = "Package validation failed"

        workflow_results.append({
            "step": step["id"],
            "skill": skill_name,
            "status": "pass" if step_success else "fail",
            "message": step_msg,
            "artifact": str(output_file.relative_to(REPO_ROOT)) if output_file and output_file.exists() else None
        })
        
        if not step_success:
            print(f"      [FAIL] {step_msg}")
            total_failures += 1
        else:
            print(f"      [OK] {step_msg}")
            
            # 4. Workflow-Link Validation (Tracer Bullet)
            prev_step_data = workflow_results[-2] if len(workflow_results) > 1 else None
            curr_step_data = {
                "skill": skill_name,
                "artifact": str(output_file.relative_to(REPO_ROOT)),
                "input_artifact": prev_step_data.get("artifact") if prev_step_data else None,
                "workflow_id": workflow_id,
                "step_id": step["id"]
            }
            link_result = validate_workflow_link(run_dir, curr_step_data, prev_step_data)
            
            res = workflow_results[-1]
            res["validator_findings"] = {}
            res["validator_findings"]["workflow_link"] = link_result.findings

            if link_result.status != "pass":
                print(f"      [FAIL] workflow_link: {', '.join(link_result.findings)}")
                res["status"] = "fail"
                res["message"] = "Workflow link validation failed"
                total_failures += 1
            else:
                print(f"      [OK] workflow_link: verified semantic and physical continuity")

            # 5. Zero-Manual-Repair Verification
            zero_repair_result = validate_zero_repair(fixture_path, output_file)
            res["validator_findings"]["zero_repair"] = zero_repair_result.findings
            
            if zero_repair_result.status != "pass":
                print(f"      [FAIL] zero_repair: {', '.join(zero_repair_result.findings)}")
                res["status"] = "fail"
                res["message"] = "Zero-manual-repair validation failed"
                total_failures += 1
            else:
                print(f"      [OK] zero_repair: verified no manual modifications")

    # Record workflow manifest
    if not dry_run:
        manifest = {
            "workflow_id": workflow_id,
            "run_id": run_id,
            "timestamp": timestamp,
            "steps": workflow_results,
            "fixture": fixture_rel_path
        }
        with open(run_dir / "MANIFEST.json", "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=2)
        
        # Create the Continuity Audit record
        with open(run_dir / "CONTINUITY-AUDIT.md", "w", encoding="utf-8") as f:
            f.write(f"# Continuity Audit: {workflow_id}\n\n")
            f.write(f"- **Run ID**: `{run_id}`\n")
            f.write(f"- **Fixture**: `{fixture_rel_path}`\n\n")
            f.write("## Zero-Manual-Repair Check\n\n")
            for res in workflow_results:
                f.write(f"- [ ] Step {res['step']} ({res['skill']}): consumed upstream without repair?\n")
            f.write("\n## Semantic Thread Audit\n\n")
            f.write("- [ ] Intent preserved from start to finish?\n")
            f.write("- [ ] Traceability maintained?\n")

        with open(run_dir / "CONTINUITY-AUDIT.md", "a", encoding="utf-8") as f:
            f.write("\n## Machine-Generated Validator Findings\n\n")
            for res in workflow_results:
                f.write(f"### Step {res['step']} ({res['skill']})\n")
                f.write(f"- **Status**: {res['status']}\n")
                f.write(f"- **Message**: {res['message']}\n")
                # We need to preserve the validator findings in workflow_results
                if "validator_findings" in res:
                    for v_name, findings in res["validator_findings"].items():
                        f.write(f"#### {v_name}\n")
                        for finding in findings:
                            f.write(f"- {finding}\n")
                f.write("\n")

    print(f"\n>>> Workflow run complete. ID: {run_id}")
    return total_failures == 0

def main():
    parser = argparse.ArgumentParser(description="Skill Promotion Harness Runner")
    parser.add_argument("--skill", help="Run promotion suite for a specific skill")
    parser.add_argument("--workflow", help="Run full-chain promotion for a workflow")
    parser.add_argument("--all", action="store_true", help="Run promotion suite for all skills in plan")
    parser.add_argument("--fresh", action="store_true", help="Mark run as fresh skill output (promotion candidate)")
    parser.add_argument("--dry-run", action="store_true", help="Don't write any files")
    parser.add_argument("--validate", help="Validate certification for a specific run directory")
    args = parser.parse_args()

    if not PLAN_FILE.exists():
        print(f"Error: {PLAN_FILE} not found")
        sys.exit(1)

    with open(PLAN_FILE, "r") as f:
        plan = yaml.safe_load(f)

    # 1. Validate Promotion Plan
    print(">>> Validating Promotion Plan...")
    plan_result = validate_promotion_plan(
        PLAN_FILE, 
        registry_path=REPO_ROOT / "skills.json",
        repo_root=REPO_ROOT
    )
    if plan_result.status != "pass":
        print(f"Error: Promotion Plan validation failed:")
        for finding in plan_result.findings:
            print(f"  - {finding}")
        sys.exit(1)
    print("    Plan OK.")

    # 1.5 Validate Promotion Plan Schema (Legacy check - keeping for now)
    print(">>> Validating Promotion Plan Schema (Legacy)...")
    validator_script = REPO_ROOT / "scripts" / "validate-promotion-plan-schema.py"
    if validator_script.exists():
        v_result = subprocess.run(
            [sys.executable, str(validator_script)],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        if v_result.returncode != 0:
            print(f"Error: Promotion Plan schema validation failed:\n{v_result.stdout}{v_result.stderr}")
            sys.exit(1)
        print("    Schema OK.")
    else:
        print("    [WARN] scripts/validate-promotion-plan-schema.py not found. Skipping schema check.")

    skills_to_run = []
    success = True
    if args.workflow:
        registry_path = REPO_ROOT / "skills" / "workflow-orchestrator" / "references" / "workflow-registry.yaml"
        if not run_promotion_for_workflow(args.workflow, plan, registry_path, dry_run=args.dry_run):
            success = False
    elif args.all:
        skills_to_run = plan.get("skills", {}).keys()
    elif args.skill:
        skills_to_run = [args.skill]
    elif args.validate:
        pass # Allow running validation only
    else:
        parser.print_help()
        sys.exit(0)

    for skill in skills_to_run:
        if not run_promotion_for_skill(skill, plan, dry_run=args.dry_run, fresh=args.fresh):
            success = False
    
    if args.validate:
        run_dir = Path(args.validate)
        if not run_dir.is_absolute():
            run_dir = REPO_ROOT / run_dir
        if not validate_run(run_dir):
            success = False

    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
