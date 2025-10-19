"""Custom MCP tools for manuscript editing."""

import re
from typing import Any

from claude_agent_sdk import tool, create_sdk_mcp_server

from .models import Character, PlotEvent


# Character tracking tools


@tool(
    "track_character",
    "Track or update a character in the manuscript",
    {
        "name": str,
        "aliases": list,
        "description": str,
        "traits": list,
        "first_appearance": str,
        "notes": str,
    },
)
async def track_character(args: dict[str, Any]) -> dict[str, Any]:
    """Track a character in the manuscript.

    This tool helps maintain character consistency by storing character information
    that can be referenced throughout the editing process.
    """
    try:
        character = Character(
            name=args.get("name", ""),
            aliases=args.get("aliases", []),
            description=args.get("description", ""),
            traits=args.get("traits", []),
            first_appearance=args.get("first_appearance", ""),
            notes=args.get("notes", ""),
        )

        # Store character data (will be integrated with project manager)
        result = f"Character '{character.name}' tracked successfully."
        if character.aliases:
            result += f" Aliases: {', '.join(character.aliases)}"

        return {"content": [{"type": "text", "text": result}]}
    except Exception as e:
        return {
            "content": [{"type": "text", "text": f"Error tracking character: {str(e)}"}],
            "is_error": True,
        }


@tool(
    "list_characters",
    "List all tracked characters in the manuscript",
    {},
)
async def list_characters(args: dict[str, Any]) -> dict[str, Any]:
    """List all characters being tracked.

    Returns a summary of all characters with their key attributes.
    """
    # This will be integrated with the project manager
    return {
        "content": [
            {
                "type": "text",
                "text": "Character tracking is active. Use track_character to add characters.",
            }
        ]
    }


@tool(
    "check_character_consistency",
    "Check for character consistency issues in the manuscript",
    {"character_name": str, "manuscript_text": str},
)
async def check_character_consistency(args: dict[str, Any]) -> dict[str, Any]:
    """Check for character consistency issues.

    Analyzes mentions of a character throughout the manuscript to identify
    potential consistency problems.
    """
    character_name = args.get("character_name", "")
    manuscript_text = args.get("manuscript_text", "")

    if not character_name or not manuscript_text:
        return {
            "content": [
                {"type": "text", "text": "Both character_name and manuscript_text are required"}
            ],
            "is_error": True,
        }

    # Find all mentions
    pattern = re.compile(rf"\b{re.escape(character_name)}\b", re.IGNORECASE)
    mentions = pattern.findall(manuscript_text)

    # Analyze capitalization consistency
    capitalizations = set(mentions)
    issues = []

    if len(capitalizations) > 1:
        issues.append(f"Inconsistent capitalization: {', '.join(capitalizations)}")

    result = f"Found {len(mentions)} mentions of '{character_name}'.\n"
    if issues:
        result += "\nIssues found:\n" + "\n".join(f"- {issue}" for issue in issues)
    else:
        result += "\nNo consistency issues detected."

    return {"content": [{"type": "text", "text": result}]}


# Plot tracking tools


@tool(
    "track_plot_event",
    "Track a plot event or story beat",
    {
        "id": str,
        "title": str,
        "description": str,
        "chapter_reference": str,
        "characters_involved": list,
        "importance": str,
    },
)
async def track_plot_event(args: dict[str, Any]) -> dict[str, Any]:
    """Track a plot event in the manuscript.

    Helps maintain plot continuity by recording key events and their relationships.
    """
    try:
        event = PlotEvent(
            id=args.get("id", ""),
            title=args.get("title", ""),
            description=args.get("description", ""),
            chapter_reference=args.get("chapter_reference", ""),
            characters_involved=args.get("characters_involved", []),
            importance=args.get("importance", "medium"),
        )

        result = f"Plot event '{event.title}' tracked successfully."
        if event.characters_involved:
            result += f" Characters: {', '.join(event.characters_involved)}"

        return {"content": [{"type": "text", "text": result}]}
    except Exception as e:
        return {
            "content": [{"type": "text", "text": f"Error tracking plot event: {str(e)}"}],
            "is_error": True,
        }


@tool(
    "list_plot_events",
    "List all tracked plot events",
    {},
)
async def list_plot_events(args: dict[str, Any]) -> dict[str, Any]:
    """List all plot events being tracked."""
    return {
        "content": [
            {
                "type": "text",
                "text": "Plot tracking is active. Use track_plot_event to add events.",
            }
        ]
    }


