import os
import re
import json

TODO_PATTERN = re.compile(r'(## TODO|- \[ \] TODO|TODO \(Human Review Required\))')

VALID_STATUSES = {'draft', 'current', 'approved', 'complete', 'superseded', 'stable'}

REQUIRED_SECTIONS_STABLE = [
    '## When to use this skill',
    '## Workflow',
    '## Output template',
    '## Acceptance criteria',
]


def validate_shared_references(repo_root):
    """Check that no shared/references file contains an unresolved TODO marker.

    Shared references ship as part of the public toolkit — a TODO here is a
    promise that wasn't kept, not an internal note.
    """
    refs_dir = os.path.join(repo_root, 'shared', 'references')
    if not os.path.isdir(refs_dir):
        return True

    passed = True
    for filename in sorted(os.listdir(refs_dir)):
        if not filename.endswith('.md'):
            continue
        path = os.path.join(refs_dir, filename)
        with open(path, 'r', encoding='utf-8') as f:
            if TODO_PATTERN.search(f.read()):
                print(f"[shared/references/{filename}] [FAIL] Unresolved 'TODO (Human Review Required)' marker. Resolve it before release.")
                passed = False
            else:
                print(f"[shared/references/{filename}] [OK] Valid")
    return passed


def validate_readme_skill_map(repo_root, skill_folders, target_skill=None):
    """Check that every skill folder has a row in the README Skill Map table."""
    readme_path = os.path.join(repo_root, 'README.md')
    if not os.path.exists(readme_path):
        print("[README] [FAIL] README.md not found")
        return False

    with open(readme_path, 'r', encoding='utf-8') as f:
        readme_content = f.read()

    # Prefer validating against a machine-readable registry if present
    registry_path = os.path.join(repo_root, 'skills.json')
    if os.path.exists(registry_path):
        try:
            with open(registry_path, 'r', encoding='utf-8') as rf:
                registry = json.load(rf)
        except Exception as exc:
            print(f"[README] [FAIL] Could not parse skills.json: {exc}")
            return False

        passed = True
        skills = registry.get('skills', [])
        for entry in skills:
            name = entry.get('name')
            status = entry.get('status', '').lower()
            if not name:
                print("[skills.json] [WARN] Skill entry without a name")
                continue
            
            # Filter by target_skill if provided
            if target_skill and name != target_skill:
                continue

            if f'`{name}`' not in readme_content:
                print(f"[{name}] [FAIL] Not found in README Skill Map table (registry expects this skill)")
                passed = False
                continue

            # Find the line in README containing the skill name to inspect any draft marker
            row_line = ''
            for line in readme_content.splitlines():
                if f'`{name}`' in line:
                    row_line = line
                    break

            # README uses a [DRAFT] marker to indicate draft items in the human-readable map.
            has_draft_marker = '[DRAFT]' in row_line or '⚠️' in row_line
            if status == 'draft' and not has_draft_marker:
                print(f"[{name}] [WARN] Registry status=draft but README row lacks '[DRAFT]' marker")
            if status != 'draft' and has_draft_marker:
                print(f"[{name}] [WARN] Registry status={status} but README row has '[DRAFT]' marker")

        return passed

    # Fallback: simple presence check (legacy behavior)
    passed = True
    for skill_folder in skill_folders:
        if f'`{skill_folder}`' not in readme_content:
            print(f"[{skill_folder}] [FAIL] Not found in README Skill Map table")
            passed = False
    return passed


def validate_distribution_registry(repo_root):
    """Check that skills.json has a valid top-level 'distribution' block."""
    registry_path = os.path.join(repo_root, 'skills.json')
    if not os.path.exists(registry_path):
        # validate_readme_skill_map handles a missing registry separately
        return True

    try:
        with open(registry_path, 'r', encoding='utf-8') as f:
            registry = json.load(f)
    except Exception as exc:
        print(f'[skills.json] [FAIL] Could not parse: {exc}')
        return False

    dist = registry.get('distribution')
    if dist is None:
        print("[skills.json] [FAIL] Missing top-level 'distribution' key")
        return False

    methods = dist.get('methods')
    if not isinstance(methods, dict) or not methods:
        print("[skills.json] [FAIL] 'distribution.methods' must be a non-empty object")
        return False

    passed = True
    for method_name, method in methods.items():
        script = method.get('script')
        if not script:
            print(f"[skills.json] [FAIL] distribution.methods.{method_name} missing 'script'")
            passed = False
            continue
        script_path = os.path.join(repo_root, script)
        if not os.path.exists(script_path):
            print(f"[skills.json] [FAIL] distribution.methods.{method_name}.script '{script}' does not exist")
            passed = False
        if not method.get('target'):
            print(f"[skills.json] [FAIL] distribution.methods.{method_name} missing 'target'")
            passed = False

    if passed:
        print('[skills.json] [OK] distribution registry valid')
    return passed


