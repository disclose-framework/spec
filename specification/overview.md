# Disclose Framework — Official Specification

## Overview

The Disclose Framework is an open standard for merchant disclosure attestations designed for the emerging era of agentic commerce. As AI agents increasingly act as intermediaries between buyers and merchants — researching products, comparing options, and making or informing purchasing recommendations — they require structured, machine-readable, and verifiable information about merchant practices before they can responsibly recommend where to buy.

Disclose provides that infrastructure layer. It enables AI agents, platforms, and automated systems to access verified, machine-readable information about merchant practices — including return policies, fulfillment performance, review authenticity, and other behavioural signals — when making or informing purchasing decisions on behalf of buyers.

Disclose operates as a disclosure layer that sits above the transaction. Before an agent decides where to buy, Disclose provides the structured signal data needed to make a trustworthy recommendation. It does not process payments, manage checkout sessions, or execute transactions. Its sole function is to standardize how merchants publish verified disclosures and how agents consume them.

---

## Overarching Guidelines

The key words MUST, MUST NOT, REQUIRED, SHALL, SHALL NOT, SHOULD, SHOULD NOT, RECOMMENDED, MAY, and OPTIONAL in this document are to be interpreted as described in RFC 2119 and RFC 8174.

Schema notes:

- **Date format:** Always specified as RFC 3339 unless otherwise specified.
- **Numeric values:** Expressed as decimals unless otherwise noted (e.g., 0.92 for 92%).
- **Rates and ratios:** Always expressed as a decimal between 0 and 1 (e.g., 0.06 for 6%).
- **Time-bounded metrics:** MUST include a `_period_days` companion field declaring the observation window. The default observation window is 90 days unless otherwise specified.
- **Measurement methodology:** Where a metric's value depends on how it is computed (e.g., whether exchanges are counted as returns, or whether return rate is measured by units or orders), the attesting Verifier's methodology governs. Agents SHOULD consider the Verifier's stated methodology when interpreting attested values, particularly for attributes where platform definitions vary.

---

## Design Philosophy

### Trust Is Emergent, Not Engineered

The Disclose Framework does not produce trust scores, badges, tiers, or rankings. It produces structured, verifiable facts about merchant behaviour. Trust emerges from those facts as agents and buyers draw their own conclusions.

This is a deliberate architectural choice with three consequences:

**Merchants disclose behaviour, not claims.** Every attribute in the Disclose schema is grounded in operational outcomes — repeat purchases, return rates, fulfillment accuracy, chargeback rates. These are things that happened, not assertions about quality or intent.

**The framework enforces structure, not interpretation.** Disclose defines what attributes mean, how they are measured, and how they are verified. It does not define how agents should weight them, combine them, or surface them to buyers. That discretion belongs to the platform.

**No centralized authority renders verdicts.** There is no "Disclose Score." There is no tier that grants a badge. A merchant that publishes a low return rate, high on-time shipment rate, and fast refund processing becomes intuitively trustworthy — not because a framework said so, but because the evidence is visible and verifiable.

This philosophy also protects against gaming. Scores and badges create targets. Raw, time-bounded, verifier-attested metrics are far harder to manipulate without changing actual operations.

### Self-Reported Attribute Integrity

Merchants MAY publish disclosures without attestations. Self-reported attributes carry no third-party verification and agents SHOULD treat them accordingly. The framework does not currently define a formal dispute process for false self-reported disclosures; however, platforms consuming Disclose data MAY implement their own policies for flagging or deprioritizing merchants whose self-reported attributes are demonstrably inconsistent with other observable signals. A future extension to this specification will define a community-based flagging and review process.

---

## Core Concepts

### The Three-Party Model

Disclose defines three participants:

| Participant | Role |
|-------------|------|
| Merchant | Publishes disclosure data about their own practices under their own domain |
| Verifier | An authorized third party that attests to the accuracy of specific merchant disclosures using cryptographic signatures |
| Agent | A platform, AI assistant, or automated system that queries and consumes disclosure data on behalf of a buyer |

Unlike transaction protocols, Disclose does not require real-time negotiation between parties. Merchants publish; verifiers attest; agents consume. The flow is asynchronous and cacheable.

### Merchant Sovereignty

