import os
import yaml
import sys
import argparse
import re

def parse_frontmatter(content):
    """
    Parses frontmatter from markdown content.
    Returns (metadata, body, error)
    """
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            try:
                fm = yaml.safe_load(parts[1]) or {}
                return fm, parts[2], None
            except yaml.YAMLError as e:
                return {}, content, str(e)
    return {}, content, None

def get_report_base_type(filename):
    name = filename.upper()
    if "-REPORT" in name:
        return name.split("-REPORT")[0] + "-REPORT"
    return "REPORT"

def validate_spec_package(package_path):
    issues = []
    reports = []

    # Use os.walk for recursive scanning
    for root, dirs, files in os.walk(package_path):
        for filename in files:
            if not filename.endswith(".md"):
                continue

            filepath = os.path.join(root, filename)
            # relative path from package_path for reporting
            rel_path = os.path.relpath(filepath, package_path)
            
            with open(filepath, "r", encoding="utf-8") as f:
                try:
                    content = f.read()
                except UnicodeDecodeError:
                    issues.append(f"- [ERROR] {rel_path}: Could not read file (encoding error)")
                    continue

            fm, body, yaml_error = parse_frontmatter(content)

            if yaml_error:
                issues.append(f"- [ERROR] {rel_path}: Malformed YAML frontmatter: {yaml_error}")

            # 1. based_on references must resolve to real files
            if "based_on" in fm:
                based_on_val = fm.get("based_on")

                # Safely handle None values from empty yaml keys
                if based_on_val is not None:
                    based_on_files = [based_on_val] if isinstance(based_on_val, str) else based_on_val
                    for b_file in based_on_files:
                        # Allow 'none' as a special value meaning no reference
                        if b_file.lower().startswith("none"):
                            continue
                            
                        # References are relative to the file containing them, or the package root?
                        # Standard Interface Skills logic: references are relative to the file's directory
                        b_path = os.path.join(root, b_file)
                        if not os.path.exists(b_path):
                            issues.append(f"- [ERROR] {rel_path}: `based_on` reference `{b_file}` does not exist")

            # 2. .deprecated files cannot have status: current
            if ".deprecated" in filename.lower() and fm.get("status") == "current":
                issues.append(f"- [ERROR] {rel_path}: .deprecated files cannot have `status: current`")

            # 3 & 4. Reports logic
            if "REPORT" in filename.upper() or fm.get("spec_type") == "report" or fm.get("type") == "report":
                reports.append((rel_path, fm))

                status = fm.get("status", "")
                if status == "historical":
                    if "superseded_by" not in fm and fm.get("current_report") is not False:
                        issues.append(f"- [ERROR] {rel_path}: historical report must have `superseded_by` or `current_report: false`")

            # 5. [A] acceptance markers must specify an automation mechanism
            for line in body.split("\n"):
                if "[A]" in line:
                    if not re.search(r'\[A\]\s*\([a-zA-Z0-9_-]+\)', line) and "automation:" not in line.lower():
                        issues.append(f"- [ERROR] {rel_path}: `[A]` marker lacks automation mechanism (e.g., `[A] (playwright)`)")

    # Check for multiple current reports per type
    current_reports_by_type = {}
    for rel_path, fm in reports:
        if fm.get("status") == "current" or fm.get("current_report") is True:
            # Use basename for type identification to allow grouped reports across folders
            filename = os.path.basename(rel_path)
            base_type = get_report_base_type(filename)
            if base_type not in current_reports_by_type:
                current_reports_by_type[base_type] = []
            current_reports_by_type[base_type].append(rel_path)

    for base_type, current_files in current_reports_by_type.items():
        if len(current_files) > 1:
            issues.append(f"- [ERROR] Multiple current reports found for type {base_type}: {', '.join(current_files)}")

    return issues

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="Path to the spec package")
    args = parser.parse_args()

    if not os.path.isdir(args.path):
        print(f"Error: {args.path} is not a directory")
        sys.exit(2)

    issues = validate_spec_package(args.path)

    if not issues:
        print("# Spec Package Validation: SUCCESS")
        sys.exit(0)
    else:
        print("# Spec Package Validation: FAILED")
        for issue in issues:
            print(issue)
        sys.exit(1)