def validate_skills(target_skill=None):
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    skills_dir = os.path.join(repo_root, 'skills')

    if not os.path.exists(skills_dir):
        print("Error: skills/ directory not found.")
        return False

    all_passed = validate_shared_references(repo_root)

    if not validate_distribution_registry(repo_root):
        all_passed = False

    skill_folders = sorted(
        f for f in os.listdir(skills_dir)
        if os.path.isdir(os.path.join(skills_dir, f))
    )

    if target_skill:
        if target_skill in skill_folders:
            skill_folders = [target_skill]
        else:
            print(f"Error: Skill '{target_skill}' not found in {skills_dir}")
            return False

    # Check README skill map coverage (prefer registry-driven validation)
    if not validate_readme_skill_map(repo_root, skill_folders, target_skill=target_skill):
        all_passed = False

    for skill_folder in skill_folders:
        skill_path = os.path.join(skills_dir, skill_folder)
        skill_passed = True
        skill_md_path = os.path.join(skill_path, 'SKILL.md')
        
        if not os.path.exists(skill_md_path):
            print(f"[{skill_folder}] [FAIL] Missing SKILL.md")
            all_passed = False
            continue
            
        with open(skill_md_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Check agents/openai.yaml exists
        openai_yaml_path = os.path.join(skill_path, 'agents', 'openai.yaml')
        if not os.path.exists(openai_yaml_path):
            print(f"[{skill_folder}] [FAIL] Missing agents/openai.yaml")
            skill_passed = False
            
        # Check frontmatter
        frontmatter_match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
        if not frontmatter_match:
            print(f"[{skill_folder}] [FAIL] Missing YAML frontmatter")
            all_passed = False
            continue
            
        frontmatter = frontmatter_match.group(1)
        
        # Check allowed frontmatter keys (allow optional promotion_candidate flag)
        allowed_keys = {'name', 'description', 'status', 'promotion_candidate'}
        lines = frontmatter.strip().split('\n')
        for line in lines:
            if ':' in line:
                key = line.split(':', 1)[0].strip()
                if key not in allowed_keys:
                    print(f"[{skill_folder}] [FAIL] Unexpected frontmatter key '{key}'")
                    skill_passed = False
        
        # Check name
        name_match = re.search(r'name:\s*(.+)', frontmatter)
        if not name_match:
            print(f"[{skill_folder}] [FAIL] Missing 'name' in frontmatter")
            skill_passed = False
        else:
            name = name_match.group(1).strip()
            if not re.match(r'^[a-z0-9\-]+$', name):
                print(f"[{skill_folder}] [FAIL] Name '{name}' is not lowercase hyphenated")
                skill_passed = False
            if name != skill_folder:
                print(f"[{skill_folder}] [FAIL] Frontmatter name '{name}' does not match folder name '{skill_folder}'")
                skill_passed = False
                
        # Parse promotion candidate flag (optional)
        promotion_match = re.search(r'promotion_candidate:\s*(true|false)', frontmatter, re.I)
        promotion_candidate = False
        if promotion_match:
            promotion_candidate = promotion_match.group(1).strip().lower() == 'true'

        # Check status — missing or invalid now fails
        status_match = re.search(r'status:\s*(.+)', frontmatter)
        if not status_match:
            print(f"[{skill_folder}] [FAIL] Missing 'status' in frontmatter")
            skill_passed = False
            status = None
        else:
            status = status_match.group(1).strip()
            if status not in VALID_STATUSES:
                print(f"[{skill_folder}] [FAIL] Invalid status '{status}'. Must be one of: {sorted(VALID_STATUSES)}")
                skill_passed = False
                
        # Check description
        desc_match = re.search(r'description:\s*(.+)', frontmatter)
        if not desc_match or not desc_match.group(1).strip():
            print(f"[{skill_folder}] [FAIL] Missing or empty 'description' in frontmatter")
            skill_passed = False
        else:
            desc = desc_match.group(1).strip()
            if len(desc) < 20:
                print(f"[{skill_folder}] [FAIL] Description is too short (< 20 chars)")
                skill_passed = False
                
        # If this skill is being promoted or is non-draft, enforce strict checks.
        strict_mode = promotion_candidate or (status is not None and status != 'draft')

        # Check TODOs for strict-mode skills (non-draft or promotion candidates)
        if strict_mode and TODO_PATTERN.search(content):
            print(f"[{skill_folder}] [FAIL] 'TODO' section found in non-draft skill. Resolve it or mark as draft.")
            skill_passed = False

        # Check required sections: fail in strict mode, warn in draft mode
        for section in REQUIRED_SECTIONS_STABLE:
            if section not in content:
                if strict_mode:
                    print(f"[{skill_folder}] [FAIL] Missing required section '{section}' in non-draft skill")
                    skill_passed = False
                else:
                    print(f"[{skill_folder}] [WARN] Missing recommended section '{section}' in draft skill")

        # Check referenced shared files explicitly
        shared_refs = re.findall(r'shared/references/([\w-]+\.md)', content)
        for filename in shared_refs:
            ref_path = os.path.join(repo_root, 'shared', 'references', filename)
            if not os.path.exists(ref_path):
                print(f"[{skill_folder}] [FAIL] Explicitly referenced shared file '{filename}' does not exist")
                skill_passed = False
            
        if skill_passed:
            print(f"[{skill_folder}] [OK] Valid")
        else:
            all_passed = False

    return all_passed

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--skill', help='Validate a specific skill folder')
    args = parser.parse_args()

    if validate_skills(args.skill):
        print("\nValidation passed! [SUCCESS]")
        exit(0)
    else:
        print("\nValidation failed. [ERROR]")
        exit(1)
