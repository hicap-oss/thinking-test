# test_extended_thinking.py
# Python 3.8+
# Dependencies: requests, colorama (pip install requests colorama)
#
# Interactive test for extended thinking functionality with Claude Sonnet 4.5
# via the HiCap AI API endpoint.

import requests
import json
import sys
import os
from datetime import datetime
from typing import Optional, Dict, Any, List

# =============================================================================
# Color Support (cross-platform)
# =============================================================================
try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
    COLORS_AVAILABLE = True
except ImportError:
    # Fallback if colorama not installed
    COLORS_AVAILABLE = False
    class Fore:
        RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = WHITE = RESET = ""
        LIGHTBLACK_EX = LIGHTGREEN_EX = LIGHTBLUE_EX = LIGHTYELLOW_EX = ""
        LIGHTMAGENTA_EX = LIGHTCYAN_EX = LIGHTWHITE_EX = ""
    class Back:
        RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = WHITE = RESET = ""
        LIGHTBLACK_EX = ""
    class Style:
        BRIGHT = DIM = NORMAL = RESET_ALL = ""

# =============================================================================
# Configuration Defaults
# =============================================================================
DEFAULT_API_ENDPOINT = "https://api.hicap.ai/v2/openai/chat/completions"
DEFAULT_API_KEY = "key_goes_here"
DEFAULT_MODEL = "claude-sonnet-4.5"
DEFAULT_THINKING_BUDGET_TOKENS = 2500
DEFAULT_MAX_TOKENS = 16000  # Max tokens for response (prevents truncation)
DEFAULT_SYSTEM_PROMPT = "You are a helpful assistant."
DEFAULT_USER_PROMPT = "tell me a short story"

# Config file path
CONFIG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config")
CONFIG_FILE = os.path.join(CONFIG_DIR, "settings.json")


def ensure_config_folder():
    """Ensure the config folder exists."""
    if not os.path.exists(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)
    return CONFIG_DIR


def load_config() -> Dict[str, Any]:
    """Load configuration from file, or return defaults if not found."""
    ensure_config_folder()
    
    default_config = {
        "endpoint": DEFAULT_API_ENDPOINT,
        "api_key": os.environ.get("HICAP_API_KEY", DEFAULT_API_KEY),
        "model": DEFAULT_MODEL,
        "thinking_budget": DEFAULT_THINKING_BUDGET_TOKENS,
        "max_tokens": DEFAULT_MAX_TOKENS,
        "system_prompt": DEFAULT_SYSTEM_PROMPT,
        "user_prompt": DEFAULT_USER_PROMPT
    }
    
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                saved_config = json.load(f)
                # Merge with defaults (in case new fields are added)
                for key in default_config:
                    if key not in saved_config:
                        saved_config[key] = default_config[key]
                return saved_config
        except Exception as e:
            print(f"{Fore.YELLOW}Warning: Could not load config: {e}{Style.RESET_ALL}")
            return default_config
    
    return default_config


def save_config(config: Dict[str, Any]):
    """Save configuration to file."""
    ensure_config_folder()
    try:
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"{Fore.RED}Could not save config: {e}{Style.RESET_ALL}")
        return False


def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


# =============================================================================
# Fun Loading Animation
# =============================================================================
import threading
import time
import random

SILLY_MESSAGES = [
    "Warming up the neural pathways...",
    "Consulting the silicon oracle...",
    "Brewing artificial intelligence...",
    "Tickling the transformer layers...",
    "Aligning the attention heads...",
    "Polishing the embeddings...",
    "Feeding the model some tokens...",
    "Charging the thinking capacitors...",
    "Waking up the AI hamsters...",
    "Calculating the meaning of life...",
    "Reorganizing the weight matrices...",
    "Spinning up the thought generators...",
    "Convincing electrons to cooperate...",
    "Loading imagination modules...",
    "Defragmenting the brain cells...",
    "Summoning the Claude consciousness...",
    "Untangling the neural spaghetti...",
    "Poking the language model...",
    "Bribing the GPU with electricity...",
    "Asking nicely for a response...",
]

SPINNER_FRAMES = [
    "⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"
]

BRAIN_FRAMES = [
    r"  (o_o)  ",
    r"  (o_O)  ",
    r"  (O_o)  ",
    r"  (O_O)  ",
    r"  (@_@)  ",
    r"  (^_^)  ",
]

class LoadingAnimation:
    """Animated loading indicator with silly messages."""
    
    def __init__(self):
        self.running = False
        self.thread = None
        self.message = random.choice(SILLY_MESSAGES)
    
    def _animate(self):
        """Animation loop running in background thread."""
        frame_idx = 0
        brain_idx = 0
        dots = 0
        
        while self.running:
            spinner = SPINNER_FRAMES[frame_idx % len(SPINNER_FRAMES)]
            brain = BRAIN_FRAMES[brain_idx % len(BRAIN_FRAMES)]
            dot_str = "." * (dots % 4)
            
            # Build the animation line
            line = f"\r{Fore.CYAN}{spinner}{Style.RESET_ALL} {Fore.YELLOW}{self.message}{dot_str.ljust(4)}{Style.RESET_ALL}"
            
            print(line, end="", flush=True)
            
            frame_idx += 1
            dots += 1
            if frame_idx % 5 == 0:
                brain_idx += 1
            
            time.sleep(0.1)
        
        # Clear the line when done
        print("\r" + " " * 80 + "\r", end="", flush=True)
    
    def start(self, message: str = None):
        """Start the loading animation."""
        if self.running:
            return
        
        self.message = message or random.choice(SILLY_MESSAGES)
        self.running = True
        self.thread = threading.Thread(target=self._animate, daemon=True)
        self.thread.start()
    
    def stop(self):
        """Stop the loading animation."""
        self.running = False
        if self.thread:
            self.thread.join(timeout=0.5)
            self.thread = None


# Global loading animation instance
loading = LoadingAnimation()


def print_header():
    """Print the application header with default values."""
    print_header_with_config(None)


def print_header_with_config(config: Optional[Dict[str, Any]]):
    """Print the application header with config values."""
    model = config.get('model', DEFAULT_MODEL) if config else DEFAULT_MODEL
    endpoint = config.get('endpoint', DEFAULT_API_ENDPOINT) if config else DEFAULT_API_ENDPOINT
    
    print(f"\n{Fore.CYAN}{Style.BRIGHT}{'=' * 70}")
    print(f"{Fore.CYAN}{Style.BRIGHT}    Extended Thinking Test - Claude Sonnet 4.5")
    print(f"{Fore.CYAN}{Style.BRIGHT}{'=' * 70}{Style.RESET_ALL}")
    print(f"{Fore.WHITE}    Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{Fore.WHITE}    Model: {Fore.YELLOW}{model}")
    print(f"{Fore.WHITE}    Endpoint: {Fore.LIGHTBLACK_EX}{endpoint}")
    print(f"{Fore.CYAN}{'=' * 70}{Style.RESET_ALL}\n")


def print_menu():
    """Print the interactive menu."""
    print(f"{Fore.GREEN}{Style.BRIGHT}OPTIONS:{Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}[1]{Fore.WHITE} Run test with default prompt (stream thinking + response)")
    print(f"  {Fore.YELLOW}[2]{Fore.WHITE} Run test with custom prompt")
    print(f"  {Fore.YELLOW}[3]{Fore.WHITE} Run test (response only, hide thinking)")
    print(f"  {Fore.YELLOW}[4]{Fore.WHITE} Budget scaling test (compare different budget sizes)")
    print(f"  {Fore.YELLOW}[5]{Fore.WHITE} Signature verification test")
    print(f"  {Fore.YELLOW}[6]{Fore.WHITE} Multi-turn chat (test message linking with thinking)")
    print(f"  {Fore.YELLOW}[7]{Fore.WHITE} Configure settings")
    print(f"  {Fore.YELLOW}[8]{Fore.WHITE} View current configuration")
    print(f"  {Fore.YELLOW}[9]{Fore.WHITE} Help")
    print(f"  {Fore.YELLOW}[0]{Fore.WHITE} Exit")
    print()