A core principle of the Disclose Framework is that merchants retain full sovereignty over their disclosures. Participation is voluntary. Merchants choose which attributes to disclose, which verifiers to authorize, and when disclosures are updated or removed. The framework standardizes the format and verification mechanism — not the content or extent of disclosure.

### Selective Disclosure

There is no all-or-nothing requirement. A merchant may publish a single attribute and add additional attributes over time as their business matures or as competitive incentives emerge. This progressive enhancement model lowers the barrier to participation while preserving the integrity of the standard.

### Commerce Risk Coverage

The standard attribute set is designed to address the core risks an agent must evaluate before recommending a purchase:

| Risk Dimension | Covered By |
|----------------|------------|
| Product Quality | Repeat purchase rate, product return rate |
| Delivery Reliability | On-time shipment rate, order accuracy rate |
| Financial Risk | Refund processing time, chargeback rate |
| Service Reliability | Customer support resolution time |
| Demand Authenticity | Search-to-conversion rate |
| Pricing Integrity | Average discount rate |
| Long-term Value | Subscription churn rate |

No single dimension dominates. Agents weight these signals according to their own risk models and buyer context.

---

## Discovery

### Publication Endpoint

Merchants publish their disclosure document at a well-known URI:

```
/.well-known/disclose
```

This endpoint MUST return a valid JSON document conforming to the Disclose schema. The endpoint SHOULD support HTTP caching via standard `Cache-Control` headers.

Example request:

```
GET /.well-known/disclose HTTP/1.1
Host: merchant.example.com
Accept: application/json
```

### Discovery by Agents

Agents MAY fetch the disclosure document before, during, or after capability negotiation with a merchant's commerce infrastructure. Agents SHOULD cache disclosure documents according to HTTP cache-control directives.

Agents MUST NOT require a disclosure document to be present in order to complete a transaction. The absence of a disclosure document is itself a signal; agents MAY surface this to buyers or use it in ranking logic.

---

## Disclosure Document Structure

### Top-Level Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `disclose_version` | string | Yes | Specification version (e.g., `"0.1"`) |
| `merchant_domain` | string | Yes | The canonical domain of the merchant (e.g., `"merchant.example.com"`) |
| `issued_at` | string | Yes | RFC 3339 timestamp of when this document was generated |
| `expires_at` | string | No | RFC 3339 timestamp after which agents SHOULD re-fetch |
| `attributes` | object | Yes | Flat key-value map of disclosed merchant attributes |
| `attestations` | array | No | Array of verifier attestation objects |

### Attribute Namespace

All disclosure attributes exist in the `disclose:` namespace as flat properties. There are no nested categories or composite objects. This design prioritizes agent parsability over human organizational preference, and is consistent with the framework's principle that each metric stand alone.

Each time-bounded metric MUST be accompanied by a corresponding `_period_days` attribute declaring the observation window used to compute it.

Example `attributes` object:

```json
{
  "disclose:repeat_purchase_rate": 0.38,
  "disclose:repeat_purchase_rate_period_days": 90,
  "disclose:product_return_rate": 0.06,
  "disclose:product_return_rate_period_days": 90,
  "disclose:refund_processing_time_median_days": 3.2,
  "disclose:refund_processing_time_p90_days": 6.1,
  "disclose:on_time_shipment_rate": 0.97,
  "disclose:on_time_shipment_rate_period_days": 90,
  "disclose:order_accuracy_rate": 0.991,
  "disclose:order_accuracy_rate_period_days": 90,
  "disclose:chargeback_rate": 0.003,
  "disclose:chargeback_rate_period_days": 90,
  "disclose:support_resolution_time_median_hours": 4.2,
  "disclose:support_resolution_time_p90_hours": 22.0,
  "disclose:search_to_conversion_rate": 0.047,
  "disclose:average_discount_rate": 0.12,
  "disclose:average_discount_rate_period_days": 90,
  "disclose:subscription_churn_rate": 0.04,
  "disclose:subscription_churn_rate_period_days": 30,
  "disclose:return_policy_type": "free",
  "disclose:return_window_days": 30,
  "disclose:subscription_cancel_online": true,
  "disclose:sustainability_certified": true,
  "disclose:sustainability_certifier": "B Corp"
}
```

Agents MUST ignore unknown attributes without error. Merchants MAY include attributes not yet defined in the core specification using their own `disclose:{merchant-domain}:` prefix.

