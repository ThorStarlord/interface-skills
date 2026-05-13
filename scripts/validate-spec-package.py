import os
import yaml
import sys
import argparse
import re

def parse_frontmatter(content):
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            try:
                return yaml.safe_load(parts[1]) or {}, parts[2]
            except yaml.YAMLError:
                return {}, content
    return {}, content

def get_report_base_type(filename):
    name = filename.upper()
    if "-REPORT" in name:
        return name.split("-REPORT")[0] + "-REPORT"
    return "REPORT"

def validate_spec_package(package_path):
    issues = []
    reports = []

    for filename in os.listdir(package_path):
        if not filename.endswith(".md"):
            continue

        filepath = os.path.join(package_path, filename)
        with open(filepath, "r") as f:
            content = f.read()

        fm, body = parse_frontmatter(content)

        # 1. based_on references must resolve to real files
        if "based_on" in fm:
            based_on_val = fm.get("based_on")

            # CRITICAL FIX from Code Review: Safely handle None values from empty yaml keys
            if based_on_val is not None:
                based_on_files = [based_on_val] if isinstance(based_on_val, str) else based_on_val
                for b_file in based_on_files:
                    b_path = os.path.join(package_path, b_file)
                    if not os.path.exists(b_path):
                        issues.append(f"- [ERROR] {filename}: `based_on` reference `{b_file}` does not exist")

        # 2. .deprecated files cannot have status: current
        if ".deprecated" in filename.lower() and fm.get("status") == "current":
            issues.append(f"- [ERROR] {filename}: .deprecated files cannot have `status: current`")

        # 3 & 4. Reports logic
        if "REPORT" in filename.upper() or fm.get("type") == "report":
            reports.append((filename, fm))

            status = fm.get("status", "")
            if status == "historical":
                if "superseded_by" not in fm and fm.get("current_report") is not False:
                    issues.append(f"- [ERROR] {filename}: historical report must have `superseded_by` or `current_report: false`")

        # 5. [A] acceptance markers must specify an automation mechanism
        for line in body.split("\n"):
            if "[A]" in line:
                if not re.search(r'\[A\]\s*\([a-zA-Z0-9_-]+\)', line) and "automation:" not in line.lower():
                    issues.append(f"- [ERROR] {filename}: `[A]` marker lacks automation mechanism (e.g., `[A] (playwright)`)")

    # Check for multiple current reports per type
    current_reports_by_type = {}
    for filename, fm in reports:
        if fm.get("status") == "current":
            base_type = get_report_base_type(filename)
            if base_type not in current_reports_by_type:
                current_reports_by_type[base_type] = []
            current_reports_by_type[base_type].append(filename)

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