def print_config(config: Dict[str, Any]):
    """Print current configuration."""
    print(f"\n{Fore.CYAN}{Style.BRIGHT}Current Configuration:{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'-' * 50}{Style.RESET_ALL}")
    print(f"  {Fore.WHITE}Config File: {Fore.LIGHTBLACK_EX}{CONFIG_FILE}")
    print(f"  {Fore.WHITE}API Endpoint: {Fore.YELLOW}{config['endpoint']}")
    print(f"  {Fore.WHITE}API Key: {Fore.YELLOW}{config['api_key'][:8]}...{config['api_key'][-4:]}")
    print(f"  {Fore.WHITE}Model: {Fore.YELLOW}{config['model']}")
    print(f"  {Fore.WHITE}Thinking Budget: {Fore.YELLOW}{config['thinking_budget']} tokens")
    print(f"  {Fore.WHITE}Max Tokens: {Fore.YELLOW}{config.get('max_tokens', DEFAULT_MAX_TOKENS)}")
    print(f"  {Fore.WHITE}System Prompt: {Fore.LIGHTBLACK_EX}{config['system_prompt'][:50]}...")
    print(f"  {Fore.WHITE}User Prompt: {Fore.LIGHTBLACK_EX}{config['user_prompt'][:50]}...")
    print(f"{Fore.CYAN}{'-' * 50}{Style.RESET_ALL}\n")


def print_help():
    """Print help information."""
    print(f"\n{Fore.CYAN}{Style.BRIGHT}Help - Extended Thinking Test{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'-' * 50}{Style.RESET_ALL}")
    print(f"""
{Fore.WHITE}This tool tests extended thinking functionality for Claude Sonnet 4.5.

{Fore.GREEN}What is Extended Thinking?{Style.RESET_ALL}
Extended thinking allows Claude to show its reasoning process before
generating a response. This includes chain-of-thought reasoning that
helps the model produce more accurate and thoughtful responses.

{Fore.GREEN}How it works:{Style.RESET_ALL}
1. A request is sent with thinking enabled and a token budget
2. Claude first outputs its thinking process (shown in {Fore.MAGENTA}magenta{Fore.WHITE})
3. Then Claude outputs its final response (shown in {Fore.GREEN}green{Fore.WHITE})

{Fore.GREEN}Test Success Criteria:{Style.RESET_ALL}
- Response contains thinking content blocks
- Thinking content is non-empty
- Text response is generated after thinking

{Fore.GREEN}Command Line Options:{Style.RESET_ALL}
  --help, -h, /?    Show this help
  --auto            Run test automatically without menu
  --quiet           Minimal output (pass/fail only)
""")
    print(f"{Fore.CYAN}{'-' * 50}{Style.RESET_ALL}\n")


def parse_sse_line(line: str) -> Optional[Dict[str, Any]]:
    """Parse a Server-Sent Events (SSE) line."""
    line = line.strip()
    
    if not line:
        return None
        
    if line.startswith("data: "):
        data_str = line[6:]
        
        if data_str == "[DONE]":
            return {"done": True}
            
        try:
            return json.loads(data_str)
        except json.JSONDecodeError:
            return None
            
    return None


def stream_test(
    config: Dict[str, Any],
    show_thinking: bool = True,
    custom_prompt: Optional[str] = None,
    custom_budget: Optional[int] = None
) -> Dict[str, Any]:
    """
    Run the extended thinking test with streaming output.
    
    Returns a dict with test results.
    """
    result = {
        "passed": False,
        "thinking_detected": False,
        "thinking_content": "",
        "text_content": "",
        "error": None,
        "events_count": 0,
        "thinking_budget": custom_budget or config['thinking_budget'],
        "signature": None,
        "signature_present": False
    }
    
    user_prompt = custom_prompt if custom_prompt else config['user_prompt']
    thinking_budget = custom_budget if custom_budget else config['thinking_budget']
    
    # Prepare request
    headers = {
        "Content-Type": "application/json",
        "api-key": config['api_key'],
        "Accept": "text/event-stream",
    }
    
    payload = {
        "stream": True,
        "model": config['model'],
        "thinking": {
            "type": "enabled",
            "budget_tokens": thinking_budget
        },
        "messages": [
            {"role": "system", "content": config['system_prompt']},
            {"role": "user", "content": user_prompt}
        ]
    }
    
    # Print request info
    print(f"\n{Fore.CYAN}{Style.BRIGHT}Sending Request...{Style.RESET_ALL}")
    print(f"{Fore.WHITE}Prompt: {Fore.YELLOW}\"{user_prompt}\"{Style.RESET_ALL}")
    print(f"{Fore.WHITE}Thinking Budget: {Fore.YELLOW}{thinking_budget} tokens{Style.RESET_ALL}")
    print()
    
    # Start loading animation
    loading.start()
    
    try:
        response = requests.post(
            config['endpoint'],
            headers=headers,
            json=payload,
            stream=True,
            timeout=120
        )
        
        # Stop loading when we get a response
        loading.stop()
        
        if response.status_code != 200:
            result["error"] = f"API returned status {response.status_code}"
            print(f"{Fore.RED}[ERROR] {result['error']}{Style.RESET_ALL}")
            try:
                error_body = response.text[:500]
                print(f"{Fore.RED}{error_body}{Style.RESET_ALL}")
            except:
                pass
            return result
        
        # Streaming output
        thinking_started = False
        text_started = False
        current_thinking = ""
        current_text = ""
        
        if show_thinking:
            print(f"{Fore.MAGENTA}{Style.BRIGHT}[THINKING]{Style.RESET_ALL} ", end="", flush=True)
        
        for line in response.iter_lines(decode_unicode=True):
            if not line:
                continue
                
            parsed = parse_sse_line(line)
            if not parsed:
                continue
                
            if parsed.get("done"):
                break
                
            result["events_count"] += 1
            
            # Check rawEvents for streaming deltas
            raw_events = parsed.get("rawEvents", {})
            event = raw_events.get("event", {})
            event_type = event.get("type", "")
            
            if event_type == "content_block_start":
                content_block = event.get("content_block", {})
                if content_block.get("type") == "thinking":
                    result["thinking_detected"] = True
                    thinking_started = True
                    # Capture signature if present
                    sig = content_block.get("signature", "")
                    if sig:
                        result["signature"] = sig
                        result["signature_present"] = True
                    
            elif event_type == "content_block_delta":
                delta = event.get("delta", {})
                delta_type = delta.get("type", "")
                
                if delta_type == "thinking_delta":
                    thinking_text = delta.get("thinking", "")
                    if thinking_text:
                        current_thinking += thinking_text
                        result["thinking_content"] = current_thinking
                        if show_thinking:
                            # Stream thinking in magenta
                            print(f"{Fore.MAGENTA}{thinking_text}{Style.RESET_ALL}", end="", flush=True)
                            
                elif delta_type == "text_delta":
                    text = delta.get("text", "")
                    if text:
                        if not text_started and show_thinking:
                            # Transition from thinking to text
                            print(f"\n\n{Fore.GREEN}{Style.BRIGHT}[RESPONSE]{Style.RESET_ALL} ", end="", flush=True)
                            text_started = True
                        elif not text_started and not show_thinking:
                            print(f"{Fore.GREEN}{Style.BRIGHT}[RESPONSE]{Style.RESET_ALL} ", end="", flush=True)
                            text_started = True
                        current_text += text
                        result["text_content"] = current_text
                        # Stream text in green
                        print(f"{Fore.GREEN}{text}{Style.RESET_ALL}", end="", flush=True)
            
            # Check for signature_delta (signature comes at end of thinking block)
            elif event_type == "content_block_delta":
                delta = event.get("delta", {})
                if delta.get("type") == "signature_delta":
                    sig = delta.get("signature", "")
                    if sig:
                        result["signature"] = (result.get("signature") or "") + sig
                        result["signature_present"] = True
            
            # Also check content array in snapshot
            content = parsed.get("content", [])
            for block in content:
                if block.get("type") == "thinking":
                    result["thinking_detected"] = True
                    # Capture signature from snapshot
                    sig = block.get("signature", "")
                    if sig and len(sig) > len(result.get("signature") or ""):
                        result["signature"] = sig
                        result["signature_present"] = True
        
        print("\n")  # End streaming output
        
        # Determine pass/fail
        result["passed"] = result["thinking_detected"] and len(result["thinking_content"]) > 0
        
    except requests.exceptions.Timeout:
        loading.stop()
        result["error"] = "Request timed out"
        print(f"\n{Fore.RED}[ERROR] {result['error']}{Style.RESET_ALL}")
        
    except requests.exceptions.ConnectionError as e:
        loading.stop()
        result["error"] = f"Connection error: {str(e)}"
        print(f"\n{Fore.RED}[ERROR] {result['error']}{Style.RESET_ALL}")
        
    except Exception as e:
        loading.stop()
        result["error"] = f"Unexpected error: {str(e)}"
        print(f"\n{Fore.RED}[ERROR] {result['error']}{Style.RESET_ALL}")
    
    return result


