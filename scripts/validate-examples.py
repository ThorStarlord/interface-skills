#!/usr/bin/env python3
"""
validate-examples.py — Validates the structural integrity of all example spec packages.

Checks:
- Each examples/*/ directory has a 00-index.md (or manifest.md fallback)
- Every file listed in 00-index.md exists on disk
- Frontmatter status values are valid
- component-specs/ directory exists when referenced in the index
- redlines/inspector-report.md exists when listed in the index
- Packages marked intentionally_incomplete: true are excluded from completeness checks

Usage:
  python scripts/validate-examples.py
  python scripts/validate-examples.py --verbose
  python scripts/validate-examples.py --examples-dir examples/spec-recovery-create
"""

import argparse
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None

VALID_STATUSES = {"draft", "current", "approved", "complete", "superseded"}
VALID_ROUTING_STATUSES = {"wired", "partial", "missing", "not_required"}
INDEX_FILENAMES = ("00-index.md", "manifest.md")


def parse_frontmatter(text: str) -> dict:
    """Extract YAML frontmatter key-value pairs from a markdown file."""
    fm = {}
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return fm
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" in line:
            key, _, value = line.partition(":")
            fm[key.strip()] = value.strip()
    return fm


def find_index(package_dir: Path) -> Path | None:
    """Find the canonical index file in a package directory."""
    for name in INDEX_FILENAMES:
        candidate = package_dir / name
        if candidate.exists():
            return candidate
    return None


def extract_file_rows(index_text: str) -> list[str]:
    """
    Extract file paths from the Files table in 00-index.md.
    Looks for markdown table rows of the form: | N | path/to/file.md | ... |
    The path cell may contain plain text, backtick-wrapped text, or a markdown link.
    Returns a list of relative file path strings.
    """
    # Regex to extract href from markdown link: [label](href)
    _md_link_re = re.compile(r"\[.*?\]\((.+?)\)")

    paths = []
    in_table = False
    for line in index_text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            if in_table:
                break
            continue
        # Skip separator rows (e.g. |---|---|)
        if re.match(r"^\|[\s\-|:]+\|$", stripped):
            continue
        # Detect header row (contains "File" or "file" in second column)
        parts = [p.strip() for p in stripped.strip("|").split("|")]
        if len(parts) < 2:
            continue
        if not in_table and parts[1].strip().lower() in ("file", "path"):
            in_table = True
            continue
        if not in_table and "#" in parts[0] and re.search(r"\bfile\b", parts[1], re.I):
            in_table = True
            continue
        in_table = True
        path_cell = parts[1].strip()
        # Try markdown link first: [text](path)
        md_match = _md_link_re.search(path_cell)
        if md_match:
            path = md_match.group(1).strip()
        else:
            # Fall back: strip backticks and whitespace
            path = path_cell.strip("`").strip()
        skip_values = {"file", "path", "—", "-", ""}
        if path.lower() not in skip_values and not path.startswith("#"):
            paths.append(path)
    return paths


def load_config(repo_root: Path) -> dict:
    """Load configuration from .interface-skills.yaml if it exists."""
    config_path = repo_root / ".interface-skills.yaml"
    if config_path.exists():
        if yaml is None:
            print("Warning: PyYAML not installed. Skipping .interface-skills.yaml config.")
            return {}
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            print(f"Warning: Could not parse {config_path}: {e}")
    return {}