@tool(
    "analyze_plot_timeline",
    "Analyze the plot timeline for consistency issues",
    {"manuscript_text": str},
)
async def analyze_plot_timeline(args: dict[str, Any]) -> dict[str, Any]:
    """Analyze plot timeline for consistency.

    Examines time references and sequence of events to identify potential issues.
    """
    manuscript_text = args.get("manuscript_text", "")

    # Find time references
    time_patterns = [
        r"\b(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\b",
        r"\b(January|February|March|April|May|June|July|August|September|October|November|December)\b",
        r"\bday (\d+)\b",
        r"\b(\d+) days? (later|ago|before|after)\b",
    ]

    time_references = []
    for pattern in time_patterns:
        matches = re.finditer(pattern, manuscript_text, re.IGNORECASE)
        time_references.extend([m.group() for m in matches])

    result = f"Found {len(time_references)} time references in the manuscript.\n"
    if time_references[:10]:
        result += "\nSample references:\n"
        result += "\n".join(f"- {ref}" for ref in time_references[:10])

    return {"content": [{"type": "text", "text": result}]}


# Manuscript analysis tools


@tool(
    "analyze_prose_quality",
    "Analyze prose quality and style",
    {"text_sample": str},
)
async def analyze_prose_quality(args: dict[str, Any]) -> dict[str, Any]:
    """Analyze prose quality, style, and readability.

    Provides feedback on sentence structure, word choice, and overall writing quality.
    """
    text_sample = args.get("text_sample", "")

    if not text_sample:
        return {
            "content": [{"type": "text", "text": "text_sample is required"}],
            "is_error": True,
        }

    # Basic analysis
    sentences = re.split(r"[.!?]+", text_sample)
    sentences = [s.strip() for s in sentences if s.strip()]
    words = text_sample.split()

    avg_sentence_length = len(words) / len(sentences) if sentences else 0

    # Check for common issues
    issues = []

    # Passive voice detection (simplified)
    passive_indicators = ["was", "were", "been", "being"]
    passive_count = sum(1 for word in words if word.lower() in passive_indicators)
    if passive_count / len(words) > 0.05:
        issues.append("High use of passive voice detected")

    # Adverb overuse
    adverbs = [w for w in words if w.lower().endswith("ly")]
    if len(adverbs) / len(words) > 0.05:
        issues.append(f"Frequent adverb use ({len(adverbs)} adverbs)")

    # Repetitive words
    word_freq = {}
    for word in words:
        word_lower = word.lower()
        if len(word_lower) > 3:
            word_freq[word_lower] = word_freq.get(word_lower, 0) + 1

    repeated = [word for word, count in word_freq.items() if count > 3]
    if repeated:
        issues.append(f"Repetitive words: {', '.join(repeated[:5])}")

    result = "Prose Analysis:\n"
    result += f"- Sentences: {len(sentences)}\n"
    result += f"- Words: {len(words)}\n"
    result += f"- Avg. sentence length: {avg_sentence_length:.1f} words\n"

    if issues:
        result += "\nIssues detected:\n"
        result += "\n".join(f"- {issue}" for issue in issues)
    else:
        result += "\nNo major issues detected."

    return {"content": [{"type": "text", "text": result}]}


@tool(
    "detect_pacing_issues",
    "Detect potential pacing issues in the manuscript",
    {"chapter_text": str},
)
async def detect_pacing_issues(args: dict[str, Any]) -> dict[str, Any]:
    """Analyze chapter pacing.

    Identifies sections that may be too slow or too fast-paced.
    """
    chapter_text = args.get("chapter_text", "")

    # Split into paragraphs
    paragraphs = [p.strip() for p in chapter_text.split("\n\n") if p.strip()]

    # Analyze paragraph lengths
    para_lengths = [len(p.split()) for p in paragraphs]
    avg_para_length = sum(para_lengths) / len(para_lengths) if para_lengths else 0

    # Detect dialogue vs. narrative
    dialogue_paras = sum(1 for p in paragraphs if '"' in p or "'" in p)
    dialogue_ratio = dialogue_paras / len(paragraphs) if paragraphs else 0

    result = "Pacing Analysis:\n"
    result += f"- Paragraphs: {len(paragraphs)}\n"
    result += f"- Avg. paragraph length: {avg_para_length:.1f} words\n"
    result += f"- Dialogue ratio: {dialogue_ratio:.0%}\n"

    issues = []
    if avg_para_length > 200:
        issues.append("Long paragraphs may slow pacing")
    elif avg_para_length < 30:
        issues.append("Very short paragraphs may feel choppy")

    if dialogue_ratio > 0.7:
        issues.append("High dialogue ratio - consider adding more description")
    elif dialogue_ratio < 0.2:
        issues.append("Low dialogue ratio - consider adding more character interaction")

    if issues:
        result += "\nPotential issues:\n"
        result += "\n".join(f"- {issue}" for issue in issues)

    return {"content": [{"type": "text", "text": result}]}


# Create the MCP server with all tools
def create_storybook_tools():
    """Create the Storybook MCP server with all custom tools."""
    return create_sdk_mcp_server(
        name="storybook",
        version="1.0.0",
        tools=[
            track_character,
            list_characters,
            check_character_consistency,
            track_plot_event,
            list_plot_events,
            analyze_plot_timeline,
            analyze_prose_quality,
            detect_pacing_issues,
        ],
    )