def print_result(result: Dict[str, Any]):
    """Print the test result summary."""
    print(f"\n{Fore.CYAN}{'=' * 70}{Style.RESET_ALL}")
    
    if result["passed"]:
        print(f"{Fore.GREEN}{Style.BRIGHT}    TEST RESULT: PASSED{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}{Style.BRIGHT}    TEST RESULT: FAILED{Style.RESET_ALL}")
    
    print(f"{Fore.CYAN}{'=' * 70}{Style.RESET_ALL}")
    print(f"  {Fore.WHITE}Thinking Budget: {Fore.YELLOW}{result.get('thinking_budget', 'N/A')} tokens")
    print(f"  {Fore.WHITE}Thinking Detected: {Fore.YELLOW}{'Yes' if result['thinking_detected'] else 'No'}")
    print(f"  {Fore.WHITE}Thinking Length: {Fore.YELLOW}{len(result['thinking_content'])} characters")
    print(f"  {Fore.WHITE}Response Length: {Fore.YELLOW}{len(result['text_content'])} characters")
    print(f"  {Fore.WHITE}Signature Present: {Fore.YELLOW}{'Yes' if result.get('signature_present') else 'No'}")
    sig = result.get('signature')
    if sig:
        print(f"  {Fore.WHITE}Signature Length: {Fore.YELLOW}{len(sig)} characters")
    print(f"  {Fore.WHITE}Events Processed: {Fore.YELLOW}{result['events_count']}")
    
    if result["error"]:
        print(f"  {Fore.RED}Error: {result['error']}")
    
    print(f"{Fore.CYAN}{'=' * 70}{Style.RESET_ALL}\n")


def configure_settings(config: Dict[str, Any]) -> Dict[str, Any]:
    """Interactive configuration menu with auto-save."""
    changed = False
    
    while True:
        print(f"\n{Fore.CYAN}{Style.BRIGHT}Configuration Menu:{Style.RESET_ALL}")
        print(f"{Fore.LIGHTBLACK_EX}  (Settings auto-save to config/settings.json){Style.RESET_ALL}")
        print(f"  {Fore.YELLOW}[1]{Fore.WHITE} Change API Endpoint")
        print(f"  {Fore.YELLOW}[2]{Fore.WHITE} Change API Key")
        print(f"  {Fore.YELLOW}[3]{Fore.WHITE} Change Model")
        print(f"  {Fore.YELLOW}[4]{Fore.WHITE} Change Thinking Budget")
        print(f"  {Fore.YELLOW}[5]{Fore.WHITE} Change Max Tokens (response length)")
        print(f"  {Fore.YELLOW}[6]{Fore.WHITE} Change System Prompt")
        print(f"  {Fore.YELLOW}[7]{Fore.WHITE} Change Default User Prompt")
        print(f"  {Fore.YELLOW}[8]{Fore.WHITE} Reset to defaults")
        print(f"  {Fore.YELLOW}[0]{Fore.WHITE} Back to main menu")
        print()
        
        choice = input(f"{Fore.GREEN}Enter choice: {Style.RESET_ALL}").strip()
        
        if choice == "0":
            if changed:
                if save_config(config):
                    print(f"{Fore.GREEN}Configuration saved.{Style.RESET_ALL}")
            break
        elif choice == "1":
            new_val = input(f"{Fore.WHITE}New endpoint [{config['endpoint']}]: {Style.RESET_ALL}").strip()
            if new_val:
                config['endpoint'] = new_val
                changed = True
                save_config(config)
                print(f"{Fore.GREEN}Endpoint updated and saved.{Style.RESET_ALL}")
        elif choice == "2":
            new_val = input(f"{Fore.WHITE}New API key: {Style.RESET_ALL}").strip()
            if new_val:
                config['api_key'] = new_val
                changed = True
                save_config(config)
                print(f"{Fore.GREEN}API key updated and saved.{Style.RESET_ALL}")
        elif choice == "3":
            new_val = input(f"{Fore.WHITE}New model [{config['model']}]: {Style.RESET_ALL}").strip()
            if new_val:
                config['model'] = new_val
                changed = True
                save_config(config)
                print(f"{Fore.GREEN}Model updated and saved.{Style.RESET_ALL}")
        elif choice == "4":
            new_val = input(f"{Fore.WHITE}New thinking budget [{config['thinking_budget']}]: {Style.RESET_ALL}").strip()
            if new_val:
                try:
                    config['thinking_budget'] = int(new_val)
                    changed = True
                    save_config(config)
                    print(f"{Fore.GREEN}Thinking budget updated and saved.{Style.RESET_ALL}")
                except ValueError:
                    print(f"{Fore.RED}Invalid number.{Style.RESET_ALL}")
        elif choice == "5":
            current_max = config.get('max_tokens', DEFAULT_MAX_TOKENS)
            new_val = input(f"{Fore.WHITE}New max tokens [{current_max}]: {Style.RESET_ALL}").strip()
            if new_val:
                try:
                    config['max_tokens'] = int(new_val)
                    changed = True
                    save_config(config)
                    print(f"{Fore.GREEN}Max tokens updated and saved.{Style.RESET_ALL}")
                except ValueError:
                    print(f"{Fore.RED}Invalid number.{Style.RESET_ALL}")
        elif choice == "6":
            new_val = input(f"{Fore.WHITE}New system prompt: {Style.RESET_ALL}").strip()
            if new_val:
                config['system_prompt'] = new_val
                changed = True
                save_config(config)
                print(f"{Fore.GREEN}System prompt updated and saved.{Style.RESET_ALL}")
        elif choice == "7":
            new_val = input(f"{Fore.WHITE}New default user prompt: {Style.RESET_ALL}").strip()
            if new_val:
                config['user_prompt'] = new_val
                changed = True
                save_config(config)
                print(f"{Fore.GREEN}User prompt updated and saved.{Style.RESET_ALL}")
        elif choice == "8":
            confirm = input(f"{Fore.YELLOW}Reset all settings to defaults? (y/n): {Style.RESET_ALL}").strip().lower()
            if confirm == 'y':
                config = {
                    "endpoint": DEFAULT_API_ENDPOINT,
                    "api_key": DEFAULT_API_KEY,
                    "model": DEFAULT_MODEL,
                    "thinking_budget": DEFAULT_THINKING_BUDGET_TOKENS,
                    "max_tokens": DEFAULT_MAX_TOKENS,
                    "system_prompt": DEFAULT_SYSTEM_PROMPT,
                    "user_prompt": DEFAULT_USER_PROMPT
                }
                save_config(config)
                print(f"{Fore.GREEN}Settings reset to defaults and saved.{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Invalid choice.{Style.RESET_ALL}")
    
    return config


