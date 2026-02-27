"""
example_agent.py
----------------
Shows how to wire fetch_merchant_trust_signals into a Claude-powered
shopping agent using the Anthropic API tool_use pattern.

This is the reference integration pattern agent developers should follow.
"""

import anthropic
from disclose_tool import TOOL_SCHEMA, handle_tool_call

client = anthropic.Anthropic()
MODEL = "claude-opus-4-6"

SYSTEM_PROMPT = """You are a shopping agent helping users make purchases.

Before recommending a merchant or completing any purchase, you MUST call
fetch_merchant_trust_signals to retrieve that merchant's published Disclose
Framework data. Use the signals to:

- Prefer merchants with review_rating >= 4.0
- Warn the user if return_rate > 0.15 (15%)
- Flag merchants with dispute_rate > 0.02 (2%)
- Factor fulfillment_days_p50 into delivery expectations

If a merchant has no Disclose signals, note this and recommend with lower
confidence. Never fabricate signals.
"""


def run_shopping_agent(user_message: str):
    messages = [{"role": "user", "content": user_message}]

    while True:
        response = client.messages.create(
            model=MODEL,
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            tools=[TOOL_SCHEMA],
            messages=messages,
        )

        # Collect text output
        for block in response.content:
            if hasattr(block, "text"):
                print(f"Agent: {block.text}")

        # Check if we're done
        if response.stop_reason == "end_turn":
            break

        # Handle tool calls
        if response.stop_reason == "tool_use":
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    print(f"\n[Fetching Disclose signals for: {block.input.get('merchant_domain')}]")
                    result = handle_tool_call(block.name, block.input)
                    print(result)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result,
                    })

            # Append assistant turn + tool results
            messages.append({"role": "assistant", "content": response.content})
            messages.append({"role": "user", "content": tool_results})
        else:
            break


if __name__ == "__main__":
    run_shopping_agent(
        "I want to buy a standing desk. I've found two options: "
        "one from upliftdesk.com and one from fully.com. "
        "Which merchant should I trust more?"
    )
