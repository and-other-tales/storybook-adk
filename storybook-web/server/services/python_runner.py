#!/usr/bin/env python3
"""
Python Runner - Executes Python CLI functions from Node.js
"""

import sys
import json
import importlib
from typing import Any, Dict


def execute_command(command: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute a Python function dynamically

    Args:
        command: {
            "module": "storybook.web_integration",
            "function": "list_projects",
            "args": []
        }

    Returns:
        {"success": True, "data": result} or {"success": False, "error": message}
    """
    try:
        module_name = command.get("module")
        function_name = command.get("function")
        args = command.get("args", [])

        if not module_name or not function_name:
            return {
                "success": False,
                "error": "Missing module or function name"
            }

        # Import the module
        module = importlib.import_module(module_name)

        # Get the function
        func = getattr(module, function_name)

        # Execute the function with positional and keyword args
        if isinstance(args, list):
            result = func(*args)
        elif isinstance(args, dict):
            result = func(**args)
        else:
            result = func(args)

        # Result should already be JSON-serializable from web_integration
        return {
            "success": True,
            "data": result
        }

    except Exception as e:
        import traceback
        return {
            "success": False,
            "error": str(e),
            "traceback": traceback.format_exc()
        }


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print(json.dumps({
            "success": False,
            "error": "No command provided"
        }))
        sys.exit(1)

    try:
        command = json.loads(sys.argv[1])
        result = execute_command(command)
        print(json.dumps(result))
        sys.exit(0 if result["success"] else 1)
    except Exception as e:
        print(json.dumps({
            "success": False,
            "error": f"Failed to parse command: {str(e)}"
        }))
        sys.exit(1)


if __name__ == "__main__":
    main()
