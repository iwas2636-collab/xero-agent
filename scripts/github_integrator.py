#!/usr/bin/env python3
"""
GitHub Integration Manager for PDD Projects
Automates repository creation, version control, and GitHub features
"""

import os
import subprocess
import json
import requests
from pathlib import Path
from typing import Optional, Dict, Any

class GitHubIntegrator:
    def __init__(self):
        self.config_file = Path("config.json")
        self.git_config = {}
        self.github_token = None
        self.github_username = None
        
    def load_config(self):
        """Load existing configuration"""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                config = json.load(f)
                self.git_config = config.get('git_integration', {})
                oauth_clients = config.get('oauth_clients', {})
                github_oauth = oauth_clients.get('github', {})
                self.github_token = self.git_config.get('access_token') or github_oauth.get('access_token')
                self.github_username = self.git_config.get('username')
    
    def save_config(self, config_updates):
        """Save configuration updates"""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                config = json.load(f)
        else:
            config = {}
            
        if 'git_integration' not in config:
            config['git_integration'] = {}
            
        config['git_integration'].update(config_updates)
        
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
    
    def check_git_installation(self):
        """Check if Git is installed and configured"""
        try:
            # Check Git installation
            result = subprocess.run(['git', '--version'], capture_output=True, text=True)
            if result.returncode != 0:
                print("❌ Git is not installed or not in PATH")
                print("📥 Please install Git from: https://git-scm.com/downloads")
                return False
                
            print(f"✅ Git installed: {result.stdout.strip()}")
            
            # Check Git configuration
            try:
                name_result = subprocess.run(['git', 'config', 'user.name'], capture_output=True, text=True)
                email_result = subprocess.run(['git', 'config', 'user.email'], capture_output=True, text=True)
                
                if name_result.returncode == 0 and email_result.returncode == 0:
                    print(f"✅ Git configured for: {name_result.stdout.strip()} <{email_result.stdout.strip()}>")
                    return True
                else:
                    print("⚠️  Git not configured with user details")
                    return self.configure_git()
                    
            except Exception:
                print("⚠️  Could not check Git configuration")
                return self.configure_git()
                
        except FileNotFoundError:
            print("❌ Git is not installed or not in PATH")
            print("📥 Please install Git from: https://git-scm.com/downloads")
            return False
    
    def configure_git(self):
        """Configure Git with user details"""
        print("\n🔧 Git Configuration Required")
        print("-" * 30)
        
        name = input("Enter your Git username: ").strip()
        email = input("Enter your Git email: ").strip()
        
        if name and email:
            try:
                subprocess.run(['git', 'config', '--global', 'user.name', name], check=True)
                subprocess.run(['git', 'config', '--global', 'user.email', email], check=True)
                print(f"✅ Git configured for: {name} <{email}>")
                return True
            except subprocess.CalledProcessError as e:
                print(f"❌ Failed to configure Git: {e}")
                return False
        else:
            print("❌ Name and email are required")
            return False
    
    def get_github_token(self):
        """Get GitHub personal access token"""
        if self.github_token:
            return self.github_token
            
        print("\n🔐 GitHub Personal Access Token Required")
        print("-" * 40)
        print("To create repositories and manage them, you need a GitHub Personal Access Token.")
        print("\n📋 Steps to create token:")
        print("1. Go to: https://github.com/settings/tokens")
        print("2. Click 'Generate new token (classic)'")
        print("3. Select scopes: repo, workflow, user")
        print("4. Copy the generated token")
        print()
        
        token = input("Enter your GitHub Personal Access Token: ").strip()
        if token:
            self.github_token = token
            
            # Test the token
            if self.test_github_token(token):
                # Save token to config
                self.save_config({'access_token': token, 'username': self.github_username})
                return token
            else:
                print("❌ Invalid token or insufficient permissions")
                return None
        else:
            print("❌ Token is required for GitHub integration")
            return None
    
    def test_github_token(self, token):
        """Test GitHub token and get username"""
        try:
            headers = {
                'Authorization': f'token {token}',
                'Accept': 'application/vnd.github.v3+json'
            }
            
            response = requests.get('https://api.github.com/user', headers=headers)
            if response.status_code == 200:
                user_data = response.json()
                self.github_username = user_data['login']
                print(f"✅ GitHub token valid for user: {self.github_username}")
                return True
            else:
                print(f"❌ GitHub API error: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Error testing GitHub token: {e}")
            return False
    
    def init_local_repository(self):
        """Initialize local Git repository"""
        if Path('.git').exists():
            print("✅ Git repository already initialized")
            return True
            
        try:
            subprocess.run(['git', 'init'], check=True, capture_output=True)
            print("✅ Git repository initialized")
            
            # Create initial .gitignore if it doesn't exist
            if not Path('.gitignore').exists():
                self.create_gitignore()
                
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to initialize Git repository: {e}")
            return False
    
    def create_gitignore(self):
        """Create comprehensive .gitignore for PDD projects"""
        gitignore_content = """# PDD Project .gitignore

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Virtual environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Project specific
config.json
*.log
.chainlit/
temp_visualization_files/
output/
*.tmp

# Sensitive files (keep these private)
# config.json  # Uncomment if you want to keep config private
# .env         # Already included above

# PHR session data (optional - you might want to keep these private)
docs/prompts/.session.json

# Build artifacts
*.exe
*.msi
*.dmg
*.pkg
"""
        
        with open('.gitignore', 'w') as f:
            f.write(gitignore_content)
            
        print("✅ Created comprehensive .gitignore")
    
    def create_github_repository(self, repo_name, description="", private=False):
        """Create repository on GitHub"""
        if not self.github_token:
            print("❌ GitHub token required")
            return None
            
        try:
            headers = {
                'Authorization': f'token {self.github_token}',
                'Accept': 'application/vnd.github.v3+json'
            }
            
            data = {
                'name': repo_name,
                'description': description,
                'private': private,
                'auto_init': False,  # We'll push our existing content
                'has_issues': True,
                'has_projects': True,
                'has_wiki': True
            }
            
            response = requests.post('https://api.github.com/user/repos', 
                                   headers=headers, json=data)
            
            if response.status_code == 201:
                repo_data = response.json()
                print(f"✅ GitHub repository created: {repo_data['html_url']}")
                return repo_data
            elif response.status_code == 422:
                print(f"⚠️  Repository '{repo_name}' already exists")
                # Try to get existing repository
                response = requests.get(f'https://api.github.com/repos/{self.github_username}/{repo_name}',
                                      headers=headers)
                if response.status_code == 200:
                    return response.json()
                return None
            else:
                print(f"❌ Failed to create repository: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Error creating GitHub repository: {e}")
            return None
    
    def add_remote_origin(self, repo_url):
        """Add GitHub repository as remote origin"""
        try:
            # Check if origin already exists
            result = subprocess.run(['git', 'remote', 'get-url', 'origin'], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                current_origin = result.stdout.strip()
                if current_origin == repo_url:
                    print("✅ Remote origin already configured correctly")
                    return True
                else:
                    print(f"⚠️  Updating remote origin from {current_origin} to {repo_url}")
                    subprocess.run(['git', 'remote', 'set-url', 'origin', repo_url], check=True)
            else:
                # Add new origin
                subprocess.run(['git', 'remote', 'add', 'origin', repo_url], check=True)
                
            print(f"✅ Remote origin configured: {repo_url}")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to configure remote origin: {e}")
            return False
    
    def create_initial_commit(self):
        """Create initial commit with all project files"""
        try:
            # Add all files
            subprocess.run(['git', 'add', '.'], check=True)
            
            # Check if there are changes to commit
            result = subprocess.run(['git', 'status', '--porcelain'], 
                                  capture_output=True, text=True)
            
            if not result.stdout.strip():
                print("✅ No changes to commit")
                return True
            
            # Create commit
            commit_message = "🚀 Initial PDD project setup with universal LLM support\n\n- Multi-LLM provider support (OpenAI, DeepSeek, Anthropic, Gemini, Azure)\n- Automatic prompt recording as PHRs\n- OAuth integration for external APIs\n- Complete development automation"
            
            subprocess.run(['git', 'commit', '-m', commit_message], check=True)
            print("✅ Initial commit created")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to create initial commit: {e}")
            return False
    
    def push_to_github(self, branch='main'):
        """Push local repository to GitHub"""
        try:
            # Check if we're on the main branch, if not create it
            current_branch = subprocess.run(['git', 'branch', '--show-current'], 
                                          capture_output=True, text=True)
            
            if current_branch.returncode == 0:
                current = current_branch.stdout.strip()
                if current != branch:
                    # Create and switch to main branch
                    subprocess.run(['git', 'checkout', '-b', branch], check=True)
                    print(f"✅ Switched to {branch} branch")
            
            # Push to GitHub
            result = subprocess.run(['git', 'push', '-u', 'origin', branch], 
                                  capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ Repository pushed to GitHub ({branch} branch)")
                return True
            else:
                print(f"❌ Failed to push to GitHub: {result.stderr}")
                return False
                
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to push to GitHub: {e}")
            return False
    
    def setup_github_actions(self):
        """Create GitHub Actions workflow for PDD projects"""
        workflows_dir = Path('.github/workflows')
        workflows_dir.mkdir(parents=True, exist_ok=True)
        
        # Create PDD workflow
        workflow_content = """name: PDD Project CI/CD

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, '3.10', '3.11']

    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v3
      with:
        python-version: ${{ matrix.python-version }}
    
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        python -m pytest tests/ -v --cov=src
    
    - name: Lint with ruff
      run: |
        pip install ruff
        ruff check .
    
    - name: Format check with black
      run: |
        pip install black
        black --check .

  security:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Run security checks
      uses: securecodewarrior/github-action-add-sarif@v1
      with:
        sarif-file: 'security-results.sarif'

  phr-validation:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Validate PHR format
      run: |
        python -c "
        import os
        import re
        from pathlib import Path
        
        phr_dir = Path('docs/prompts')
        if phr_dir.exists():
            for phr_file in phr_dir.glob('*.prompt.md'):
                content = phr_file.read_text()
                if not re.search(r'^---\s*id:\s*\d+', content, re.MULTILINE):
                    print(f'Invalid PHR format: {phr_file}')
                    exit(1)
            print('All PHRs are valid')
        else:
            print('No PHRs to validate')
        "
"""
        
        workflow_file = workflows_dir / 'pdd-ci.yml'
        with open(workflow_file, 'w') as f:
            f.write(workflow_content)
            
        print("✅ GitHub Actions workflow created")
    
    def create_issue_templates(self):
        """Create GitHub issue templates"""
        issue_dir = Path('.github/ISSUE_TEMPLATE')
        issue_dir.mkdir(parents=True, exist_ok=True)
        
        # Bug report template
        bug_template = """---
name: Bug report
about: Create a report to help us improve
title: '[BUG] '
labels: 'bug'
assignees: ''
---

**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1. Go to '...'
2. Click on '....'
3. Scroll down to '....'
4. See error

**Expected behavior**
A clear and concise description of what you expected to happen.

**PHR Context**
- PHR ID where issue occurred:
- Stage (architect/red/green/refactor):
- LLM Provider used:

**Environment:**
- OS: [e.g. Windows 10]
- Python version: [e.g. 3.11]
- LLM Provider: [e.g. OpenAI, Gemini]

**Additional context**
Add any other context about the problem here.
"""
        
        # Feature request template
        feature_template = """---
name: Feature request
about: Suggest an idea for this project
title: '[FEATURE] '
labels: 'enhancement'
assignees: ''
---

**Is your feature request related to a problem? Please describe.**
A clear and concise description of what the problem is. Ex. I'm always frustrated when [...]

**Describe the solution you'd like**
A clear and concise description of what you want to happen.

**PDD Integration**
- Which PDD stage would this affect?
- Would this require new PHR templates?
- LLM provider compatibility needed?

**Additional context**
Add any other context or screenshots about the feature request here.
"""
        
        with open(issue_dir / 'bug_report.md', 'w') as f:
            f.write(bug_template)
            
        with open(issue_dir / 'feature_request.md', 'w') as f:
            f.write(feature_template)
            
        print("✅ GitHub issue templates created")
    
    def create_pull_request_template(self):
        """Create pull request template"""
        github_dir = Path('.github')
        github_dir.mkdir(exist_ok=True)
        
        pr_template = """## Description
Brief description of the changes in this PR.

## PDD Context
- **PHR ID(s) affected**: 
- **PDD Stage**: [ ] Architect [ ] Red [ ] Green [ ] Refactor [ ] Explainer
- **LLM Provider tested**: 

## Type of change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update
- [ ] PHR addition/update

## Testing
- [ ] Tests pass locally
- [ ] New tests added for new functionality
- [ ] PHR documentation updated
- [ ] LLM provider compatibility verified

## Checklist
- [ ] My code follows the PDD methodology
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
"""
        
        with open(github_dir / 'pull_request_template.md', 'w') as f:
            f.write(pr_template)
            
        print("✅ Pull request template created")
    
    def run_full_integration(self):
        """Run complete GitHub integration setup"""
        print("🐙 PDD GitHub Integration Setup")
        print("=" * 50)
        
        # Load existing configuration
        self.load_config()
        
        # Step 1: Check Git installation
        if not self.check_git_installation():
            return False
        
        # Step 2: Get project details
        print("\n📝 Project Information")
        print("-" * 20)
        
        project_path = Path.cwd()
        default_name = project_path.name
        
        repo_name = input(f"Repository name (default: {default_name}): ").strip() or default_name
        description = input("Repository description: ").strip()
        
        private_input = input("Private repository? [y/N]: ").strip().lower()
        private = private_input in ['y', 'yes']
        
        # Step 3: Get GitHub token
        if not self.get_github_token():
            return False
        
        # Step 4: Initialize local repository
        if not self.init_local_repository():
            return False
        
        # Step 5: Create GitHub repository
        repo_data = self.create_github_repository(repo_name, description, private)
        if not repo_data:
            return False
        
        # Step 6: Set up GitHub templates and workflows
        self.setup_github_actions()
        self.create_issue_templates()
        self.create_pull_request_template()
        
        # Step 7: Configure remote origin
        if not self.add_remote_origin(repo_data['clone_url']):
            return False
        
        # Step 8: Create initial commit
        if not self.create_initial_commit():
            return False
        
        # Step 9: Push to GitHub
        if not self.push_to_github():
            return False
        
        # Success summary
        print("\n" + "=" * 50)
        print("🎉 GitHub Integration Complete!")
        print("=" * 50)
        print(f"📁 Repository: {repo_data['html_url']}")
        print(f"🔒 Privacy: {'Private' if private else 'Public'}")
        print(f"👤 Owner: {self.github_username}")
        print("\n✅ Features enabled:")
        print("   • Version control with Git")
        print("   • GitHub Actions CI/CD")
        print("   • Issue tracking templates")
        print("   • Pull request templates")
        print("   • PHR validation workflow")
        print("   • Security scanning")
        
        print("\n💡 Next steps:")
        print(f"   • Visit: {repo_data['html_url']}")
        print("   • Enable GitHub Pages (optional)")
        print("   • Set up branch protection rules")
        print("   • Invite collaborators")
        print("   • Configure secrets for CI/CD")
        
        return True

def main():
    integrator = GitHubIntegrator()
    success = integrator.run_full_integration()
    
    if success:
        print("\n🚀 Your PDD project is now on GitHub with full integration!")
    else:
        print("\n❌ GitHub integration failed. Please check the errors above.")
    
    input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()