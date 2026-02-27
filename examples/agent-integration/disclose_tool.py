"""
disclose_tool.py
----------------
Reference implementation of a `fetch_merchant_trust_signals` tool
for AI agent frameworks (LangChain, AutoGen, custom Claude agents).

Fetches and parses Disclose Framework JSON-LD from a merchant's
well-known endpoint, returning structured signals an LLM can reason over.

Usage with LangChain:
    from disclose_tool import DiscloseSignalsTool
    tools = [DiscloseSignalsTool()]

Usage with raw Anthropic API (tool_use):
    See TOOL_SCHEMA below — pass as an entry in `tools=[...]`
"""

import json
import urllib.request
import urllib.error
from dataclasses import dataclass, field
from typing import Optional

# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------

TOOL_SCHEMA = {
    "name": "fetch_merchant_trust_signals",
    "description": (
        "Fetches machine-readable trust signals published by a merchant "
        "using the Disclose Framework (discloseframework.dev). "
        "Returns verified data on return rates, fulfillment time, review "
        "ratings, and dispute rates. Use this before recommending a merchant "
        "or completing a purchase on a user's behalf."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "merchant_domain": {
                "type": "string",
                "description": (
                    "The merchant's root domain, e.g. 'acme.com'. "
                    "The tool will look up /.well-known/disclose.json automatically."
                ),
            },
            "signals": {
                "type": "array",
                "items": {"type": "string"},
                "description": (
                    "Optional list of specific signal keys to retrieve, e.g. "
                    "['disclose:return_rate', 'disclose:review_rating']. "
                    "If omitted, all available signals are returned."
                ),
            },
        },
        "required": ["merchant_domain"],
    },
}


# ---------------------------------------------------------------------------
# Core fetch logic
# ---------------------------------------------------------------------------

WELL_KNOWN_PATH = "/.well-known/disclose.json"
TIMEOUT_SECONDS = 5


@dataclass
class DiscloseSignals:
    """Parsed signals from a merchant's Disclose endpoint."""

    merchant_domain: str
    raw: dict = field(repr=False)
    signals: dict = field(default_factory=dict)
    verifier: Optional[str] = None
    verified_at: Optional[str] = None
    error: Optional[str] = None

    def summary(self) -> str:
        """Human/LLM-readable summary of signals for prompt injection."""
        if self.error:
            return f"[Disclose] Could not retrieve signals for {self.merchant_domain}: {self.error}"

        lines = [f"[Disclose signals for {self.merchant_domain}]"]
        if self.verifier:
            lines.append(f"  Verified by: {self.verifier} at {self.verified_at or 'unknown time'}")
        for key, value in self.signals.items():
            short_key = key.replace("disclose:", "")
            lines.append(f"  {short_key}: {_format_value(short_key, value)}")
        if not self.signals:
            lines.append("  No signals published.")
        return "\n".join(lines)

    def score(self) -> Optional[float]:
        """
        Simple composite score (0–1) for quick agent ranking.
        Weights are illustrative — agent developers should tune these.

        Returns None if insufficient data.
        """
        weights = {
            "disclose:review_rating": (5.0, 0.35),   # (max_value, weight)
            "disclose:return_rate":   (1.0, -0.25),  # negative: lower is better
            "disclose:dispute_rate":  (1.0, -0.20),  # negative
            "disclose:fulfillment_days_p50": (30.0, -0.20),  # negative
        }
        score = 0.0
        total_weight = 0.0
        for key, (max_val, w) in weights.items():
            val = self.signals.get(key)
            if val is None:
                continue
            normalized = float(val) / max_val
            if w < 0:
                # Invert: lower value → higher score contribution
                score += abs(w) * (1 - normalized)
            else:
                score += w * normalized
            total_weight += abs(w)

        return round(score / total_weight, 3) if total_weight > 0 else None


