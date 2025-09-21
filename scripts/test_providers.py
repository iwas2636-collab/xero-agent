#!/usr/bin/env python3
"""
Test all LLM providers to ensure they work correctly
"""

import os
import asyncio
import json
from pathlib import Path

# Import all possible LLM clients
try:
    from openai import AsyncOpenAI
    openai_available = True
except ImportError:
    openai_available = False

try:
    import anthropic
    anthropic_available = True
except ImportError:
    anthropic_available = False

try:
    import google.generativeai as genai
    gemini_available = True
except ImportError:
    gemini_available = False

class LLMTester:
    def __init__(self):
        self.results = {}
        
    async def test_openai(self, api_key, model="gpt-3.5-turbo"):
        """Test OpenAI connection"""
        if not openai_available:
            return {"status": "error", "message": "OpenAI package not installed"}
            
        try:
            client = AsyncOpenAI(api_key=api_key)
            response = await client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": "Say 'OpenAI test successful'"}],
                max_tokens=10
            )
            return {"status": "success", "response": response.choices[0].message.content}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    async def test_deepseek(self, api_key, model="deepseek-chat"):
        """Test DeepSeek connection"""
        if not openai_available:
            return {"status": "error", "message": "OpenAI package not installed (required for DeepSeek)"}
            
        try:
            client = AsyncOpenAI(
                api_key=api_key,
                base_url="https://api.deepseek.com/v1"
            )
            response = await client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": "Say 'DeepSeek test successful'"}],
                max_tokens=10
            )
            return {"status": "success", "response": response.choices[0].message.content}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    async def test_anthropic(self, api_key, model="claude-3-haiku-20240307"):
        """Test Anthropic connection"""
        if not anthropic_available:
            return {"status": "error", "message": "Anthropic package not installed"}
            
        try:
            client = anthropic.AsyncAnthropic(api_key=api_key)
            response = await client.messages.create(
                model=model,
                max_tokens=10,
                messages=[{"role": "user", "content": "Say 'Anthropic test successful'"}]
            )
            return {"status": "success", "response": response.content[0].text}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    async def test_gemini(self, api_key, model="gemini-2.0-flash-exp"):
        """Test Gemini connection"""
        if not gemini_available:
            return {"status": "error", "message": "google-generativeai package not installed"}
            
        try:
            genai.configure(api_key=api_key)
            model_instance = genai.GenerativeModel(model)
            
            # Gemini doesn't have native async, so use executor
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None, 
                model_instance.generate_content, 
                "Say 'Gemini test successful'"
            )
            return {"status": "success", "response": response.text}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    async def test_azure(self, api_key, base_url, model="gpt-4", api_version="2024-02-15-preview"):
        """Test Azure OpenAI connection"""
        if not openai_available:
            return {"status": "error", "message": "OpenAI package not installed (required for Azure)"}
            
        try:
            client = AsyncOpenAI(
                api_key=api_key,
                base_url=base_url,
                api_version=api_version
            )
            response = await client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": "Say 'Azure test successful'"}],
                max_tokens=10
            )
            return {"status": "success", "response": response.choices[0].message.content}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def load_config(self):
        """Load configuration from config.json"""
        config_file = Path("config.json")
        if not config_file.exists():
            return None
            
        with open(config_file, 'r') as f:
            return json.load(f)
    
    async def test_all_providers(self):
        """Test all configured providers"""
        config = self.load_config()
        if not config:
            print("❌ No configuration found. Run start-universal.bat first.")
            return
        
        print("🧪 Testing All LLM Providers")
        print("=" * 50)
        
        providers = config.get("providers", {})
        
        for provider_name, provider_config in providers.items():
            if not provider_config.get("api_key"):
                print(f"⏭️  {provider_name.title()}: No API key configured")
                continue
                
            print(f"\n🔍 Testing {provider_name.title()}...")
            
            try:
                if provider_name == "openai":
                    result = await self.test_openai(
                        provider_config["api_key"], 
                        provider_config["model"]
                    )
                elif provider_name == "deepseek":
                    result = await self.test_deepseek(
                        provider_config["api_key"], 
                        provider_config["model"]
                    )
                elif provider_name == "anthropic":
                    result = await self.test_anthropic(
                        provider_config["api_key"], 
                        provider_config["model"]
                    )
                elif provider_name == "gemini":
                    result = await self.test_gemini(
                        provider_config["api_key"], 
                        provider_config["model"]
                    )
                elif provider_name == "azure":
                    result = await self.test_azure(
                        provider_config["api_key"],
                        provider_config["base_url"], 
                        provider_config["model"],
                        provider_config.get("api_version", "2024-02-15-preview")
                    )
                elif provider_name == "local":
                    print(f"⏭️  {provider_name.title()}: Local testing requires running server")
                    continue
                else:
                    print(f"⚠️  {provider_name.title()}: Unknown provider")
                    continue
                
                if result["status"] == "success":
                    print(f"✅ {provider_name.title()}: {result['response']}")
                else:
                    print(f"❌ {provider_name.title()}: {result['message']}")
                    
                self.results[provider_name] = result
                
            except Exception as e:
                print(f"❌ {provider_name.title()}: Unexpected error - {str(e)}")
                self.results[provider_name] = {"status": "error", "message": str(e)}
        
        # Summary
        print("\n" + "=" * 50)
        print("📊 Test Summary")
        print("=" * 50)
        
        successful = sum(1 for r in self.results.values() if r["status"] == "success")
        total = len(self.results)
        
        print(f"✅ Successful: {successful}/{total}")
        
        if successful > 0:
            print("\n🎉 Ready providers:")
            for provider, result in self.results.items():
                if result["status"] == "success":
                    print(f"   • {provider.title()}")
        
        if successful < total:
            print("\n⚠️  Issues found:")
            for provider, result in self.results.items():
                if result["status"] == "error":
                    print(f"   • {provider.title()}: {result['message']}")
    
    async def test_current_provider(self):
        """Test only the currently configured provider"""
        config = self.load_config()
        if not config:
            print("❌ No configuration found. Run start-universal.bat first.")
            return
        
        current_provider = config.get("llm_provider", "openai")
        provider_config = config["providers"].get(current_provider, {})
        
        if not provider_config.get("api_key"):
            print(f"❌ {current_provider.title()}: No API key configured")
            return
        
        print(f"🧪 Testing Current Provider: {current_provider.title()}")
        print("=" * 50)
        
        # Test the current provider
        await self.test_all_providers()

async def main():
    import sys
    
    tester = LLMTester()
    
    if len(sys.argv) > 1 and sys.argv[1] == "current":
        await tester.test_current_provider()
    else:
        await tester.test_all_providers()

if __name__ == "__main__":
    asyncio.run(main())