def ensure_results_folder():
    """Ensure the results folder exists."""
    results_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    return results_dir


def save_results(result: Dict[str, Any], filename: str = "thinking_test_results.json"):
    """Save test results to JSON file in results folder."""
    results_dir = ensure_results_folder()
    try:
        output = {
            "timestamp": datetime.now().isoformat(),
            "passed": result["passed"],
            "thinking_detected": result["thinking_detected"],
            "thinking_content": result["thinking_content"],
            "text_content": result["text_content"],
            "error": result["error"],
            "events_count": result["events_count"],
            "thinking_budget": result.get("thinking_budget"),
            "thinking_length": len(result["thinking_content"]),
            "signature_present": result.get("signature_present", False),
            "signature_length": len(result.get("signature") or "")
        }
        filepath = os.path.join(results_dir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        print(f"{Fore.LIGHTBLACK_EX}Results saved to: {filepath}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Could not save results: {e}{Style.RESET_ALL}")


def ask_for_budget(default: int) -> int:
    """Ask user for thinking budget tokens."""
    print(f"\n{Fore.CYAN}Thinking Budget Configuration{Style.RESET_ALL}")
    print(f"{Fore.WHITE}Enter the thinking budget in tokens (min: 1024)")
    print(f"{Fore.LIGHTBLACK_EX}Suggested values: 1024 (minimal), 2500 (default), 5000 (medium), 10000 (large){Style.RESET_ALL}")
    
    user_input = input(f"{Fore.YELLOW}Budget [{default}]: {Style.RESET_ALL}").strip()
    
    if not user_input:
        return default
    
    try:
        budget = int(user_input)
        if budget < 1024:
            print(f"{Fore.YELLOW}Warning: Budget below 1024 may not work. Using 1024.{Style.RESET_ALL}")
            return 1024
        return budget
    except ValueError:
        print(f"{Fore.YELLOW}Invalid input. Using default: {default}{Style.RESET_ALL}")
        return default


def run_budget_scaling_test(config: Dict[str, Any]):
    """Run tests with multiple budget sizes to compare thinking output."""
    print(f"\n{Fore.CYAN}{Style.BRIGHT}Budget Scaling Test{Style.RESET_ALL}")
    print(f"{Fore.WHITE}This test runs the same prompt with different thinking budgets")
    print(f"{Fore.WHITE}to compare how budget affects thinking output length.{Style.RESET_ALL}\n")
    
    # Ask for budgets to test
    print(f"{Fore.CYAN}Enter budget values to test (comma-separated)")
    print(f"{Fore.LIGHTBLACK_EX}Example: 1024,2500,5000,10000{Style.RESET_ALL}")
    budget_input = input(f"{Fore.YELLOW}Budgets [1024,2500,5000]: {Style.RESET_ALL}").strip()
    
    if not budget_input:
        budgets = [1024, 2500, 5000]
    else:
        try:
            budgets = [int(b.strip()) for b in budget_input.split(",")]
        except ValueError:
            print(f"{Fore.RED}Invalid input. Using defaults.{Style.RESET_ALL}")
            budgets = [1024, 2500, 5000]
    
    # Ask for prompt
    print(f"\n{Fore.WHITE}Enter test prompt (or press Enter for default):{Style.RESET_ALL}")
    prompt = input(f"{Fore.YELLOW}> {Style.RESET_ALL}").strip()
    if not prompt:
        prompt = config['user_prompt']
    
    results = []
    
    print(f"\n{Fore.CYAN}{'=' * 70}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Running {len(budgets)} tests with prompt: \"{prompt[:40]}...\"{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'=' * 70}{Style.RESET_ALL}\n")
    
    for i, budget in enumerate(budgets):
        print(f"\n{Fore.YELLOW}{Style.BRIGHT}Test {i+1}/{len(budgets)}: Budget = {budget} tokens{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'-' * 50}{Style.RESET_ALL}")
        
        # Run test with this budget
        result = stream_test(
            config, 
            show_thinking=True, 
            custom_prompt=prompt,
            custom_budget=budget
        )
        result["thinking_budget"] = budget
        results.append(result)
        
        print(f"\n{Fore.CYAN}{'-' * 50}{Style.RESET_ALL}")
    
    # Summary comparison
    print(f"\n{Fore.CYAN}{Style.BRIGHT}{'=' * 70}")
    print(f"    BUDGET SCALING COMPARISON")
    print(f"{'=' * 70}{Style.RESET_ALL}")
    print(f"\n{Fore.WHITE}{'Budget':>10} | {'Thinking Len':>14} | {'Response Len':>14} | {'Status':>10}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'-' * 60}{Style.RESET_ALL}")
    
    for r in results:
        status = f"{Fore.GREEN}PASS{Style.RESET_ALL}" if r["passed"] else f"{Fore.RED}FAIL{Style.RESET_ALL}"
        print(f"{r['thinking_budget']:>10} | {len(r['thinking_content']):>14} | {len(r['text_content']):>14} | {status:>10}")
    
    print(f"{Fore.CYAN}{'-' * 60}{Style.RESET_ALL}")
    
    # Calculate scaling ratio
    if len(results) >= 2 and results[0]["passed"] and results[-1]["passed"]:
        ratio = len(results[-1]["thinking_content"]) / max(len(results[0]["thinking_content"]), 1)
        budget_ratio = results[-1]["thinking_budget"] / results[0]["thinking_budget"]
        print(f"\n{Fore.WHITE}Budget increase: {budget_ratio:.1f}x")
        print(f"{Fore.WHITE}Thinking length increase: {ratio:.1f}x{Style.RESET_ALL}")
    
    print(f"\n{Fore.CYAN}{'=' * 70}{Style.RESET_ALL}\n")
    
    # Save all results to results folder
    results_dir = ensure_results_folder()
    try:
        filepath = os.path.join(results_dir, f"budget_scaling_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "budgets_tested": budgets,
                "results": [{
                    "budget": r["thinking_budget"],
                    "thinking_length": len(r["thinking_content"]),
                    "response_length": len(r["text_content"]),
                    "passed": r["passed"],
                    "thinking_content": r["thinking_content"][:500],
                    "text_content": r["text_content"][:500]
                } for r in results]
            }, f, indent=2)
        print(f"{Fore.LIGHTBLACK_EX}Results saved to: {filepath}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Could not save results: {e}{Style.RESET_ALL}")


