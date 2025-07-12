#!/usr/bin/env python3
"""
Simple Claude Code SDK interaction example.
This demonstrates basic usage of the claude-code-sdk Python package.
"""

import anyio
from claude_code_sdk import query, ClaudeCodeOptions, Message


async def main():
    """Main function demonstrating Claude Code SDK usage."""
    print("Starting Claude Code SDK interaction...")
    
    # Store messages from the conversation
    messages: list[Message] = []
    
    # Code review query - check diff against best practices
    review_prompt = """
    Check if new code in diff adheres to best_practices/CLAUDE.md
    
    Provide an objective, concise assessment and suggestions for improvements to be more aligned with rules.
    
    DO NOT provide code changes - only analysis and recommendations.
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
            system_prompt="You are a code reviewer. Analyze and suggest improvements but never write or modify code."
        )
    ):
        messages.append(message)
        
        message_type = type(message).__name__
        print(f"Received: {message_type}")
        
        # Show authentication details from SystemMessage
        if message_type == 'SystemMessage':
            if hasattr(message, 'data'):
                data = message.data
                print(f"  API Key Source: {data.get('apiKeySource', 'unknown')}")
                print(f"  Model: {data.get('model', 'unknown')}")
                print(f"  Session ID: {data.get('session_id', 'unknown')}")
        
        # Show assistant responses
        elif message_type == 'AssistantMessage':
            if hasattr(message, 'content') and message.content:
                # Extract text from the content
                text_parts = []
                for content_item in message.content:
                    if hasattr(content_item, 'text'):
                        text_parts.append(content_item.text)
                if text_parts:
                    print(f"  Assistant: {text_parts[0][:200]}...")
        
        # Show final result
        elif message_type == 'ResultMessage':
            print(f"  Cost: ${message.total_cost_usd:.4f}")
            print(f"  Duration: {message.duration_ms}ms")
            print(f"  Turns: {message.num_turns}")
            if hasattr(message, 'result') and message.result:
                print(f"  Final result: {message.result[:200]}...")
            else:
                print("  No final result returned")
    
    print(f"\nConversation completed with {len(messages)} messages")
    
    # Extract the actual review from assistant messages
    print("\n" + "="*50)
    print("🔍 CODE REVIEW ASSESSMENT")
    print("="*50)
    
    review_found = False
    for message in messages:
        if type(message).__name__ == 'AssistantMessage':
            if hasattr(message, 'content') and message.content:
                # Extract text from the content
                text_parts = []
                for content_item in message.content:
                    if hasattr(content_item, 'text'):
                        text_parts.append(content_item.text)
                if text_parts:
                    review_found = True
                    full_text = "\n".join(text_parts)
                    print(full_text)
                    print("-" * 30)
    
    if not review_found:
        print("⚠️  No review content found")
    
    print("="*50)


if __name__ == "__main__":
    anyio.run(main)