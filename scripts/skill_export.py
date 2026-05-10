import os
import re
import shutil
import tempfile
from pathlib import Path


IGNORED_NAMES = {'.git', '__pycache__', '.DS_Store', 'node_modules', 'dist'}
INTERNAL_FRONTMATTER_KEYS = {'status'}


def strip_frontmatter_metadata(content):
    """Strip repo-internal frontmatter keys from exported skill content."""
    parts = re.split(r'^---\s*\r?\n', content, maxsplit=2, flags=re.MULTILINE)
    if len(parts) < 3:
        return content

    frontmatter = parts[1]
    filtered_lines = []
    for line in frontmatter.splitlines():
        if ':' in line:
            key = line.split(':', 1)[0].strip()
            if key in INTERNAL_FRONTMATTER_KEYS:
                continue
        filtered_lines.append(line)

    new_frontmatter = '\n'.join(filtered_lines)
    return f"---\n{new_frontmatter}\n---\n{parts[2]}"


def get_repo_root():
    return Path(__file__).resolve().parent.parent


def copy_skill_tree(skill_dir, destination):
    def ignore_patterns(_path, names):
        return [name for name in names if name in IGNORED_NAMES]

    shutil.copytree(skill_dir, destination, ignore=ignore_patterns, dirs_exist_ok=True)


def bundle_shared_references(skill_root, repo_root):
    skill_md_path = skill_root / 'SKILL.md'
    content = skill_md_path.read_text(encoding='utf-8')

    refs = re.findall(r'shared/references/([\w-]+\.md)', content)
    if refs:
        ref_dir = skill_root / 'references'
        ref_dir.mkdir(exist_ok=True)
        for ref_file in set(refs):
            src_ref_path = repo_root / 'shared' / 'references' / ref_file
            if not src_ref_path.exists():
                raise FileNotFoundError(f'Referenced shared file not found: {src_ref_path}')

            shutil.copy2(src_ref_path, ref_dir / ref_file)
            content = content.replace(
                f'shared/references/{ref_file}',
                f'references/{ref_file}',
            )

    skill_md_path.write_text(strip_frontmatter_metadata(content), encoding='utf-8')


def export_skill_to_directory(skill_dir, destination):
    skill_dir = Path(skill_dir).resolve()
    destination = Path(destination).resolve()
    skill_md_path = skill_dir / 'SKILL.md'
    if not skill_md_path.exists():
        raise FileNotFoundError(f'{skill_md_path} not found.')

    if destination.exists():
        shutil.rmtree(destination)

    destination.parent.mkdir(parents=True, exist_ok=True)
    repo_root = get_repo_root()

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_root = Path(temp_dir)
        copy_skill_tree(skill_dir, temp_root)
        bundle_shared_references(temp_root, repo_root)
        shutil.copytree(temp_root, destination)

    return destination