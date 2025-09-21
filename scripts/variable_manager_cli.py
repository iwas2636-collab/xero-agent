#!/usr/bin/env python3
"""
Variable Manager Command Line Interface
Supports automated configuration from command line arguments
"""

import sys
import argparse
from variable_manager import VariableManager

def auto_configure_provider(provider: str, api_key: str = None):
    """Auto-configure a specific provider with minimal prompts"""
    manager = VariableManager()
    
    # Map provider names to variable keys
    provider_mappings = {
        "openai": {"api_key": "OPENAI_API_KEY", "model": "OPENAI_MODEL"},
        "gemini": {"api_key": "GOOGLE_API_KEY", "model": "GEMINI_MODEL"},
        "anthropic": {"api_key": "ANTHROPIC_API_KEY", "model": "ANTHROPIC_MODEL"},
        "deepseek": {"api_key": "DEEPSEEK_API_KEY", "model": "DEEPSEEK_MODEL"},
        "azure": {"api_key": "AZURE_OPENAI_API_KEY", "endpoint": "AZURE_OPENAI_ENDPOINT", "deployment": "AZURE_OPENAI_DEPLOYMENT"}
    }
    
    if provider not in provider_mappings:
        print(f"❌ Unknown provider: {provider}")
        return False
    
    mapping = provider_mappings[provider]
    
    # Set API key if provided
    if api_key and "api_key" in mapping:
        manager.variables[mapping["api_key"]] = api_key
        print(f"✅ {provider} API key configured")
    
    # Set default model
    if "model" in mapping:
        model_defaults = {
            "OPENAI_MODEL": "gpt-4o-mini",
            "GEMINI_MODEL": "gemini-2.0-flash-exp",
            "ANTHROPIC_MODEL": "claude-3-5-sonnet-20241022",
            "DEEPSEEK_MODEL": "deepseek-chat"
        }
        default_model = model_defaults.get(mapping["model"])
        if default_model:
            manager.variables[mapping["model"]] = default_model
            print(f"✅ {provider} model set to {default_model}")
    
    # Add basic application settings
    manager.variables["CHAINLIT_PORT"] = "8001"
    manager.variables["DEBUG"] = "false"
    manager.variables["LOG_LEVEL"] = "INFO"
    
    # Update files
    try:
        manager.update_config_json()
        manager.update_env_file()
        manager.update_chainlit_app()
        manager.update_requirements_txt()
        manager.update_gitignore()
        print(f"✅ {provider} provider configured successfully")
        return True
    except Exception as e:
        print(f"❌ Configuration failed: {e}")
        return False

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(description="PDD Universal Variable Manager")
    parser.add_argument("--provider", choices=["openai", "gemini", "anthropic", "deepseek", "azure"], 
                       help="Auto-configure specific provider")
    parser.add_argument("--api-key", help="API key for the provider")
    parser.add_argument("--auto", action="store_true", help="Run in automated mode")
    parser.add_argument("--interactive", action="store_true", help="Run interactive configuration")
    
    args = parser.parse_args()
    
    if args.provider and args.auto:
        # Automated provider configuration
        success = auto_configure_provider(args.provider, args.api_key)
        sys.exit(0 if success else 1)
    
    elif args.interactive or len(sys.argv) == 1:
        # Interactive configuration
        manager = VariableManager()
        success = manager.run_full_configuration()
        sys.exit(0 if success else 1)
    
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()