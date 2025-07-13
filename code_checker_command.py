#!/usr/bin/env python3
"""
Command-line wrapper for automated code review.
This script can be invoked via Claude Code slash commands.
"""

import anyio
from claude_code_sdk import query, ClaudeCodeOptions, Message


async def run_code_review():
    """Run automated code review using slash command."""
    print("🔍 Starting automated code review...")
    
    # Store messages from the conversation
    messages: list[Message] = []
    
    # Simple call to the slash command
    review_prompt = "/code-review"
    
    async for message in query(
        prompt=review_prompt,
        options=ClaudeCodeOptions(
            max_turns=20,
            cwd=".",
            # Only allow reading tools - no code changes
            allowed_tools=["Read", "Grep", "Glob", "Bash(git*)"],
            # Use appropriate model for code review
            model="claude-sonnet-4-20250514",
            # Add system prompt to reinforce review-only behavior
            system_prompt="Code reviewer. Only assess against /best_practices directory guidelines. No code changes. Use git commands to analyze diffs when needed."
        )
    ):
        messages.append(message)
        
        # Show final metrics
        message_type = type(message).__name__
        if message_type == 'ResultMessage':
            print(f"✅ Review completed: ${message.total_cost_usd:.4f} | {message.duration_ms}ms | {message.num_turns} turns")
    
    # Extract and display review assessment
    print("\n" + "="*60)
    print("📋 CODE REVIEW ASSESSMENT")
    print("="*60)
    
    review_found = False
    for message in messages:
        if type(message).__name__ == 'AssistantMessage':
            if hasattr(message, 'content') and message.content:
                text_parts = []
                for content_item in message.content:
                    if hasattr(content_item, 'text'):
                        text_parts.append(content_item.text)
                if text_parts:
                    review_found = True
                    full_text = "\n".join(text_parts)
                    print(full_text)
                    print("-" * 40)
    
    if not review_found:
        print("⚠️  No review content found")
    
    print("="*60)


def main():
    """Main entry point for GitHub Actions pipeline."""
    print("🔄 Running code review via slash command...")
    anyio.run(run_code_review())


if __name__ == "__main__":
    main()