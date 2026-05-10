import os
import argparse
import shutil
import sys
from pathlib import Path

from skill_export import export_skill_to_directory

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

    try:
        export_skill_to_directory(skill_dir, target_dir)
    except FileNotFoundError as exc:
        print(f"Error: {exc}")
        sys.exit(1)

    print(f"Successfully installed {skill_name} ({scope})")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Install an Interface Skill for Claude Code.')
    parser.add_argument('skill_dir', help='Path to the skill directory')
    parser.add_argument('--scope', choices=['global', 'project'], default='project', help='Installation scope (default: project)')
    parser.add_argument('--target', help='Override default target directory')
    
    args = parser.parse_args()
    install_skill(args.skill_dir, args.scope, args.target)
