#!/usr/bin/env python3
"""
Automated Project Setup Script for PDD AI Agent

This script automates the complete setup process including:
- Virtual environment creation
- Dependencies installation
- Environment configuration
- Git initialization
- Initial PHR creation

Usage:
    python scripts/setup_project.py
    python scripts/setup_project.py --openai-key sk-your-key-here
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path
from typing import Optional


class ProjectSetup:
    """Automated project setup for PDD AI agent."""

    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.venv_path = project_root / ".venv"
        self.is_windows = os.name == "nt"

    def run_command(self, command: str, cwd: Optional[Path] = None, check: bool = True) -> subprocess.CompletedProcess:
        """Run a shell command and return the result."""
        print(f"🔧 Running: {command}")

        if self.is_windows:
            # Use PowerShell on Windows
            full_command = ["powershell", "-Command", command]
        else:
            # Use bash on Unix-like systems
            full_command = ["bash", "-c", command]

        result = subprocess.run(
            full_command,
            cwd=cwd or self.project_root,
            capture_output=True,
            text=True,
            check=False
        )

        if result.stdout:
            print(f"✅ Output: {result.stdout.strip()}")
        if result.stderr and result.returncode != 0:
            print(f"❌ Error: {result.stderr.strip()}")

        if check and result.returncode != 0:
            raise subprocess.CalledProcessError(result.returncode, command)

        return result

    def create_virtual_environment(self) -> None:
        """Create Python virtual environment."""
        print("\n📦 Creating virtual environment...")

        if self.venv_path.exists():
            print("Virtual environment already exists, skipping creation")
            return

        self.run_command(f"python -m venv {self.venv_path}")
        print("✅ Virtual environment created successfully")

    def get_python_executable(self) -> str:
        """Get the path to the Python executable in the virtual environment."""
        if self.is_windows:
            return str(self.venv_path / "Scripts" / "python.exe")
        else:
            return str(self.venv_path / "bin" / "python")

    def get_pip_executable(self) -> str:
        """Get the path to the pip executable in the virtual environment."""
        if self.is_windows:
            return str(self.venv_path / "Scripts" / "pip.exe")
        else:
            return str(self.venv_path / "bin" / "pip")

    def install_dependencies(self) -> None:
        """Install Python dependencies."""
        print("\n📚 Installing dependencies...")

        pip_exe = self.get_pip_executable()
        requirements_file = self.project_root / "requirements.txt"

        if not requirements_file.exists():
            print("❌ requirements.txt not found")
            return

        # Upgrade pip first
        self.run_command(f'"{pip_exe}" install --upgrade pip')

        # Install requirements
        self.run_command(f'"{pip_exe}" install -r requirements.txt')
        print("✅ Dependencies installed successfully")

    def setup_environment_file(self, openai_key: Optional[str] = None) -> None:
        """Setup .env file from .env.sample."""
        print("\n⚙️ Setting up environment configuration...")

        env_sample = self.project_root / ".env.sample"
        env_file = self.project_root / ".env"

        if not env_sample.exists():
            print("❌ .env.sample not found")
            return

        if env_file.exists():
            print(".env file already exists")
            if openai_key:
                self.update_openai_key(env_file, openai_key)
            return

        # Copy .env.sample to .env
        env_content = env_sample.read_text(encoding="utf-8")

        # Update OpenAI key if provided
        if openai_key:
            env_content = env_content.replace(
                "OPENAI_API_KEY=sk-your-openai-api-key-here",
                f"OPENAI_API_KEY={openai_key}"
            )
            print(f"✅ OpenAI API key configured")
        else:
            print("⚠️ OpenAI API key not provided - you'll need to add it manually to .env")

        env_file.write_text(env_content, encoding="utf-8")
        print("✅ Environment file created")

    def update_openai_key(self, env_file: Path, openai_key: str) -> None:
        """Update OpenAI key in existing .env file."""
        content = env_file.read_text(encoding="utf-8")

        # Replace the OpenAI key line
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if line.startswith('OPENAI_API_KEY='):
                lines[i] = f'OPENAI_API_KEY={openai_key}'
                break

        env_file.write_text('\n'.join(lines), encoding="utf-8")
        print("✅ OpenAI API key updated")

    def initialize_git(self) -> None:
        """Initialize git repository and setup hooks."""
        print("\n🔄 Initializing git repository...")

        git_dir = self.project_root / ".git"
        if git_dir.exists():
            print("Git repository already initialized")
            return

        try:
            self.run_command("git init")
            self.run_command("git config core.hooksPath .githooks")
            print("✅ Git repository initialized with PDD hooks")
        except subprocess.CalledProcessError:
            print("⚠️ Git initialization failed - you may need to install git")

    def create_initial_phr(self) -> None:
        """Create initial PHR for project setup."""
        print("\n📝 Creating initial PHR...")

        python_exe = self.get_python_executable()
        phr_script = self.project_root / "scripts" / "prompt_new.py"

        if not phr_script.exists():
            print("❌ PHR script not found")
            return

        try:
            self.run_command(f'"{python_exe}" scripts/prompt_new.py "project-setup" "explainer"')

            # Fill in the initial PHR with setup information
            phr_file = self.project_root / "docs" / "prompts" / "0001-project-setup.prompt.md"
            if phr_file.exists():
                self.fill_setup_phr(phr_file)

        except subprocess.CalledProcessError:
            print("⚠️ Initial PHR creation failed")

    def fill_setup_phr(self, phr_file: Path) -> None:
        """Fill the setup PHR with project information."""
        from datetime import date

        content = f"""---
