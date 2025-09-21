#!/usr/bin/env python3
        """
        Create new PHR (Prompt History Record) file following PDD methodology.

        Usage:
            python scripts/prompt_new.py "feature-name" "architect"
        """

        import sys
        import datetime
        from pathlib import Path


        def main():
            if len(sys.argv) < 2:
                print("Usage: python scripts/prompt_new.py <SLUG> [STAGE]")
                print("Stages: architect, red, green, refactor, explainer, adr, pr")
                sys.exit(1)

            slug = sys.argv[1]
            stage = sys.argv[2] if len(sys.argv) > 2 else "architect"

            # Create prompts directory
            prompts_dir = Path("docs/prompts")
            prompts_dir.mkdir(parents=True, exist_ok=True)

            # Find next PHR ID
            existing = sorted([p.name for p in prompts_dir.glob("[0-9][0-9][0-9][0-9]-*.prompt.md")])
            next_id = int(existing[-1].split("-")[0]) + 1 if existing else 1
            id_str = f"{next_id:04d}"

            date_str = datetime.date.today().isoformat()

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
<!-- Paste the exact prompt used with the AI assistant -->
```
[PASTE PROMPT HERE]
```

## Outcome
<!-- Document what was achieved -->
- **Files changed:** 
- **Tests added:** 
- **Key decisions:** 
- **Next steps:** 

## Notes
<!-- Any additional observations or learnings -->
"""

            # Write PHR file
            phr_path = prompts_dir / f"{id_str}-{slug}.prompt.md"
            phr_path.write_text(content, encoding="utf-8")

            print(f"✅ Created PHR-{id_str}: {phr_path}")
            print(f"📝 Stage: {stage}")
            print("🔥 Next: Add your prompt and document the outcome!")


        if __name__ == "__main__":
            main()
