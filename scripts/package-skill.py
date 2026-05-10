import os
import argparse
import subprocess
import tempfile
import zipfile
import sys

from skill_export import export_skill_to_directory

def validate_skill_before_packaging(skill_dir):
    """Run validate-skill.py scoped to the single skill being packaged.
    Returns True if validation passes, False otherwise.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    validator_path = os.path.join(script_dir, 'validate-skill.py')
    result = subprocess.run(
        [sys.executable, validator_path],
        capture_output=True, text=True
    )
    skill_name = os.path.basename(os.path.normpath(skill_dir))
    # Filter output to lines relevant to this skill (or shared references)
    relevant = [
        line for line in result.stdout.splitlines()
        if skill_name in line or 'shared/references' in line or 'ERROR' in line or 'SUCCESS' in line
    ]
    if relevant:
        print('\n'.join(relevant))
    if result.returncode != 0:
        # Any validation failure should block packaging. Print validator output for context.
        print(result.stdout)
        return False
    return True


def package_skill(skill_dir, output_dir, filename=None, skip_validation=False):
    skill_dir = os.path.normpath(skill_dir)
    skill_name = os.path.basename(skill_dir)
    skill_md_path = os.path.join(skill_dir, 'SKILL.md')

    if not os.path.exists(skill_md_path):
        print(f"Error: {skill_md_path} not found.")
        sys.exit(1)

    if not skip_validation:
        print(f"Validating {skill_name} before packaging...")
        if not validate_skill_before_packaging(skill_dir):
            print(f"Error: {skill_name} failed validation. Fix the errors above or use --skip-validation to bypass.")
            sys.exit(1)

    # Create output dir if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with tempfile.TemporaryDirectory() as temp_dir:
        export_root = os.path.join(temp_dir, skill_name)
        try:
            export_skill_to_directory(skill_dir, export_root)
        except FileNotFoundError as exc:
            print(f"Error: {exc}")
            sys.exit(1)

        out_filename = filename if filename else f"{skill_name}.zip"
        zip_path = os.path.join(output_dir, out_filename)
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for root, dirs, files in os.walk(export_root):
                for file in files:
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, export_root)
                    zip_file.write(full_path, rel_path)
        
        print(f"Packaged {skill_name} into {zip_path}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Package a skill for distribution.')
    parser.add_argument('skill_dir', help='Path to the skill directory')
    parser.add_argument('--output-dir', default='dist', help='Output directory for the package (default: dist)')
    parser.add_argument('--filename', help='Optional custom filename for the ZIP (default: <skill-name>.zip)')
    parser.add_argument('--skip-validation', action='store_true', help='Skip pre-packaging validation (not recommended)')
    
    args = parser.parse_args()
    package_skill(args.skill_dir, args.output_dir, args.filename, skip_validation=args.skip_validation)
