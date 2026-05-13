import os
import shutil
import subprocess
import tempfile
import sys
from pathlib import Path

# Add the scripts directory to the path so we can import from skill_export
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
try:
    from skill_export import export_skill_to_directory
except ImportError:
    # If we can't import it, we'll fall back to a simple copy
    export_skill_to_directory = None

# --- CONFIGURATION ---
# List of skill sources to sync from
SOURCES = [
    {
        "name": "mattpocock",
        "url": "https://github.com/mattpocock/skills.git",
        "categories": ["engineering", "productivity", "misc", "personal"],
        "prefix": "",
        "skip_list": ["handoff"]
    },
    {
        "name": "sensemaking",
        "url": "https://github.com/ThorStarlord/sensemaking-skills.git",
        "categories": None, # None means look directly in the skills/ directory (flat structure)
        "prefix": "",
        "skip_list": []
    }
]
# ---------------------

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills"

def sync_skills():
    """
    Sync skills from external repositories.
    Handles prefixing and skipping based on configuration.
    """
    synced_total = 0
    skipped_total = 0
    
    for source in SOURCES:
        name = source["name"]
        url = source["url"]
        categories = source.get("categories")
        prefix = source.get("prefix", "")
        skip_list = source.get("skip_list", [])
        
        with tempfile.TemporaryDirectory() as tmpdir:
            print(f"\n--- Syncing Source: {name} ({url}) ---")
            print(f"Cloning...")
            try:
                subprocess.run(["git", "clone", "--depth", "1", url, tmpdir], check=True, capture_output=True)
            except subprocess.CalledProcessError as e:
                print(f"Error cloning repository: {e.stderr.decode()}")
                continue

            src_skills_root = Path(tmpdir) / "skills"
            if not src_skills_root.exists():
                print(f"Warning: 'skills' directory not found in {name}")
                continue
            
            # Determine which directories to scan
            scan_dirs = []
            if categories:
                for cat in categories:
                    cat_path = src_skills_root / cat
                    if cat_path.exists():
                        scan_dirs.append((cat, cat_path))
            else:
                # Flat structure: skills are directly in src_skills_root
                scan_dirs.append(("", src_skills_root))
            
            source_synced = 0
            source_skipped = 0
            
            for cat_name, scan_path in scan_dirs:
                for skill_path in scan_path.iterdir():
                    if not skill_path.is_dir():
                        continue
                    
                    skill_name = skill_path.name
                    skill_md = skill_path / "SKILL.md"
                    
                    if not skill_md.exists():
                        continue
                    
                    # Check skip list
                    if skill_name in skip_list:
                        print(f"Skipping {skill_name} (in skip_list)")
                        source_skipped += 1
                        continue
                    
                    # Apply prefix
                    target_skill_name = f"{prefix}{skill_name}"
                    target_path = SKILLS_DIR / target_skill_name
                    
                    log_label = f"{cat_name}/{skill_name}" if cat_name else skill_name
                    print(f"Syncing {log_label} -> {target_skill_name}")
                    
                    try:
                        if export_skill_to_directory:
                            # Use the repo's idiomatic export tool
                            export_skill_to_directory(skill_path, target_path)
                        else:
                            # Fallback copy
                            if target_path.exists():
                                shutil.rmtree(target_path)
                            shutil.copytree(skill_path, target_path)
                        source_synced += 1
                    except Exception as e:
                        print(f"  Failed to sync {skill_name}: {e}")

            print(f"Source {name} complete: {source_synced} synced, {source_skipped} skipped.")
            synced_total += source_synced
            skipped_total += source_skipped

    print(f"\nSummary: Successfully synced {synced_total} skills total (Skipped {skipped_total}).")

if __name__ == "__main__":
    sync_skills()
