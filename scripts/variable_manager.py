#!/usr/bin/env python3
"""
PDD Universal Variable Manager
Collects all required variables and updates all configuration files automatically
"""

import os
import json
import re
from pathlib import Path
from typing import Dict, List, Any, Optional
import getpass

class VariableManager:
    def __init__(self):
        self.variables = {}
        self.config_file = Path("config.json")
        self.env_file = Path(".env")
        
        # Define all possible variables with their metadata
        self.variable_definitions = {
            # LLM Providers
            "OPENAI_API_KEY": {
                "description": "OpenAI API Key (starts with sk-)",
                "category": "LLM Providers",
                "required_for": ["OpenAI GPT models"],
                "pattern": r"^sk-[a-zA-Z0-9_-]+$",
                "secure": True,
                "url": "https://platform.openai.com/api-keys"
            },
            "OPENAI_MODEL": {
                "description": "OpenAI Model",
                "category": "LLM Providers",
                "default": "gpt-4o-mini",
                "options": ["gpt-4", "gpt-4-turbo", "gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo"],
                "required_for": ["OpenAI configuration"]
            },
            "GOOGLE_API_KEY": {
                "description": "Google Gemini API Key",
                "category": "LLM Providers",
                "required_for": ["Google Gemini models"],
                "secure": True,
                "url": "https://makersuite.google.com/app/apikey"
            },
            "GEMINI_MODEL": {
                "description": "Gemini Model",
                "category": "LLM Providers",
                "default": "gemini-2.0-flash-exp",
                "options": ["gemini-pro", "gemini-pro-vision", "gemini-2.0-flash-exp", "gemini-1.5-flash", "gemini-1.5-pro"],
                "required_for": ["Gemini configuration"]
            },
            "ANTHROPIC_API_KEY": {
                "description": "Anthropic Claude API Key",
                "category": "LLM Providers",
                "required_for": ["Anthropic Claude models"],
                "secure": True,
                "url": "https://console.anthropic.com/"
            },
            "ANTHROPIC_MODEL": {
                "description": "Anthropic Model",
                "category": "LLM Providers",
                "default": "claude-3-5-sonnet-20241022",
                "options": ["claude-3-5-sonnet-20241022", "claude-3-opus-20240229", "claude-3-haiku-20240307"],
                "required_for": ["Anthropic configuration"]
            },
            "DEEPSEEK_API_KEY": {
                "description": "DeepSeek API Key",
                "category": "LLM Providers",
                "required_for": ["DeepSeek models"],
                "secure": True,
                "url": "https://platform.deepseek.com/api_keys"
            },
            "DEEPSEEK_MODEL": {
                "description": "DeepSeek Model",
                "category": "LLM Providers",
                "default": "deepseek-chat",
                "options": ["deepseek-chat", "deepseek-coder"],
                "required_for": ["DeepSeek configuration"]
            },
            "AZURE_OPENAI_API_KEY": {
                "description": "Azure OpenAI API Key",
                "category": "LLM Providers",
                "required_for": ["Azure OpenAI models"],
                "secure": True,
                "url": "https://portal.azure.com/"
            },
            "AZURE_OPENAI_ENDPOINT": {
                "description": "Azure OpenAI Endpoint URL",
                "category": "LLM Providers",
                "required_for": ["Azure OpenAI configuration"],
                "pattern": r"^https://.*\.openai\.azure\.com/?$"
            },
            "AZURE_OPENAI_DEPLOYMENT": {
                "description": "Azure OpenAI Deployment Name",
                "category": "LLM Providers",
                "required_for": ["Azure OpenAI configuration"]
            },
            
            # GitHub OAuth
            "GITHUB_CLIENT_ID": {
                "description": "GitHub OAuth Client ID",
                "category": "OAuth Clients",
                "required_for": ["GitHub API integration"],
                "url": "https://github.com/settings/developers"
            },
            "GITHUB_CLIENT_SECRET": {
                "description": "GitHub OAuth Client Secret",
                "category": "OAuth Clients",
                "required_for": ["GitHub API integration"],
                "secure": True,
                "url": "https://github.com/settings/developers"
            },
            "GITHUB_TOKEN": {
                "description": "GitHub Personal Access Token",
                "category": "OAuth Clients",
                "required_for": ["GitHub repository management"],
                "secure": True,
                "pattern": r"^gh[pousr]_[a-zA-Z0-9_]+$",
                "url": "https://github.com/settings/tokens"
            },
            
            # Xero OAuth
            "XERO_CLIENT_ID": {
                "description": "Xero OAuth Client ID",
                "category": "OAuth Clients",
                "required_for": ["Xero accounting integration"],
                "url": "https://developer.xero.com/app/manage"
            },
            "XERO_CLIENT_SECRET": {
                "description": "Xero OAuth Client Secret",
                "category": "OAuth Clients",
                "required_for": ["Xero accounting integration"],
                "secure": True,
                "url": "https://developer.xero.com/app/manage"
            },
            "XERO_REDIRECT_URI": {
                "description": "Xero OAuth Redirect URI",
                "category": "OAuth Clients",
                "default": "http://localhost:8080/callback",
                "required_for": ["Xero OAuth flow"]
            },
            
            # Google OAuth
            "GOOGLE_CLIENT_ID": {
                "description": "Google OAuth Client ID",
                "category": "OAuth Clients",
                "required_for": ["Google API integration"],
                "url": "https://console.cloud.google.com/apis/credentials"
            },
            "GOOGLE_CLIENT_SECRET": {
                "description": "Google OAuth Client Secret",
                "category": "OAuth Clients",
                "required_for": ["Google API integration"],
                "secure": True,
                "url": "https://console.cloud.google.com/apis/credentials"
            },
            
            # Microsoft OAuth
            "MICROSOFT_CLIENT_ID": {
                "description": "Microsoft OAuth Client ID",
                "category": "OAuth Clients",
                "required_for": ["Microsoft Graph API integration"],
                "url": "https://portal.azure.com/#view/Microsoft_AAD_RegisteredApps"
            },
            "MICROSOFT_CLIENT_SECRET": {
                "description": "Microsoft OAuth Client Secret",
                "category": "OAuth Clients",
                "required_for": ["Microsoft Graph API integration"],
                "secure": True,
                "url": "https://portal.azure.com/#view/Microsoft_AAD_RegisteredApps"
            },
            
            # Application Settings
            "CHAINLIT_PORT": {
                "description": "Chainlit Application Port",
                "category": "Application Settings",
                "default": "8001",
                "pattern": r"^\d{4,5}$",
                "required_for": ["Chainlit web interface"]
            },
            "DEBUG": {
                "description": "Enable Debug Mode",
                "category": "Application Settings",
                "default": "false",
                "options": ["true", "false"],
                "required_for": ["Development debugging"]
            },
            "LOG_LEVEL": {
                "description": "Logging Level",
                "category": "Application Settings",
                "default": "INFO",
                "options": ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                "required_for": ["Application logging"]
            },
            "SESSION_SECRET": {
                "description": "Session Secret Key (auto-generated if empty)",
                "category": "Application Settings",
                "secure": True,
                "auto_generate": True,
                "required_for": ["Session security"]
            },
            
            # Database Settings
            "DATABASE_URL": {
                "description": "Database Connection URL",
                "category": "Database Settings",
                "default": "sqlite:///pdd_project.db",
                "required_for": ["Data persistence"]
            },
            "REDIS_URL": {
                "description": "Redis Connection URL (for caching)",
                "category": "Database Settings",
                "default": "redis://localhost:6379",
                "required_for": ["Caching and sessions"]
            }
        }
    
    def generate_secure_key(self, length=32):
        """Generate a secure random key"""
        import secrets
        import string
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphabet) for _ in range(length))
    
    def validate_variable(self, key: str, value: str) -> tuple[bool, str]:
        """Validate a variable value against its definition"""
        definition = self.variable_definitions.get(key, {})
        
        if not value and not definition.get("default"):
            return False, "Value cannot be empty"
        
        # Check pattern if defined
        pattern = definition.get("pattern")
        if pattern and value and not re.match(pattern, value):
            return False, f"Value doesn't match expected format: {pattern}"
        
        # Check options if defined
        options = definition.get("options")
        if options and value and value not in options:
            return False, f"Value must be one of: {', '.join(options)}"
        
        return True, "Valid"
    
    def get_user_input(self, key: str, definition: Dict[str, Any]) -> str:
        """Get user input for a variable"""
        description = definition.get("description", key)
        default = definition.get("default", "")
        options = definition.get("options")
        secure = definition.get("secure", False)
        url = definition.get("url")
        
        # Build prompt
        prompt = f"\n{description}"
        if url:
            prompt += f"\n  📋 Get from: {url}"
        if options:
            prompt += f"\n  💡 Options: {', '.join(options)}"
        if default:
            prompt += f"\n  🔧 Default: {default}"
        
        prompt += f"\n  Enter value"
        if default:
            prompt += f" (press Enter for default)"
        prompt += ": "
        
        while True:
            if secure:
                value = getpass.getpass(prompt)
            else:
                value = input(prompt).strip()
            
            # Use default if empty
            if not value and default:
                value = default
            
            # Auto-generate if needed
            if not value and definition.get("auto_generate"):
                value = self.generate_secure_key()
                print(f"  🔐 Auto-generated secure key")
            
            # Validate
            is_valid, message = self.validate_variable(key, value)
            if is_valid:
                return value
            else:
                print(f"  ❌ {message}")
                if not secure:  # Don't show invalid secure values
                    print(f"  You entered: '{value}'")
    
    def collect_variables_by_category(self):
        """Collect variables organized by category"""
        print("🔧 PDD Universal Variable Configuration")
        print("=" * 50)
        print()
        print("This will collect all required variables for your PDD project.")
        print("You can skip categories you don't need by pressing Enter.")
        print()
        
        # Group variables by category
        categories = {}
        for key, definition in self.variable_definitions.items():
            category = definition.get("category", "Other")
            if category not in categories:
                categories[category] = []
            categories[category].append((key, definition))
        
        # Process each category
        for category, variables in categories.items():
            print(f"\n📂 {category}")
            print("-" * len(category))
            
            # Ask if user wants to configure this category
            configure = input(f"Configure {category}? [y/N]: ").strip().lower()
            if configure not in ['y', 'yes']:
                print(f"⏭️  Skipping {category}")
                continue
            
            # Collect variables in this category
            for key, definition in variables:
                print(f"\n🔹 {key}")
                value = self.get_user_input(key, definition)
                
                if value:
                    self.variables[key] = value
                    if definition.get("secure"):
                        print(f"✅ {key} configured (secure)")
                    else:
                        print(f"✅ {key} = {value}")
        
        print(f"\n✅ Variable collection complete!")
        print(f"📊 Collected {len(self.variables)} variables")
    
    def update_config_json(self):
        """Update config.json with collected variables"""
        print("\n📄 Updating config.json...")
        
        # Load existing config or create new
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                config = json.load(f)
        else:
            config = {}
        
        # Determine default provider
        default_provider = None
        if "OPENAI_API_KEY" in self.variables:
            default_provider = "openai"
        elif "GOOGLE_API_KEY" in self.variables:
            default_provider = "gemini"
        elif "ANTHROPIC_API_KEY" in self.variables:
            default_provider = "anthropic"
        elif "DEEPSEEK_API_KEY" in self.variables:
            default_provider = "deepseek"
        elif "AZURE_OPENAI_API_KEY" in self.variables:
            default_provider = "azure"
        
        if default_provider:
            config["default_provider"] = default_provider
        
        # Update LLM providers
        if "OPENAI_API_KEY" in self.variables:
            config["openai"] = {
                "api_key": self.variables["OPENAI_API_KEY"],
                "model": self.variables.get("OPENAI_MODEL", "gpt-4o-mini")
            }
        
        if "GOOGLE_API_KEY" in self.variables:
            config["gemini"] = {
                "api_key": self.variables["GOOGLE_API_KEY"],
                "model": self.variables.get("GEMINI_MODEL", "gemini-2.0-flash-exp")
            }
        
        if "ANTHROPIC_API_KEY" in self.variables:
            config["anthropic"] = {
                "api_key": self.variables["ANTHROPIC_API_KEY"],
                "model": self.variables.get("ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022")
            }
        
        if "DEEPSEEK_API_KEY" in self.variables:
            config["deepseek"] = {
                "api_key": self.variables["DEEPSEEK_API_KEY"],
                "model": self.variables.get("DEEPSEEK_MODEL", "deepseek-chat")
            }
        
        if "AZURE_OPENAI_API_KEY" in self.variables:
            config["azure"] = {
                "api_key": self.variables["AZURE_OPENAI_API_KEY"],
                "endpoint": self.variables.get("AZURE_OPENAI_ENDPOINT", ""),
                "deployment": self.variables.get("AZURE_OPENAI_DEPLOYMENT", ""),
                "api_version": "2024-02-15-preview"
            }
        
        # Update OAuth clients
        oauth_clients = config.get("oauth_clients", {})
        
        if "GITHUB_CLIENT_ID" in self.variables:
            oauth_clients["github"] = {
                "client_id": self.variables["GITHUB_CLIENT_ID"],
                "client_secret": self.variables.get("GITHUB_CLIENT_SECRET", ""),
                "access_token": self.variables.get("GITHUB_TOKEN", "")
            }
        
        if "XERO_CLIENT_ID" in self.variables:
            oauth_clients["xero"] = {
                "client_id": self.variables["XERO_CLIENT_ID"],
                "client_secret": self.variables.get("XERO_CLIENT_SECRET", ""),
                "redirect_uri": self.variables.get("XERO_REDIRECT_URI", "http://localhost:8080/callback")
            }
        
        if "GOOGLE_CLIENT_ID" in self.variables:
            oauth_clients["google"] = {
                "client_id": self.variables["GOOGLE_CLIENT_ID"],
                "client_secret": self.variables.get("GOOGLE_CLIENT_SECRET", "")
            }
        
        if "MICROSOFT_CLIENT_ID" in self.variables:
            oauth_clients["microsoft"] = {
                "client_id": self.variables["MICROSOFT_CLIENT_ID"],
                "client_secret": self.variables.get("MICROSOFT_CLIENT_SECRET", "")
            }
        
        if oauth_clients:
            config["oauth_clients"] = oauth_clients
        
        # Update application settings
        app_settings = config.get("app_settings", {})
        if "CHAINLIT_PORT" in self.variables:
            app_settings["chainlit_port"] = int(self.variables["CHAINLIT_PORT"])
        if "DEBUG" in self.variables:
            app_settings["debug"] = self.variables["DEBUG"].lower() == "true"
        if "LOG_LEVEL" in self.variables:
            app_settings["log_level"] = self.variables["LOG_LEVEL"]
        if "DATABASE_URL" in self.variables:
            app_settings["database_url"] = self.variables["DATABASE_URL"]
        if "REDIS_URL" in self.variables:
            app_settings["redis_url"] = self.variables["REDIS_URL"]
        
        if app_settings:
            config["app_settings"] = app_settings
        
        # Save config
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"✅ config.json updated")
    
    def update_env_file(self):
        """Update .env file with collected variables"""
        print("\n📄 Updating .env file...")
        
        env_content = []
        env_content.append("# PDD Project Environment Variables")
        env_content.append("# Generated by PDD Universal Variable Manager")
        env_content.append("")
        
        # Group by category for better organization
        categories = {}
        for key, value in self.variables.items():
            definition = self.variable_definitions.get(key, {})
            category = definition.get("category", "Other")
            if category not in categories:
                categories[category] = []
            categories[category].append((key, value))
        
        for category, variables in categories.items():
            env_content.append(f"# {category}")
            for key, value in variables:
                env_content.append(f"{key}={value}")
            env_content.append("")
        
        with open(self.env_file, 'w') as f:
            f.write('\n'.join(env_content))
        
        print(f"✅ .env file updated")
    
    def update_chainlit_app(self):
        """Update chainlit_app.py with configuration"""
        print("\n📄 Updating chainlit_app.py...")
        
        chainlit_app = Path("chainlit_app.py")
        if not chainlit_app.exists():
            self.create_chainlit_app()
            return
        
        # Read existing file
        content = chainlit_app.read_text()
        
        # Update port configuration
        if "CHAINLIT_PORT" in self.variables:
            port = self.variables["CHAINLIT_PORT"]
            # Update port in chainlit config
            content = re.sub(
                r'port\s*=\s*\d+',
                f'port = {port}',
                content
            )
        
        # Write updated content
        chainlit_app.write_text(content)
        print(f"✅ chainlit_app.py updated")
    
    def create_chainlit_app(self):
        """Create chainlit_app.py if it doesn't exist"""
        print("📄 Creating chainlit_app.py...")
        
        port = self.variables.get("CHAINLIT_PORT", "8001")
        debug = self.variables.get("DEBUG", "false").lower() == "true"
        
        content = f'''#!/usr/bin/env python3
"""
PDD Universal Chainlit Application
Multi-LLM chat interface with automatic PHR recording
"""

import os
import json
import chainlit as cl
from pathlib import Path
from typing import Dict, Any

# Load configuration
def load_config():
    config_file = Path("config.json")
    if config_file.exists():
        with open(config_file, 'r') as f:
            return json.load(f)
    return {{}}

config = load_config()

@cl.on_chat_start
async def start():
    """Initialize chat session"""
    default_provider = config.get("default_provider", "openai")
    
    await cl.Message(
        content=f"""🚀 **PDD Universal Chat Interface**

**Current LLM Provider**: {default_provider.title()}

**Available Commands**:
- `/switch <provider>` - Switch LLM provider
- `/config` - Show current configuration
- `/help` - Show help information

**Automatic PHR Recording**: ✅ Active
Your prompts are automatically recorded as PHRs in `docs/prompts/`

Start chatting to begin your PDD development session!
""",
        author="System"
    ).send()

@cl.on_message
async def main(message: cl.Message):
    """Handle incoming messages"""
    content = message.content.strip()
    
    # Handle commands
    if content.startswith('/'):
        await handle_command(content)
        return
    
    # Regular chat processing
    response = await process_llm_request(content)
    await cl.Message(content=response).send()

async def handle_command(command: str):
    """Handle chat commands"""
    parts = command.split()
    cmd = parts[0].lower()
    
    if cmd == "/config":
        config_info = f"""📋 **Current Configuration**

**Default Provider**: {{config.get("default_provider", "Not set")}}
**Available Providers**: {{", ".join(config.keys()) if config else "None"}}
**Chainlit Port**: {port}
**Debug Mode**: {debug}
"""
        await cl.Message(content=config_info, author="System").send()
    
    elif cmd == "/help":
        help_text = """🆘 **Help - PDD Universal Chat**

**Commands**:
- `/config` - Show configuration
- `/switch <provider>` - Switch LLM provider
- `/help` - This help message

**PDD Methodology**:
- **Architect**: Design and planning
- **Red**: Test-driven development
- **Green**: Implementation
- **Refactor**: Code improvement

**PHR System**:
Your prompts are automatically saved as Prompt History Records (PHRs) in numbered files.
"""
        await cl.Message(content=help_text, author="System").send()
    
    else:
        await cl.Message(content=f"❌ Unknown command: {{cmd}}", author="System").send()

async def process_llm_request(prompt: str) -> str:
    """Process request with configured LLM provider"""
    default_provider = config.get("default_provider")
    
    if not default_provider:
        return "❌ No LLM provider configured. Please run configuration setup."
    
    # This would integrate with actual LLM APIs
    return f"🤖 **[{{default_provider.title()}}]** Response to: {{prompt}}\\n\\n⚠️ **Note**: LLM integration not yet implemented. This is a placeholder response."

if __name__ == "__main__":
    # Configuration for chainlit run
    import chainlit as cl
    cl.run(
        port={port},
        debug={str(debug).lower()},
        headless=False,
        watch=True
    )
'''
        
        with open("chainlit_app.py", 'w') as f:
            f.write(content)
        
        print(f"✅ chainlit_app.py created")
    
    def update_requirements_txt(self):
        """Update requirements.txt with all dependencies"""
        print("\n📄 Updating requirements.txt...")
        
        requirements = [
            "# PDD Universal Project Requirements",
            "",
            "# Core framework",
            "chainlit>=1.0.0",
            "python-dotenv>=1.0.0",
            "",
            "# LLM Providers",
            "openai>=1.0.0",
            "google-generativeai>=0.3.0",
            "anthropic>=0.8.0",
            "",
            "# OAuth and API integrations",
            "requests>=2.31.0",
            "authlib>=1.2.0",
            "",
            "# Utilities",
            "click>=8.0.0",
            "rich>=13.0.0",
            "pyyaml>=6.0",
            "",
            "# Development",
            "pytest>=7.0.0",
            "black>=23.0.0",
            "ruff>=0.1.0",
        ]
        
        # Add database dependencies if configured
        if "DATABASE_URL" in self.variables:
            if "sqlite" in self.variables["DATABASE_URL"]:
                requirements.extend(["", "# Database", "sqlalchemy>=2.0.0"])
            elif "postgresql" in self.variables["DATABASE_URL"]:
                requirements.extend(["", "# Database", "sqlalchemy>=2.0.0", "psycopg2-binary>=2.9.0"])
        
        if "REDIS_URL" in self.variables:
            requirements.extend(["", "# Caching", "redis>=4.0.0"])
        
        with open("requirements.txt", 'w') as f:
            f.write('\n'.join(requirements))
        
        print(f"✅ requirements.txt updated")
    
    def update_gitignore(self):
        """Update .gitignore with sensitive files"""
        print("\n📄 Updating .gitignore...")
        
        gitignore_content = '''# PDD Project .gitignore

# Environment and configuration
.env
config.json
*.log

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

# Chainlit
.chainlit/
temp_visualization_files/

# Project specific
output/
*.tmp
*.backup

# OAuth tokens and secrets (keep these private!)
# Uncomment if you want to keep PHR sessions private
# docs/prompts/.session.json
'''
        
        with open(".gitignore", 'w') as f:
            f.write(gitignore_content)
        
        print(f"✅ .gitignore updated")
    
    def run_full_configuration(self):
        """Run complete variable collection and file updates"""
        print("🚀 PDD Universal Variable Manager")
        print("=" * 50)
        print()
        print("This tool will:")
        print("  ✅ Collect all required variables")
        print("  ✅ Update config.json")
        print("  ✅ Update .env file")
        print("  ✅ Update chainlit_app.py")
        print("  ✅ Update requirements.txt")
        print("  ✅ Update .gitignore")
        print()
        
        proceed = input("Proceed with variable collection? [Y/n]: ").strip().lower()
        if proceed in ['n', 'no']:
            print("❌ Configuration cancelled")
            return False
        
        # Collect variables
        self.collect_variables_by_category()
        
        if not self.variables:
            print("⚠️  No variables collected. Configuration skipped.")
            return False
        
        # Update all files
        print("\n🔄 Updating configuration files...")
        self.update_config_json()
        self.update_env_file()
        self.update_chainlit_app()
        self.update_requirements_txt()
        self.update_gitignore()
        
        # Summary
        print("\n" + "=" * 50)
        print("🎉 Variable Configuration Complete!")
        print("=" * 50)
        print(f"📊 Variables configured: {len(self.variables)}")
        print()
        print("📁 Files updated:")
        print("   • config.json - LLM and OAuth configuration")
        print("   • .env - Environment variables")
        print("   • chainlit_app.py - Application configuration")
        print("   • requirements.txt - Python dependencies")
        print("   • .gitignore - Protected sensitive files")
        print()
        
        # Show configured categories
        categories = set()
        for key in self.variables.keys():
            definition = self.variable_definitions.get(key, {})
            category = definition.get("category", "Other")
            categories.add(category)
        
        print("🔧 Configured categories:")
        for category in sorted(categories):
            print(f"   • {category}")
        
        print()
        print("🚀 Next steps:")
        print("   1. Run: start-universal.bat")
        print("   2. Visit: http://localhost:8001")
        print("   3. Start building with PDD methodology!")
        print()
        
        return True

def main():
    """Main entry point"""
    manager = VariableManager()
    success = manager.run_full_configuration()
    
    if success:
        print("✅ All variables configured successfully!")
    else:
        print("❌ Variable configuration cancelled or failed.")
    
    input("Press Enter to continue...")

if __name__ == "__main__":
    main()