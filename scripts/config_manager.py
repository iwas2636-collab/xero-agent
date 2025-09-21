#!/usr/bin/env python3
"""
Universal Configuration Manager for PDD Development
Supports multiple LLM providers and OAuth configurations
"""

import os
import json
from pathlib import Path
from typing import Dict, Any

class ConfigManager:
    def __init__(self):
        self.config_file = Path("config.json")
        self.env_file = Path(".env")
        self.config = self.load_config()

    def load_config(self) -> Dict[str, Any]:
        """Load existing configuration or create default"""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                return json.load(f)
        return self.get_default_config()

    def get_default_config(self) -> Dict[str, Any]:
        """Default configuration template"""
        return {
            "llm_provider": "openai",
            "providers": {
                "openai": {
                    "api_key": "",
                    "model": "gpt-4",
                    "base_url": "https://api.openai.com/v1"
                },
                "deepseek": {
                    "api_key": "",
                    "model": "deepseek-chat",
                    "base_url": "https://api.deepseek.com/v1"
                },
                "anthropic": {
                    "api_key": "",
                    "model": "claude-3-sonnet-20240229",
                    "base_url": "https://api.anthropic.com/v1"
                },
                "local": {
                    "api_key": "local",
                    "model": "llama2",
                    "base_url": "http://localhost:11434/v1"
                },
                "azure": {
                    "api_key": "",
                    "model": "gpt-4",
                    "base_url": "https://your-resource.openai.azure.com/",
                    "api_version": "2024-02-15-preview"
                },
                "gemini": {
                    "api_key": "",
                    "model": "gemini-2.0-flash-exp",
                    "base_url": "https://generativelanguage.googleapis.com/v1beta"
                }
            },
            "oauth_clients": {
                "xero": {
                    "client_id": "",
                    "client_secret": "",
                    "redirect_uri": "http://localhost:8001/callback",
                    "scopes": "accounting.transactions,accounting.contacts,accounting.settings"
                },
                "github": {
                    "client_id": "",
                    "client_secret": "",
                    "redirect_uri": "http://localhost:8001/callback",
                    "scopes": "repo,user"
                },
                "google": {
                    "client_id": "",
                    "client_secret": "",
                    "redirect_uri": "http://localhost:8001/callback",
                    "scopes": "openid,email,profile"
                },
                "microsoft": {
                    "client_id": "",
                    "client_secret": "",
                    "redirect_uri": "http://localhost:8001/callback",
                    "scopes": "User.Read"
                }
            },
            "session": {
                "auto_prompt_recording": True,
                "auto_start_watcher": True,
                "port": 8001,
                "debug": False
            }
        }

    def save_config(self):
        """Save configuration to file"""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)

    def setup_interactive(self):
        """Interactive configuration setup"""
        print("🔧 PDD Universal Configuration Setup")
        print("=" * 50)

        # LLM Provider Selection
        print("\n📱 Select your AI provider:")
        providers = list(self.config["providers"].keys())
        for i, provider in enumerate(providers, 1):
            current = " (current)" if provider == self.config["llm_provider"] else ""
            print(f"   {i}. {provider.title()}{current}")

        choice = input(f"Enter choice (1-{len(providers)}) or press Enter for current: ")
        if choice.strip():
            try:
                provider_idx = int(choice) - 1
                if 0 <= provider_idx < len(providers):
                    self.config["llm_provider"] = providers[provider_idx]
                    print(f"✅ Selected: {providers[provider_idx].title()}")
            except ValueError:
                print("Invalid choice, keeping current provider")

        # Configure selected provider
        provider = self.config["llm_provider"]
        provider_config = self.config["providers"][provider]

        print(f"\n🔑 Configure {provider.title()} API settings:")
        
        api_key = input(f"API Key (current: {'*' * min(len(provider_config['api_key']), 8) if provider_config['api_key'] else 'not set'}): ")
        if api_key.strip():
            provider_config["api_key"] = api_key.strip()

        model = input(f"Model (current: {provider_config['model']}): ")
        if model.strip():
            provider_config["model"] = model.strip()

        if provider != "local":
            base_url = input(f"Base URL (current: {provider_config['base_url']}): ")
            if base_url.strip():
                provider_config["base_url"] = base_url.strip()

        # Azure specific configuration
        if provider == "azure":
            api_version = input(f"API Version (current: {provider_config.get('api_version', 'not set')}): ")
            if api_version.strip():
                provider_config["api_version"] = api_version.strip()

        # OAuth Configuration
        print("\n🔐 OAuth Client Configuration:")
        print("Configure OAuth clients for integration (optional):")

        for client_name, client_config in self.config["oauth_clients"].items():
            print(f"\n--- {client_name.title()} OAuth ---")
            
            configure = input(f"Configure {client_name.title()}? [y/N]: ")
            if configure.lower() in ['y', 'yes']:
                client_id = input(f"Client ID: ")
                if client_id.strip():
                    client_config["client_id"] = client_id.strip()

                client_secret = input(f"Client Secret: ")
                if client_secret.strip():
                    client_config["client_secret"] = client_secret.strip()

                # Custom redirect URI
                redirect_uri = input(f"Redirect URI (current: {client_config['redirect_uri']}): ")
                if redirect_uri.strip():
                    client_config["redirect_uri"] = redirect_uri.strip()

        # Session Settings
        print("\n⚙️ Session Settings:")
        
        auto_record = input(f"Auto-record prompts? (current: {self.config['session']['auto_prompt_recording']}) [y/n]: ")
        if auto_record.lower() in ['y', 'yes']:
            self.config["session"]["auto_prompt_recording"] = True
        elif auto_record.lower() in ['n', 'no']:
            self.config["session"]["auto_prompt_recording"] = False

        port = input(f"Port (current: {self.config['session']['port']}): ")
        if port.strip() and port.isdigit():
            self.config["session"]["port"] = int(port)

        debug = input(f"Debug mode? (current: {self.config['session']['debug']}) [y/n]: ")
        if debug.lower() in ['y', 'yes']:
            self.config["session"]["debug"] = True
        elif debug.lower() in ['n', 'no']:
            self.config["session"]["debug"] = False

        return True

    def create_env_file(self):
        """Create .env file from configuration"""
        provider = self.config["llm_provider"]
        provider_config = self.config["providers"][provider]

        env_content = f"""# PDD Universal Configuration
# Generated automatically by config_manager.py

# AI Provider Configuration
LLM_PROVIDER={provider}
API_KEY={provider_config['api_key']}
MODEL={provider_config['model']}
BASE_URL={provider_config['base_url']}
"""

        # Azure specific
        if provider == "azure":
            env_content += f"API_VERSION={provider_config.get('api_version', '2024-02-15-preview')}\n"

        # OpenAI Specific (for compatibility)
        env_content += f"""
# OpenAI Specific (for compatibility)
OPENAI_API_KEY={provider_config['api_key'] if provider == 'openai' else ''}
OPENAI_MODEL={provider_config['model'] if provider == 'openai' else 'gpt-4'}

# Session Configuration
PORT={self.config['session']['port']}
DEBUG={str(self.config['session']['debug']).lower()}
AUTO_PROMPT_RECORDING={str(self.config['session']['auto_prompt_recording']).lower()}

"""

        # Add OAuth configurations
        for client_name, client_config in self.config["oauth_clients"].items():
            if client_config["client_id"] or client_config["client_secret"]:
                env_content += f"""# {client_name.title()} OAuth Configuration
{client_name.upper()}_CLIENT_ID={client_config['client_id']}
{client_name.upper()}_CLIENT_SECRET={client_config['client_secret']}
{client_name.upper()}_REDIRECT_URI={client_config['redirect_uri']}
"""
                if "scopes" in client_config:
                    env_content += f"{client_name.upper()}_SCOPES={client_config['scopes']}\n"
                env_content += "\n"

        with open(self.env_file, 'w') as f:
            f.write(env_content)

        print(f"✅ Created .env file with {provider.title()} configuration")

    def create_requirements(self):
        """Create requirements.txt with all possible dependencies"""
        requirements = [
            "# Core Framework",
            "chainlit>=1.2.0",
            "python-dotenv>=1.0.1",
            "",
            "# AI Providers",
            "openai>=1.40.0",
            "anthropic>=0.25.0",
            "google-generativeai>=0.3.0",
            "",
            "# Auto Prompt Recording",
            "pyperclip>=1.8.0",
            "psutil>=5.9.0",
            "",
            "# OAuth and HTTP",
            "requests>=2.31.0",
            "requests-oauthlib>=1.3.0",
            "authlib>=1.2.0",
            "",
            "# Data Handling",
            "pydantic>=2.0.0",
            "python-dateutil>=2.8.0",
            "",
            "# Development Tools",
            "pytest>=8.0.0",
            "pytest-asyncio>=0.23.0",
            "black>=23.0.0",
            "ruff>=0.5.0",
            "",
            "# Optional: Xero Integration",
            "xero-python>=4.0.0  # Uncomment if using Xero",
            "",
            "# Optional: Database",
            "sqlalchemy>=2.0.0  # Uncomment if using database",
            "alembic>=1.12.0  # Uncomment if using database"
        ]

        with open("requirements.txt", 'w') as f:
            f.write("\n".join(requirements))

        print("✅ Created/updated requirements.txt with all dependencies")

    def run(self):
        """Main configuration workflow"""
        # Check if we need interactive setup
        provider = self.config["llm_provider"]
        provider_config = self.config["providers"][provider]

        needs_setup = (
            not provider_config["api_key"] or
            not self.config_file.exists() or
            not self.env_file.exists()
        )

        if needs_setup:
            print("🔧 Initial setup required or missing configuration detected")
            if not self.setup_interactive():
                return False
        else:
            print(f"✅ Using existing configuration: {provider.title()}")
            
            # Quick check if user wants to change anything
            change = input("Change configuration? [y/N]: ")
            if change.lower() in ['y', 'yes']:
                if not self.setup_interactive():
                    return False

        # Save configuration and create files
        self.save_config()
        self.create_env_file()
        self.create_requirements()

        # Update chainlit app for multi-LLM support
        self.update_chainlit_app()

        print("\n🎉 Configuration complete!")
        print(f"🤖 AI Provider: {self.config['llm_provider'].title()}")
        print(f"📱 Model: {self.config['providers'][self.config['llm_provider']]['model']}")
        
        oauth_count = sum(1 for client in self.config['oauth_clients'].values() if client['client_id'])
        if oauth_count > 0:
            print(f"🔐 OAuth Clients: {oauth_count} configured")
        
        print(f"📝 Auto-recording: {self.config['session']['auto_prompt_recording']}")
        print("\n🚀 Starting development session...")
        
        return True

    def update_chainlit_app(self):
        """Update chainlit app to support multiple LLM providers"""
        app_content = '''#!/usr/bin/env python3
"""
Universal Chainlit App with Multi-LLM Support
Supports: OpenAI, DeepSeek, Anthropic, Local LLMs, Azure OpenAI
"""

import os
import asyncio
import chainlit as cl
from typing import Optional, Dict, Any
import json
from pathlib import Path

# Import LLM clients
try:
    from openai import AsyncOpenAI
except ImportError:
    AsyncOpenAI = None

try:
    import anthropic
except ImportError:
    anthropic = None

try:
    import google.generativeai as genai
except ImportError:
    genai = None

# Load configuration
config_file = Path("config.json")
if config_file.exists():
    with open(config_file, 'r') as f:
        app_config = json.load(f)
else:
    app_config = {"llm_provider": "openai"}

class UniversalLLMClient:
    def __init__(self):
        self.provider = os.getenv("LLM_PROVIDER", app_config.get("llm_provider", "openai"))
        self.api_key = os.getenv("API_KEY")
        self.model = os.getenv("MODEL")
        self.base_url = os.getenv("BASE_URL")
        self.client = self.setup_client()

    def setup_client(self):
        """Setup client based on provider"""
        if self.provider == "openai":
            return AsyncOpenAI(
                api_key=self.api_key,
                base_url=None  # Use default OpenAI URL
            )
        elif self.provider == "deepseek":
            return AsyncOpenAI(
                api_key=self.api_key,
                base_url=self.base_url
            )
        elif self.provider == "azure":
            return AsyncOpenAI(
                api_key=self.api_key,
                base_url=self.base_url,
                api_version=os.getenv("API_VERSION", "2024-02-15-preview")
            )
        elif self.provider == "anthropic":
            if anthropic:
                return anthropic.AsyncAnthropic(api_key=self.api_key)
            else:
                raise ImportError("anthropic package not installed. Run: pip install anthropic")
        elif self.provider == "local":
            return AsyncOpenAI(
                api_key="local",
                base_url=self.base_url
            )
        elif self.provider == "gemini":
            if genai:
                genai.configure(api_key=self.api_key)
                return genai  # Return the configured module
            else:
                raise ImportError("google-generativeai package not installed. Run: pip install google-generativeai")
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")

    async def chat_completion(self, messages: list) -> str:
        """Universal chat completion"""
        try:
            if self.provider == "anthropic":
                # Anthropic format
                response = await self.client.messages.create(
                    model=self.model,
                    max_tokens=2000,
                    messages=messages
                )
                return response.content[0].text
            elif self.provider == "gemini":
                # Gemini format
                model = self.client.GenerativeModel(self.model)
                # Convert messages to Gemini format - combine into single prompt
                prompt_parts = []
                for msg in messages:
                    if msg['role'] == 'system':
                        prompt_parts.append(f"Instructions: {msg['content']}")
                    elif msg['role'] == 'user':
                        prompt_parts.append(f"User: {msg['content']}")
                    elif msg['role'] == 'assistant':
                        prompt_parts.append(f"Assistant: {msg['content']}")
                
                prompt = "\n\n".join(prompt_parts)
                
                # Generate response (Gemini doesn't have native async, so we'll wrap it)
                import asyncio
                loop = asyncio.get_event_loop()
                response = await loop.run_in_executor(None, model.generate_content, prompt)
                return response.text
            else:
                # OpenAI-compatible format
                response = await self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    max_tokens=2000,
                    temperature=0.7
                )
                return response.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"

# Initialize LLM client
llm_client = UniversalLLMClient()

@cl.on_chat_start
async def start():
    """Initialize chat session"""
    provider = llm_client.provider.title()
    model = llm_client.model
    
    # OAuth client info
    oauth_info = ""
    config_file = Path("config.json")
    if config_file.exists():
        with open(config_file, 'r') as f:
            config = json.load(f)
            oauth_clients = [name for name, client in config.get('oauth_clients', {}).items() 
                           if client.get('client_id')]
            if oauth_clients:
                oauth_info = f"\\n🔐 **OAuth Clients:** {', '.join(oauth_clients).title()}"
    
    welcome_msg = f"""# Welcome to PDD Universal AI Agent!

🤖 **AI Provider:** {provider}
📱 **Model:** {model}
📝 **Auto-recording:** {"Enabled" if os.getenv("AUTO_PROMPT_RECORDING", "true").lower() == "true" else "Disabled"}{oauth_info}

I'm ready to help you with your development tasks using Prompt-Driven Development methodology!

**Available Commands:**
- Ask me anything about your project
- Request code implementation  
- Get architectural guidance
- Debug issues
- Integrate with external services (Xero, GitHub, etc.)

Your prompts are automatically recorded as PHRs for documentation.
"""
    
    await cl.Message(
        content=welcome_msg,
        author="System"
    ).send()

@cl.on_message
async def main(message: cl.Message):
    """Handle user messages"""
    try:
        # Prepare messages for LLM
        messages = [
            {"role": "system", "content": "You are a helpful AI assistant specialized in Prompt-Driven Development. Help users with coding, architecture, and development tasks. You can also help with API integrations including OAuth flows for services like Xero, GitHub, Google, etc."},
            {"role": "user", "content": message.content}
        ]

        # Get response from LLM
        response = await llm_client.chat_completion(messages)

        # Send response
        await cl.Message(
            content=response,
            author="Assistant"
        ).send()

    except Exception as e:
        error_msg = f"Sorry, I encountered an error: {str(e)}"
        await cl.Message(
            content=error_msg,
            author="System"
        ).send()

if __name__ == "__main__":
    # This should not be called directly
    pass
'''

        with open("chainlit_app.py", 'w') as f:
            f.write(app_content)

        print("✅ Updated chainlit_app.py for multi-LLM support")

if __name__ == "__main__":
    manager = ConfigManager()
    success = manager.run()
    exit(0 if success else 1)