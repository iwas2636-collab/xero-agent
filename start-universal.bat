@echo off
REM PDD Universal Development Session Starter
REM Supports multiple LLM providers, OAuth clients, and full automation

title PDD Universal Development Session

echo.
echo  ██████╗ ██████╗ ██████╗     ██╗   ██╗███╗   ██╗██╗██╗   ██╗███████╗██████╗ ███████╗ █████╗ ██╗     
echo  ██╔══██╗██╔══██╗██╔══██╗    ██║   ██║████╗  ██║██║██║   ██║██╔════╝██╔══██╗██╔════╝██╔══██╗██║     
echo  ██████╔╝██║  ██║██║  ██║    ██║   ██║██╔██╗ ██║██║██║   ██║█████╗  ██████╔╝███████╗███████║██║     
echo  ██╔═══╝ ██║  ██║██║  ██║    ██║   ██║██║╚██╗██║██║╚██╗ ██╔╝██╔══╝  ██╔══██╗╚════██║██╔══██║██║     
echo  ██║     ██████╔╝██████╔╝    ╚██████╔╝██║ ╚████║██║ ╚████╔╝ ███████╗██║  ██║███████║██║  ██║███████╗
echo  ╚═╝     ╚═════╝ ╚═════╝      ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚══════╝
echo.
echo  Prompt-Driven Development
echo  Auto Session Manager
echo.

REM Check for command line arguments
if "%1"=="test" (
    echo 🧪 Testing LLM Providers...
    python scripts\test_providers.py
    pause
    goto :eof
)

if "%1"=="config" (
    echo ⚙️ Configuration Only...
    python scripts\config_manager.py
    pause
    goto :eof
)
echo  Supports: OpenAI, DeepSeek, Anthropic, Local LLMs + OAuth Integration
echo.

REM Check if configuration utility exists, if not create it
if not exist "scripts\config_manager.py" (
    echo 🔧 Setting up configuration manager...
    python -c "
import os
os.makedirs('scripts', exist_ok=True)
" 2>nul
    call :create_config_manager
)

REM Check if environment configurator exists
if not exist "scripts\env_configurator.py" (
    echo 🔧 Setting up environment configurator...
    call :create_env_configurator
)

REM Run the universal configuration and startup
echo 🚀 Starting Universal PDD Session...

REM Check for configuration
if not exist "config.json" (
    echo ⚠️  No configuration found
    echo.
    echo Choose configuration option:
    echo   1. Run full variable configuration (recommended)
    echo   2. Run basic LLM setup
    echo   3. Continue without configuration
    echo.
    set /p CONFIG_CHOICE="Enter choice (1-3): "
    
    if "!CONFIG_CHOICE!"=="1" (
        echo.
        echo 🔧 Starting full variable configuration...
        if exist "configure-variables.bat" (
            call configure-variables.bat
        ) else (
            python scripts\variable_manager.py
        )
    ) else if "!CONFIG_CHOICE!"=="2" (
        echo.
        echo 🔧 Starting basic LLM configuration...
        python scripts\config_manager.py
    ) else (
        echo.
        echo ⚠️  Continuing without configuration...
        echo You can configure later by running: configure-variables.bat
        timeout /t 3 >nul
    )
) else (
    echo ✅ Configuration found
)

python scripts\config_manager.py

REM If config succeeded, start the session
if not errorlevel 1 (
    python scripts\dev_session.py
) else (
    echo.
    echo ❌ Configuration failed. Please check your settings.
    pause
)

goto :eof

