import os
import re

TODO_PATTERN = re.compile(r'(## TODO|- \[ \] TODO|TODO \(Human Review Required\))')

VALID_STATUSES = {'draft', 'stable'}

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


def validate_readme_skill_map(repo_root, skill_folders):
    """Check that every skill folder has a row in the README Skill Map table."""
    readme_path = os.path.join(repo_root, 'README.md')
    if not os.path.exists(readme_path):
        print("[README] [FAIL] README.md not found")
        return False

    with open(readme_path, 'r', encoding='utf-8') as f:
        readme_content = f.read()

    passed = True
    for skill_folder in skill_folders:
        # A skill appears in the table if its backtick-quoted name is present
        if f'`{skill_folder}`' not in readme_content:
            print(f"[{skill_folder}] [FAIL] Not found in README Skill Map table")
            passed = False
    return passed


def validate_skills():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    skills_dir = os.path.join(repo_root, 'skills')

    if not os.path.exists(skills_dir):
        print("Error: skills/ directory not found.")
        return False

    all_passed = validate_shared_references(repo_root)

    skill_folders = sorted(
        f for f in os.listdir(skills_dir)
        if os.path.isdir(os.path.join(skills_dir, f))
    )

    # Check README skill map coverage for all skill folders up front
    if not validate_readme_skill_map(repo_root, skill_folders):
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
        
        # Check allowed frontmatter keys
        allowed_keys = {'name', 'description', 'status'}
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
                
        # Check TODOs in stable skills
        if status == 'stable' and TODO_PATTERN.search(content):
            print(f"[{skill_folder}] [FAIL] 'TODO' section found in stable skill. Resolve it or mark as draft.")
            skill_passed = False

        # Check required sections in stable skills
        if status == 'stable':
            for section in REQUIRED_SECTIONS_STABLE:
                if section not in content:
                    print(f"[{skill_folder}] [FAIL] Missing required section '{section}' in stable skill")
                    skill_passed = False

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
    if validate_skills():
        print("\nAll skills passed validation! [SUCCESS]")
        exit(0)
    else:
        print("\nSome skills failed validation. [ERROR]")
        exit(1)