def fetch_signals(
    merchant_domain: str,
    signals: Optional[list[str]] = None,
) -> DiscloseSignals:
    """
    Fetches Disclose signals from a merchant's well-known endpoint.

    Args:
        merchant_domain: Root domain of the merchant (e.g. 'acme.com').
        signals: Optional list of signal keys to filter to.

    Returns:
        DiscloseSignals dataclass with parsed data.
    """
    domain = merchant_domain.rstrip("/").removeprefix("https://").removeprefix("http://")
    url = f"https://{domain}{WELL_KNOWN_PATH}"

    try:
        req = urllib.request.Request(
            url,
            headers={
                "Accept": "application/ld+json, application/json",
                "User-Agent": "DiscloseFrameworkAgent/0.1 (+https://discloseframework.dev)",
            },
        )
        with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS) as resp:
            raw = json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return DiscloseSignals(
            merchant_domain=domain, raw={},
            error=f"HTTP {e.code}: merchant may not support Disclose Framework"
        )
    except urllib.error.URLError as e:
        return DiscloseSignals(merchant_domain=domain, raw={}, error=str(e.reason))
    except json.JSONDecodeError:
        return DiscloseSignals(merchant_domain=domain, raw={}, error="Invalid JSON at endpoint")
    except Exception as e:
        return DiscloseSignals(merchant_domain=domain, raw={}, error=str(e))

    # Parse signals — support both flat namespace and nested @graph format
    all_signals = _extract_signals(raw)

    filtered = (
        {k: v for k, v in all_signals.items() if k in signals}
        if signals else all_signals
    )

    return DiscloseSignals(
        merchant_domain=domain,
        raw=raw,
        signals=filtered,
        verifier=raw.get("disclose:verifier", {}).get("@id") or raw.get("disclose:verifier"),
        verified_at=raw.get("disclose:verified_at"),
    )


def _extract_signals(raw: dict) -> dict:
    """Extract disclose: namespaced keys from raw JSON-LD."""
    signals = {}
    # Direct namespace keys at root
    for k, v in raw.items():
        if k.startswith("disclose:"):
            signals[k] = v
    # Nested under @graph
    for node in raw.get("@graph", []):
        if isinstance(node, dict):
            for k, v in node.items():
                if k.startswith("disclose:"):
                    signals[k] = v
    return signals


def _format_value(key: str, value) -> str:
    if key == "return_rate":
        return f"{float(value)*100:.1f}%"
    if key == "dispute_rate":
        return f"{float(value)*100:.2f}%"
    if key == "review_rating":
        return f"{value}/5.0"
    if "days" in key:
        return f"{value} days"
    return str(value)


# ---------------------------------------------------------------------------
# LangChain integration (optional — only if langchain is installed)
# ---------------------------------------------------------------------------

try:
    from langchain.tools import BaseTool
    from pydantic import BaseModel, Field as PydanticField

    class _DiscloseInput(BaseModel):
        merchant_domain: str = PydanticField(..., description="Root domain of the merchant")
        signals: Optional[list[str]] = PydanticField(None, description="Signal keys to filter")

    class DiscloseSignalsTool(BaseTool):
        name = "fetch_merchant_trust_signals"
        description = TOOL_SCHEMA["description"]
        args_schema = _DiscloseInput

        def _run(self, merchant_domain: str, signals: Optional[list[str]] = None) -> str:
            result = fetch_signals(merchant_domain, signals)
            return result.summary()

        async def _arun(self, *args, **kwargs):
            raise NotImplementedError("Use async fetch wrapper if needed")

except ImportError:
    pass  # LangChain not installed — that's fine


# ---------------------------------------------------------------------------
# Anthropic tool_use handler
# ---------------------------------------------------------------------------

def handle_tool_call(tool_name: str, tool_input: dict) -> str:
    """
    Drop-in handler for Anthropic API tool_use blocks.

    Example:
        if block.type == "tool_use" and block.name == "fetch_merchant_trust_signals":
            result = handle_tool_call(block.name, block.input)
            # Return as tool_result in next messages turn
    """
    if tool_name != "fetch_merchant_trust_signals":
        return f"Unknown tool: {tool_name}"
    result = fetch_signals(
        merchant_domain=tool_input["merchant_domain"],
        signals=tool_input.get("signals"),
    )
    return result.summary()


# ---------------------------------------------------------------------------
# CLI demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys

    domain = sys.argv[1] if len(sys.argv) > 1 else "example-merchant.com"
    print(f"Fetching Disclose signals for: {domain}\n")
    result = fetch_signals(domain)
    print(result.summary())
    score = result.score()
    if score is not None:
        print(f"\n  Composite trust score: {score} / 1.0")