---

## Standard Attributes

The following attributes are defined in this version of the specification. All are optional unless noted. Time-bounded metrics default to a 90-day observation window unless the corresponding `_period_days` attribute specifies otherwise.

### Product Quality

| Attribute | Type | Description |
|-----------|------|-------------|
| `disclose:repeat_purchase_rate` | decimal | Rate of buyers who make a second purchase within the observation window (0–1) |
| `disclose:repeat_purchase_rate_period_days` | integer | Observation window in days (default: 90) |
| `disclose:product_return_rate` | decimal | Rate of units returned across all orders (0–1). Measured as returned units divided by shipped units. May be disclosed at SKU or category level. See measurement note below. |
| `disclose:product_return_rate_period_days` | integer | Observation window in days (default: 90) |

> **Measurement note:** Return rate is measured as returned units divided by total shipped units within the observation window. Exchanges (where the buyer selects a replacement item) are NOT counted as returns in this metric. Returnless refunds where no item is physically returned ARE counted. Where a Verifier attests this attribute, the Verifier's methodology governs and agents SHOULD consult the Verifier's published methodology documentation for definitional details.

### Returns & Refunds

| Attribute | Type | Description |
|-----------|------|-------------|
| `disclose:return_policy_type` | string | One of: `free`, `label_fee`, `buyer_pays`, `no_returns` |
| `disclose:return_window_days` | integer | Number of days a buyer has to initiate a return |
| `disclose:refund_processing_time_median_days` | decimal | Median business days from warehouse receipt of returned item to refund completion. The clock starts when the returned item is received at the merchant's designated return facility, not at return initiation or carrier pickup. |
| `disclose:refund_processing_time_p90_days` | decimal | 90th percentile business days from warehouse receipt to refund completion (same clock-start as median) |
| `disclose:exchange_rate` | decimal | Rate of return transactions where the buyer selected a replacement item rather than a refund (0–1). A higher exchange rate signals product confidence and buyer intent to remain a customer. |
| `disclose:exchange_rate_period_days` | integer | Observation window in days (default: 90) |

### Fulfillment — Shipment Reliability

| Attribute | Type | Description |
|-----------|------|-------------|
| `disclose:on_time_shipment_rate` | decimal | Rate of orders shipped within the merchant's stated fulfillment window (0–1) |
| `disclose:on_time_shipment_rate_period_days` | integer | Observation window in days (default: 90) |
| `disclose:shipment_delay_median_hours` | decimal | Median hours by which late shipments missed the promised window |
| `disclose:shipment_delay_p90_hours` | decimal | 90th percentile hours by which late shipments missed the promised window |

### Fulfillment — Order Accuracy

| Attribute | Type | Description |
|-----------|------|-------------|
| `disclose:order_accuracy_rate` | decimal | Rate of orders fulfilled without incorrect or damaged items (0–1) |
| `disclose:order_accuracy_rate_period_days` | integer | Observation window in days (default: 90) |
| `disclose:incorrect_item_rate` | decimal | Rate of orders containing a wrong item (0–1) |
| `disclose:damaged_item_rate` | decimal | Rate of orders containing a damaged item at delivery (0–1) |

### Financial Risk

| Attribute | Type | Description |
|-----------|------|-------------|
| `disclose:chargeback_rate` | decimal | Chargebacks as a proportion of total transactions (0–1) |
| `disclose:chargeback_rate_period_days` | integer | Observation window in days (default: 90) |

### Customer Support

| Attribute | Type | Description |
|-----------|------|-------------|
| `disclose:support_resolution_time_median_hours` | decimal | Median hours from support contact to resolution |
| `disclose:support_resolution_time_p90_hours` | decimal | 90th percentile hours from support contact to resolution |

### Demand Authenticity

| Attribute | Type | Description |
|-----------|------|-------------|
| `disclose:search_to_conversion_rate` | decimal | Rate of product page visits that result in a completed purchase (0–1) |

### Pricing Integrity

| Attribute | Type | Description |
|-----------|------|-------------|
| `disclose:average_discount_rate` | decimal | Average discount applied across completed transactions as a proportion of list price (0–1) |
| `disclose:average_discount_rate_period_days` | integer | Observation window in days (default: 90) |

### Subscriptions

