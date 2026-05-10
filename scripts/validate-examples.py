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
    python scripts/validate-examples.py --strict-local-sources
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
    seen = set()
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
        if path.lower() not in skip_values and not path.startswith("#") and path not in seen:
            paths.append(path)
            seen.add(path)

    # Support bullet-link indexes used by several fixtures.
    # Example: - [brief.md](./brief.md)
    bullet_link_re = re.compile(r"^\s*[-*]\s+\[[^\]]+\]\(([^)]+)\)")
    for line in index_text.splitlines():
        match = bullet_link_re.match(line)
        if not match:
            continue
        href = match.group(1).strip()
        if not href:
            continue
        # Ignore in-document anchors and absolute URLs.
        if href.startswith("#") or re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", href):
            continue
        normalized = href
        if normalized.startswith("./"):
            normalized = normalized[2:]
        if normalized and normalized not in seen:
            paths.append(normalized)
            seen.add(normalized)

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


def _load_yaml_file(file_path: Path) -> dict:
    if yaml is None:
        return {}
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def _extract_path_entries(value) -> list[str]:
    """Extract path entries from either string lists or object lists with {path, role}."""
    paths: list[str] = []
    if isinstance(value, list):
        for item in value:
            if isinstance(item, str) and item.strip():
                paths.append(item.strip())
            elif isinstance(item, dict):
                path_value = item.get("path")
                if isinstance(path_value, str) and path_value.strip():
                    paths.append(path_value.strip())
    return paths


