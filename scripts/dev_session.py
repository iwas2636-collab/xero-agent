#!/usr/bin/env python3
"""
PDD Development Session Manager
Starts and manages both Chainlit app and automatic prompt watcher
"""

import subprocess
import sys
import time
import signal
import os
from pathlib import Path
import threading
import psutil

class DevSessionManager:
    def __init__(self):
        self.chainlit_process = None
        self.watcher_process = None
        self.running = False
        
    def check_requirements(self):
        """Check if environment is properly set up"""
        print("🔍 Checking development environment...")
        
        # Check config file
        if not Path("config.json").exists():
            print("❌ Configuration not found!")
            print("Please run the configuration first")
            return False
            
        # Check .env file
        if not Path(".env").exists():
            print("❌ .env file not found!")
            print("Please run the configuration first")
            return False
            
        # Check API key
        try:
            with open(".env", "r") as f:
                env_content = f.read()
                if "API_KEY=" not in env_content or "API_KEY=\n" in env_content:
                    print("⚠️  API key not configured in .env file")
                    print("Please run the configuration to add your API key")
        except:
            pass
            
        # Check required packages
        try:
            import pyperclip
            import chainlit
        except ImportError as e:
            print(f"📦 Installing missing package: {e.name}")
            subprocess.run([sys.executable, "-m", "pip", "install", "pyperclip", "chainlit"])
            
        print("✅ Environment check complete")
        return True
        
    def start_prompt_watcher(self):
        """Start the automatic prompt watcher"""
        print("🤖 Starting automatic prompt watcher...")
        try:
            self.watcher_process = subprocess.Popen(
                [sys.executable, "scripts/prompt_watcher.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Give it a moment to start
            time.sleep(1)
            
            if self.watcher_process.poll() is None:
                print("✅ Prompt watcher started successfully")
                return True
            else:
                print("❌ Failed to start prompt watcher")
                return False
                
        except Exception as e:
            print(f"❌ Error starting prompt watcher: {e}")
            return False
            
    def start_chainlit(self):
        """Start the Chainlit application"""
        print("🌐 Starting Chainlit application...")
        try:
            self.chainlit_process = subprocess.Popen(
                [sys.executable, "-m", "chainlit", "run", "chainlit_app.py", "-w", "--port", "8001"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            print("✅ Chainlit starting on http://localhost:8001")
            return True
            
        except Exception as e:
            print(f"❌ Error starting Chainlit: {e}")
            return False
            
    def monitor_processes(self):
        """Monitor both processes and restart if needed"""
        while self.running:
            try:
                # Check watcher
                if self.watcher_process and self.watcher_process.poll() is not None:
                    print("⚠️  Prompt watcher stopped, restarting...")
                    self.start_prompt_watcher()
                    
                # Check chainlit
                if self.chainlit_process and self.chainlit_process.poll() is not None:
                    print("⚠️  Chainlit stopped")
                    self.running = False
                    break
                    
                time.sleep(5)
                
            except Exception as e:
                print(f"Monitor error: {e}")
                time.sleep(5)
                
    def stop_all(self):
        """Stop all processes"""
        print("\n🛑 Stopping development session...")
        self.running = False
        
        if self.watcher_process:
            try:
                self.watcher_process.terminate()
                self.watcher_process.wait(timeout=5)
                print("✅ Prompt watcher stopped")
            except:
                try:
                    self.watcher_process.kill()
                except:
                    pass
                    
        if self.chainlit_process:
            try:
                self.chainlit_process.terminate()
                self.chainlit_process.wait(timeout=5)
                print("✅ Chainlit stopped")
            except:
                try:
                    self.chainlit_process.kill()
                except:
                    pass
                    
    def show_status(self):
        """Show current session status"""
        # Load configuration to show current settings
        try:
            import json
            with open("config.json", "r") as f:
                config = json.load(f)
            provider = config["llm_provider"].title()
            model = config["providers"][config["llm_provider"]]["model"]
            oauth_clients = [name for name, client in config["oauth_clients"].items() if client.get("client_id")]
        except:
            provider = "Unknown"
            model = "Unknown"
            oauth_clients = []

        print("\n" + "="*60)
        print("🔥 PDD Universal Development Session Active")
        print("="*60)
        print(f"🤖 AI Provider:    {provider}")
        print(f"📱 Model:          {model}")
        print(f"🌐 Chainlit App:   http://localhost:8001")
        print(f"📝 PHR Location:   docs/prompts/")
        print(f"🔐 OAuth Clients:  {', '.join(oauth_clients).title() if oauth_clients else 'None configured'}")
        print("="*60)
        print("\n💡 Tips:")
        print("   • Copy AI prompts (Ctrl+C) for auto-recording")
        print("   • Check docs/prompts/ for your PHR files")
        print("   • Update PHRs with outcomes after development")
        print("   • Press Ctrl+C to stop session")
        print()
        
    def start(self):
        """Start the complete development session"""
        if not self.check_requirements():
            return False
            
        print("\n🚀 Starting PDD Development Session...")
        
        # Start services
        if not self.start_prompt_watcher():
            return False
            
        if not self.start_chainlit():
            self.stop_all()
            return False
            
        self.running = True
        
        # Show status
        self.show_status()
        
        # Start monitoring in background
        monitor_thread = threading.Thread(target=self.monitor_processes, daemon=True)
        monitor_thread.start()
        
        # Wait for Chainlit process or Ctrl+C
        try:
            self.chainlit_process.wait()
        except KeyboardInterrupt:
            pass
        finally:
            self.stop_all()
            
        print("✅ Development session ended")
        return True

def main():
    # Handle Ctrl+C gracefully
    def signal_handler(sig, frame):
        print("\n🛑 Received interrupt signal...")
        if hasattr(signal_handler, 'manager'):
            signal_handler.manager.stop_all()
        sys.exit(0)
        
    signal.signal(signal.SIGINT, signal_handler)
    
    manager = DevSessionManager()
    signal_handler.manager = manager  # Store reference for signal handler
    
    if len(sys.argv) > 1 and sys.argv[1] == 'status':
        # Show watcher status
        from scripts.prompt_watcher import PromptWatcher
        watcher = PromptWatcher()
        if watcher.session_data['auto_created']:
            print("📊 Auto-created PHRs this session:")
            for phr in watcher.session_data['auto_created'][-5:]:
                print(f"   PHR-{phr['id']}: {phr['feature']} ({phr['stage']})")
        else:
            print("📭 No auto-created PHRs yet")
        return
        
    # Start the session
    success = manager.start()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()