def validate_package(package_dir: Path, config: dict, verbose: bool = False) -> list[str]:
    """Validate a single example package directory. Returns a list of error strings."""
    errors = []
    name = package_dir.name

    # 1. Find index file
    index_path = find_index(package_dir)
    if index_path is None:
        errors.append(f"[{name}] MISSING index file (expected 00-index.md or manifest.md)")
        return errors

    index_text = index_path.read_text(encoding="utf-8")
    index_fm = parse_frontmatter(index_text)

    # 2. Check if intentionally_incomplete — skip completeness checks if so
    intentionally_incomplete = index_fm.get("intentionally_incomplete", "").lower() == "true"
    if intentionally_incomplete:
        if verbose:
            print(f"  [{name}] Skipping completeness checks (intentionally_incomplete: true)")

    # 3. Validate index frontmatter status
    index_status = index_fm.get("status", "")
    if index_status and index_status not in VALID_STATUSES:
        errors.append(
            f"[{name}] {index_path.name}: invalid status '{index_status}' "
            f"(valid: {', '.join(sorted(VALID_STATUSES))})"
        )

    # New: Validate agent_routing status
    routing_status = index_fm.get("agent_routing", "")
    if routing_status and routing_status not in VALID_ROUTING_STATUSES:
        errors.append(
            f"[{name}] {index_path.name}: invalid agent_routing '{routing_status}' "
            f"(valid: {', '.join(sorted(VALID_ROUTING_STATUSES))})"
        )

    # New: Check for "How agents find this package" section
    if "## How agents find this package" not in index_text and not intentionally_incomplete:
        errors.append(f"[{name}] {index_path.name}: missing '## How agents find this package' section")

    if intentionally_incomplete:
        return errors  # Skip file existence checks for intentionally broken packages

    # 4. Extract listed files from the Files table
    listed_files = extract_file_rows(index_text)

    # 5. Check each listed file exists on disk
    for rel_path in listed_files:
        abs_path = package_dir / rel_path
        if not abs_path.exists():
            errors.append(f"[{name}] Listed file not found on disk: {rel_path}")
            continue

        # 6. Validate frontmatter status of each listed file
        try:
            file_text = abs_path.read_text(encoding="utf-8")
            file_fm = parse_frontmatter(file_text)
            file_status = file_fm.get("status", "")
            if file_status and file_status not in VALID_STATUSES:
                errors.append(
                    f"[{name}] {rel_path}: invalid status '{file_status}'"
                )
        except Exception as exc:
            errors.append(f"[{name}] Could not read {rel_path}: {exc}")

    # 7. If component-specs/ is referenced, check the directory exists
    if any("component-specs/" in p for p in listed_files):
        comp_dir = package_dir / "component-specs"
        if not comp_dir.is_dir():
            errors.append(
                f"[{name}] component-specs/ directory referenced in index but does not exist"
            )

    # 8. If redlines/inspector-report.md is referenced, check it exists
    inspector_paths = [p for p in listed_files if "inspector-report" in p]
    for ip in inspector_paths:
        abs_ip = package_dir / ip
        if not abs_ip.exists():
            errors.append(f"[{name}] Inspector report listed but not found: {ip}")

    # 9. Validate routing reports
    routing_reports = [p for p in listed_files if "agent-routing-report" in p or p.endswith("ui-agent-routing-report.md")]
    for rp in routing_reports:
        abs_rp = package_dir / rp
        if abs_rp.exists():
            rp_text = abs_rp.read_text(encoding="utf-8")
            rp_fm = parse_frontmatter(rp_text)
            rp_routing_status = rp_fm.get("agent_routing", "")
            if rp_routing_status and rp_routing_status not in VALID_ROUTING_STATUSES:
                errors.append(f"[{name}] {rp}: invalid agent_routing status '{rp_routing_status}'")

            # If report is PASS, check required entry points (from config or defaults)
            if "**PASS**" in rp_text or "result: PASS" in rp_text or "Result: PASS" in rp_text:
                required = config.get("agent_routing", {}).get("required_entrypoints", [
                    "CLAUDE.md", "AGENTS.md", "GEMINI.md", ".github/copilot-instructions.md"
                ])
                for entry in required:
                    if entry not in rp_text:
                        # Report may not need all if it's a specific example, but generally it should mention them
                        # We'll make this a warning or a soft error for now
                        if verbose:
                            print(f"  Warning: [{name}] routing report {rp} claims PASS but doesn't mention required entry point '{entry}'")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate structural integrity of example spec packages."
    )
    parser.add_argument(
        "--examples-dir",
        default="examples",
        help="Root directory containing example packages (default: examples/)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print details for each package, including passes.",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).parent.parent
    examples_root = repo_root / args.examples_dir

    config = load_config(repo_root)

    if not examples_root.is_dir():
        print(f"ERROR: examples directory not found: {examples_root}", file=sys.stderr)
        return 1

    # Collect all immediate subdirectories of the examples root
    package_dirs = sorted(
        d for d in examples_root.iterdir()
        if d.is_dir() and not d.name.startswith(".")
    )

    if not package_dirs:
        print(f"No example packages found in {examples_root}")
        return 0

    all_errors: list[str] = []
    passed = 0
    failed = 0

    for pkg_dir in package_dirs:
        # A directory is a "container" (like orchestrator-states/) if it has no index file
        # itself but contains subdirectories that each have index files.
        # A directory is a regular package if it has its own index file (even if it also
        # has subdirectories like component-specs/ or redlines/).
        has_own_index = find_index(pkg_dir) is not None
        if has_own_index:
            errors = validate_package(pkg_dir, config, verbose=args.verbose)
            if errors:
                for e in errors:
                    print(f"  FAIL  {e}")
                all_errors.extend(errors)
                failed += 1
            else:
                if args.verbose:
                    print(f"  PASS  [{pkg_dir.name}]")
                passed += 1
        else:
            # No own index — treat as container and recurse into children
            subdirs = sorted(
                d for d in pkg_dir.iterdir()
                if d.is_dir() and not d.name.startswith(".")
            )
            if not subdirs:
                errors = [f"[{pkg_dir.name}] MISSING index file (expected 00-index.md or manifest.md)"]
                for e in errors:
                    print(f"  FAIL  {e}")
                all_errors.extend(errors)
                failed += 1
                continue
            for subdir in subdirs:
                sub_index = find_index(subdir)
                if sub_index is None:
                    err = f"[{pkg_dir.name}/{subdir.name}] MISSING index file"
                    print(f"  FAIL  {err}")
                    all_errors.append(err)
                    failed += 1
                    continue
                errors = validate_package(subdir, config, verbose=args.verbose)
                if errors:
                    for e in errors:
                        print(f"  FAIL  {e}")
                    all_errors.extend(errors)
                    failed += 1
                else:
                    if args.verbose:
                        print(f"  PASS  [{pkg_dir.name}/{subdir.name}]")
                    passed += 1

    print()
    print(f"Results: {passed} passed, {failed} failed, {len(all_errors)} total errors")

    if all_errors:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
