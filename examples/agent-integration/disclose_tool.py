"""
disclose_tool.py
----------------
Reference implementation of a `fetch_merchant_trust_signals` tool
for AI agent frameworks (LangChain, AutoGen, custom Claude agents).

Fetches and parses a Disclose Framework disclosure document from a
merchant's well-known endpoint, returning structured signals an LLM
can reason over.

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
        "Fetches machine-readable disclosure signals published by a merchant "
        "using the Disclose Framework (discloseframework.dev). "
        "Returns verified data on return rates, fulfillment performance, "
        "review signals, chargeback rates, and more. Use this before "
        "recommending a merchant or completing a purchase on a user's behalf."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "merchant_domain": {
                "type": "string",
                "description": (
                    "The merchant's root domain, e.g. 'acme.com'. "
                    "The tool will check /.well-known/disclose.json first, "
                    "falling back to /disclose.json at the domain root."
                ),
            },
            "signals": {
                "type": "array",
                "items": {"type": "string"},
                "description": (
                    "Optional list of specific signal keys to retrieve, e.g. "
                    "['disclose:product_return_rate', 'disclose:review_rating']. "
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
FALLBACK_PATH = "/disclose.json"
TIMEOUT_SECONDS = 5


@dataclass
class DiscloseSignals:
    """Parsed signals from a merchant's Disclose endpoint."""

    merchant_domain: str
    raw: dict = field(repr=False)
    attributes: dict = field(default_factory=dict)
    attestations: list = field(default_factory=list)
    error: Optional[str] = None

    def attested_by(self) -> list[str]:
        """Returns list of verifier names who have attested signals."""
        return [a.get("verifier_name", a.get("verifier_id", "Unknown"))
                for a in self.attestations]

    def is_attested(self, attribute_key: str) -> bool:
        """Returns True if the attribute has at least one valid attestation."""
        for attestation in self.attestations:
            if attribute_key in attestation.get("attested_attributes", []):
                return True
        return False

    def summary(self) -> str:
        """Human/LLM-readable summary of signals for prompt injection."""
        if self.error:
            return f"[Disclose] Could not retrieve signals for {self.merchant_domain}: {self.error}"

        lines = [f"[Disclose signals for {self.merchant_domain}]"]

        verifiers = self.attested_by()
        if verifiers:
            lines.append(f"  Attested by: {', '.join(verifiers)}")

        for key, value in self.attributes.items():
            # Skip _period_days companion fields from summary display
            if key.endswith("_period_days"):
                continue
            short_key = key.replace("disclose:", "")
            attested = " ✓" if self.is_attested(key) else ""
            lines.append(f"  {short_key}: {_format_value(short_key, value)}{attested}")

        if not self.attributes:
            lines.append("  No signals published.")

        return "\n".join(lines)

    def score(self) -> Optional[float]:
        """
        Simple composite score (0–1) for quick agent ranking.
        Weights are illustrative — agent developers should tune these.

        Returns None if insufficient data.
        """
        weights = {
            # (max_value, weight) — negative weight means lower is better
            "disclose:review_rating":        (5.0,   0.35),
            "disclose:product_return_rate":  (1.0,  -0.25),
            "disclose:chargeback_rate":      (1.0,  -0.20),
            "disclose:on_time_shipment_rate": (1.0,  0.20),
        }
        score = 0.0
        total_weight = 0.0
        for key, (max_val, w) in weights.items():
            val = self.attributes.get(key)
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
    Fetches Disclose signals from a merchant's disclosure endpoint.
    Checks /.well-known/disclose.json first, falls back to /disclose.json.

    Args:
        merchant_domain: Root domain of the merchant (e.g. 'acme.com').
        signals: Optional list of attribute keys to filter to.

    Returns:
        DiscloseSignals dataclass with parsed data.
    """
    domain = merchant_domain.rstrip("/").removeprefix("https://").removeprefix("http://")

    raw = None
    last_error = None

    for path in [WELL_KNOWN_PATH, FALLBACK_PATH]:
        url = f"https://{domain}{path}"
        try:
            req = urllib.request.Request(
                url,
                headers={
                    "Accept": "application/json",
                    "User-Agent": "DiscloseFrameworkAgent/0.2 (+https://discloseframework.dev)",
                },
            )
            with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS) as resp:
                raw = json.loads(resp.read().decode())
            break  # Success — stop trying paths
        except urllib.error.HTTPError as e:
            if e.code == 404:
                last_error = f"HTTP 404 at {path}"
                continue  # Try fallback path
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

    if raw is None:
        return DiscloseSignals(
            merchant_domain=domain, raw={},
            error=last_error or "Disclosure document not found at canonical or fallback path"
        )

    # Extract attributes from the flat disclose: namespace
    all_attributes = _extract_attributes(raw)

    filtered = (
        {k: v for k, v in all_attributes.items() if k in signals}
        if signals else all_attributes
    )

    return DiscloseSignals(
        merchant_domain=domain,
        raw=raw,
        attributes=filtered,
        attestations=raw.get("attestations", []),
    )


def _extract_attributes(raw: dict) -> dict:
    """Extract disclose: namespaced keys from a v0.2 disclosure document."""
    attributes = {}

    # v0.2 flat attributes object
    for k, v in raw.get("attributes", {}).items():
        if k.startswith("disclose:"):
            attributes[k] = v

    # Also support bare disclose: keys at root (JSON-LD format)
    for k, v in raw.items():
        if k.startswith("disclose:") and k not in attributes:
            attributes[k] = v

    # Support @graph nodes (JSON-LD multi-scope documents)
    for node in raw.get("@graph", []):
        if isinstance(node, dict):
            for k, v in node.items():
                if k.startswith("disclose:") and k not in attributes:
                    attributes[k] = v

    return attributes


def _format_value(key: str, value) -> str:
    """Format attribute values for human-readable summary output."""
    rate_keys = {
        "product_return_rate", "chargeback_rate", "dispute_win_rate",
        "on_time_shipment_rate", "delivered_on_time_rate", "order_accuracy_rate",
        "in_stock_rate", "inventory_accuracy_rate", "review_verified_purchase_rate",
        "first_contact_resolution_rate", "returnless_refund_rate",
    }
    if key in rate_keys:
        return f"{float(value)*100:.1f}%"
    if key == "review_rating":
        return f"{value}/5.0"
    if "days" in key:
        return f"{value} days"
    if "hours" in key:
        return f"{value} hrs"
    return str(value)


# ---------------------------------------------------------------------------
# LangChain integration (optional — only if langchain is installed)
# ---------------------------------------------------------------------------

try:
    from langchain.tools import BaseTool
    from pydantic import BaseModel, Field as PydanticField

    class _DiscloseInput(BaseModel):
        merchant_domain: str = PydanticField(..., description="Root domain of the merchant")
        signals: Optional[list[str]] = PydanticField(None, description="Attribute keys to filter")

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
        print(f"\n  Composite score: {score} / 1.0")
