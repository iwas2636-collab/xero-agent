#!/usr/bin/env python3
"""
Universal dependency installer for PDD projects
Handles all possible LLM providers and OAuth integrations
"""

import subprocess
import sys
import os
from pathlib import Path

def install_base_requirements():
    """Install base requirements for PDD"""
    base_packages = [
        "chainlit>=1.2.0",
        "python-dotenv>=1.0.1",
        "pyperclip>=1.8.0",
        "psutil>=5.9.0",
        "requests>=2.31.0",
        "pydantic>=2.0.0",
    ]
    
    print("📦 Installing base PDD requirements...")
    for package in base_packages:
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", package], 
                         check=True, capture_output=True)
            print(f"✅ {package}")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install {package}: {e}")

def install_llm_providers():
    """Install LLM provider packages"""
    llm_packages = {
        "openai": "openai>=1.40.0",
        "anthropic": "anthropic>=0.25.0",
        "azure": "openai>=1.40.0",  # Azure uses OpenAI SDK
        "gemini": "google-generativeai>=0.3.0",
    }
    
    print("\n📱 Installing LLM provider packages...")
    for provider, package in llm_packages.items():
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", package], 
                         check=True, capture_output=True)
            print(f"✅ {provider}: {package}")
        except subprocess.CalledProcessError as e:
            print(f"⚠️  Optional {provider} provider failed: {e}")

def install_oauth_packages():
    """Install OAuth and integration packages"""
    oauth_packages = [
        "requests-oauthlib>=1.3.0",
        "authlib>=1.2.0",
        "python-dateutil>=2.8.0",
    ]
    
    print("\n🔐 Installing OAuth packages...")
    for package in oauth_packages:
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", package], 
                         check=True, capture_output=True)
            print(f"✅ {package}")
        except subprocess.CalledProcessError as e:
            print(f"⚠️  Optional OAuth package failed: {e}")

def install_optional_packages():
    """Install optional integration packages"""
    optional_packages = {
        "xero": "xero-python>=4.0.0",
        "database": "sqlalchemy>=2.0.0",
        "testing": "pytest>=8.0.0",
        "formatting": "black>=23.0.0",
    }
    
    print("\n📋 Installing optional packages...")
    for category, package in optional_packages.items():
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", package], 
                         check=True, capture_output=True)
            print(f"✅ {category}: {package}")
        except subprocess.CalledProcessError as e:
            print(f"⚠️  Optional {category} package failed: {e}")

def check_installation():
    """Check if all packages are properly installed"""
    print("\n🔍 Checking installation...")
    
    critical_packages = ["chainlit", "pyperclip", "requests", "pydantic"]
    llm_packages = ["openai", "anthropic", "google.generativeai"]
    
    all_good = True
    
    # Check critical packages
    for package in critical_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - REQUIRED")
            all_good = False
    
    # Check LLM packages (at least one should work)
    llm_available = []
    for package in llm_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
            llm_available.append(package)
        except ImportError:
            print(f"⚠️  {package} - Optional")
    
    if not llm_available:
        print("❌ No LLM providers available - install at least OpenAI or Anthropic")
        all_good = False
    
    return all_good

def main():
    """Main installation process"""
    print("🚀 PDD Universal Dependency Installer")
    print("=" * 50)
    
    # Install base requirements
    install_base_requirements()
    
    # Install LLM providers
    install_llm_providers()
    
    # Install OAuth packages
    install_oauth_packages()
    
    # Install optional packages
    install_optional_packages()
    
    # Check installation
    if check_installation():
        print("\n🎉 Installation complete! All dependencies ready.")
        print("\n🚀 Next steps:")
        print("   1. Run: start-universal.bat")
        print("   2. Configure your LLM provider and API keys")
        print("   3. Start developing with PDD methodology!")
        return True
    else:
        print("\n❌ Installation incomplete. Please check errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)