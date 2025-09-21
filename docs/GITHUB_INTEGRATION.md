# GitHub Integration Guide for PDD Projects

## Quick Start

### Prerequisites
1. **GitHub Account**: You already have this connected to VS Code ✅
2. **Git Installed**: Usually comes with VS Code installation
3. **Personal Access Token**: Required for repository creation

### Automated Setup (Recommended)
```bash
python scripts/github_integrator.py
```

This script will:
- ✅ Verify Git installation and configuration
- 🔐 Set up GitHub Personal Access Token
- 📁 Initialize local Git repository
- 🐙 Create GitHub repository
- 🚀 Push your PDD project to GitHub
- ⚙️ Set up GitHub Actions CI/CD
- 📋 Create issue and PR templates

---

## Manual Setup (Step by Step)

### Step 1: Create Personal Access Token

1. Go to [GitHub Settings > Tokens](https://github.com/settings/tokens)
2. Click "Generate new token (classic)"
3. Give it a name: "PDD Project Access"
4. Select scopes:
   - ✅ `repo` (Full repository access)
   - ✅ `workflow` (GitHub Actions)
   - ✅ `user` (User information)
5. Click "Generate token"
6. **COPY THE TOKEN** (you can't see it again!)

### Step 2: Initialize Git Repository

```bash
# Navigate to your project directory
cd path/to/your/pdd-project

# Initialize Git repository
git init

# Configure Git (if not already done)
git config user.name "Your Name"
git config user.email "your.email@example.com"

# Add all files
git add .

# Create initial commit
git commit -m "🚀 Initial PDD project setup"
```

### Step 3: Create GitHub Repository

**Option A: Via GitHub Web Interface**
1. Go to [GitHub](https://github.com)
2. Click "+" → "New repository"
3. Name: `my-pdd-project` (or your choice)
4. Description: "PDD-powered AI project with universal LLM support"
5. Choose Public/Private
6. **DON'T** initialize with README (we have files already)
7. Click "Create repository"

**Option B: Via GitHub CLI (if installed)**
```bash
gh repo create my-pdd-project --public --description "PDD-powered AI project"
```

### Step 4: Connect Local to GitHub

```bash
# Add GitHub as remote origin
git remote add origin https://github.com/yourusername/my-pdd-project.git

# Push to GitHub
git branch -M main
git push -u origin main
```

---

## VS Code Integration

### Connect Repository
Since you already have GitHub connected to VS Code:

1. **Open Command Palette**: `Ctrl+Shift+P`
2. **Type**: "Git: Clone"
3. **Select**: Your new repository
4. **Or** use the Source Control panel in VS Code

### Source Control Features
- **Commit changes**: Source Control panel (Ctrl+Shift+G)
- **Push/Pull**: Sync button in status bar
- **Branch management**: Click branch name in status bar
- **Merge conflicts**: VS Code shows them inline

---

## Version Control Best Practices

### Branch Strategy
```bash
# Create feature branch for new PDD features
git checkout -b feature/new-phr-template

# Work on your changes...
git add .
git commit -m "feat: Add new PHR template for API integration"

# Push feature branch
git push -u origin feature/new-phr-template

# Create Pull Request on GitHub
# After review, merge to main
```

### Commit Message Convention
Use conventional commits for better tracking:

```bash
# PDD-specific commit types
git commit -m "feat: Add Gemini 2.5 support to config manager"
git commit -m "fix: Resolve PHR auto-detection issue"
git commit -m "docs: Update README with GitHub integration"
git commit -m "phr: Add architecture template for microservices"
git commit -m "refactor: Improve LLM provider switching"

# Standard types
git commit -m "test: Add unit tests for prompt watcher"
git commit -m "ci: Update GitHub Actions workflow"
git commit -m "style: Format code with black"
```

### Protecting Sensitive Data

Your `.gitignore` already includes:
```gitignore
# Sensitive files
config.json       # Your API keys and tokens
.env             # Environment variables
*.log            # Log files
.chainlit/       # Chainlit cache

# Optional: Keep PHR sessions private
docs/prompts/.session.json
```

**Configuration Security Options:**

**Option 1: Keep config.json private (recommended)**
- `config.json` stays in `.gitignore`
- Share `config.template.json` instead
- Team members copy and configure their own

**Option 2: Use environment variables**
```bash
# Create .env file (already in .gitignore)
OPENAI_API_KEY=your_key_here
GITHUB_TOKEN=your_token_here

# Reference in config.json
{
  "openai": {
    "api_key": "${OPENAI_API_KEY}"
  }
}
```

---

## GitHub Features for PDD Projects

### 1. Issues for Task Tracking
Create issues for:
- 🏗️ **Architecture decisions**: "Design API integration strategy"
- 🔴 **Red phase tasks**: "Implement user authentication"
- 🟢 **Green phase tasks**: "Add tests for auth module"
- 🔧 **Refactor tasks**: "Optimize database queries"
- 📚 **Documentation**: "Update PHR templates"

### 2. Projects for PDD Workflow
1. Go to your repository → **Projects** tab
2. Create "PDD Development Board"
3. Add columns:
   - 📋 **Backlog**
   - 🏗️ **Architect**
   - 🔴 **Red**
   - 🟢 **Green**
   - 🔧 **Refactor**
   - ✅ **Done**

### 3. Actions for Automation
Your GitHub Actions will automatically:
- ✅ Run tests on every push
- 🔍 Check code quality
- 📝 Validate PHR format
- 🔒 Run security scans
- 📊 Generate coverage reports

### 4. Releases for Versions
```bash
# Tag a release
git tag -a v1.0.0 -m "Release v1.0.0: Universal LLM support"
git push origin v1.0.0

# GitHub will create a release automatically
```

---

## Collaboration Workflow

### For Solo Development
```bash
# Daily workflow
git pull origin main           # Get latest changes
# ... work on features ...
git add .                     # Stage changes
git commit -m "feat: ..."     # Commit with message
git push origin main          # Push to GitHub
```

### For Team Development
```bash
# Feature development
git checkout -b feature/oauth-integration
# ... implement feature ...
git push -u origin feature/oauth-integration
# Create Pull Request on GitHub
# After review and approval, merge
```

### PHR Collaboration
- **Individual PHRs**: Keep in personal branches
- **Shared templates**: Merge to main branch
- **Session data**: Usually keep private (in `.gitignore`)

---

## Advanced GitHub Integration

### GitHub Pages for Documentation
1. Repository → **Settings** → **Pages**
2. Source: **GitHub Actions**
3. Auto-deploys your `docs/` folder
4. Access at: `https://yourusername.github.io/my-pdd-project`

### GitHub Codespaces
- Cloud development environment
- VS Code in browser
- All extensions and settings synced

### GitHub CLI Integration
```bash
# Install GitHub CLI
winget install GitHub.cli

# Useful commands
gh repo view                  # View repository
gh issue create             # Create issue
gh pr create                # Create pull request
gh workflow run             # Trigger workflow
```

---

## Troubleshooting

### Authentication Issues
```bash
# Update stored credentials
git config --global credential.helper manager-core

# Or use Personal Access Token
git remote set-url origin https://token@github.com/username/repo.git
```

### Large File Issues
```bash
# Install Git LFS for large files
git lfs install
git lfs track "*.pdf"
git add .gitattributes
```

### Sync Issues
```bash
# Force sync with remote
git fetch origin
git reset --hard origin/main  # ⚠️ Loses local changes!

# Or merge conflicts
git pull origin main
# Resolve conflicts in VS Code
git add .
git commit -m "resolve: Merge conflicts"
```

---

## Security Best Practices

### Repository Security
1. **Enable branch protection**:
   - Repository → Settings → Branches
   - Add rule for `main` branch
   - Require PR reviews
   - Require status checks

2. **Set up secrets**:
   - Repository → Settings → Secrets
   - Add `OPENAI_API_KEY`, etc.
   - Use in GitHub Actions

3. **Security scanning**:
   - Dependabot alerts (auto-enabled)
   - Code scanning with GitHub Actions
   - Secret scanning (auto-enabled for public repos)

### Token Management
- ⏰ **Rotate tokens** every 90 days
- 🔒 **Use minimal scopes** required
- 🗑️ **Delete unused tokens**
- 📝 **Track token usage** in GitHub settings

---

## Next Steps

1. **Run the automated setup**:
   ```bash
   python scripts/github_integrator.py
   ```

2. **Customize your workflow**:
   - Edit `.github/workflows/pdd-ci.yml`
   - Add more issue templates
   - Set up branch protection

3. **Start collaborating**:
   - Invite team members
   - Create first issues
   - Set up project board

4. **Monitor your project**:
   - Check Actions tab for CI status
   - Review security alerts
   - Track issues and PRs

---

**🎉 Your PDD project is now ready for collaborative development with full GitHub integration!**