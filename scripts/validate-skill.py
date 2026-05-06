import os
import re

def validate_skills():
    skills_dir = os.path.join(os.path.dirname(__file__), '..', 'skills')
    
    if not os.path.exists(skills_dir):
        print("Error: skills/ directory not found.")
        return False
        
    all_passed = True
    
    for skill_folder in os.listdir(skills_dir):
        skill_path = os.path.join(skills_dir, skill_folder)
        
        if not os.path.isdir(skill_path):
            continue
            
        skill_md_path = os.path.join(skill_path, 'SKILL.md')
        
        if not os.path.exists(skill_md_path):
            print(f"[{skill_folder}] [FAIL] Missing SKILL.md")
            all_passed = False
            continue
            
        with open(skill_md_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Check frontmatter
        frontmatter_match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
        if not frontmatter_match:
            print(f"[{skill_folder}] [FAIL] Missing YAML frontmatter")
            all_passed = False
            continue
            
        frontmatter = frontmatter_match.group(1)
        
        # Check name
        name_match = re.search(r'name:\s*(.+)', frontmatter)
        if not name_match:
            print(f"[{skill_folder}] [FAIL] Missing 'name' in frontmatter")
            all_passed = False
        else:
            name = name_match.group(1).strip()
            if not re.match(r'^[a-z0-9\-]+$', name):
                print(f"[{skill_folder}] [FAIL] Name '{name}' is not lowercase hyphenated")
                all_passed = False
                
        # Check description
        desc_match = re.search(r'description:\s*(.+)', frontmatter)
        if not desc_match or not desc_match.group(1).strip():
            print(f"[{skill_folder}] [FAIL] Missing or empty 'description' in frontmatter")
            all_passed = False
            
        if all_passed:
            print(f"[{skill_folder}] [OK] Valid")

    return all_passed

if __name__ == '__main__':
    if validate_skills():
        print("\nAll skills passed validation! [SUCCESS]")
        exit(0)
    else:
        print("\nSome skills failed validation. [ERROR]")
        exit(1)