REM ============================================================================
REM CREATE CONFIG MANAGER
REM ============================================================================
:create_config_manager
echo Creating config_manager.py...
(
echo #!/usr/bin/env python3
echo """
echo Universal Configuration Manager for PDD Development
echo Supports multiple LLM providers and OAuth configurations
echo """
echo.
echo import os
echo import json
echo from pathlib import Path
echo from typing import Dict, Any
echo.
echo class ConfigManager:
echo     def __init__^(self^):
echo         self.config_file = Path^("config.json"^)
echo         self.env_file = Path^(".env"^)
echo         self.config = self.load_config^(^)
echo.
echo     def load_config^(self^) -^> Dict[str, Any]:
echo         """Load existing configuration or create default"""
echo         if self.config_file.exists^(^):
echo             with open^(self.config_file, 'r'^) as f:
echo                 return json.load^(f^)
echo         return self.get_default_config^(^)
echo.
echo     def get_default_config^(self^) -^> Dict[str, Any]:
echo         """Default configuration template"""
echo         return {
echo             "llm_provider": "openai",
echo             "providers": {
echo                 "openai": {
echo                     "api_key": "",
echo                     "model": "gpt-4",
echo                     "base_url": "https://api.openai.com/v1"
echo                 },
echo                 "deepseek": {
echo                     "api_key": "",
echo                     "model": "deepseek-chat",
echo                     "base_url": "https://api.deepseek.com/v1"
echo                 },
echo                 "anthropic": {
echo                     "api_key": "",
echo                     "model": "claude-3-sonnet-20240229",
echo                     "base_url": "https://api.anthropic.com/v1"
echo                 },
echo                 "local": {
echo                     "api_key": "local",
echo                     "model": "llama2",
echo                     "base_url": "http://localhost:11434/v1"
echo                 }
echo             },
echo             "oauth_clients": {
echo                 "xero": {
echo                     "client_id": "",
echo                     "client_secret": "",
echo                     "redirect_uri": "http://localhost:8001/callback",
echo                     "scopes": "accounting.transactions,accounting.contacts"
echo                 },
echo                 "github": {
echo                     "client_id": "",
echo                     "client_secret": "",
echo                     "redirect_uri": "http://localhost:8001/callback"
echo                 },
echo                 "google": {
echo                     "client_id": "",
echo                     "client_secret": "",
echo                     "redirect_uri": "http://localhost:8001/callback"
echo                 }
echo             },
echo             "session": {
echo                 "auto_prompt_recording": True,
echo                 "auto_start_watcher": True,
echo                 "port": 8001,
echo                 "debug": False
echo             }
echo         }
echo.
echo     def save_config^(self^):
echo         """Save configuration to file"""
echo         with open^(self.config_file, 'w'^) as f:
echo             json.dump^(self.config, f, indent=2^)
echo.
echo     def setup_interactive^(self^):
echo         """Interactive configuration setup"""
echo         print^("🔧 PDD Universal Configuration Setup"^)
echo         print^("=" * 50^)
echo.
echo         # LLM Provider Selection
echo         print^("\\n📱 Select your AI provider:"^)
echo         providers = list^(self.config["providers"].keys^(^)^)
echo         for i, provider in enumerate^(providers, 1^):
echo             current = " ^(current^)" if provider == self.config["llm_provider"] else ""
echo             print^(f"   {i}. {provider.title^(^)}{current}"^)
echo.
echo         choice = input^("Enter choice ^(1-{}^) or press Enter for current: ".format^(len^(providers^)^)^)
echo         if choice.strip^(^):
echo             try:
echo                 provider_idx = int^(choice^) - 1
echo                 if 0 ^<= provider_idx ^< len^(providers^):
echo                     self.config["llm_provider"] = providers[provider_idx]
echo                     print^(f"✅ Selected: {providers[provider_idx].title^(^)}"^)
echo             except ValueError:
echo                 print^("Invalid choice, keeping current provider"^)
echo.
echo         # Configure selected provider
echo         provider = self.config["llm_provider"]
echo         provider_config = self.config["providers"][provider]
echo.
echo         print^(f"\\n🔑 Configure {provider.title^(^)} API settings:"^)
echo         
echo         api_key = input^(f"API Key ^(current: {'*' * min^(len^(provider_config['api_key']^), 8^) if provider_config['api_key'] else 'not set'}^): "^)
echo         if api_key.strip^(^):
echo             provider_config["api_key"] = api_key.strip^(^)
echo.
echo         model = input^(f"Model ^(current: {provider_config['model']}^): "^)
echo         if model.strip^(^):
echo             provider_config["model"] = model.strip^(^)
echo.
echo         if provider != "local":
echo             base_url = input^(f"Base URL ^(current: {provider_config['base_url']}^): "^)
echo             if base_url.strip^(^):
echo                 provider_config["base_url"] = base_url.strip^(^)
echo.
echo         # OAuth Configuration
echo         print^("\\n🔐 OAuth Client Configuration:"^)
echo         print^("Configure OAuth clients for integration ^(optional^):"^)
echo.
echo         for client_name, client_config in self.config["oauth_clients"].items^(^):
echo             print^(f"\\n--- {client_name.title^(^)} OAuth ---"^)
echo             
echo             client_id = input^(f"Client ID ^(current: {'*' * min^(len^(client_config['client_id']^), 8^) if client_config['client_id'] else 'not set'}^): "^)
echo             if client_id.strip^(^):
echo                 client_config["client_id"] = client_id.strip^(^)
echo.
echo             client_secret = input^(f"Client Secret ^(current: {'*' * min^(len^(client_config['client_secret']^), 8^) if client_config['client_secret'] else 'not set'}^): "^)
echo             if client_secret.strip^(^):
echo                 client_config["client_secret"] = client_secret.strip^(^)
echo.
echo         # Session Settings
echo         print^("\\n⚙️ Session Settings:"^)
echo         
echo         auto_record = input^(f"Auto-record prompts? ^(current: {self.config['session']['auto_prompt_recording']}^) [y/n]: "^)
echo         if auto_record.lower^(^) in ['y', 'yes']:
echo             self.config["session"]["auto_prompt_recording"] = True
echo         elif auto_record.lower^(^) in ['n', 'no']:
echo             self.config["session"]["auto_prompt_recording"] = False
echo.
echo         port = input^(f"Port ^(current: {self.config['session']['port']}^): "^)
echo         if port.strip^(^) and port.isdigit^(^):
echo             self.config["session"]["port"] = int^(port^)
echo.
echo         return True
echo.
echo     def create_env_file^(self^):
echo         """Create .env file from configuration"""
echo         provider = self.config["llm_provider"]
echo         provider_config = self.config["providers"][provider]
echo.
echo         env_content = f"""# PDD Universal Configuration
echo # Generated automatically by config_manager.py
echo.
echo # AI Provider Configuration
echo LLM_PROVIDER={provider}
echo API_KEY={provider_config['api_key']}
echo MODEL={provider_config['model']}
echo BASE_URL={provider_config['base_url']}
echo.
echo # OpenAI Specific ^(for compatibility^)
echo OPENAI_API_KEY={provider_config['api_key'] if provider == 'openai' else ''}
echo OPENAI_MODEL={provider_config['model'] if provider == 'openai' else 'gpt-4'}
echo.
echo # Session Configuration
echo PORT={self.config['session']['port']}
echo DEBUG={str^(self.config['session']['debug']^).lower^(^)}
echo AUTO_PROMPT_RECORDING={str^(self.config['session']['auto_prompt_recording']^).lower^(^)}
echo.
echo """
echo.
echo         # Add OAuth configurations
echo         for client_name, client_config in self.config["oauth_clients"].items^(^):
echo             if client_config["client_id"] or client_config["client_secret"]:
echo                 env_content += f"""# {client_name.title^(^)} OAuth Configuration
echo {client_name.upper^(^)}_CLIENT_ID={client_config['client_id']}
echo {client_name.upper^(^)}_CLIENT_SECRET={client_config['client_secret']}
echo {client_name.upper^(^)}_REDIRECT_URI={client_config['redirect_uri']}
echo """
echo                 if "scopes" in client_config:
echo                     env_content += f"{client_name.upper^(^)}_SCOPES={client_config['scopes']}\\n"
echo                 env_content += "\\n"
echo.
echo         with open^(self.env_file, 'w'^) as f:
echo             f.write^(env_content^)
echo.
echo         print^(f"✅ Created .env file with {provider.title^(^)} configuration"^)
echo.
echo     def run^(self^):
echo         """Main configuration workflow"""
echo         # Check if we need interactive setup
echo         provider = self.config["llm_provider"]
echo         provider_config = self.config["providers"][provider]
echo.
echo         needs_setup = ^(
echo             not provider_config["api_key"] or
echo             not self.config_file.exists^(^) or
echo             not self.env_file.exists^(^)
echo         ^)
echo.
echo         if needs_setup:
echo             print^("🔧 Initial setup required or missing configuration detected"^)
echo             if not self.setup_interactive^(^):
echo                 return False
echo         else:
echo             print^(f"✅ Using existing configuration: {provider.title^(^)}"^)
echo             
echo             # Quick check if user wants to change anything
echo             change = input^("Change configuration? [y/N]: "^)
echo             if change.lower^(^) in ['y', 'yes']:
echo                 if not self.setup_interactive^(^):
echo                     return False
echo.
echo         # Save configuration and create .env
echo         self.save_config^(^)
echo         self.create_env_file^(^)
echo.
echo         print^("\\n🎉 Configuration complete!"^)
echo         print^(f"🤖 AI Provider: {self.config['llm_provider'].title^(^)}"^)
echo         print^(f"📱 Model: {self.config['providers'][self.config['llm_provider']]['model']}"^)
echo         
echo         oauth_count = sum^(1 for client in self.config['oauth_clients'].values^(^) if client['client_id']^)
echo         if oauth_count ^> 0:
echo             print^(f"🔐 OAuth Clients: {oauth_count} configured"^)
echo         
echo         print^(f"📝 Auto-recording: {self.config['session']['auto_prompt_recording']}"^)
echo         print^("\\n🚀 Starting development session..."^)
echo         
echo         return True
echo.
echo if __name__ == "__main__":
echo     manager = ConfigManager^(^)
echo     success = manager.run^(^)
echo     exit^(0 if success else 1^)
) > scripts\config_manager.py

