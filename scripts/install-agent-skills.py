import argparse
import os
import shutil
import sys
from pathlib import Path

from skill_export import export_skill_to_directory


def get_target_base(scope, target_override=None):
    if target_override:
        return Path(target_override)
    if scope == 'global':
        return Path.home() / '.agents' / 'skills'
    return Path.cwd() / '.agents' / 'skills'


def install_skill(skill_dir, scope, mode='copy', target_override=None, force=False):
    skill_path = Path(os.path.normpath(skill_dir))
    skill_name = skill_path.name
    skill_md_path = skill_path / 'SKILL.md'
    if not skill_md_path.exists():
        print(f'Error: {skill_md_path} not found.')
        sys.exit(1)

    target_base = get_target_base(scope, target_override=target_override)
    target_dir = target_base / skill_name
    print(f'Installing {skill_name} to {target_dir} using {mode} mode...')

    if target_dir.exists() or target_dir.is_symlink():
        if not force:
            print(
                f'Skipping {skill_name}: {target_dir} already exists. '
                f'Use --force to overwrite.'
            )
            return
        if target_dir.is_symlink() or target_dir.is_file():
            target_dir.unlink()
        else:
            shutil.rmtree(target_dir)

    target_base.mkdir(parents=True, exist_ok=True)

    if mode == 'symlink':
        try:
            target_dir.symlink_to(skill_path.resolve(), target_is_directory=True)
        except (OSError, NotImplementedError) as exc:
            print(
                f'Error: symlink creation failed — {exc}\n'
                f'Tip: on Windows, symlinks require Developer Mode or Administrator '
                f'privileges. Use --mode copy instead.'
            )
            sys.exit(1)
    else:
        try:
            export_skill_to_directory(skill_path, target_dir)
        except FileNotFoundError as exc:
            print(f'Error: {exc}')
            sys.exit(1)

    print(f'Successfully installed {skill_name} ({scope}, {mode})')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Install an Interface Skill into the universal .agents/skills layout.'
    )
    parser.add_argument('skill_dir', nargs='+', help='Path(s) to one or more skill directories')
    parser.add_argument(
        '--scope',
        choices=['global', 'project'],
        default='project',
        help='Installation scope (default: project)',
    )
    parser.add_argument(
        '--mode',
        choices=['copy', 'symlink'],
        default='copy',
        help='Install by copying a bundled export or by creating a symlink (default: copy)',
    )
    parser.add_argument('--target', help='Override default target directory')
    parser.add_argument(
        '--force',
        action='store_true',
        help='Overwrite an existing installation (default: skip if already installed)',
    )

    args = parser.parse_args()
    for skill_dir in args.skill_dir:
        install_skill(skill_dir, args.scope, mode=args.mode, target_override=args.target, force=args.force)