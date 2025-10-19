#!/usr/bin/env python3
"""
Review Bridge - Handles automated review streaming from Python to Node.js
"""

import sys
import json
import asyncio
from typing import List, Optional
from storybook.project_manager import ProjectManager
from storybook.editor import LiteraryEditor


async def stream_review(project_id: str, focus_areas: Optional[List[str]] = None):
    """
    Stream review events to stdout as JSON lines

    Events:
    - {"type": "progress", "message": "...", "detail": "..."}
    - {"type": "complete", "data": {...review...}}
    - {"type": "error", "message": "..."}
    """
    try:
        # Load project
        pm = ProjectManager()
        project = pm.load_project(project_id)

        # Create editor
        editor = LiteraryEditor(project)

        # Progress callback
        def on_progress(message: str, detail: str = ""):
            print(json.dumps({
                "type": "progress",
                "message": message,
                "detail": detail
            }), flush=True)

        # Run review
        print(json.dumps({
            "type": "progress",
            "message": "Starting automated review...",
            "detail": "Loading manuscript"
        }), flush=True)

        review = await editor.run_review_async(
            focus_areas=focus_areas,
            on_progress=on_progress
        )

        # Convert review to dict
        review_data = review.model_dump() if hasattr(review, "model_dump") else review

        # Send completion event
        print(json.dumps({
            "type": "complete",
            "data": review_data
        }), flush=True)

    except Exception as e:
        print(json.dumps({
            "type": "error",
            "message": f"Review failed: {str(e)}"
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
    focus_areas = None

    if len(sys.argv) > 2:
        try:
            focus_areas = json.loads(sys.argv[2])
        except json.JSONDecodeError:
            pass

    try:
        asyncio.run(stream_review(project_id, focus_areas))
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