def run_signature_verification_test(config: Dict[str, Any]):
    """
    Run signature verification test for extended thinking.
    
    Tests that:
    1. Signature field is present in thinking blocks
    2. Signature is non-empty
    3. Signature format looks valid (base64-like)
    """
    print(f"\n{Fore.CYAN}{Style.BRIGHT}{'=' * 70}")
    print(f"    Signature Verification Test")
    print(f"{'=' * 70}{Style.RESET_ALL}")
    
    print(f"""
{Fore.WHITE}This test verifies that extended thinking responses include a valid
cryptographic signature. The signature is used to verify that thinking
blocks came from Claude and haven't been tampered with.{Style.RESET_ALL}

{Fore.CYAN}What we check:{Style.RESET_ALL}
  1. Signature field is present in thinking blocks
  2. Signature is non-empty  
  3. Signature format appears valid (base64-encoded)
  4. Signature length is reasonable (typically 100+ chars)
""")
    
    # Ask for budget
    budget = ask_for_budget(config['thinking_budget'])
    
    print(f"\n{Fore.CYAN}Running test...{Style.RESET_ALL}")
    
    # Run a test to capture the signature
    result = stream_test(
        config,
        show_thinking=True,
        custom_prompt="What is 2+2? Think step by step.",
        custom_budget=budget
    )
    
    # Analyze signature
    print(f"\n{Fore.CYAN}{Style.BRIGHT}{'=' * 70}")
    print(f"    Signature Analysis Results")
    print(f"{'=' * 70}{Style.RESET_ALL}")
    
    sig = result.get("signature")
    sig_present = result.get("signature_present", False)
    
    checks = []
    
    # Check 1: Signature present
    check1_pass = sig_present and sig is not None
    checks.append(("Signature field present", check1_pass))
    print(f"\n  {Fore.WHITE}1. Signature field present: ", end="")
    if check1_pass:
        print(f"{Fore.GREEN}YES{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}NO{Style.RESET_ALL}")
    
    # Check 2: Signature non-empty
    check2_pass = sig is not None and len(sig) > 0
    checks.append(("Signature non-empty", check2_pass))
    print(f"  {Fore.WHITE}2. Signature non-empty: ", end="")
    if check2_pass:
        print(f"{Fore.GREEN}YES ({len(sig)} chars){Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}NO{Style.RESET_ALL}")
    
    # Check 3: Signature format (base64-like characters)
    import re
    base64_pattern = re.compile(r'^[A-Za-z0-9+/=_-]+$')
    check3_pass = sig is not None and len(sig) > 0 and bool(base64_pattern.match(sig))
    checks.append(("Valid format (base64-like)", check3_pass))
    print(f"  {Fore.WHITE}3. Valid format (base64-like): ", end="")
    if check3_pass:
        print(f"{Fore.GREEN}YES{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}UNKNOWN{Style.RESET_ALL}")
    
    # Check 4: Reasonable length
    check4_pass = sig is not None and len(sig) >= 50
    checks.append(("Reasonable length (50+ chars)", check4_pass))
    print(f"  {Fore.WHITE}4. Reasonable length (50+ chars): ", end="")
    if check4_pass:
        print(f"{Fore.GREEN}YES{Style.RESET_ALL}")
    else:
        print(f"{Fore.YELLOW}NO (length: {len(sig) if sig else 0}){Style.RESET_ALL}")
    
    # Overall result
    all_passed = all(c[1] for c in checks[:2])  # First 2 checks are critical
    
    print(f"\n{Fore.CYAN}{'-' * 70}{Style.RESET_ALL}")
    
    if all_passed:
        print(f"{Fore.GREEN}{Style.BRIGHT}    SIGNATURE VERIFICATION: PASSED{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}{Style.BRIGHT}    SIGNATURE VERIFICATION: FAILED{Style.RESET_ALL}")
    
    print(f"{Fore.CYAN}{'-' * 70}{Style.RESET_ALL}")
    
    # Show signature preview
    if sig:
        print(f"\n{Fore.WHITE}Signature preview (first 80 chars):{Style.RESET_ALL}")
        print(f"{Fore.LIGHTBLACK_EX}{sig[:80]}...{Style.RESET_ALL}")
        print(f"\n{Fore.WHITE}Full signature length: {Fore.YELLOW}{len(sig)} characters{Style.RESET_ALL}")
    
    print(f"\n{Fore.CYAN}{'=' * 70}{Style.RESET_ALL}\n")
    
    # Save results to results folder
    results_dir = ensure_results_folder()
    try:
        filepath = os.path.join(results_dir, f"signature_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "passed": all_passed,
                "signature_present": sig_present,
                "signature_length": len(sig) if sig else 0,
                "signature_preview": sig[:200] if sig else None,
                "checks": [{"name": c[0], "passed": c[1]} for c in checks],
                "thinking_content": result["thinking_content"][:500],
                "text_content": result["text_content"][:500]
            }, f, indent=2)
        print(f"{Fore.LIGHTBLACK_EX}Results saved to: {filepath}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Could not save results: {e}{Style.RESET_ALL}")
    
    return all_passed


def ensure_chats_folder():
    """Ensure the chats folder exists."""
    chats_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "chats")
    if not os.path.exists(chats_dir):
        os.makedirs(chats_dir)
    return chats_dir