echo ✅ Created config_manager.py
goto :eof

REM ============================================================================
REM CREATE ENVIRONMENT CONFIGURATOR
REM ============================================================================
:create_env_configurator
echo Creating env_configurator.py...
(
echo #!/usr/bin/env python3
echo """
echo Environment Configurator - Updates Chainlit app for multiple LLM providers
echo """
echo.
echo import os
echo import json
echo from pathlib import Path
echo.
echo class EnvConfigurator:
echo     def __init__^(self^):
echo         self.chainlit_app = Path^("chainlit_app.py"^)
echo         self.config_file = Path^("config.json"^)
echo.
echo     def update_chainlit_app^(self^):
echo         """Update chainlit app to support multiple LLM providers"""
echo         if not self.config_file.exists^(^):
echo             return False
echo.
echo         with open^(self.config_file, 'r'^) as f:
echo             config = json.load^(f^)
echo.
echo         # Create universal chainlit app
echo         app_content = '''#!/usr/bin/env python3
echo """
echo Universal Chainlit App with Multi-LLM Support
echo Supports: OpenAI, DeepSeek, Anthropic, Local LLMs
echo """
echo.
echo import os
echo import asyncio
echo import chainlit as cl
echo from typing import Optional, Dict, Any
echo import json
echo from pathlib import Path
echo.
echo # Import LLM clients
echo try:
echo     from openai import AsyncOpenAI
echo except ImportError:
echo     AsyncOpenAI = None
echo.
echo try:
echo     import anthropic
echo except ImportError:
echo     anthropic = None
echo.
echo # Load configuration
echo config_file = Path^("config.json"^)
echo if config_file.exists^(^):
echo     with open^(config_file, 'r'^) as f:
echo         app_config = json.load^(f^)
echo else:
echo     app_config = {"llm_provider": "openai"}
echo.
echo class UniversalLLMClient:
echo     def __init__^(self^):
echo         self.provider = os.getenv^("LLM_PROVIDER", app_config.get^("llm_provider", "openai"^)^)
echo         self.api_key = os.getenv^("API_KEY"^)
echo         self.model = os.getenv^("MODEL"^)
echo         self.base_url = os.getenv^("BASE_URL"^)
echo         self.client = self.setup_client^(^)
echo.
echo     def setup_client^(self^):
echo         """Setup client based on provider"""
echo         if self.provider == "openai":
echo             return AsyncOpenAI^(
echo                 api_key=self.api_key,
echo                 base_url=self.base_url if self.base_url != "https://api.openai.com/v1" else None
echo             ^)
echo         elif self.provider == "deepseek":
echo             return AsyncOpenAI^(
echo                 api_key=self.api_key,
echo                 base_url=self.base_url
echo             ^)
echo         elif self.provider == "anthropic":
echo             if anthropic:
echo                 return anthropic.AsyncAnthropic^(api_key=self.api_key^)
echo             else:
echo                 raise ImportError^("anthropic package not installed"^)
echo         elif self.provider == "local":
echo             return AsyncOpenAI^(
echo                 api_key="local",
echo                 base_url=self.base_url
echo             ^)
echo         else:
echo             raise ValueError^(f"Unsupported provider: {self.provider}"^)
echo.
echo     async def chat_completion^(self, messages: list^) -^> str:
echo         """Universal chat completion"""
echo         try:
echo             if self.provider == "anthropic":
echo                 # Anthropic format
echo                 response = await self.client.messages.create^(
echo                     model=self.model,
echo                     max_tokens=2000,
echo                     messages=messages
echo                 ^)
echo                 return response.content[0].text
echo             else:
echo                 # OpenAI-compatible format
echo                 response = await self.client.chat.completions.create^(
echo                     model=self.model,
echo                     messages=messages,
echo                     max_tokens=2000,
echo                     temperature=0.7
echo                 ^)
echo                 return response.choices[0].message.content
echo         except Exception as e:
echo             return f"Error: {str^(e^)}"
echo.
echo # Initialize LLM client
echo llm_client = UniversalLLMClient^(^)
echo.
echo @cl.on_chat_start
echo async def start^(^):
echo     """Initialize chat session"""
echo     provider = llm_client.provider.title^(^)
echo     model = llm_client.model
echo     
echo     welcome_msg = f"""# Welcome to PDD Universal AI Agent!
echo.
echo 🤖 **AI Provider:** {provider}
echo 📱 **Model:** {model}
echo 📝 **Auto-recording:** {"Enabled" if os.getenv^("AUTO_PROMPT_RECORDING", "true"^).lower^(^) == "true" else "Disabled"}
echo.
echo I'm ready to help you with your development tasks using Prompt-Driven Development methodology!
echo.
echo **Available Commands:**
echo - Ask me anything about your project
echo - Request code implementation
echo - Get architectural guidance
echo - Debug issues
echo.
echo Your prompts are automatically recorded as PHRs for documentation.
echo """
echo     
echo     await cl.Message^(
echo         content=welcome_msg,
echo         author="System"
echo     ^).send^(^)
echo.
echo @cl.on_message
echo async def main^(message: cl.Message^):
echo     """Handle user messages"""
echo     try:
echo         # Prepare messages for LLM
echo         messages = [
echo             {"role": "system", "content": "You are a helpful AI assistant specialized in Prompt-Driven Development. Help users with coding, architecture, and development tasks."},
echo             {"role": "user", "content": message.content}
echo         ]
echo.
echo         # Get response from LLM
echo         response = await llm_client.chat_completion^(messages^)
echo.
echo         # Send response
echo         await cl.Message^(
echo             content=response,
echo             author="Assistant"
echo         ^).send^(^)
echo.
echo     except Exception as e:
echo         error_msg = f"Sorry, I encountered an error: {str^(e^)}"
echo         await cl.Message^(
echo             content=error_msg,
echo             author="System"
echo         ^).send^(^)
echo.
echo if __name__ == "__main__":
echo     # This should not be called directly
echo     pass
echo '''
echo.
echo         with open^(self.chainlit_app, 'w'^) as f:
echo             f.write^(app_content^)
echo.
echo         print^("✅ Updated chainlit_app.py for multi-LLM support"^)
echo         return True
echo.
echo if __name__ == "__main__":
echo     configurator = EnvConfigurator^(^)
echo     configurator.update_chainlit_app^(^)
) > scripts\env_configurator.py

echo ✅ Created env_configurator.py
goto :eof