def validate_package(
    package_dir: Path,
    config: dict,
    verbose: bool = False,
    strict_local_sources: bool = False,
) -> tuple[list[str], list[str]]:
    """Validate a single example package directory. Returns (errors, warnings)."""
    errors = []
    warnings = []
    name = package_dir.name

    # 1. Find index file
    index_path = find_index(package_dir)
    if index_path is None:
        errors.append(f"[{name}] MISSING index file (expected 00-index.md or manifest.md)")
        return errors, warnings

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

    # New: Rubric fixtures must include a reproducibility manifest.
    fixture_type = index_fm.get("fixture_type", "").lower()
    if fixture_type == "rubric":
        fixture_manifest = package_dir / "fixture.yaml"
        if not fixture_manifest.exists():
            errors.append(f"[{name}] fixture_type=rubric requires fixture.yaml")
        else:
            fixture_text = fixture_manifest.read_text(encoding="utf-8")
            fixture_data = _load_yaml_file(fixture_manifest)
            required_scalar_keys = [
                "fixture_id:",
                "source_repo:",
                "source_commit:",
                "surface:",
                "workflow:",
            ]
            for key in required_scalar_keys:
                if key not in fixture_text:
                    errors.append(f"[{name}] fixture.yaml missing required key '{key[:-1]}'")

            # Minimal list checks for source and routing context.
            if "source_files:" not in fixture_text:
                errors.append(f"[{name}] fixture.yaml missing 'source_files' list")
            elif not re.search(r"^\s*-\s+\S+", fixture_text, re.MULTILINE):
                errors.append(f"[{name}] fixture.yaml source_files list appears empty")

            if "routing_files:" not in fixture_text:
                errors.append(f"[{name}] fixture.yaml missing 'routing_files' list")

        # Guard: if fixture files look auto-generated, require explicit refresh marker.
        auto_generated_pattern = re.compile(
            r"(?i)(fixture_generated:\s*true|generated from current state|auto-generated|this report was generated)"
        )
        auto_generated_hits = []
        for md_file in package_dir.rglob("*.md"):
            md_text = md_file.read_text(encoding="utf-8")
            if auto_generated_pattern.search(md_text):
                auto_generated_hits.append(md_file)

        if auto_generated_hits:
            notes_path = package_dir / "notes.md"
            if not notes_path.exists():
                errors.append(
                    f"[{name}] auto-generated-looking files detected but notes.md is missing"
                )
            else:
                notes_text = notes_path.read_text(encoding="utf-8")
                if "Fixture refresh marker:" not in notes_text:
                    rel_hits = ", ".join(str(p.relative_to(package_dir)) for p in auto_generated_hits[:5])
                    errors.append(
                        f"[{name}] auto-generated-looking fixture files require explicit 'Fixture refresh marker:' in notes.md (examples: {rel_hits})"
                    )

            if strict_local_sources:
                local_hint = fixture_data.get("source_repo_local_hint") if fixture_data else None
                if not isinstance(local_hint, str) or not local_hint.strip():
                    warnings.append(f"[{name}] strict-local-sources: fixture.yaml missing source_repo_local_hint; skipped local source checks")
                else:
                    local_repo = Path(local_hint)
                    if not local_repo.exists():
                        warnings.append(
                            f"[{name}] strict-local-sources: source_repo_local_hint not found ({local_repo}); skipped local source checks"
                        )
                    else:
                        source_paths = _extract_path_entries(fixture_data.get("source_files"))
                        routing_paths = _extract_path_entries(fixture_data.get("routing_files"))

                        if not source_paths:
                            errors.append(f"[{name}] strict-local-sources: source_files list is empty in fixture.yaml")
                        if not routing_paths:
                            errors.append(f"[{name}] strict-local-sources: routing_files list is empty in fixture.yaml")

                        for rel_path in source_paths:
                            abs_path = local_repo / rel_path
                            if not abs_path.exists():
                                errors.append(
                                    f"[{name}] strict-local-sources: missing source file at {abs_path}"
                                )

                        for rel_path in routing_paths:
                            abs_path = local_repo / rel_path
                            if not abs_path.exists():
                                errors.append(
                                    f"[{name}] strict-local-sources: missing routing file at {abs_path}"
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
        return errors, warnings  # Skip file existence checks for intentionally broken packages

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

    # 10. Lint report supersession rules (for realistic multi-report packages)
    lint_reports = sorted(package_dir.glob("reports/SPEC-LINT-REPORT*.md"))
    if len(lint_reports) > 1:
        active_reports = []
        for report_path in lint_reports:
            report_text = report_path.read_text(encoding="utf-8")
            report_fm = parse_frontmatter(report_text)
            if report_fm.get("active_report", "").lower() == "true":
                active_reports.append(report_path)

            supersedes = report_fm.get("supersedes", "")
            if supersedes:
                supersedes_path = package_dir / supersedes
                if not supersedes_path.exists():
                    errors.append(f"[{name}] {report_path.relative_to(package_dir)} supersedes missing file: {supersedes}")

        if len(active_reports) == 0:
            errors.append(f"[{name}] Multiple lint reports found but none marked active_report: true")
        elif len(active_reports) > 1:
            errors.append(f"[{name}] Multiple lint reports marked active_report: true")

    # 11. Docs-sync FAIL must hand off to ui-agent-routing
    docs_sync_report = package_dir / "reports" / "DOCS-SYNC-REPORT.md"
    if docs_sync_report.exists():
        ds_text = docs_sync_report.read_text(encoding="utf-8")
        ds_fm = parse_frontmatter(ds_text)
        result = ds_fm.get("result", "").lower()
        if result == "fail":
            next_skill = ds_fm.get("next_skill", "")
            if next_skill != "ui-agent-routing":
                errors.append(f"[{name}] reports/DOCS-SYNC-REPORT.md result=fail must set next_skill: ui-agent-routing")

    # 12. Agent-routing PASS should mention a direct 00-index link
    routing_summary = package_dir / "reports" / "UI-AGENT-ROUTING-SUMMARY.md"
    if routing_summary.exists():
        rs_text = routing_summary.read_text(encoding="utf-8")
        rs_fm = parse_frontmatter(rs_text)
        if rs_fm.get("result", "").lower() == "pass" and "00-index.md" not in rs_text:
            errors.append(f"[{name}] reports/UI-AGENT-ROUTING-SUMMARY.md result=pass but no direct 00-index.md link found")

    # 13. Critical redlines must map to issues or reconcile decisions
    redline_report = package_dir / "input" / "07-redline-audit.md"
    issues_plan = package_dir / "reports" / "GITHUB-ISSUES-PLAN.md"
    reconcile_report = package_dir / "reports" / "SPEC-RECONCILE-SUMMARY.md"
    if redline_report.exists() and issues_plan.exists() and reconcile_report.exists():
        redline_text = redline_report.read_text(encoding="utf-8")
        issues_text = issues_plan.read_text(encoding="utf-8")
        reconcile_text = reconcile_report.read_text(encoding="utf-8")
        critical_ids = sorted(set(re.findall(r"\[Critical\]\s*(K-\d+)", redline_text)))
        for item_id in critical_ids:
            if item_id not in issues_text and item_id not in reconcile_text:
                errors.append(f"[{name}] Critical redline item {item_id} missing issue/reconcile coverage")

    # 14. Subjective fixtures must include explicit human-review markers
    fixture_notes = package_dir / "notes.md"
    if fixture_notes.exists():
        notes_text = fixture_notes.read_text(encoding="utf-8")
        if "Human review required" not in notes_text:
            errors.append(f"[{name}] notes.md missing 'Human review required' marker")

    return errors, warnings


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
    parser.add_argument(
        "--strict-local-sources",
        action="store_true",
        help="When fixture.yaml provides source_repo_local_hint and the path exists, verify all source_files and routing_files exist locally.",
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
    all_warnings: list[str] = []
    passed = 0
    failed = 0

    for pkg_dir in package_dirs:
        # A directory is a "container" (like orchestrator-states/) if it has no index file
        # itself but contains subdirectories that each have index files.
        # A directory is a regular package if it has its own index file (even if it also
        # has subdirectories like component-specs/ or redlines/).
        has_own_index = find_index(pkg_dir) is not None
        if has_own_index:
            errors, warnings = validate_package(
                pkg_dir,
                config,
                verbose=args.verbose,
                strict_local_sources=args.strict_local_sources,
            )
            if errors:
                for e in errors:
                    print(f"  FAIL  {e}")
                all_errors.extend(errors)
                failed += 1
            else:
                if args.verbose:
                    print(f"  PASS  [{pkg_dir.name}]")
                passed += 1
            for w in warnings:
                print(f"  WARN  {w}")
            all_warnings.extend(warnings)
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
                errors, warnings = validate_package(
                    subdir,
                    config,
                    verbose=args.verbose,
                    strict_local_sources=args.strict_local_sources,
                )
                if errors:
                    for e in errors:
                        print(f"  FAIL  {e}")
                    all_errors.extend(errors)
                    failed += 1
                else:
                    if args.verbose:
                        print(f"  PASS  [{pkg_dir.name}/{subdir.name}]")
                    passed += 1
                for w in warnings:
                    print(f"  WARN  {w}")
                all_warnings.extend(warnings)

    print()
    print(
        f"Results: {passed} passed, {failed} failed, "
        f"{len(all_errors)} total errors, {len(all_warnings)} total warnings"
    )

    if all_errors:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
