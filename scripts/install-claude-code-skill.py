import os
import re
import argparse
import shutil
import tempfile
import sys
from pathlib import Path

def strip_frontmatter_metadata(content):
    """Strip repo-internal frontmatter like 'status'."""
    parts = re.split(r'^---\s*\r?\n', content, maxsplit=2, flags=re.MULTILINE)
    if len(parts) < 3:
        return content
    
    frontmatter = parts[1]
    lines = frontmatter.splitlines()
    filtered_lines = []
    for line in lines:
        if ':' in line:
            key = line.split(':', 1)[0].strip()
            if key in ['status']:
                continue
        filtered_lines.append(line)
    
    new_frontmatter = '\n'.join(filtered_lines)
    return f"---\n{new_frontmatter}\n---\n{parts[2]}"

def install_skill(skill_dir, scope, target_override=None):
    skill_dir = os.path.normpath(skill_dir)
    skill_name = os.path.basename(skill_dir)
    skill_md_path = os.path.join(skill_dir, 'SKILL.md')

    if not os.path.exists(skill_md_path):
        print(f"Error: {skill_md_path} not found.")
        sys.exit(1)

    # Determine target directory
    if target_override:
        target_base = Path(target_override)
    elif scope == 'global':
        target_base = Path.home() / '.claude' / 'skills'
    else:
        target_base = Path.cwd() / '.claude' / 'skills'

    target_dir = target_base / skill_name
    print(f"Installing {skill_name} to {target_dir}...")

    # Derive repo root from the script's location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.abspath(os.path.join(script_dir, ".."))
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # 1. Copy all skill-local content
        def ignore_patterns(path, names):
            ignored = []
            for name in names:
                if name in ['.git', '__pycache__', '.DS_Store', 'node_modules', 'dist']:
                    ignored.append(name)
            return ignored

        shutil.copytree(skill_dir, temp_dir, ignore=ignore_patterns, dirs_exist_ok=True)

        # 2. Process SKILL.md
        temp_skill_md_path = os.path.join(temp_dir, 'SKILL.md')
        with open(temp_skill_md_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Detect and bundle shared references
        refs = re.findall(r'shared/references/([\w-]+\.md)', content)
        if refs:
            ref_dir = os.path.join(temp_dir, 'references')
            os.makedirs(ref_dir, exist_ok=True)
            for ref_file in set(refs):
                src_ref_path = os.path.join(repo_root, 'shared', 'references', ref_file)
                if os.path.exists(src_ref_path):
                    shutil.copy2(src_ref_path, os.path.join(ref_dir, ref_file))
                    content = content.replace(f'shared/references/{ref_file}', f'references/{ref_file}')
                else:
                    print(f"Error: Referenced shared file {src_ref_path} not found.")
                    sys.exit(1)
        
        processed_content = strip_frontmatter_metadata(content)
        with open(temp_skill_md_path, 'w', encoding='utf-8') as f:
            f.write(processed_content)
        
        # 3. Copy to final destination
        if os.path.exists(target_dir):
            shutil.rmtree(target_dir)
        
        os.makedirs(target_base, exist_ok=True)
        shutil.copytree(temp_dir, target_dir)
        
        print(f"Successfully installed {skill_name} ({scope})")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Install an Interface Skill for Claude Code.')
    parser.add_argument('skill_dir', help='Path to the skill directory')
    parser.add_argument('--scope', choices=['global', 'project'], default='project', help='Installation scope (default: project)')
    parser.add_argument('--target', help='Override default target directory')
    
    args = parser.parse_args()
    install_skill(args.skill_dir, args.scope, args.target)
