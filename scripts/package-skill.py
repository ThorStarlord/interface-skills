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

def package_skill(skill_dir, output_dir):
    skill_dir = os.path.normpath(skill_dir)
    skill_name = os.path.basename(skill_dir)
    skill_md_path = os.path.join(skill_dir, 'SKILL.md')
    openai_yaml_path = os.path.join(skill_dir, 'agents', 'openai.yaml')

    if not os.path.exists(skill_md_path):
        print(f"Error: {skill_md_path} not found.")
        sys.exit(1)

    # Create output dir if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Determine repo root (assuming script is in scripts/ and skills are in skills/)
    # A more reliable way is to look for the .git or README.md in parent dirs
    repo_root = os.getcwd() # Simple assumption: run from repo root
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # 1. Process SKILL.md
        with open(skill_md_path, 'r', encoding='utf-8') as f:
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
                    print(f"Warning: Referenced file {src_ref_path} not found.")
        
        processed_content = strip_frontmatter_metadata(content)
        
        with open(os.path.join(temp_dir, 'SKILL.md'), 'w', encoding='utf-8') as f:
            f.write(processed_content)
        
        # 2. Process agents/openai.yaml if it exists
        if os.path.exists(openai_yaml_path):
            os.makedirs(os.path.join(temp_dir, 'agents'))
            shutil.copy2(openai_yaml_path, os.path.join(temp_dir, 'agents', 'openai.yaml'))
        
        # 3. Zip it
        zip_path = os.path.join(output_dir, f"{skill_name}.zip")
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
    
    args = parser.parse_args()
    package_skill(args.skill_dir, args.output_dir)