| Attribute | Type | Description |
|-----------|------|-------------|
| `disclose:subscription_churn_rate` | decimal | Rate of active subscriptions cancelled within the observation window (0–1) |
| `disclose:subscription_churn_rate_period_days` | integer | Observation window in days (default: 30) |
| `disclose:subscription_cancel_online` | boolean | Whether subscriptions can be cancelled without contacting support |
| `disclose:subscription_pause_available` | boolean | Whether subscriptions can be paused |
| `disclose:subscription_trial_days` | integer | Free trial duration in days, if offered |

### Sustainability & Ethics

| Attribute | Type | Description |
|-----------|------|-------------|
| `disclose:sustainability_certified` | boolean | Whether merchant holds a recognized sustainability certification |
| `disclose:sustainability_certifier` | string | Name of certifying body, if applicable |
| `disclose:ethical_sourcing_certified` | boolean | Whether merchant holds a recognized ethical sourcing certification |

### Subjective & Qualitative Signals

The attributes in this section differ in kind from the operational metrics above. They are human-assessed rather than operationally derived — aggregated judgments rather than recorded outcomes. They are included in the Disclose schema because they carry recognized signal value and agents are likely to encounter them. However, they are more susceptible to manipulation than behavioral metrics, and their meaning is platform- and context-dependent in ways that operational data is not.

Agents SHOULD weight these attributes with appropriate caution and SHOULD consider them in combination with operational signals rather than in isolation. A high review rating accompanied by a low `disclose:review_verified_purchase_rate` carries materially less evidential weight than the rating alone would suggest.

Review recency is a critical dimension of review signal quality. A merchant with 10,000 lifetime reviews but minimal recent review activity has a materially different trust profile than a merchant with comparable volume but active recent engagement. Agents SHOULD weight `disclose:review_recency_90d_rate` and `disclose:review_recency_365d_rate` when interpreting `disclose:review_rating`, and SHOULD surface review recency context to buyers where relevant.

| Attribute | Type | Description |
|-----------|------|-------------|
| `disclose:review_rating` | decimal | Aggregate review score on a 0–5 scale |
| `disclose:review_count` | integer | Total number of reviews included in the aggregate rating |
| `disclose:review_verified_purchase_rate` | decimal | Proportion of reviews attributed to verified purchases (0–1). The most manipulation-resistant of the review signals. |
| `disclose:review_recency_90d_rate` | decimal | Proportion of total reviews submitted within the last 90 days (0–1). Signals active and ongoing customer engagement. |
| `disclose:review_recency_365d_rate` | decimal | Proportion of total reviews submitted within the last 365 days (0–1). Provides a longer-horizon view of review activity relative to lifetime review volume. |

---

## Attestations

### Purpose

An attestation is a cryptographically signed statement from an authorized Verifier confirming that one or more disclosed attributes have been independently verified against source data. Attestations distinguish Disclose from self-reported trust signals that can be easily manipulated.

Merchants MAY publish disclosures without attestations. Unattested attributes are self-reported and agents SHOULD treat them accordingly. Attested attributes carry the reputational weight of the signing Verifier.

### Attestation Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `verifier_id` | string | Yes | Unique identifier for the Verifier (e.g., `"loop-returns.com"`) |
| `verifier_name` | string | Yes | Human-readable name of the Verifier |
| `attested_attributes` | array of strings | Yes | List of `disclose:` attribute keys this attestation covers |
| `attested_at` | string | Yes | RFC 3339 timestamp of when the attestation was issued |
| `expires_at` | string | No | RFC 3339 timestamp after which the attestation should no longer be trusted |
| `signature` | string | Yes | Base64url-encoded cryptographic signature over the attestation payload |
| `signing_key_id` | string | Yes | Key ID (`kid`) corresponding to the Verifier's published signing key |

Example attestation:

```json
{
  "verifier_id": "loop-returns.com",
  "verifier_name": "Loop Returns",
  "attested_attributes": [
    "disclose:product_return_rate",
    "disclose:product_return_rate_period_days",
    "disclose:return_policy_type",
    "disclose:return_window_days",
    "disclose:refund_processing_time_median_days",
    "disclose:refund_processing_time_p90_days",
    "disclose:exchange_rate",
    "disclose:exchange_rate_period_days"
  ],
  "attested_at": "2026-02-01T00:00:00Z",
  "expires_at": "2026-08-01T00:00:00Z",
  "signature": "eyJhbGciOiJFUzI1NiIsImtpZCI6Imxvb3AtMjAyNiJ9...",
  "signing_key_id": "loop-2026"
}
```