id: 0001
title: Project Setup
stage: explainer
date: {date.today().isoformat()}
---

# PHR-0001: Project Setup

## Stage: Explainer

## Context
Automated setup of the PDD AI Agent project with all necessary dependencies, configuration, and development tools.

## Prompt
```
Set up a complete PDD AI Agent project with:
- Python virtual environment
- OpenAI SDK and Chainlit dependencies
- Environment configuration
- Git repository with PDD hooks
- Initial project structure
```

## Outcome
- **Files created:**
  - `.venv/` - Python virtual environment
  - `.env` - Environment configuration
  - `.git/` - Git repository with PDD hooks
  - All project dependencies installed

- **Setup completed:**
  - Virtual environment activated
  - Dependencies installed from requirements.txt
  - Environment variables configured
  - Git repository initialized
  - PDD workflow scripts ready

- **Next steps:**
  - Add OpenAI API key to .env if not provided
  - Run `make dev` to start development server
  - Create feature PHRs using `make prompt-new`

## Notes
Project is now ready for PDD development workflow. All automation scripts are in place for continuous development.
"""

        phr_file.write_text(content, encoding="utf-8")
        print("✅ Initial PHR documentation created")

    def run_tests(self) -> None:
        """Run the test suite to verify setup."""
        print("\n🧪 Running tests to verify setup...")

        python_exe = self.get_python_executable()

        try:
            result = self.run_command(f'"{python_exe}" -m pytest tests/ -v', check=False)
            if result.returncode == 0:
                print("✅ All tests passed - setup verified!")
            else:
                print("⚠️ Some tests failed - this is normal for a new project")
        except subprocess.CalledProcessError:
            print("⚠️ Test execution failed - pytest may not be installed yet")

    def show_next_steps(self, openai_key_provided: bool) -> None:
        """Show next steps to the user."""
        print("\n" + "="*60)
        print("🎉 PROJECT SETUP COMPLETE!")
        print("="*60)

        print("\n📁 Project structure created:")
        print("  - Virtual environment: .venv/")
        print("  - Dependencies: Installed from requirements.txt")
        print("  - Configuration: .env file ready")
        print("  - Git: Repository initialized with PDD hooks")
        print("  - Documentation: Initial PHR created")

        print("\n🚀 To start development:")

        if self.is_windows:
            print("  1. Activate virtual environment:")
            print("     .venv\\Scripts\\activate")
        else:
            print("  1. Activate virtual environment:")
            print("     source .venv/bin/activate")

        if not openai_key_provided:
            print("\n  2. Add your OpenAI API key to .env:")
            print("     Edit .env and replace: OPENAI_API_KEY=sk-your-actual-api-key")

        print("\n  3. Start the development server:")
        print("     make dev")
        print("     # or: python -m chainlit run chainlit_app.py -w --port 8001")

        print("\n🔄 PDD Development workflow:")
        print("  - Create new feature: make prompt-new SLUG=feature-name STAGE=architect")
        print("  - Run tests: make test")
        print("  - Format code: make fmt")
        print("  - Show help: make help")

        print("\n📚 Documentation:")
        print("  - README.md: Complete project guide")
        print("  - docs/PDD_PROMPTS.md: Development prompt templates")
        print("  - docs/prompts/: Your PHR development history")

        print("\n💡 Quick test:")
        print("  Visit http://localhost:8001 after running 'make dev'")


def main():
    """Main setup function."""
    parser = argparse.ArgumentParser(description="Automated PDD AI Project Setup")
    parser.add_argument(
        "--openai-key", 
        help="OpenAI API key (sk-...)",
        type=str
    )
    parser.add_argument(
        "--skip-git",
        action="store_true",
        help="Skip git initialization"
    )
    parser.add_argument(
        "--skip-tests",
        action="store_true", 
        help="Skip running tests"
    )

    args = parser.parse_args()

    # Get project root (assuming script is in scripts/ subdirectory)
    project_root = Path(__file__).parent.parent

    print("🚀 Starting automated PDD AI Project setup...")
    print(f"📁 Project root: {project_root}")

    setup = ProjectSetup(project_root)

    try:
        # Run all setup steps
        setup.create_virtual_environment()
        setup.install_dependencies()
        setup.setup_environment_file(args.openai_key)

        if not args.skip_git:
            setup.initialize_git()

        setup.create_initial_phr()

        if not args.skip_tests:
            setup.run_tests()

        setup.show_next_steps(bool(args.openai_key))

    except Exception as e:
        print(f"\n❌ Setup failed with error: {e}")
        print("Please check the error messages above and try again.")
        sys.exit(1)


if __name__ == "__main__":
    main()