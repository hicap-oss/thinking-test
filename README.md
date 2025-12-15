# Extended Thinking Test Suite

A comprehensive, interactive Python test suite for verifying Claude's Extended Thinking functionality via the HiCap AI API.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## What is Extended Thinking?

Extended Thinking is an Anthropic feature that allows Claude to show its reasoning process before generating a response. This includes chain-of-thought reasoning that helps the model produce more accurate and thoughtful responses.

**How it works:**
1. A request is sent with `thinking` enabled and a token budget
2. Claude first outputs its thinking process (internal reasoning)
3. Then Claude outputs its final response based on that reasoning

## Features

| Feature | Description |
|---------|-------------|
| **Streaming Test** | Real-time streaming of thinking and response with colored output |
| **Custom Prompt Test** | Test with your own prompts and custom thinking budgets |
| **Budget Scaling Test** | Compare thinking depth across different token budgets |
| **Signature Verification** | Validate cryptographic signatures in thinking blocks |
| **Multi-turn Chat** | Interactive chat with message linking and thinking preservation |
| **Persistent Config** | Settings saved between sessions |
| **Fun Loading Animation** | Silly messages while waiting for AI responses |

## Installation

### Prerequisites
- Python 3.8 or higher
- An API key from [HiCap AI](https://hicap.ai)

### Setup

1. **Clone or download this repository**

2. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

3. **Configure your API key:**
   
   Edit `test_extended_thinking.py` and replace:
   ```python
   DEFAULT_API_KEY = "YOUR_API_KEY"
   ```
   
   Or configure it via the Settings menu (option 7) when running the script.

## Usage

### Interactive Mode (Recommended)

```powershell
python test_extended_thinking.py
```

This launches the interactive menu:

```
╔══════════════════════════════════════════════════════════════╗
║           EXTENDED THINKING TEST SUITE                       ║
╚══════════════════════════════════════════════════════════════╝

  [1] Run Default Test
  [2] Run with Custom Prompt
  [3] Run with Custom Prompt + Budget
  [4] Budget Scaling Test
  [5] Signature Verification Test
  [6] Multi-turn Chat (with message linking)
  [7] Settings
  [8] Help
  [0] Exit
```

### Command Line Options

```powershell
# Show help
python test_extended_thinking.py --help

# Run test automatically (non-interactive)
python test_extended_thinking.py --auto

# Minimal output mode
python test_extended_thinking.py --quiet
```

## Test Modes

### 1. Default Test
Runs a standard test with the default prompt ("Tell me a short story") and thinking budget (2500 tokens).

### 2. Custom Prompt Test
Enter your own prompt while using the default thinking budget.

### 3. Custom Prompt + Budget
Full control over both the prompt and thinking token budget.

### 4. Budget Scaling Test
Compare how thinking depth changes with different budgets. Enter comma-separated values:
```
Enter budgets (comma-separated): 1000, 2500, 5000, 10000
```

### 5. Signature Verification Test
Validates that thinking blocks contain proper cryptographic signatures:
- Presence check
- Non-empty validation
- Base64 format verification
- Length validation (100+ characters)

### 6. Multi-turn Chat
Interactive conversation mode with full thinking support:

**Chat Commands:**
| Command | Description |
|---------|-------------|
| `/quit` | Exit chat and save history |
| `/clear` | Clear conversation history |
| `/history` | Browse and resume saved chats |
| `/thinking` | Toggle thinking display on/off |
| `/save` | Manually save current conversation |
| `/status` | Show conversation status |
| `/budget <n>` | Change thinking budget mid-session |
| `/` | Show all available commands |

**Features:**
- Real-time streaming of thoughts and responses
- Message verification after each turn
- Auto-save to `chats/` folder
- Resume previous conversations with full thinking history

### 7. Settings
Configure persistent settings:
- API Endpoint
- API Key
- Model name
- Default thinking budget
- Max tokens (response length)
- System prompt

Settings are saved to `config/settings.json`.

## Project Structure

```
thinking-test/
├── test_extended_thinking.py   # Main test script
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── config/                     # Persistent configuration
│   └── settings.json
├── results/                    # Test result files
│   └── *.json
└── chats/                      # Saved chat histories
    └── *.json
```

## API Request Format

The script sends requests in this format:

```json
{
  "stream": true,
  "model": "claude-sonnet-4.5",
  "max_tokens": 16000,
  "thinking": {
    "type": "enabled",
    "budget_tokens": 2500
  },
  "messages": [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Your prompt here"}
  ]
}
```

## Response Structure

Extended thinking responses include special content blocks:

```json
{
  "content": [
    {
      "type": "thinking",
      "thinking": "The user wants... Let me consider...",
      "signature": "base64-encoded-signature..."
    },
    {
      "type": "text",
      "text": "Here is my response..."
    }
  ]
}
```

## Multi-turn Message Linking

For multi-turn conversations, previous thinking blocks must be preserved with their signatures. The script handles this automatically:

```json
{
  "messages": [
    {"role": "user", "content": "Hello"},
    {"role": "assistant", "content": [
      {"type": "thinking", "thinking": "...", "signature": "..."},
      {"type": "text", "text": "Hi there!"}
    ]},
    {"role": "user", "content": "How are you?"}
  ]
}
```

## Troubleshooting

### "Invalid signature in thinking block"
This occurs when resuming a chat saved in the old format. The script now handles this by stripping thinking from legacy saves.

### Response truncation
Increase `max_tokens` in Settings (option 7). Default is 16,000.

### Connection errors
Check your API key and endpoint configuration in Settings.

### Unicode errors on Windows
The script uses UTF-8 encoding. If you see encoding errors, ensure your terminal supports UTF-8.

## Dependencies

- `requests` - HTTP client for API calls
- `colorama` - Cross-platform colored terminal output

## License

MIT License - Feel free to modify and distribute.

## Author

Created for testing Extended Thinking functionality with Claude models via HiCap AI.