def run_multi_turn_chat(config: Dict[str, Any]):
    """
    Run an interactive multi-turn chat session with extended thinking.
    
    Tests message linking by properly including thinking blocks in conversation history.
    Per Anthropic docs, thinking blocks must be preserved in the message history.
    """
    # Ensure chats folder exists
    chats_dir = ensure_chats_folder()
    
    print(f"\n{Fore.CYAN}{Style.BRIGHT}{'=' * 70}")
    print(f"    Multi-Turn Chat with Extended Thinking & Message Verification")
    print(f"{'=' * 70}{Style.RESET_ALL}")
    
    print(f"""
{Fore.WHITE}This mode tests multi-turn conversations with extended thinking.
When Claude responds with thinking blocks, they are preserved in the
conversation history (message linking) as required by Anthropic's API.

{Fore.GREEN}Message Verification:{Style.RESET_ALL} After each response, the signature is 
validated and linked messages are verified for the next request.{Style.RESET_ALL}

{Fore.CYAN}Commands during chat:{Style.RESET_ALL}
  {Fore.YELLOW}/{Fore.WHITE}         - Show all available commands
  {Fore.YELLOW}/quit{Fore.WHITE}     - Exit chat
  {Fore.YELLOW}/clear{Fore.WHITE}    - Clear conversation history  
  {Fore.YELLOW}/status{Fore.WHITE}   - Show current conversation status
  {Fore.YELLOW}/history{Fore.WHITE}  - Browse and resume saved chats
  {Fore.YELLOW}/verify{Fore.WHITE}   - Show detailed message verification status
  {Fore.YELLOW}/thinking{Fore.WHITE} - Toggle thinking display on/off
  {Fore.YELLOW}/save{Fore.WHITE}     - Save conversation to file
""")
    
    # Ask for budget
    budget = ask_for_budget(config['thinking_budget'])
    
    # Initialize conversation (using content block format for extended thinking compatibility)
    messages = [{"role": "system", "content": config['system_prompt']}]  # System can stay as string
    signatures = []  # Track signatures for verification
    show_thinking = True
    turn_count = 0
    
    print(f"\n{Fore.GREEN}Chat started. Type your messages below.{Style.RESET_ALL}")
    print(f"{Fore.LIGHTBLACK_EX}(Thinking display: ON | Chats saved to: chats/){Style.RESET_ALL}\n")
    
    while True:
        # Get user input
        try:
            user_input = input(f"{Fore.CYAN}You: {Style.RESET_ALL}").strip()
        except EOFError:
            break
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}Chat interrupted.{Style.RESET_ALL}")
            break
        
        if not user_input:
            continue
        
        # Handle commands
        if user_input == "/":
            # Show all available commands
            print(f"\n{Fore.CYAN}{Style.BRIGHT}Available Commands:{Style.RESET_ALL}")
            print(f"  {Fore.YELLOW}/quit{Fore.WHITE}     - Exit chat and save")
            print(f"  {Fore.YELLOW}/clear{Fore.WHITE}    - Clear conversation history")
            print(f"  {Fore.YELLOW}/status{Fore.WHITE}   - Show current conversation status")
            print(f"  {Fore.YELLOW}/history{Fore.WHITE}  - Browse and resume saved chats")
            print(f"  {Fore.YELLOW}/verify{Fore.WHITE}   - Show message verification status")
            print(f"  {Fore.YELLOW}/thinking{Fore.WHITE} - Toggle thinking display (currently: {'ON' if show_thinking else 'OFF'})")
            print(f"  {Fore.YELLOW}/save{Fore.WHITE}     - Save current conversation")
            print(f"  {Fore.YELLOW}/budget{Fore.WHITE}   - Change thinking budget for this session")
            print()
            continue
        
        if user_input.lower() == "/quit":
            print(f"{Fore.CYAN}Exiting chat...{Style.RESET_ALL}")
            break
            
        elif user_input.lower() == "/clear":
            messages = [{"role": "system", "content": config['system_prompt']}]  # System stays as string
            signatures = []
            turn_count = 0
            print(f"{Fore.GREEN}Conversation and verification chain cleared.{Style.RESET_ALL}\n")
            continue
        
        elif user_input.lower() == "/budget":
            new_budget = ask_for_budget(budget)
            if new_budget != budget:
                budget = new_budget
                print(f"{Fore.GREEN}Thinking budget updated to {budget} tokens for this session.{Style.RESET_ALL}\n")
            continue
            
        elif user_input.lower() == "/status":
            # Show current conversation status
            print(f"\n{Fore.CYAN}Current Conversation Status:{Style.RESET_ALL}")
            print(f"  {Fore.WHITE}Total messages: {Fore.YELLOW}{len(messages)}")
            print(f"  {Fore.WHITE}Turns: {Fore.YELLOW}{turn_count}")
            print(f"  {Fore.WHITE}Thinking budget: {Fore.YELLOW}{budget} tokens")
            print(f"  {Fore.WHITE}Signatures collected: {Fore.YELLOW}{len(signatures)}")
            for i, msg in enumerate(messages):
                role = msg.get("role", "unknown")
                content = msg.get("content", "")
                if isinstance(content, list):
                    types = [c.get("type", "?") for c in content]
                    text_blocks = [c for c in content if c.get("type") == "text"]
                    if text_blocks:
                        text_preview = text_blocks[0].get("text", "")[:30]
                        print(f"  {Fore.LIGHTBLACK_EX}[{i}] {role}: {types} \"{text_preview}...\"{Style.RESET_ALL}")
                    else:
                        print(f"  {Fore.LIGHTBLACK_EX}[{i}] {role}: {types}{Style.RESET_ALL}")
                else:
                    preview = content[:50] + "..." if len(content) > 50 else content
                    print(f"  {Fore.LIGHTBLACK_EX}[{i}] {role}: {preview}{Style.RESET_ALL}")
            print()
            continue
        
        elif user_input.lower() == "/history":
            # Browse and resume saved chats
            print(f"\n{Fore.CYAN}{Style.BRIGHT}Saved Chat History:{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'-' * 50}{Style.RESET_ALL}")
            
            # List chat files
            chat_files = []
            try:
                for f in sorted(os.listdir(chats_dir), reverse=True):
                    if f.endswith('.json'):
                        chat_files.append(f)
            except Exception as e:
                print(f"{Fore.RED}Error reading chats folder: {e}{Style.RESET_ALL}")
            
            if not chat_files:
                print(f"  {Fore.LIGHTBLACK_EX}No saved chats found.{Style.RESET_ALL}")
            else:
                for i, f in enumerate(chat_files[:10]):  # Show last 10
                    filepath = os.path.join(chats_dir, f)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as file:
                            data = json.load(file)
                            turns = data.get('turns', '?')
                            msg_count = data.get('message_count', len(data.get('messages', [])))
                            # Get timestamp from filename
                            print(f"  {Fore.YELLOW}[{i+1}]{Fore.WHITE} {f}")
                            print(f"      {Fore.LIGHTBLACK_EX}Turns: {turns} | Messages: {msg_count}{Style.RESET_ALL}")
                    except:
                        print(f"  {Fore.YELLOW}[{i+1}]{Fore.WHITE} {f}")
                
                if len(chat_files) > 10:
                    print(f"\n  {Fore.LIGHTBLACK_EX}...and {len(chat_files) - 10} more{Style.RESET_ALL}")
                
                print(f"\n{Fore.WHITE}Enter number to resume, or press Enter to cancel:{Style.RESET_ALL}")
                choice = input(f"{Fore.YELLOW}> {Style.RESET_ALL}").strip()
                
                if choice.isdigit():
                    idx = int(choice) - 1
                    if 0 <= idx < len(chat_files):
                        filepath = os.path.join(chats_dir, chat_files[idx])
                        try:
                            with open(filepath, 'r', encoding='utf-8') as file:
                                data = json.load(file)
                                
                            # Check if this is a resumable chat
                            is_resumable = data.get('resumable', False)
                            loaded_messages = data.get('messages', [])
                            loaded_turns = data.get('turns', 0)
                            loaded_sigs = data.get('signatures', [])
                            
                            if is_resumable:
                                # Full data available - direct restore
                                messages = loaded_messages
                                turn_count = loaded_turns
                                signatures = loaded_sigs
                                
                                # Verify signatures are intact
                                sig_count = 0
                                for msg in messages:
                                    if msg.get('role') == 'assistant' and isinstance(msg.get('content'), list):
                                        for block in msg['content']:
                                            if block.get('type') == 'thinking' and block.get('signature'):
                                                sig_count += 1
                                
                                print(f"\n{Fore.GREEN}Chat restored: {chat_files[idx]}{Style.RESET_ALL}")
                                print(f"{Fore.LIGHTBLACK_EX}Loaded {len(messages)} messages, {turn_count} turns, {sig_count} valid signatures{Style.RESET_ALL}")
                                print(f"{Fore.GREEN}This chat is fully resumable with thinking history intact.{Style.RESET_ALL}\n")
                            else:
                                # Old format or summarized - can't properly resume with thinking
                                # Strip thinking blocks to avoid signature errors
                                messages = []
                                for msg in loaded_messages:
                                    if msg.get('role') == 'assistant' and isinstance(msg.get('content'), list):
                                        # Keep only text blocks, drop thinking blocks
                                        text_only = [b for b in msg['content'] if b.get('type') == 'text']
                                        if text_only:
                                            messages.append({"role": "assistant", "content": text_only})
                                    else:
                                        messages.append(msg)
                                
                                turn_count = loaded_turns
                                signatures = []  # Reset signatures since thinking was stripped
                                
                                print(f"\n{Fore.YELLOW}Chat restored (legacy format): {chat_files[idx]}{Style.RESET_ALL}")
                                print(f"{Fore.LIGHTBLACK_EX}Loaded {len(messages)} messages, {turn_count} turns{Style.RESET_ALL}")
                                print(f"{Fore.YELLOW}Note: Thinking history was stripped (old save format). New messages will have thinking.{Style.RESET_ALL}\n")
                        except Exception as e:
                            print(f"{Fore.RED}Error loading chat: {e}{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.RED}Invalid selection.{Style.RESET_ALL}")
            print()
            continue
            
        elif user_input.lower() == "/thinking":
            show_thinking = not show_thinking
            status = "ON" if show_thinking else "OFF"
            print(f"{Fore.GREEN}Thinking display: {status}{Style.RESET_ALL}\n")
            continue
        
        elif user_input.lower() == "/verify":
            # Show detailed message verification status
            print(f"\n{Fore.CYAN}{Style.BRIGHT}Message Verification Status{Style.RESET_ALL}")
            print(f"{Fore.CYAN}{'-' * 50}{Style.RESET_ALL}")
            print(f"  {Fore.WHITE}Total Messages: {Fore.YELLOW}{len(messages)}")
            print(f"  {Fore.WHITE}Conversation Turns: {Fore.YELLOW}{turn_count}")
            print(f"  {Fore.WHITE}Linked Signatures: {Fore.YELLOW}{len(signatures)}")
            
            if signatures:
                print(f"\n  {Fore.GREEN}Signature Chain:{Style.RESET_ALL}")
                for i, sig_info in enumerate(signatures):
                    print(f"    {Fore.WHITE}Turn {sig_info['turn']}: ", end="")
                    if sig_info['valid']:
                        print(f"{Fore.GREEN}VALID{Style.RESET_ALL} ", end="")
                    else:
                        print(f"{Fore.RED}MISSING{Style.RESET_ALL} ", end="")
                    print(f"{Fore.LIGHTBLACK_EX}({sig_info['length']} chars){Style.RESET_ALL}")
                
                # Verify chain integrity
                all_valid = all(s['valid'] for s in signatures)
                print(f"\n  {Fore.WHITE}Chain Integrity: ", end="")
                if all_valid:
                    print(f"{Fore.GREEN}VERIFIED - All messages properly linked{Style.RESET_ALL}")
                else:
                    print(f"{Fore.YELLOW}PARTIAL - Some signatures missing{Style.RESET_ALL}")
            else:
                print(f"\n  {Fore.LIGHTBLACK_EX}No responses yet - send a message to start.{Style.RESET_ALL}")
            
            print(f"{Fore.CYAN}{'-' * 50}{Style.RESET_ALL}\n")
            continue
            
        elif user_input.lower() == "/save":
            try:
                filename = os.path.join(chats_dir, f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
                with open(filename, "w", encoding="utf-8") as f:
                    json.dump({
                        "timestamp": datetime.now().isoformat(),
                        "turns": turn_count,
                        "message_count": len(messages),
                        "signatures": signatures,
                        "resumable": True,
                        "messages": messages  # Complete messages for resume
                    }, f, indent=2, ensure_ascii=False)
                print(f"{Fore.GREEN}Conversation saved to: {filename}{Style.RESET_ALL}")
                print(f"{Fore.LIGHTBLACK_EX}(Resumable with /history){Style.RESET_ALL}\n")
            except Exception as e:
                print(f"{Fore.RED}Failed to save: {e}{Style.RESET_ALL}\n")
            continue
        
        # Add user message to history (plain string format)
        messages.append({
            "role": "user", 
            "content": user_input
        })
        turn_count += 1
        
        # Prepare request
        headers = {
            "Content-Type": "application/json",
            "api-key": config['api_key'],
            "Accept": "text/event-stream",
        }
        
        payload = {
            "stream": True,
            "model": config['model'],
            "max_tokens": config.get('max_tokens', DEFAULT_MAX_TOKENS),
            "thinking": {
                "type": "enabled",
                "budget_tokens": budget
            },
            "messages": messages
        }
        
        # Send request with loading animation
        loading.start()
        try:
            response = requests.post(
                config['endpoint'],
                headers=headers,
                json=payload,
                stream=True,
                timeout=120
            )
            loading.stop()
            
            if response.status_code != 200:
                print(f"{Fore.RED}[ERROR] API returned status {response.status_code}{Style.RESET_ALL}")
                try:
                    print(f"{Fore.RED}{response.text[:300]}{Style.RESET_ALL}")
                except:
                    pass
                # Remove the failed user message
                messages.pop()
                turn_count -= 1
                continue
            
            # Stream response
            if show_thinking:
                print(f"\n{Fore.MAGENTA}[THINKING]{Style.RESET_ALL} ", end="", flush=True)
            
            current_thinking = ""
            current_text = ""
            current_signature = ""
            redacted_thinking_blocks = []  # Store any redacted thinking blocks
            text_started = False
            
            for line in response.iter_lines(decode_unicode=True):
                if not line:
                    continue
                    
                parsed = parse_sse_line(line)
                if not parsed or parsed.get("done"):
                    break
                
                # Process events
                raw_events = parsed.get("rawEvents", {})
                event = raw_events.get("event", {})
                event_type = event.get("type", "")
                
                if event_type == "content_block_delta":
                    delta = event.get("delta", {})
                    delta_type = delta.get("type", "")
                    
                    if delta_type == "thinking_delta":
                        thinking_text = delta.get("thinking", "")
                        if thinking_text:
                            current_thinking += thinking_text
                            if show_thinking:
                                print(f"{Fore.MAGENTA}{thinking_text}{Style.RESET_ALL}", end="", flush=True)
                                
                    elif delta_type == "text_delta":
                        text = delta.get("text", "")
                        if text:
                            if not text_started:
                                if show_thinking:
                                    print(f"\n\n{Fore.GREEN}Claude:{Style.RESET_ALL} ", end="", flush=True)
                                else:
                                    print(f"\n{Fore.GREEN}Claude:{Style.RESET_ALL} ", end="", flush=True)
                                text_started = True
                            current_text += text
                            print(f"{Fore.WHITE}{text}{Style.RESET_ALL}", end="", flush=True)
                    
                    elif delta_type == "signature_delta":
                        current_signature += delta.get("signature", "")
                
                # Also capture signature and redacted_thinking from content blocks
                content = parsed.get("content", [])
                for block in content:
                    if block.get("type") == "thinking":
                        sig = block.get("signature", "")
                        if sig and len(sig) > len(current_signature):
                            current_signature = sig
                    elif block.get("type") == "redacted_thinking":
                        # Store redacted thinking blocks to preserve in history
                        if block not in redacted_thinking_blocks:
                            redacted_thinking_blocks.append(block)
                            if show_thinking:
                                print(f"{Fore.YELLOW}[REDACTED THINKING BLOCK]{Style.RESET_ALL} ", end="", flush=True)
            
            print("\n")  # End response
            
            # Build assistant message with proper structure for message linking
            assistant_content = []
            
            # Add thinking block (required for message linking)
            if current_thinking:
                thinking_block = {
                    "type": "thinking",
                    "thinking": current_thinking
                }
                if current_signature:
                    thinking_block["signature"] = current_signature
                assistant_content.append(thinking_block)
            
            # Add any redacted thinking blocks (must be preserved unchanged)
            for redacted_block in redacted_thinking_blocks:
                assistant_content.append(redacted_block)
            
            # Add text block
            if current_text:
                assistant_content.append({
                    "type": "text",
                    "text": current_text
                })
            
            # Add assistant message to history with content blocks
            if assistant_content:
                messages.append({
                    "role": "assistant",
                    "content": assistant_content
                })
            
            # Track signature for verification
            sig_valid = bool(current_signature and len(current_signature) > 0)
            signatures.append({
                "turn": turn_count,
                "valid": sig_valid,
                "length": len(current_signature) if current_signature else 0,
                "preview": current_signature[:50] if current_signature else None
            })
            
            # Show message verification status
            print(f"{Fore.CYAN}{'-' * 60}{Style.RESET_ALL}")
            print(f"{Fore.WHITE}  Message Verification for Turn {turn_count}:{Style.RESET_ALL}")
            
            # Thinking verification
            if current_thinking:
                print(f"    {Fore.GREEN}[OK]{Style.RESET_ALL} Thinking block captured ({len(current_thinking)} chars)")
            else:
                print(f"    {Fore.RED}[--]{Style.RESET_ALL} No thinking block")
            
            # Signature verification  
            if sig_valid:
                print(f"    {Fore.GREEN}[OK]{Style.RESET_ALL} Signature present ({len(current_signature)} chars)")
                # Validate signature format
                import re
                if re.match(r'^[A-Za-z0-9+/=_-]+$', current_signature):
                    print(f"    {Fore.GREEN}[OK]{Style.RESET_ALL} Signature format valid (base64)")
                else:
                    print(f"    {Fore.YELLOW}[??]{Style.RESET_ALL} Signature format unknown")
            else:
                print(f"    {Fore.YELLOW}[--]{Style.RESET_ALL} No signature (may not be required)")
            
            # Redacted thinking verification
            if redacted_thinking_blocks:
                print(f"    {Fore.YELLOW}[!!]{Style.RESET_ALL} Redacted thinking blocks: {len(redacted_thinking_blocks)} (preserved)")
            
            # Message linking status
            linked_count = sum(1 for m in messages if isinstance(m.get("content"), list))
            print(f"    {Fore.GREEN}[OK]{Style.RESET_ALL} Message linked to history ({linked_count} assistant msgs with blocks)")
            
            # Chain integrity
            if len(signatures) > 1:
                chain_valid = all(s['valid'] for s in signatures)
                if chain_valid:
                    print(f"    {Fore.GREEN}[OK]{Style.RESET_ALL} Signature chain intact ({len(signatures)} turns)")
                else:
                    print(f"    {Fore.YELLOW}[!!]{Style.RESET_ALL} Signature chain incomplete")
            
            print(f"{Fore.CYAN}{'-' * 60}{Style.RESET_ALL}")
            print(f"{Fore.LIGHTBLACK_EX}[Turn {turn_count} complete | Total messages: {len(messages)}]{Style.RESET_ALL}\n")
            
        except requests.exceptions.Timeout:
            loading.stop()
            print(f"\n{Fore.RED}[ERROR] Request timed out{Style.RESET_ALL}")
            messages.pop()
            turn_count -= 1
            
        except requests.exceptions.ConnectionError as e:
            loading.stop()
            print(f"\n{Fore.RED}[ERROR] Connection error: {e}{Style.RESET_ALL}")
            messages.pop()
            turn_count -= 1
            
        except Exception as e:
            loading.stop()
            print(f"\n{Fore.RED}[ERROR] {e}{Style.RESET_ALL}")
            messages.pop()
            turn_count -= 1
    
    # Save final conversation to chats folder (full data for resume capability)
    try:
        filename = os.path.join(chats_dir, f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}_final.json")
        with open(filename, "w", encoding="utf-8") as f:
            # Save complete messages with full thinking blocks and signatures for resume
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "turns": turn_count,
                "message_count": len(messages),
                "signatures": signatures,
                "resumable": True,  # Flag indicating this chat can be resumed
                "verification_summary": {
                    "total_signatures": len(signatures),
                    "valid_signatures": sum(1 for s in signatures if s['valid']),
                    "chain_intact": all(s['valid'] for s in signatures) if signatures else True
                },
                "messages": messages  # Save complete messages for proper resume
            }, f, indent=2, ensure_ascii=False)
        print(f"{Fore.LIGHTBLACK_EX}Chat history saved to: {filename}{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}Could not save chat history: {e}{Style.RESET_ALL}")
    
    print(f"\n{Fore.CYAN}{'=' * 70}{Style.RESET_ALL}\n")


