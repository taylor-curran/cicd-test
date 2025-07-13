#!/usr/bin/env python3
"""
Automated code review using Claude Code SDK.
Reviews code changes against best practices guidelines.
"""

import anyio
from claude_code_sdk import query, ClaudeCodeOptions, Message


async def main():
    """Run automated code review against best practices."""
    print("🔍 Starting automated code review...")
    
    # Store messages from the conversation
    messages: list[Message] = []
    
    # Code review query - check diff against best practices
    review_prompt = """
    Check if new code in diff adheres to guidelines in /best_practices directory.
    
    ONLY assess against /best_practices guidelines. Do not suggest improvements outside of those guidelines.
    
    Provide concise assessment of compliance and violations found.
    """
    
    async for message in query(
        prompt=review_prompt,
        options=ClaudeCodeOptions(
            max_turns=20,  # Increase further to ensure complete analysis
            cwd=".",
            # Only allow reading tools - no code changes
            allowed_tools=["Read", "Grep", "Glob"],
            # Use cheaper model for code review
            model="claude-sonnet-4-20250514",
            # Add system prompt to reinforce no-code-changes behavior
            system_prompt="Code reviewer. Only assess against /best_practices directory guidelines. No code changes."
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


if __name__ == "__main__":
    anyio.run(main)