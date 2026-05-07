import os
import re
import argparse
import shutil
import tempfile
import zipfile

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
    skill_name = os.path.basename(os.path.normpath(skill_dir))
    skill_md_path = os.path.join(skill_dir, 'SKILL.md')
    openai_yaml_path = os.path.join(skill_dir, 'agents', 'openai.yaml')

    if not os.path.exists(skill_md_path):
        print(f"Error: {skill_md_path} not found.")
        return

    # Create output dir if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with tempfile.TemporaryDirectory() as temp_dir:
        # 1. Process SKILL.md
        with open(skill_md_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        processed_content = strip_frontmatter_metadata(content)
        
        with open(os.path.join(temp_dir, 'SKILL.md'), 'w', encoding='utf-8') as f:
            f.write(processed_content)
        
        # 2. Process agents/openai.yaml if it exists
        if os.path.exists(openai_yaml_path):
            os.makedirs(os.path.join(temp_dir, 'agents'))
            with open(openai_yaml_path, 'r', encoding='utf-8') as f:
                yaml_content = f.read()
            
            # User mentioned: "That script should strip repo-only frontmatter like status"
            # It also said "include agents/openai.yaml".
            # It didn't explicitly say to strip interface metadata from openai.yaml, 
            # but it mentioned "strip before uploading to platforms that only accept name + description".
            # I'll keep it simple for now and just copy it.
            
            with open(os.path.join(temp_dir, 'agents', 'openai.yaml'), 'w', encoding='utf-8') as f:
                f.write(yaml_content)
        
        # 3. Zip it
        zip_path = os.path.join(output_dir, f"{skill_name}.zip")
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    rel_path = os.path.relpath(os.path.join(root, file), temp_dir)
                    zip_file.write(os.path.join(root, file), rel_path)
        
        print(f"Packaged {skill_name} into {zip_path}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Package a skill for distribution.')
    parser.add_argument('skill_dir', help='Path to the skill directory')
    parser.add_argument('--output-dir', default='dist', help='Output directory for the package (default: dist)')
    
    args = parser.parse_args()
    package_skill(args.skill_dir, args.output_dir)