### Attestation Payload

The payload signed by the Verifier is a canonical JSON object containing:

```json
{
  "merchant_domain": "merchant.example.com",
  "verifier_id": "loop-returns.com",
  "attested_attributes": { "..." },
  "attested_at": "2026-02-01T00:00:00Z",
  "expires_at": "2026-08-01T00:00:00Z"
}
```

The `attested_attributes` object in the payload contains the actual attribute values at the time of attestation, not just the keys. This prevents merchants from changing attribute values after attestation without invalidating the signature.

### Signature Algorithm

Verifiers MUST sign attestation payloads using ES256 (ECDSA with P-256 and SHA-256). Verifiers MUST publish their signing keys as JWK (JSON Web Key) objects at:

```
/.well-known/disclose-verifier
```

---

## Verifier Registry

### Purpose

The Verifier Registry is the canonical list of authorized Disclose Verifiers. Its existence ensures that an attested disclosure carries meaningful weight — any party claiming to be a Verifier must be publicly listed, with their signing keys published and auditable.

### Registry Discovery

The Verifier Registry is published and maintained by the Disclose Framework governing body at:

```
https://discloseframework.dev/registry/verifiers.json
```

Agents SHOULD cache this registry and refresh it periodically. Agents MUST validate that the `verifier_id` in any attestation appears in the current registry before treating the attestation as trusted.

### Verifier Listing

Each entry in the Verifier Registry includes:

| Field | Type | Description |
|-------|------|-------------|
| `verifier_id` | string | Unique identifier (matches the verifier's domain) |
| `verifier_name` | string | Human-readable name |
| `verifiable_attributes` | array of strings | The `disclose:` attributes this Verifier is authorized to attest |
| `keys_url` | string | URL to the Verifier's `/.well-known/disclose-verifier` endpoint |
| `status` | string | One of: `active`, `suspended`, `revoked` |
| `listed_at` | string | RFC 3339 timestamp of when the Verifier was added to the registry |

### Registry Governance

The Verifier Registry is governed by the Disclose Framework governing body. The following process applies to all registry changes:

**Application.** Any organization seeking Verifier status MUST submit an application to the governing body via [GitHub Issues](https://github.com/disclose-framework/spec/issues) until the formal application process is established at `https://discloseframework.dev/registry/apply`. Applications must include: the applicant's domain, the `disclose:` attributes they seek authorization to attest, a description of their data access and verification methodology for each attribute, and their proposed signing key endpoint.

**Review.** The governing body will review applications for methodology soundness, data access credibility, and potential conflicts of interest. Review outcomes are published publicly.

**Listing.** Approved Verifiers are added to the registry with `status: active`. The governing body assigns the scope of `verifiable_attributes` based on the approved methodology. Verifiers MAY NOT attest attributes outside their approved scope.

**Suspension and Revocation.** The governing body MAY suspend a Verifier (setting `status: suspended`) pending investigation of a methodology concern, or revoke a Verifier (setting `status: revoked`) for material misrepresentation, methodology failure, or other cause. Agents MUST treat attestations from suspended or revoked Verifiers as unverified.

**Appeals.** Verifiers subject to suspension or revocation MAY appeal to the governing body within 30 days of the status change. The appeal process and outcomes are published publicly.

**Registry versioning.** The registry is versioned. Agents SHOULD subscribe to registry change notifications published at `https://discloseframework.dev/registry/changelog` *(coming soon)*.

### Verifier Benchmarks

Verifiers accumulate aggregate data across their merchant base that gives individual merchant disclosures meaningful context. A return rate of 8% means something different in apparel than in consumer electronics. Verifiers are uniquely positioned to publish this context in the form of vertical benchmarks.

Verifier benchmarks are out of scope for v0.1 of this specification. However, the field `disclose:benchmark_ref` is reserved in the attribute namespace for future use. When defined in a future extension, this field will allow merchants to reference a Verifier-published benchmark document that provides vertical or category-level distributions for one or more disclosed attributes.

Verifiers MAY publish benchmark data in any format prior to a formal extension specification. Agents MAY consume such benchmarks at their own discretion. No agent is required to fetch or interpret benchmark data under this version of the specification.

---

## Complete Disclosure Document Example

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
    "disclose:refund_processing_time_median_days": 3.2,
    "disclose:refund_processing_time_p90_days": 6.1,
    "disclose:exchange_rate": 0.22,
    "disclose:exchange_rate_period_days": 90,
    "disclose:on_time_shipment_rate": 0.97,
    "disclose:on_time_shipment_rate_period_days": 90,
    "disclose:shipment_delay_median_hours": 8.0,
    "disclose:shipment_delay_p90_hours": 36.0,
    "disclose:order_accuracy_rate": 0.991,
    "disclose:order_accuracy_rate_period_days": 90,
    "disclose:incorrect_item_rate": 0.006,
    "disclose:damaged_item_rate": 0.003,
    "disclose:chargeback_rate": 0.003,
    "disclose:chargeback_rate_period_days": 90,
    "disclose:support_resolution_time_median_hours": 4.2,
    "disclose:support_resolution_time_p90_hours": 22.0,
    "disclose:search_to_conversion_rate": 0.047,
    "disclose:average_discount_rate": 0.12,
    "disclose:average_discount_rate_period_days": 90,
    "disclose:subscription_churn_rate": 0.04,
    "disclose:subscription_churn_rate_period_days": 30,
    "disclose:subscription_cancel_online": true,
    "disclose:review_rating": 4.7,
    "disclose:review_count": 14200,
    "disclose:review_verified_purchase_rate": 0.91,
    "disclose:review_recency_90d_rate": 0.08,
    "disclose:review_recency_365d_rate": 0.31,
    "disclose:sustainability_certified": true,
    "disclose:sustainability_certifier": "B Corp"
  },
  "attestations": [
    {
      "verifier_id": "loop-returns.com",
      "verifier_name": "Loop Returns",
      "attested_attributes": [
        "disclose:product_return_rate",
        "disclose:product_return_rate_period_days",
        "disclose:return_policy_type",
        "disclose:return_window_days",
        "disclose:refund_processing_time_median_days",
        "disclose:refund_processing_time_p90_days",
        "disclose:exchange_rate",
        "disclose:exchange_rate_period_days"
      ],
      "attested_at": "2026-02-01T00:00:00Z",
      "expires_at": "2026-08-01T00:00:00Z",
      "signature": "eyJhbGciOiJFUzI1NiIsImtpZCI6Imxvb3AtMjAyNiJ9...",
      "signing_key_id": "loop-2026"
    },
    {
      "verifier_id": "narvar.com",
      "verifier_name": "Narvar",
      "attested_attributes": [
        "disclose:on_time_shipment_rate",
        "disclose:on_time_shipment_rate_period_days",
        "disclose:order_accuracy_rate",
        "disclose:order_accuracy_rate_period_days"
      ],
      "attested_at": "2026-02-10T00:00:00Z",
      "expires_at": "2026-08-10T00:00:00Z",
      "signature": "eyJhbGciOiJFUzI1NiIsImtpZCI6Im5hcnZhci0yMDI2In0...",
      "signing_key_id": "narvar-2026"
    }
  ]
}
```

---

## Security

### Transport Security

All Disclose endpoints MUST be served over HTTPS. HTTP requests MUST be rejected or redirected.

### Signature Verification

Agents MUST verify attestation signatures before treating any attested attribute as verified. The verification flow is:

1. Fetch the Verifier Registry and confirm the `verifier_id` is listed with `status: active`.
2. Fetch the Verifier's signing keys from their `keys_url`.
3. Locate the key matching `signing_key_id`.
4. Reconstruct the canonical attestation payload.
5. Verify the ES256 signature against the payload using the public key.
6. Confirm `attested_at` is in the past and `expires_at` (if present) is in the future.

Agents MUST reject attestations that fail any step of this verification flow.

### Domain Binding

The `merchant_domain` field in the disclosure document MUST match the domain from which the document was served. Agents MUST reject documents where these do not match.

### Replay Prevention

Attestations include `attested_at` and `expires_at` timestamps. Agents SHOULD treat expired attestations as unverified, equivalent to self-reported attributes.

---

## Agent Consumption Guidelines

Agents consuming Disclose data operate with significant discretion. The framework does not mandate how agents weight or surface disclosure signals — this is intentionally left to the platform and agent developer. The following are non-normative recommendations:

- Unattested attributes should be surfaced as merchant-reported and weighted accordingly.
- Attested attributes should be surfaced as independently verified, with the Verifier named when relevant to the buyer.
- Subjective & Qualitative signals (see Standard Attributes) should be distinguished from operational metrics when surfaced to buyers. Agents SHOULD treat `disclose:review_rating` as contextual rather than authoritative, and SHOULD surface `disclose:review_verified_purchase_rate` alongside it wherever possible. Agents SHOULD additionally surface `disclose:review_recency_90d_rate` or `disclose:review_recency_365d_rate` where available, as review freshness materially affects the evidential weight of aggregate ratings.
- Missing disclosures may be surfaced as "disclosure unavailable" rather than assumed positive or negative.
- Agents SHOULD NOT produce composite scores or trust tiers derived from Disclose attributes. Such aggregations are outside the scope of this framework and undermine the principle that trust is emergent from raw, verifiable signals.
- Agents SHOULD NOT penalize merchants for not disclosing specific attributes unless disclosure of that attribute is required by applicable law or platform policy.

---

## Reference Implementation

To support adoption and validate the specification, the Disclose Framework provides the following reference resources at `https://github.com/disclose-framework/spec`:

- **JSON Schema:** A machine-readable schema for validating disclosure documents against the specification.
- **Validator:** A reference validator that checks a disclosure document for schema compliance, domain binding, and `_period_days` completeness.
- **Sample document:** A complete, valid example disclosure document suitable for testing agent consumption logic.
- **Verifier mock:** A lightweight mock Verifier endpoint for testing signature verification flows without a live Verifier integration.

Implementations that conform to the specification and pass the reference validator MAY self-identify as Disclose-compatible.

---

## Versioning

### Version Format

Disclose uses semantic versioning in the format `MAJOR.MINOR` (e.g., `0.1`, `1.0`). The version is declared in the disclosure document via the `disclose_version` field.

### Backwards Compatibility

The following changes MAY be introduced without a version increment:

- Adding new optional attributes to the standard attribute set
- Adding new optional fields to the attestation object
- Adding new Verifier entries to the registry
- Verifiers publishing benchmark documents prior to a formal benchmark extension specification

The following changes MUST result in a new MAJOR version:

- Removing or renaming existing attributes
- Changing the attestation payload structure or signature algorithm
- Modifying the discovery endpoint path

---

## Glossary

| Term | Definition |
|------|------------|
| Agent | A platform, AI assistant, or automated system that queries Disclose data on behalf of a buyer |
| Attestation | A cryptographically signed statement from a Verifier confirming that specific disclosed attributes have been independently verified |
| Benchmark Reference | An optional pointer to a Verifier-published document providing vertical or category-level distributions for disclosed attributes. Reserved for a future extension; see `disclose:benchmark_ref`. |
| Disclosure Document | The JSON document published by a merchant at `/.well-known/disclose` |
| Emergent Trust | The principle that trustworthiness arises from visible, verifiable behaviour rather than from framework-assigned scores or badges |
| Exchange Rate | The proportion of return transactions where the buyer selected a replacement item rather than a refund; a signal of product confidence distinct from the return rate |
| Merchant | The entity selling goods or services, who publishes disclosure data under their own domain |
| Merchant Sovereignty | The principle that merchants retain full control over what they disclose, to whom, and when |
| Observation Window | The time period over which a metric is computed, declared via a companion `_period_days` attribute |
| Progressive Enhancement | The ability to begin participation with a single attribute and expand disclosures over time |
| Review Recency | The proportion of a merchant's total reviews that were submitted within a recent time window (90 or 365 days), used to assess the freshness and ongoing relevance of aggregate review ratings |
| Selective Disclosure | The ability to disclose specific attributes without an all-or-nothing requirement |
| Subjective & Qualitative Signals | Disclosure attributes that are human-assessed rather than operationally derived, such as review ratings. Included in the schema for their recognized signal value but distinguished from behavioral metrics in weighting guidance. |
| Verifier | An authorized third party that cryptographically attests to the accuracy of specific merchant disclosures |
| Verifier Registry | The canonical, publicly accessible list of authorized Disclose Verifiers maintained by the framework governing body |
