import os
import json
import sys
import argparse
import re

def parse_frontmatter(content):
    match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return {}
    
    yaml_text = match.group(1)
    data = {}
    for line in yaml_text.strip().split('\n'):
        if ':' in line:
            key, val = line.split(':', 1)
            data[key.strip()] = val.strip().strip('"').strip("'")
    return data

def validate_package(package_path):
    issues = []
    
    # 1. Check existence of 00-index.md
    index_path = os.path.join(package_path, "00-index.md")
    if not os.path.exists(index_path):
        issues.append("- [CRITICAL] Missing `00-index.md` (Entry point)")
    
    # 2. Check existence of RUN-MANIFEST.md or run-manifest.json
    manifest_md = os.path.join(package_path, "RUN-MANIFEST.md")
    manifest_json = os.path.join(package_path, "run-manifest.json")
    
    if not os.path.exists(manifest_md) and not os.path.exists(manifest_json):
        issues.append("- [CRITICAL] Missing `RUN-MANIFEST.md` or `run-manifest.json` (Run History)")
    
    # 3. Check for Report Lifecycle (current vs superseded)
    report_files = [f for f in os.listdir(package_path) if (f.endswith('.md') and 'REPORT' in f.upper()) or f == '09-redlines.md']
    active_reports = {} # type -> filename
    
    for report_file in report_files:
        path = os.path.join(package_path, report_file)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            fm = parse_frontmatter(content)
            
            if fm.get('spec_type') == 'report':
                rtype = fm.get('report_type')
                is_current = fm.get('current_report') == 'true'
                
                if is_current:
                    if rtype in active_reports:
                        issues.append(f"- [ERROR] Multiple reports marked as current for type `{rtype}`: `{active_reports[rtype]}` and `{report_file}`")
                    else:
                        active_reports[rtype] = report_file
                
                # Supersession check
                superseded_by = fm.get('superseded_by')
                if superseded_by:
                    if not os.path.exists(os.path.join(package_path, superseded_by)):
                        issues.append(f"- [ERROR] `{report_file}` is superseded by `{superseded_by}`, but the replacement file is missing.")
                
                # Check generated_from_commit
                if not fm.get('generated_from_commit'):
                    issues.append(f"- [WARN] Report `{report_file}` missing `generated_from_commit` metadata.")

    # 4. Canonical Numbering Check (Warn if using legacy names in a new package)
    legacy_names = ['brief.md', 'blueprint.md', 'screen-spec.md', 'acceptance.md']
    for legacy in legacy_names:
        if os.path.exists(os.path.join(package_path, legacy)):
            issues.append(f"- [INFO] Legacy filename detected: `{legacy}`. Consider migrating to numbered format.")

    # Final Report
    if not any("[CRITICAL]" in i or "[ERROR]" in i for i in issues):
        print("# Package Validation Report: SUCCESS")
        if issues:
            print("With warnings/info:")
            for issue in issues:
                print(issue)
        else:
            print("Package conforms to the Canonical Package Format.")
        return 0
    else:
        print("# Package Validation Report: FAILED")
        for issue in issues:
            print(issue)
        return 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="Path to the spec package")
    args = parser.parse_args()
    
    if not os.path.isdir(args.path):
        print(f"Error: {args.path} is not a directory")
        sys.exit(2)
        
    sys.exit(validate_package(args.path))
