#!/usr/bin/env python3
"""
Chat Bridge - Handles real-time chat streaming from Python to Node.js
"""

import sys
import json
import asyncio
from typing import Dict, Any
from storybook.project_manager import ProjectManager
from storybook.chat import ChatSession


async def stream_chat(project_id: str):
    """
    Stream chat events to stdout as JSON lines

    Events:
    - {"type": "message", "role": "assistant", "content": "..."}
    - {"type": "thinking", "content": "..."}
    - {"type": "tool", "name": "...", "input": {...}}
    - {"type": "complete"}
    """
    try:
        # Load project
        pm = ProjectManager()
        project = pm.load_project(project_id)

        # Create chat session
        chat = ChatSession(project)

        # Event handlers
        def on_message(role: str, content: str):
            print(json.dumps({
                "type": "message",
                "role": role,
                "content": content,
                "timestamp": str(asyncio.get_event_loop().time())
            }), flush=True)

        def on_thinking(content: str):
            print(json.dumps({
                "type": "thinking",
                "content": content
            }), flush=True)

        def on_tool(name: str, tool_input: Dict[str, Any]):
            print(json.dumps({
                "type": "tool",
                "name": name,
                "input": tool_input
            }), flush=True)

        # Attach event handlers
        chat.on_message = on_message
        chat.on_thinking = on_thinking
        chat.on_tool = on_tool

        # Read messages from stdin
        while True:
            line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
            if not line:
                break

            try:
                data = json.loads(line)
                if data.get("type") == "message":
                    message = data.get("content", "")

                    # Send message and stream response
                    await chat.send_message_async(message)

                    print(json.dumps({
                        "type": "complete"
                    }), flush=True)

            except json.JSONDecodeError:
                print(json.dumps({
                    "type": "error",
                    "message": "Invalid JSON input"
                }), flush=True)
            except Exception as e:
                print(json.dumps({
                    "type": "error",
                    "message": str(e)
                }), flush=True)

    except Exception as e:
        print(json.dumps({
            "type": "error",
            "message": f"Chat session failed: {str(e)}"
        }), flush=True)
        sys.exit(1)


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print(json.dumps({
            "type": "error",
            "message": "No project ID provided"
        }), flush=True)
        sys.exit(1)

    project_id = sys.argv[1]

    try:
        asyncio.run(stream_chat(project_id))
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
