#!/usr/bin/env python3
"""
Add automatic prompt recording to any existing PDD project
"""

import shutil
import sys
from pathlib import Path

def add_auto_recording(project_path="."):
    """Add automatic prompt recording to an existing PDD project"""
    project = Path(project_path)
    
    if not project.exists():
        print(f"❌ Project path {project_path} does not exist")
        return False
        
    print(f"🔧 Adding automatic prompt recording to {project.resolve()}")
    
    # Copy the required files from current project
    source_files = {
        "scripts/prompt_watcher.py": "Automatic prompt detection and recording",
        "scripts/dev_session.py": "Development session manager", 
        "start-dev.bat": "Windows development session starter",
        "watch.bat": "Prompt watcher only",
        "status.bat": "Session status checker"
    }
    
    for src_file, description in source_files.items():
        src = Path(__file__).parent / src_file
        dst = project / src_file
        
        if src.exists():
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            print(f"✅ Added {src_file} - {description}")
        else:
            print(f"⚠️  Source file not found: {src_file}")
            
    # Update requirements.txt if it exists
    req_file = project / "requirements.txt"
    if req_file.exists():
        content = req_file.read_text()
        if "pyperclip" not in content:
            with open(req_file, "a") as f:
                f.write("\n# Auto prompt recording\npyperclip>=1.8.0\npsutil>=5.9.0\n")
            print("✅ Added required packages to requirements.txt")
    
    print("\n🎉 Automatic prompt recording added successfully!")
    print("\n🚀 Usage:")
    print("   start-dev.bat    - Start full development session") 
    print("   watch.bat        - Start prompt watcher only")
    print("   status.bat       - Check status")
    print("\n💡 Just copy AI prompts (Ctrl+C) and they'll be auto-recorded!")
    
    return True

if __name__ == "__main__":
    project_path = sys.argv[1] if len(sys.argv) > 1 else "."
    add_auto_recording(project_path)