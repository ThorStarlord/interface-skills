import os
import re
import argparse
import shutil
import tempfile
import zipfile
import sys

def strip_frontmatter_metadata(content):
    """Strip repo-internal frontmatter like 'status'."""
    # Use a more flexible split for frontmatter
    # parts[0] will be empty, parts[1] will be the frontmatter, parts[2] the rest
    parts = re.split(r'^---\s*\r?\n', content, maxsplit=2, flags=re.MULTILINE)
    if len(parts) < 3:
        return content
    
    frontmatter = parts[1]
    # Filter out repo-internal keys
    lines = frontmatter.splitlines()
    filtered_lines = []
    for line in lines:
        if ':' in line:
            key = line.split(':', 1)[0].strip()
            if key in ['status']:
                continue
        filtered_lines.append(line)
    
    new_frontmatter = '\n'.join(filtered_lines)
    # Reconstruct the file
    return f"---\n{new_frontmatter}\n---\n{parts[2]}"

def package_skill(skill_dir, output_dir, filename=None):
    skill_dir = os.path.normpath(skill_dir)
    skill_name = os.path.basename(skill_dir)
    skill_md_path = os.path.join(skill_dir, 'SKILL.md')

    if not os.path.exists(skill_md_path):
        print(f"Error: {skill_md_path} not found.")
        sys.exit(1)

    # Create output dir if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Derive repo root from the script's location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.abspath(os.path.join(script_dir, ".."))
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # 1. Copy all skill-local content first (future-proofing)
        # Exclude common temp/cache folders if they exist
        def ignore_patterns(path, names):
            ignored = []
            for name in names:
                if name in ['.git', '__pycache__', '.DS_Store', 'node_modules', 'dist']:
                    ignored.append(name)
            return ignored

        # Copy everything from skill_dir to temp_dir
        # We use dirs_exist_ok=True if needed, but temp_dir is fresh
        shutil.copytree(skill_dir, temp_dir, ignore=ignore_patterns, dirs_exist_ok=True)

        # 2. Process SKILL.md in temp_dir
        temp_skill_md_path = os.path.join(temp_dir, 'SKILL.md')
        with open(temp_skill_md_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Detect and bundle shared references
        # Find shared/references/*.md
        refs = re.findall(r'shared/references/([\w-]+\.md)', content)
        if refs:
            ref_dir = os.path.join(temp_dir, 'references')
            os.makedirs(ref_dir, exist_ok=True)
            for ref_file in set(refs):
                src_ref_path = os.path.join(repo_root, 'shared', 'references', ref_file)
                if os.path.exists(src_ref_path):
                    shutil.copy2(src_ref_path, os.path.join(ref_dir, ref_file))
                    # Update content to point to local references/ directory
                    content = content.replace(f'shared/references/{ref_file}', f'references/{ref_file}')
                else:
                    print(f"Error: Referenced shared file {src_ref_path} not found.")
                    sys.exit(1)
        
        processed_content = strip_frontmatter_metadata(content)
        
        with open(temp_skill_md_path, 'w', encoding='utf-8') as f:
            f.write(processed_content)
        
        # 3. Zip it
        out_filename = filename if filename else f"{skill_name}.zip"
        zip_path = os.path.join(output_dir, out_filename)
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, temp_dir)
                    zip_file.write(full_path, rel_path)
        
        print(f"Packaged {skill_name} into {zip_path}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Package a skill for distribution.')
    parser.add_argument('skill_dir', help='Path to the skill directory')
    parser.add_argument('--output-dir', default='dist', help='Output directory for the package (default: dist)')
    parser.add_argument('--filename', help='Optional custom filename for the ZIP (default: <skill-name>.zip)')
    
    args = parser.parse_args()
    package_skill(args.skill_dir, args.output_dir, args.filename)
