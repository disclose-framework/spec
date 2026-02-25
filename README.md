# Disclose Framework

**Open-source transparency infrastructure for agentic commerce.**

Disclose is an open standard that enables merchants to publish verified, machine-readable disclosures about their business practices — and enables AI agents to consume those disclosures when making or informing purchasing decisions on behalf of buyers.

---

## The Problem

AI agents are increasingly making purchasing decisions autonomously. They need to evaluate merchants — not just by price or product, but by operational behaviour: return rates, fulfillment reliability, refund speed, chargeback rates. Today, no standard exists for merchants to publish this data in a way agents can trust and consume.

Disclose solves this.

---

## How It Works

Disclose defines three participants:

- **Merchants** publish a structured disclosure document at `/.well-known/disclose` on their domain
- **Verifiers** — authorized third parties with access to source data — cryptographically attest to the accuracy of specific disclosures
- **Agents** query disclosure documents, verify attestations, and use the signals to inform purchasing decisions

Trust is not assigned by the framework. It emerges from visible, verifiable merchant behaviour.

---

## Core Principles

- **Merchant sovereignty** — participation is voluntary; merchants choose what to disclose
- **Selective disclosure** — no all-or-nothing requirement; start with one attribute, add more over time
- **No scores, no badges** — Disclose publishes facts; agents and buyers draw their own conclusions
- **Behavior-based signals** — every operational metric is grounded in recorded outcomes, not assertions

---

## Specification

| Document | Description |
|---|---|
| [Overview](specification/overview.md) | Full specification: schema, attributes, attestations, verifier registry, security, and versioning |

This is a **v0.1 draft**. The specification is open for review and comment.

---

## Status

This specification is in active development. We are currently seeking:

- **Verifier partners** — platforms with access to merchant operational data (returns, fulfillment, payments) interested in participating as authorized attestors
- **Agent platform partners** — AI agent developers interested in consuming Disclose signals
- **Feedback** — open an Issue with questions, corrections, or proposals

---

## Contributing

This is an open standard. Feedback, corrections, and proposals are welcome via [Issues](../../issues).

---

## License

This specification is published under the [Apache License 2.0](LICENSE).
