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
# Change this to your fork URL once created: e.g. "https://github.com/ThorStarlord/skills.git"
REPO_URL = "https://github.com/mattpocock/skills.git"

# List of skills to skip during sync (e.g. because you have a better local version)
SKIP_LIST = ["handoff"]

# Optional prefix for synced skills. Set to "" if you want original names.
PREFIX = ""
# ---------------------

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills"

def sync_skills():
    """
    Sync skills from an external repository.
    Handles prefixing and skipping based on configuration.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        print(f"Cloning {REPO_URL}...")
        try:
            subprocess.run(["git", "clone", "--depth", "1", REPO_URL, tmpdir], check=True, capture_output=True)
        except subprocess.CalledProcessError as e:
            print(f"Error cloning repository: {e.stderr.decode()}")
            return

        src_skills_root = Path(tmpdir) / "skills"
        
        # Categories to sync based on Matt's repo structure
        categories = ["engineering", "productivity", "misc", "personal"]
        
        synced_count = 0
        skipped_count = 0
        for category in categories:
            cat_dir = src_skills_root / category
            if not cat_dir.exists():
                continue
                
            for skill_path in cat_dir.iterdir():
                if not skill_path.is_dir():
                    continue
                
                skill_name = skill_path.name
                skill_md = skill_path / "SKILL.md"
                
                if not skill_md.exists():
                    continue
                
                # Check skip list
                if skill_name in SKIP_LIST:
                    print(f"Skipping {category}/{skill_name} (in SKIP_LIST)")
                    skipped_count += 1
                    continue
                
                # Apply prefix
                target_skill_name = f"{PREFIX}{skill_name}"
                target_path = SKILLS_DIR / target_skill_name
                
                print(f"Syncing {category}/{skill_name} -> {target_skill_name}")
                
                try:
                    if export_skill_to_directory:
                        # Use the repo's idiomatic export tool
                        export_skill_to_directory(skill_path, target_path)
                    else:
                        # Fallback copy
                        if target_path.exists():
                            shutil.rmtree(target_path)
                        shutil.copytree(skill_path, target_path)
                    synced_count += 1
                except Exception as e:
                    print(f"  Failed to sync {skill_name}: {e}")

        print(f"\nSuccessfully synced {synced_count} skills (Skipped {skipped_count}).")

if __name__ == "__main__":
    sync_skills()
