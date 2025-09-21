#!/usr/bin/env python3
"""
Automatic Prompt Watcher - Monitors clipboard for AI prompts and auto-creates PHRs
"""

import time
import hashlib
import json
from pathlib import Path
import pyperclip
import re
from datetime import datetime, timedelta
import threading
import sys

class PromptWatcher:
    def __init__(self):
        self.last_clipboard = ""
        self.last_hash = ""
        self.running = False
        self.phr_counter = self.get_next_phr_id()
        self.session_file = Path("docs/prompts/.session.json")
        self.load_session()
        
    def get_next_phr_id(self):
        """Get next PHR ID"""
        prompts_dir = Path("docs/prompts")
        prompts_dir.mkdir(parents=True, exist_ok=True)
        
        existing = sorted([p.name for p in prompts_dir.glob("[0-9][0-9][0-9][0-9]-*.prompt.md")])
        return int(existing[-1].split("-")[0]) + 1 if existing else 1
    
    def load_session(self):
        """Load previous session data"""
        if self.session_file.exists():
            try:
                with open(self.session_file, 'r') as f:
                    self.session_data = json.load(f)
            except:
                self.session_data = {'auto_created': [], 'last_activity': None}
        else:
            self.session_data = {'auto_created': [], 'last_activity': None}
    
    def save_session(self):
        """Save session data"""
        self.session_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.session_file, 'w') as f:
            json.dump(self.session_data, f, indent=2)
    
    def is_ai_prompt(self, text):
        """Detect if text looks like an AI prompt"""
        if len(text) < 50 or len(text) > 5000:
            return False
            
        ai_indicators = [
            r'\b(create|build|implement|design|generate|write|make)\b',
            r'\b(function|class|component|feature|system|api)\b',
            r'\b(test|debug|fix|refactor|optimize)\b',
            r'\b(please|can you|help me|i need|write a)\b',
            r'(```|```python|```javascript|```typescript)',
            r'\b(requirements?|specifications?|criteria)\b',
        ]
        
        matches = sum(1 for pattern in ai_indicators if re.search(pattern, text, re.IGNORECASE))
        return matches >= 2
    
    def extract_feature_name(self, prompt):
        """Extract a reasonable feature name from the prompt"""
        # Look for key phrases that indicate what's being built
        patterns = [
            r'(?:create|build|implement|design|make)\s+(?:a\s+)?([a-zA-Z\s]{2,30})(?:\s+that|\s+for|\s+which|\.)',
            r'([a-zA-Z\s]{2,30})\s+(?:system|component|feature|function|class|api)',
            r'(?:add|create)\s+([a-zA-Z\s]{2,30})\s+(?:functionality|support|feature)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, prompt, re.IGNORECASE)
            if match:
                name = match.group(1).strip()
                # Clean up the name
                name = re.sub(r'\b(the|a|an)\b', '', name, flags=re.IGNORECASE).strip()
                name = re.sub(r'\s+', '-', name).lower()
                return name[:30]  # Limit length
        
        # Fallback: use first few meaningful words
        words = re.findall(r'\b[a-zA-Z]{3,}\b', prompt)[:3]
        return '-'.join(words).lower() if words else 'auto-prompt'
    
    def detect_stage(self, prompt):
        """Auto-detect PDD stage"""
        prompt_lower = prompt.lower()
        
        if any(word in prompt_lower for word in ['design', 'architecture', 'plan', 'requirements', 'approach']):
            return 'architect'
        elif any(word in prompt_lower for word in ['test', 'failing', 'red', 'spec', 'should fail']):
            return 'red'
        elif any(word in prompt_lower for word in ['implement', 'code', 'make tests pass', 'write the']):
            return 'green'
        elif any(word in prompt_lower for word in ['refactor', 'improve', 'cleanup', 'optimize', 'reorganize']):
            return 'refactor'
        elif any(word in prompt_lower for word in ['explain', 'document', 'summary', 'what does']):
            return 'explainer'
        else:
            return 'architect'
    
    def create_auto_phr(self, prompt_text):
        """Automatically create PHR from detected prompt"""
        feature_name = self.extract_feature_name(prompt_text)
        stage = self.detect_stage(prompt_text)
        
        id_str = f"{self.phr_counter:04d}"
        date_str = datetime.now().date().isoformat()
        timestamp = datetime.now().isoformat()
        
        content = f"""---
id: {id_str}
title: {feature_name.replace('-', ' ').title()}
stage: {stage}
date: {date_str}
auto_created: true
---

# PHR-{id_str}: {feature_name.replace('-', ' ').title()}

## Stage: {stage.title()}

## Context
<!-- AUTO-DETECTED: Add context about what you're building -->

## Prompt
<!-- AUTO-CAPTURED from clipboard at {timestamp} -->
```
{prompt_text}
```

## Outcome
<!-- TODO: Document what was achieved -->
- **Files changed:** [Update after implementation]
- **Tests added:** [Update after testing]
- **Key decisions:** [Update with decisions made]
- **Next steps:** [Update with next actions]

## Notes
<!-- AUTO-CREATED: Add any additional observations -->
- Auto-detected as {stage} stage prompt
- Feature name extracted: {feature_name}
- Created automatically by PromptWatcher

## Session Info
- **Auto-created:** {timestamp}
- **Clipboard hash:** {hashlib.md5(prompt_text.encode()).hexdigest()[:8]}
"""

        # Write PHR file
        prompts_dir = Path("docs/prompts")
        phr_path = prompts_dir / f"{id_str}-{feature_name}.prompt.md"
        phr_path.write_text(content, encoding="utf-8")
        
        # Update session tracking
        self.session_data['auto_created'].append({
            'id': id_str,
            'feature': feature_name,
            'stage': stage,
            'timestamp': timestamp,
            'file': str(phr_path)
        })
        self.session_data['last_activity'] = timestamp
        self.save_session()
        
        self.phr_counter += 1
        
        print(f"\n🤖 AUTO-PHR CREATED!")
        print(f"📝 PHR-{id_str}: {feature_name.replace('-', ' ').title()}")
        print(f"🎯 Stage: {stage}")
        print(f"📁 File: {phr_path}")
        print(f"⏰ {datetime.now().strftime('%H:%M:%S')}")
        print("💡 Remember to update Context and Outcome sections!")
        
        return phr_path
    
    def watch_clipboard(self):
        """Main clipboard monitoring loop"""
        print("🔍 PromptWatcher started - monitoring clipboard for AI prompts...")
        print("📋 Copy AI prompts to clipboard and they'll be auto-recorded!")
        print("⏹️  Press Ctrl+C to stop")
        
        self.running = True
        
        try:
            while self.running:
                try:
                    current_clipboard = pyperclip.paste()
                    current_hash = hashlib.md5(current_clipboard.encode()).hexdigest()
                    
                    # Check if clipboard changed and contains an AI prompt
                    if (current_hash != self.last_hash and 
                        current_clipboard != self.last_clipboard and
                        self.is_ai_prompt(current_clipboard)):
                        
                        print(f"\n🔍 Detected potential AI prompt ({len(current_clipboard)} chars)")
                        
                        # Create PHR automatically
                        self.create_auto_phr(current_clipboard)
                        
                        self.last_clipboard = current_clipboard
                        self.last_hash = current_hash
                    
                    time.sleep(1)  # Check every second
                    
                except Exception as e:
                    print(f"⚠️  Error monitoring clipboard: {e}")
                    time.sleep(5)
                    
        except KeyboardInterrupt:
            print("\n⏹️  PromptWatcher stopped")
            self.running = False

def main():
    if len(sys.argv) > 1 and sys.argv[1] == 'status':
        # Show session status
        watcher = PromptWatcher()
        if watcher.session_data['auto_created']:
            print("📊 Auto-created PHRs this session:")
            for phr in watcher.session_data['auto_created'][-5:]:  # Show last 5
                print(f"   PHR-{phr['id']}: {phr['feature']} ({phr['stage']})")
        else:
            print("📭 No auto-created PHRs yet")
        return
    
    # Start watching
    watcher = PromptWatcher()
    watcher.watch_clipboard()

if __name__ == "__main__":
    main()