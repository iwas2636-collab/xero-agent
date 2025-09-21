#!/usr/bin/env python3
"""
Enhanced PHR tool with automatic prompt capture from clipboard
"""

import sys
import datetime
import subprocess
from pathlib import Path
import pyperclip  # pip install pyperclip

def get_clipboard_content():
    """Get content from clipboard if available"""
    try:
        return pyperclip.paste()
    except:
        return ""

def detect_stage_from_prompt(prompt_content):
    """Auto-detect PDD stage from prompt content"""
    prompt_lower = prompt_content.lower()
    
    if any(word in prompt_lower for word in ['design', 'architecture', 'plan', 'requirements']):
        return 'architect'
    elif any(word in prompt_lower for word in ['test', 'failing', 'red', 'spec']):
        return 'red'
    elif any(word in prompt_lower for word in ['implement', 'code', 'make tests pass']):
        return 'green'
    elif any(word in prompt_lower for word in ['refactor', 'improve', 'cleanup', 'optimize']):
        return 'refactor'
    elif any(word in prompt_lower for word in ['explain', 'document', 'summary']):
        return 'explainer'
    else:
        return 'architect'

def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/prompt_enhanced.py <SLUG> [STAGE] [--clipboard]")
        print("Stages: architect, red, green, refactor, explainer, adr, pr")
        print("Use --clipboard to auto-capture prompt from clipboard")
        sys.exit(1)

    slug = sys.argv[1]
    auto_stage = len(sys.argv) < 3 or sys.argv[2] == '--clipboard'
    use_clipboard = '--clipboard' in sys.argv
    
    # Get clipboard content if requested
    clipboard_content = ""
    if use_clipboard:
        clipboard_content = get_clipboard_content()
        if clipboard_content:
            print(f"📋 Captured {len(clipboard_content)} characters from clipboard")
            
    # Auto-detect stage from clipboard content
    if auto_stage and clipboard_content:
        stage = detect_stage_from_prompt(clipboard_content)
        print(f"🤖 Auto-detected stage: {stage}")
    else:
        stage = sys.argv[2] if len(sys.argv) > 2 and sys.argv[2] != '--clipboard' else "architect"

    # Create prompts directory
    prompts_dir = Path("docs/prompts")
    prompts_dir.mkdir(parents=True, exist_ok=True)

    # Find next PHR ID
    existing = sorted([p.name for p in prompts_dir.glob("[0-9][0-9][0-9][0-9]-*.prompt.md")])
    next_id = int(existing[-1].split("-")[0]) + 1 if existing else 1
    id_str = f"{next_id:04d}"

    date_str = datetime.date.today().isoformat()
    
    # Pre-fill prompt if clipboard content available
    prompt_section = f"```\n{clipboard_content}\n```" if clipboard_content else "[PASTE PROMPT HERE]"

    content = f"""---
id: {id_str}
title: {slug.replace('-', ' ').title()}
stage: {stage}
date: {date_str}
---

# PHR-{id_str}: {slug.replace('-', ' ').title()}

## Stage: {stage.title()}

## Context
<!-- Describe the current situation and what needs to be done -->

## Prompt
<!-- The exact prompt used with the AI assistant -->
{prompt_section}

## Outcome
<!-- Document what was achieved -->
- **Files changed:** 
- **Tests added:** 
- **Key decisions:** 
- **Next steps:** 

## Notes
<!-- Any additional observations or learnings -->

## Session Info
- **Created:** {datetime.datetime.now().isoformat()}
- **Git branch:** {get_git_branch()}
- **Modified files:** {get_modified_files()}
"""

    # Write PHR file
    phr_path = prompts_dir / f"{id_str}-{slug}.prompt.md"
    phr_path.write_text(content, encoding="utf-8")

    print(f"✅ Created PHR-{id_str}: {phr_path}")
    print(f"📝 Stage: {stage}")
    if clipboard_content:
        print(f"📋 Prompt auto-filled from clipboard")
    print("🔥 Next: Complete the Context and Outcome sections!")

def get_git_branch():
    """Get current git branch"""
    try:
        result = subprocess.run(['git', 'branch', '--show-current'], 
                              capture_output=True, text=True)
        return result.stdout.strip() if result.returncode == 0 else "unknown"
    except:
        return "unknown"

def get_modified_files():
    """Get list of modified files"""
    try:
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            files = [line[3:] for line in result.stdout.split('\n') if line.strip()]
            return ', '.join(files[:5]) + ('...' if len(files) > 5 else '')
        return "none"
    except:
        return "unknown"

if __name__ == "__main__":
    main()