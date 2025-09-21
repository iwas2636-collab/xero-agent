# 🚀 Google Gemini Integration Guide

## Getting Your Gemini API Key

1. **Visit Google AI Studio**: https://makersuite.google.com/app/apikey
2. **Create API Key**: Click "Create API Key"
3. **Copy Key**: Format will be `AIzaSyXXX...`

## Gemini Models Available

| Model | Description | Best For |
|-------|-------------|----------|
| **gemini-2.0-flash-exp** | Latest experimental model | Cutting-edge capabilities, fast |
| **gemini-1.5-pro** | Most capable, multimodal | Complex reasoning, code generation |
| **gemini-1.5-flash** | Fast and efficient | Quick responses, chat |
| **gemini-1.0-pro** | Stable version | Production applications |

> **Note**: Gemini 2.5 and newer models will work automatically when available from Google.

## Configuration Example

When you run `start-universal.bat` and choose Gemini:

```
📱 Select your AI provider:
   1. OpenAI
   2. DeepSeek  
   3. Anthropic
   4. Gemini (current)
   5. Azure
   6. Local

🔑 Configure Gemini API settings:
API Key: AIzaSyXXX-your-actual-gemini-api-key
Model: gemini-2.0-flash-exp
Base URL: https://generativelanguage.googleapis.com/v1beta
```

## Generated Environment

Your `.env` file will contain:

```bash
# AI Provider Configuration
LLM_PROVIDER=gemini
API_KEY=AIzaSyXXX-your-actual-gemini-api-key
MODEL=gemini-2.0-flash-exp
BASE_URL=https://generativelanguage.googleapis.com/v1beta

# Session Configuration
PORT=8001
AUTO_PROMPT_RECORDING=true
DEBUG=false
```

## Gemini-Specific Features

### 📱 **Multimodal Support**
- Text and image inputs
- Code generation and analysis
- Document understanding

### ⚡ **High Performance**
- Fast response times with Flash model
- Large context windows
- Efficient token usage

### 🔒 **Safety Features**
- Built-in content filtering
- Responsible AI guidelines
- Enterprise-grade security

## Example Development Workflow

```bash
# 1. Start with Gemini
start-universal.bat
# Select: 4. Gemini
# Enter your AIzaSyXXX key

# 2. Copy development prompt
"Create a Xero invoice management system with error handling"

# 3. Auto-PHR created
# docs/prompts/0001-xero-invoice-management-system.prompt.md

# 4. Gemini helps implement
# Uses multimodal capabilities for code analysis
# Provides comprehensive solutions
```

## Gemini vs Other Providers

| Feature | Gemini | OpenAI | DeepSeek | Anthropic |
|---------|---------|---------|----------|-----------|
| **Multimodal** | ✅ | ✅ | ❌ | ✅ |
| **Code Gen** | ✅ | ✅ | ✅ | ✅ |
| **Context Size** | 2M tokens | 128K | 64K | 200K |
| **Cost** | Low | Medium | Low | Medium |
| **Speed** | Fast | Medium | Fast | Medium |

## Troubleshooting

### Common Issues

**❌ ImportError: google-generativeai**
```bash
pip install google-generativeai>=0.3.0
```

**❌ Invalid API Key**
- Check format: `AIzaSyXXX...`
- Verify key is active in Google AI Studio
- Ensure billing is enabled if required

**❌ Model Not Found**
- Use: `gemini-1.5-pro`, `gemini-1.5-flash`, or `gemini-1.0-pro`
- Check model availability in your region

### Best Practices

1. **Use Flash for Chat**: Fast responses for interactive development
2. **Use Pro for Complex Tasks**: Better reasoning for architecture decisions
3. **Leverage Multimodal**: Include screenshots or diagrams in prompts
4. **Monitor Usage**: Track API calls in Google Cloud Console

## Ready to Use Gemini

After configuration, your PDD development session will use Gemini for:
- ✅ **Architectural guidance** with comprehensive analysis
- ✅ **Code generation** with modern best practices  
- ✅ **Debugging assistance** with detailed explanations
- ✅ **Integration help** for Xero and other APIs
- ✅ **Automatic PHR documentation** of all interactions

**Start developing with Google's most advanced AI!** 🤖✨