def main():
    """Main entry point."""
    # Check for command line flags
    args = sys.argv[1:]
    
    if "-h" in args or "--help" in args or "/?" in args or "-?" in args:
        print_header_with_config(load_config())
        print_help()
        sys.exit(0)
    
    # Load configuration from file (or use defaults)
    config = load_config()
    print(f"{Fore.LIGHTBLACK_EX}Config loaded from: {CONFIG_FILE}{Style.RESET_ALL}")
    
    # Auto mode - run test and exit
    if "--auto" in args:
        print_header()
        result = stream_test(config, show_thinking=True)
        print_result(result)
        save_results(result)
        sys.exit(0 if result["passed"] else 1)
    
    # Quiet mode - minimal output
    if "--quiet" in args:
        result = stream_test(config, show_thinking=False)
        if result["passed"]:
            print(f"{Fore.GREEN}PASSED{Style.RESET_ALL}")
            sys.exit(0)
        else:
            print(f"{Fore.RED}FAILED{Style.RESET_ALL}")
            sys.exit(1)
    
    # Install colorama hint
    if not COLORS_AVAILABLE:
        print("Tip: Install colorama for colored output: pip install colorama")
    
    # Interactive mode
    while True:
        clear_screen()
        print_header_with_config(config)
        print_menu()
        
        choice = input(f"{Fore.GREEN}Enter choice: {Style.RESET_ALL}").strip()
        
        if choice == "0":
            print(f"\n{Fore.CYAN}Goodbye!{Style.RESET_ALL}\n")
            break
            
        elif choice == "1":
            # Run with default prompt, show thinking - ask for budget
            budget = ask_for_budget(config['thinking_budget'])
            result = stream_test(config, show_thinking=True, custom_budget=budget)
            print_result(result)
            save_results(result)
            input(f"{Fore.LIGHTBLACK_EX}Press Enter to continue...{Style.RESET_ALL}")
            
        elif choice == "2":
            # Custom prompt - ask for budget first
            budget = ask_for_budget(config['thinking_budget'])
            print(f"\n{Fore.WHITE}Enter your prompt (or leave empty to cancel):{Style.RESET_ALL}")
            custom = input(f"{Fore.YELLOW}> {Style.RESET_ALL}").strip()
            if custom:
                result = stream_test(config, show_thinking=True, custom_prompt=custom, custom_budget=budget)
                print_result(result)
                save_results(result)
            input(f"{Fore.LIGHTBLACK_EX}Press Enter to continue...{Style.RESET_ALL}")
            
        elif choice == "3":
            # Run without showing thinking
            budget = ask_for_budget(config['thinking_budget'])
            result = stream_test(config, show_thinking=False, custom_budget=budget)
            print_result(result)
            save_results(result)
            input(f"{Fore.LIGHTBLACK_EX}Press Enter to continue...{Style.RESET_ALL}")
            
        elif choice == "4":
            # Budget scaling test
            run_budget_scaling_test(config)
            input(f"{Fore.LIGHTBLACK_EX}Press Enter to continue...{Style.RESET_ALL}")
            
        elif choice == "5":
            # Signature verification test
            run_signature_verification_test(config)
            input(f"{Fore.LIGHTBLACK_EX}Press Enter to continue...{Style.RESET_ALL}")
            
        elif choice == "6":
            # Multi-turn chat with message linking
            run_multi_turn_chat(config)
            input(f"{Fore.LIGHTBLACK_EX}Press Enter to continue...{Style.RESET_ALL}")
            
        elif choice == "7":
            # Configure
            config = configure_settings(config)
            
        elif choice == "8":
            # View config
            print_config(config)
            input(f"{Fore.LIGHTBLACK_EX}Press Enter to continue...{Style.RESET_ALL}")
            
        elif choice == "9":
            # Help
            print_help()
            input(f"{Fore.LIGHTBLACK_EX}Press Enter to continue...{Style.RESET_ALL}")
            
        else:
            print(f"{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}")
            input(f"{Fore.LIGHTBLACK_EX}Press Enter to continue...{Style.RESET_ALL}")


if __name__ == "__main__":
    main()
