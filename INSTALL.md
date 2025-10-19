# Storybook Installation Guide

## Prerequisites

### 1. Python 3.10 or Higher

Check your Python version:
```bash
python3 --version
```

If you need to install or upgrade Python, visit: https://www.python.org/downloads/

### 2. Claude Code CLI

Storybook requires the Claude Code CLI to be installed on your system.

**Installation:**

Follow the instructions at: https://claude.com/claude-code

**Verification:**

After installation, verify it works:
```bash
claude --version
```

### 3. Anthropic API Key

You need an Anthropic API key to use Claude.

1. Sign up at: https://console.anthropic.com/
2. Generate an API key
3. Set it as an environment variable:

**macOS/Linux:**
```bash
export ANTHROPIC_API_KEY="your-api-key-here"

# Add to your shell profile to make it permanent
echo 'export ANTHROPIC_API_KEY="your-api-key-here"' >> ~/.bashrc
# or for zsh:
echo 'export ANTHROPIC_API_KEY="your-api-key-here"' >> ~/.zshrc
```

**Windows (PowerShell):**
```powershell
$env:ANTHROPIC_API_KEY="your-api-key-here"

# To make it permanent:
[System.Environment]::SetEnvironmentVariable('ANTHROPIC_API_KEY', 'your-api-key-here', 'User')
```

## Installation

### Option 1: Install from Source (Recommended)

1. **Clone or download the repository**

2. **Navigate to the storybook directory:**
   ```bash
   cd storybook
   ```

3. **Install Storybook:**
   ```bash
   pip install -e .
   ```

   This installs Storybook in "editable" mode, allowing you to make changes if needed.

4. **Install optional dependencies for full functionality:**
   ```bash
   pip install python-docx pypdf
   ```

   These enable DOCX and PDF import/export capabilities.

### Option 2: Install Development Version

For development with additional tools:

```bash
cd storybook
pip install -e ".[dev]"
```

This includes pytest, black, and ruff for testing and code formatting.

## Verification

Verify the installation:

```bash
storybook --help
```

If you see the Storybook help message, installation was successful!

## Quick Start

1. **Launch Storybook:**
   ```bash
   storybook
   ```

2. **Create your first project:**
   - Select "New Project" from the main menu
   - Enter a project name and details
   - Start writing or chatting with the AI editor!

## Troubleshooting

### "claude: command not found"

The Claude Code CLI is not installed or not in your PATH.

**Solution:**
- Reinstall Claude Code CLI from https://claude.com/claude-code
- Ensure it's in your system PATH

### "ANTHROPIC_API_KEY not set"

The API key environment variable is not configured.

**Solution:**
```bash
export ANTHROPIC_API_KEY="your-api-key-here"
```

### "ModuleNotFoundError: No module named 'docx'"

Optional dependencies for DOCX support are missing.

**Solution:**
```bash
pip install python-docx
```

### "ModuleNotFoundError: No module named 'pypdf'"

Optional dependencies for PDF support are missing.

**Solution:**
```bash
pip install pypdf
```

### "Permission denied" errors

You don't have write permissions for the installation directory.

**Solution:**
- Use a virtual environment (recommended)
- Or install with `--user` flag:
  ```bash
  pip install --user -e .
  ```

## Using a Virtual Environment (Recommended)

Virtual environments keep Storybook's dependencies isolated:

```bash
# Create virtual environment
python3 -m venv storybook-env

# Activate it
# macOS/Linux:
source storybook-env/bin/activate
# Windows:
storybook-env\Scripts\activate

# Install Storybook
cd storybook
pip install -e .

# When done, deactivate
deactivate
```

## Updating Storybook

To update to the latest version:

```bash
cd storybook
git pull  # if using git
pip install -e . --upgrade
```

## Uninstallation

To remove Storybook:

```bash
pip uninstall storybook
```

To remove all data:

```bash
rm -rf ~/.storybook
```

## Getting Help

- **Documentation**: See `README.md` and `USAGE.md`
- **Examples**: Check the `examples/` directory
- **Issues**: Report bugs or request features

## Next Steps

Once installed, see `USAGE.md` for a complete guide to using Storybook.

Happy writing!
