# Disclose Framework

**Open-source transparency infrastructure for agentic commerce.**

Disclose is an open standard that enables merchants to publish verified, machine-readable disclosures about their business practices — and enables AI agents to consume those disclosures when making or informing purchasing decisions on behalf of buyers.

---

## The Problem

AI agents are increasingly acting as intermediaries between buyers and merchants — researching products, comparing options, and making purchasing recommendations autonomously. Before an agent can responsibly recommend where to buy, it needs to evaluate merchants on operational behaviour: not just price and product, but reliability, trustworthiness, and risk.

Today, no standard exists for merchants to publish this data in a way agents can trust and consume. Agents are flying blind on merchant quality. Disclose solves this.

---

## How It Works

Disclose defines three participants:

- **Merchants** publish a structured disclosure document at `/.well-known/disclose` on their own domain
- **Verifiers** — authorized third parties with access to source data — cryptographically attest to the accuracy of specific disclosures
- **Agents** query disclosure documents, verify attestations, and use the signals to inform purchasing decisions

The flow is asynchronous and cacheable. Merchants publish; verifiers attest; agents consume. No centralized authority. No real-time negotiation required.

Trust is not assigned by the framework. It emerges from visible, verifiable merchant behaviour.

---

## What Merchants Disclose

Disclose defines a standard attribute set covering the core dimensions an agent must evaluate before recommending a purchase:

| Signal Category | Example Attributes |
|-----------------|-------------------|
| **Product Quality** | Repeat purchase rate, product return rate |
| **Returns & Refunds** | Return policy type, refund processing time, exchange rate |
| **Fulfillment Reliability** | On-time shipment rate, order accuracy rate |
| **Financial Risk** | Chargeback rate |
| **Customer Support** | Support resolution time |
| **Pricing Integrity** | Average discount rate |
| **Subscriptions** | Churn rate, online cancellation availability |

Every metric is time-bounded, behavior-based, and grounded in recorded outcomes — not assertions. Merchants disclose what happened, not what they claim.

---

## Core Principles

- **Merchant sovereignty** — participation is voluntary; merchants choose what to disclose, which verifiers to authorize, and when disclosures are updated or removed
- **Selective disclosure** — no all-or-nothing requirement; start with one attribute and add more over time
- **No scores, no badges** — Disclose publishes facts; agents and buyers draw their own conclusions
- **Verifier-attested signals** — authorized third parties with access to source data cryptographically sign attestations, distinguishing verified disclosures from self-reported ones
- **Manipulation-resistant by design** — raw, time-bounded, verifier-attested metrics are far harder to game than scores or badges, which create targets

---

## Quick Start

A minimal disclosure document looks like this:

```json
{
  "disclose_version": "0.1",
  "merchant_domain": "merchant.example.com",
  "issued_at": "2026-02-24T00:00:00Z",
  "expires_at": "2026-05-24T00:00:00Z",
  "attributes": {
    "disclose:repeat_purchase_rate": 0.38,
    "disclose:repeat_purchase_rate_period_days": 90,
    "disclose:product_return_rate": 0.06,
    "disclose:product_return_rate_period_days": 90,
    "disclose:return_policy_type": "free",
    "disclose:return_window_days": 30,
    "disclose:on_time_shipment_rate": 0.97,
    "disclose:on_time_shipment_rate_period_days": 90,
    "disclose:chargeback_rate": 0.003,
    "disclose:chargeback_rate_period_days": 90
  }
}
```

Publish this at `/.well-known/disclose` on your domain. That's a valid Disclose implementation.

---

## Specification

| Document | Description |
|----------|-------------|
| [Specification]((https://github.com/disclose-framework/spec/blob/main/specification/overview.md) | Full specification: schema, attributes, attestations, verifier registry, governance, security, and versioning |

This is a v0.1 draft. The specification is open for review and comment.

---

## Status & Roadmap

This specification is in active development. Current priorities:

**Verifier partners** — Platforms with access to merchant operational data (returns processors, fulfillment providers, payment platforms) interested in becoming authorized attestors. Verifiers are listed in the public registry and cryptographically sign attestations for the attributes they are authorized to verify. [See the Verifier Registry governance process →](specification/overview.md#registry-governance)

**Agent platform partners** — AI agent developers and commerce platforms interested in consuming Disclose signals to inform purchasing recommendations.

**Feedback** — Open an Issue with questions, corrections, or proposals. This is an open standard and early input shapes the direction.

---

## Why Now

The shift to agentic commerce is happening faster than the trust infrastructure needed to support it. OpenAI, Google, Meta, and Anthropic are each building commerce layers into their agent platforms. The question of how agents evaluate merchant trustworthiness is unsolved and urgent. Disclose is designed to be the answer — vendor-neutral, open-source, and built for the infrastructure layer, not the application layer.

---

## Contributing

Feedback, corrections, and proposals are welcome via [Issues](../../issues). This is an open standard. The goal is broad adoption, not ownership.

---

## License

This specification is published under the [Apache License 2.0](LICENSE).
