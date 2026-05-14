# Disclose Framework Official Specification

**Draft version:** 0.3

## Overview

The Disclose Framework is an open standard for merchant disclosure attestations designed for the emerging era of agentic commerce. As AI agents increasingly act as intermediaries between buyers and merchants, researching products, comparing options, and making or informing purchasing recommendations, they require structured, machine-readable, and verifiable information about merchant practices before they can responsibly evaluate where to buy.

Disclose provides that infrastructure layer. It enables AI agents, platforms, and automated systems to access machine-readable information about merchant practices, including returns, fulfillment performance, refund processing, payment risk, seller tenure, review authenticity, and other operational signals, when making or informing purchasing decisions on behalf of buyers.

Disclose operates as a confidence layer that sits below discovery and above the transaction. It does not generate confidence by itself. It standardizes the operational signals agents use to form confidence before recommending where to buy. Disclose does not process payments, manage checkout sessions, or execute transactions. Its sole function is to standardize how merchants publish disclosed operating signals, how publishers declare provenance and freshness, how Signatories attest specific signals, and how agents consume those signals.

Disclose does not certify merchants. It does not produce scores, badges, tiers, rankings, or recommendations. Merchants publish operating evidence. Signatories may attest specific signals within authorized scope. Agents decide what the signals mean.

## Overarching Guidelines

The key words MUST, MUST NOT, REQUIRED, SHALL, SHALL NOT, SHOULD, SHOULD NOT, RECOMMENDED, MAY, and OPTIONAL in this document are to be interpreted as described in RFC 2119 and RFC 8174.

Schema notes:

- **Date format:** All timestamps MUST be expressed as RFC 3339 unless otherwise specified.
- **Numeric values:** Numeric values are expressed as decimals unless otherwise noted, for example `0.92` for 92%.
- **Rates and ratios:** Rates and ratios MUST be expressed as decimals between 0 and 1, for example `0.06` for 6%.
- **Observation windows:** Core Commerce signals MUST use a trailing 90-day observation window. Each Core Commerce signal MUST include `observation_window_days`, `window_start`, and `window_end`.
- **Daily refresh:** Automated Core Commerce disclosures SHOULD refresh daily. Each automated Core Commerce signal MUST include `generated_at` and SHOULD include `next_expected_refresh`.
- **Manual snapshots:** Manual snapshots MAY be used for testing, validation, onboarding, or demonstration. Manual snapshots MUST declare `publication_mode: "manual_snapshot"` and MUST NOT imply daily refresh.
- **Measurement methodology:** Each Core Commerce signal MUST include `methodology_version`. Agents SHOULD consider the methodology version, source of record, computation method, and attestation level when interpreting a signal.
- **Unknown fields:** Agents MUST ignore unknown fields without error, provided required fields are present and valid.

## Design Philosophy

### Trust Is Emergent, Not Engineered

The Disclose Framework does not produce trust scores, badges, tiers, rankings, certifications, or recommendations. It produces structured, verifiable facts about merchant behaviour. Trust or distrust emerges from those facts as agents and buyers draw their own conclusions.

This is a deliberate architectural choice with three consequences:

**Merchants disclose behaviour, not claims.** Every operating attribute in the Disclose schema is grounded in operational outcomes, including returns, fulfillment accuracy, refund timing, chargeback rates, and seller tenure. These are things that happened, not assertions about quality or intent.

**The framework enforces structure, not interpretation.** Disclose defines what attributes mean, how they are measured, how they declare provenance, and how they may be verified. It does not define how agents should weight them, combine them, or surface them to buyers. That discretion belongs to the agent or platform.

**No centralized authority renders verdicts.** There is no "Disclose Score." There is no tier that grants a badge. A merchant that publishes a low return rate, high on-time shipment rate, and fast refund processing gives agents more operational evidence to evaluate. The framework does not determine what conclusion the agent should draw.

This philosophy also protects against gaming. Scores and badges create targets. Raw, time-bounded, provenance-declared, and Signatory-attested metrics are harder to manipulate without changing actual operations.

### Self-Reported Attribute Integrity

Merchants MAY publish disclosures without Signatories. Self-reported attributes carry no third-party verification and agents SHOULD treat them accordingly. Merchants MAY declare the platform origin of self-reported attributes using source metadata. Source declarations do not constitute attestation.

The framework does not currently define a formal dispute process for false self-reported disclosures. Platforms consuming Disclose data MAY implement their own policies for flagging or deprioritizing merchants whose self-reported attributes are demonstrably inconsistent with other observable signals. A future extension to this specification may define a community-based flagging and review process.

## Core Concepts

### The Three-Party Model

Disclose defines three participants:

| Participant | Role |
|-------------|------|
| Merchant | Publishes disclosure data about their own practices under their own domain |
| Signatory | An authorized third party that attests to the accuracy of specific merchant disclosures using cryptographic signatures |
| Agent | A platform, AI assistant, or automated system that queries and consumes disclosure data on behalf of a buyer |

Unlike transaction protocols, Disclose does not require real-time negotiation between parties. Merchants publish; Signatories attest; agents consume. The flow is asynchronous and cacheable.

### Merchant Sovereignty

A core principle of the Disclose Framework is that merchants retain full sovereignty over their disclosures. Participation is voluntary. Merchants choose which attributes to disclose, which Signatories to authorize, and when disclosures are updated or removed. The framework standardizes how a signal is expressed, not whether a merchant must expose it.

By default, all merchant-scoped signals reflect DTC performance only. Merchants with multi-channel operations MAY declare additional channels using `channel_scope`.

### Selective Disclosure

There is no all-or-nothing requirement. A merchant MAY publish a single attribute and add additional attributes over time as its business matures or as competitive incentives emerge. This progressive enhancement model lowers the barrier to participation while preserving the integrity of the standard.

A merchant MAY publish any subset of Core Commerce signals, including one of seven Core signals or all seven Core signals. A disclosure document remains conformant if each published signal follows the required methodology, source, freshness, and attestation metadata rules.

The absence of a Core signal has no protocol-defined meaning. Agents MUST NOT assume that an absent Core signal indicates poor merchant performance, merchant concealment, or non-compliance. Agents MAY decide how to interpret absence according to their own policies.

### Attestation Tiers

Every signal in a disclosure document carries an `attestation_level` field declaring how the value was produced:

| `attestation_level` | Meaning |
|---|---|
| `none` | Merchant self-reported. No third-party computation or signature. Agents SHOULD weight accordingly. |
| `computed` | Pulled from a source system or platform API and calculated by a third-party tool or computed publisher, for example Sure Signal from Shopify API data. Not cryptographically signed. Harder to manipulate than merchant-entered data, but carries no Signatory accountability. |
| `signatory` | Cryptographically signed by an authorized Signatory with direct access to source data or a defined verification method. The Signatory is accountable for the signed signal within its authorized scope. |

Agents SHOULD use `attestation_level` as a primary signal weighting input before evaluating the value itself.

A Signatory does not certify the merchant, require complete Core Profile coverage, or determine how agents should interpret the signal. A Signatory attests only to specified signals within its authorized scope.

### Credentialed Query (Anticipated Extension)

Some merchants may hold operational signals they are willing to share with verified agents but not publish in a public disclosure document. The current specification does not define a mechanism for this. A future extension will define a credentialed query path - allowing agents with verified identity to request non-public attributes directly from a merchant's infrastructure. Merchants who wish to signal this capability in advance MAY include a disclose:credentialed_query_supported: true attribute in their public disclosure document. No further behaviour is defined for this attribute in the current version.

### Commerce Risk Coverage

The standard attribute set is designed to address the core risks an agent may evaluate before recommending a purchase:

| Risk Dimension | Covered By |
|----------------|------------|
| Product Quality | Repeat purchase rate, product return rate, defect rate |
| Inventory Reliability | In-stock rate, inventory accuracy rate, backorder rate |
| Delivery Reliability | On-time shipment rate, delivered on time rate, order accuracy rate |
| Financial Risk | Refund processing time, chargeback rate, dispute win rate |
| Service Reliability | Customer support resolution time, first contact resolution rate |
| Pricing Integrity | Average discount rate, price stability rate, promotional frequency |
| Long-term Value | Subscription churn rate |
| Merchant Legitimacy | Business registration, domain age, platform seller tenure |

No single dimension dominates. Agents weight these signals according to their own risk models and buyer context.

### Core Commerce Profile v0.1

The Core Commerce Profile defines the first standard signal set for merchant operating evidence in agentic commerce. It is an optional signal set, not a mandatory checklist.

The Core Commerce signal set is:

| Core signal | Category | Purpose |
|---|---|---|
| `disclose:product_return_rate` | Product Quality | Measures returned units relative to shipped units. |
| `disclose:on_time_shipment_rate` | Fulfillment | Measures orders shipped within the merchant's stated fulfillment window. |
| `disclose:refund_processing_time_median_days` | Returns & Refunds | Measures median business days from return receipt to refund completion. |
| `disclose:chargeback_rate` | Financial Risk | Measures chargebacks relative to total completed transactions. |
| `disclose:dispute_win_rate` | Financial Risk | Measures disputed transactions resolved in the merchant's favour. |
| `disclose:platform_seller_tenure_days` | Identity & Legitimacy | Measures days the merchant has been active on its primary commerce platform. |
| `disclose:order_accuracy_rate` | Fulfillment | Measures orders fulfilled without incorrect or damaged items. |

Merchants MAY expose any subset of the Core Commerce signal set. A disclosure document may contain one Core signal, all seven Core signals, or any subset between one and seven. Conformance depends on the validity of each published signal, not on full Core coverage.

Core coverage is descriptive only. It indicates how many defined Core Commerce signals are present in a disclosure document. Core coverage MUST NOT be represented as a merchant score, badge, ranking, certification, endorsement, or recommendation.

All Core Commerce signals MUST use a trailing 90-day observation window unless a future Core Commerce Profile version explicitly defines a different window. Automated Core Commerce disclosures SHOULD refresh daily.

Each published Core Commerce signal MUST include:

- `value`
- `observation_window_days`
- `window_start`
- `window_end`
- `generated_at`
- `attestation_level`
- `methodology_version`

Each published Core Commerce signal SHOULD include:

- `source_of_record`
- `computed_by`, when a third-party tool or service computed the signal
- `next_expected_refresh`, when the signal is produced by an automated publisher

Publishers MAY include optional `signal_status` metadata to explain why a Core signal is not disclosed. Signal status metadata is informational and is intended to reduce ambiguity for agent consumers. It is not required for conformance.

Recommended `signal_status` values for undisclosed signals are:

| Status | Meaning |
|---|---|
| `not_disclosed` | The merchant has chosen not to expose this signal. |
| `not_available` | The source system does not provide the data required to compute this signal. |
| `insufficient_volume` | The signal exists in principle, but the qualifying sample size is below the methodology threshold. |
| `not_applicable` | The signal does not apply to the merchant's business model. |
| `expired` | The signal was previously disclosed but is no longer fresh. |
| `error` | The signal could not be generated due to a temporary system issue. |

The absence of `signal_status` has no protocol-defined meaning.

## Disclosure Scopes

The Disclose Framework organizes disclosure signals across three scopes. Every `disclose:` property belongs to one or more scopes. The scope is determined by the schema.org node type to which the property is attached - no additional metadata is required.

**Merchant → Offer → Item**

A Merchant makes an Offer on an Item. This three-node model maps directly to established schema.org types, consistent with the framework's goal of becoming a recognized schema.org extension:

| Disclose Term | schema.org Type | What it represents |
|---|---|---|
| **Merchant** | `schema:Organization` | The seller entity publishing disclosure signals |
| **Offer** | `schema:Offer` | A specific Merchant's commercial terms for a specific Item |
| **Item** | `schema:ItemOffered` | The product or service being transacted |

### Signal Scope

All attributes defined in this specification are **Merchant-scoped** unless explicitly noted otherwise. Merchant-scoped signals reflect aggregate operational performance across all of the merchant's transactions and SKUs.

Any `disclose:` attribute MAY also be published at **Offer scope** or **Item scope** when the merchant or an authorized Signatory has signal data specific to a particular product or transaction context. When the same attribute appears at multiple scopes, agents SHOULD prefer the most specific scope available.

| Scope | Node type | What it signals | Example |
|---|---|---|---|
| **Merchant** | `schema:Organization` | Aggregate performance across all transactions | Overall return rate across all SKUs |
| **Offer** | `schema:Offer` | Performance for this seller on this specific Item | Return rate for this SKU at this merchant |
| **Item** | `schema:ItemOffered` | Attributes intrinsic to the item, independent of seller | Manufacturer warranty terms, safety recall status |

### Scope in Practice: Vendor Comparison

The Merchant → Offer → Item model enables a class of agentic query that no prior merchant signal framework supports: comparing the same Item across multiple Merchants.

When an agent evaluates two Merchants selling the same Item (identified by a shared GTIN, ISBN, or manufacturer part number), it can triangulate across all three scopes:

- **Item scope** confirms it is evaluating the same product
- **Offer scope** reveals how each Merchant specifically performs on that Item (e.g., SKU-level return rate, fulfillment source, inventory accuracy)
- **Merchant scope** provides baseline seller confidence independent of the specific Item

An Offer-scoped signal takes precedence over a Merchant-scoped signal for the same attribute when both are present.

### Scope in the Disclosure Document

Offer-scoped and Item-scoped signals are published within the same `/.well-known/disclose` document. They are distinguished from Merchant-scoped signals by their node context using JSON-LD:

```json
{
  "@context": {
    "@vocab": "https://schema.org/",
    "disclose": "https://discloseframework.dev/vocab#"
  },
  "@type": "Organization",
  "disclose:product_return_rate": {
    "value": 0.07,
    "unit": "ratio",
    "observation_window_days": 90,
    "window_start": "2026-02-13T00:00:00Z",
    "window_end": "2026-05-13T23:59:59Z",
    "generated_at": "2026-05-14T00:00:00Z",
    "attestation_level": "computed",
    "methodology_version": "core-commerce-v0.1"
  },

  "makesOffer": [
    {
      "@type": "Offer",
      "itemOffered": {
        "@type": "Product",
        "gtin": "00012345678905"
      },
      "disclose:product_return_rate": {
        "value": 0.03,
        "unit": "ratio",
        "observation_window_days": 90,
        "window_start": "2026-02-13T00:00:00Z",
        "window_end": "2026-05-13T23:59:59Z",
        "generated_at": "2026-05-14T00:00:00Z",
        "attestation_level": "computed",
        "methodology_version": "core-commerce-v0.1"
      },
      "disclose:inventory_accuracy_rate": {
        "value": 0.99,
        "unit": "ratio",
        "observation_window_days": 90,
        "window_start": "2026-02-13T00:00:00Z",
        "window_end": "2026-05-13T23:59:59Z",
        "generated_at": "2026-05-14T00:00:00Z",
        "attestation_level": "computed"
      }
    }
  ]
}
```

In this example, the agent can observe that while the Merchant's overall return rate is 7%, the return rate for this specific SKU is 3% - a materially stronger signal for a purchase recommendation on this Item.

### Item-Scope Signals

The following attributes are particularly well-suited to Item scope, as they reflect properties intrinsic to the item rather than aggregate merchant behaviour. These are natural targets for brand registries, manufacturer databases, and product data platforms:

| Attribute | Item-scope meaning |
|---|---|
| `disclose:business_registration_verified` | Whether the seller is an authorized reseller of this Item's brand |
| `disclose:sustainability_certified` | Whether this specific Item carries a sustainability certification |
| `disclose:product_defect_rate` | Known defect rate for this Item across all sellers |
| `disclose:return_policy_type` | Return policy specific to this Item (e.g., non-returnable electronics) |

*The framework anticipates that dedicated Item-scope attributes - including authorized reseller status and product-level recall signals - will be formally defined in a future version of this specification.*

---

## Discovery

### Publication Endpoint

Merchants publish their disclosure document at a well-known URI:
```
/.well-known/disclose
```

This endpoint MUST return a valid JSON document conforming to the Disclose schema. The endpoint SHOULD support HTTP caching via standard `Cache-Control` headers.

Agents SHOULD check `/.well-known/disclose` first. For merchants on hosted platforms that do not support the `/.well-known/` directory, `/.well-known/disclose.json` is a supported legacy fallback, followed by `disclose.json` at the domain root. Agents MUST check the canonical path first and fall back in order if each path returns a 404.

Example request:
```
GET /.well-known/disclose HTTP/1.1
Host: merchant.example.com
Accept: application/json
```

### Discovery by Agents

Agents MAY fetch the disclosure document before, during, or after capability negotiation with a merchant's commerce infrastructure. Agents SHOULD cache disclosure documents according to HTTP cache-control directives.

Agents MUST NOT require a disclosure document to be present in order to complete a transaction. The absence of a disclosure document may be considered by agents according to their own policies. The framework does not define absence as positive or negative.

## Disclosure Document Structure

### Top-Level Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `disclose_version` | string | Yes | Specification version, for example `"0.3"`. |
| `merchant_domain` | string | Yes | The canonical domain of the merchant, for example `"merchant.example.com"`. |
| `issued_at` | string | Yes | RFC 3339 timestamp of when this document was generated. |
| `expires_at` | string | No | RFC 3339 timestamp after which agents SHOULD re-fetch. |
| `publication_mode` | string | No | One of: `automated`, `manual_snapshot`. Default if absent: `automated`. |
| `refresh_frequency` | string | No | Recommended value for automated Core Commerce disclosures: `daily`. Manual snapshots SHOULD use `none`. |
| `channel_scope` | string | No | Declares the channel reflected by signals in this document. Values: `dtc`, `all_direct`, `all_channels`. Default if absent: `dtc`. |
| `core_profile` | object | No | Metadata describing Core Commerce coverage. Required when any Core Commerce signal is present. |
| `attributes` | object | Yes | Map of disclosed merchant attributes. Each attribute is an object containing `value`, `attestation_level`, and required metadata. |
| `signal_status` | array | No | Optional explanatory metadata for Core signals that are not disclosed. |
| `sources` | array | No | Array of source-of-record objects declaring the origin of specific attributes. Source declarations do not constitute attestation. |
| `attestations` | array | No | Array of Signatory attestation objects. |

### Core Profile Object

The `core_profile` object is required when any Core Commerce signal is present.

| Field | Type | Required | Description |
|---|---|---|---|
| `name` | string | Yes | Profile name. For this version: `core-commerce`. |
| `version` | string | Yes | Profile version. For this version: `0.1`. |
| `signals_defined` | integer | Yes | Number of signals defined in the Core Commerce Profile. For v0.1: `7`. |
| `signals_disclosed` | integer | Yes | Number of Core Commerce signals present in `attributes`. |
| `coverage_note` | string | No | Optional reminder that coverage is descriptive only and not a score. |

Example:

```json
{
  "name": "core-commerce",
  "version": "0.1",
  "signals_defined": 7,
  "signals_disclosed": 6,
  "coverage_note": "Core coverage is descriptive only and is not a score, badge, ranking, certification, endorsement, or recommendation."
}
```

### Attribute Namespace

All disclosure attributes exist in the `disclose:` namespace. Each attribute is published as an object with the following fields:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `value` | varies | Yes | The signal value. |
| `unit` | string | Recommended | Unit of measurement, for example `ratio`, `days`, `hours`, `count`, `boolean`, or `string`. |
| `observation_window_days` | integer | For Core and other time-bounded metrics | Observation window in days. Core Commerce signals MUST use `90`. |
| `window_start` | string | For Core signals | RFC 3339 date or timestamp marking the start of the trailing observation window. |
| `window_end` | string | For Core signals | RFC 3339 date or timestamp marking the end of the trailing observation window. |
| `generated_at` | string | For Core signals | RFC 3339 timestamp of when the signal was generated. |
| `next_expected_refresh` | string | Recommended for automated Core signals | RFC 3339 timestamp of when the signal is next expected to refresh. |
| `reported_by` | string | Yes | Who reported this value: `merchant`, a computed publisher identifier, or the Signatory domain. |
| `source_of_record` | string | Recommended | Platform, API, or system from which the underlying data was retrieved, for example `shopify_api`. |
| `computed_by` | string | Required for `computed` | Tool or service that computed the value, for example `sure_signal`. |
| `attestation_level` | string | Yes | One of: `none`, `computed`, `signatory`. |
| `methodology_version` | string | For Core signals | Methodology used to calculate the signal, for example `core-commerce-v0.1`. |
| `attestation` | object or null | Yes | Null for `none` and `computed` tiers. Signatory attestation object for `signatory` tier. |

Agents MUST ignore unknown fields without error.

### Optional Signal Status Metadata

Merchants are not required to list absent Core signals. When a publisher wants to explain absence, it MAY include a `signal_status` array.

Example:

```json
{
  "attribute": "disclose:order_accuracy_rate",
  "status": "not_available",
  "reason": "source_system_does_not_provide_required_data"
}
```

`signal_status` is informational. It does not change conformance, and its absence has no protocol-defined meaning.

## Standard Attributes

The following attributes are defined in this version of the specification. All are optional unless included in the Core Commerce Profile and published by the merchant. The attribute library is broader than the Core Commerce Profile.

- **Core Commerce signals** are the first standardized profile for agentic commerce and carry stricter requirements around 90-day trailing windows, daily refresh expectations for automated publishers, and methodology metadata.
- **Standard attributes** are the broader optional vocabulary from which current and future profiles may be composed.
- **Future profiles** may define vertical, channel, or platform-specific signal sets.

**Categories:**
1. [Product Quality](#1-product-quality)
2. [Returns & Refunds](#2-returns--refunds)
3. [Fulfillment](#3-fulfillment)
4. [Inventory & Availability](#4-inventory--availability)
5. [Shipping & Delivery Experience](#5-shipping--delivery-experience)
6. [Financial Risk](#6-financial-risk)
7. [Customer Support](#7-customer-support)
8. [Pricing & Conversion](#8-pricing--conversion)
9. [Subscriptions](#9-subscriptions)
10. [Sustainability & Ethics](#10-sustainability--ethics)
11. [Identity & Legitimacy](#11-identity--legitimacy)
12. [Review Signals](#12-review-signals)

### Core Commerce Methodology Requirements

For each published Core Commerce signal, the methodology MUST define:

- Definition
- Numerator, where applicable
- Denominator, where applicable
- Observation window
- Exclusions
- Minimum sample guidance, where applicable
- Rounding rules
- Required metadata

The seven Core Commerce signals in v0.1 use `methodology_version: "core-commerce-v0.1"`.

#### `disclose:product_return_rate`

- **Definition:** Rate of units returned during the trailing 90-day observation window.
- **Numerator:** Returned units, including returnless refunds where no item is physically returned.
- **Denominator:** Shipped units during the same observation window.
- **Exclusions:** Test orders, cancelled orders never shipped, duplicate orders, and exchanges where the buyer selected a replacement item without a refund.
- **Rounding:** Decimal ratio rounded to four decimal places unless a publisher declares greater precision.

#### `disclose:on_time_shipment_rate`

- **Definition:** Rate of orders shipped within the merchant's stated fulfillment window during the trailing 90-day observation window.
- **Numerator:** Orders shipped on or before the promised fulfillment deadline.
- **Denominator:** Orders requiring shipment during the same observation window.
- **Exclusions:** Cancelled orders, digital-only orders, test orders, and orders delayed by buyer action.
- **Rounding:** Decimal ratio rounded to four decimal places unless a publisher declares greater precision.

#### `disclose:refund_processing_time_median_days`

- **Definition:** Median business days from receipt of returned item at the merchant's return facility to refund completion during the trailing 90-day observation window.
- **Numerator/denominator:** Not a ratio. Calculated across qualifying refund events.
- **Exclusions:** Returnless refunds, refunds initiated before item receipt, test orders, and refunds blocked by buyer payment method or external processor delay where known.
- **Rounding:** Decimal days rounded to one decimal place unless a publisher declares greater precision.

#### `disclose:chargeback_rate`

- **Definition:** Chargebacks as a proportion of completed transactions during the trailing 90-day observation window.
- **Numerator:** Chargeback events associated with completed transactions in the observation window.
- **Denominator:** Completed transactions in the same observation window.
- **Exclusions:** Test transactions, voided authorizations, and cancelled transactions never captured.
- **Rounding:** Decimal ratio rounded to four decimal places unless a publisher declares greater precision.

#### `disclose:dispute_win_rate`

- **Definition:** Rate of disputed transactions resolved in the merchant's favour during the trailing 90-day observation window.
- **Numerator:** Disputes resolved in the merchant's favour.
- **Denominator:** Disputes resolved during the same observation window.
- **Exclusions:** Open disputes and cancelled dispute records.
- **Rounding:** Decimal ratio rounded to four decimal places unless a publisher declares greater precision.

#### `disclose:platform_seller_tenure_days`

- **Definition:** Number of days the merchant has been an active seller on its primary commerce platform as of `generated_at`.
- **Numerator/denominator:** Not a ratio.
- **Observation window:** Not time-bounded. This signal MUST include `generated_at` and SHOULD include `source_of_record` and `platform_seller_tenure_platform`.
- **Rounding:** Integer days.

#### `disclose:order_accuracy_rate`

- **Definition:** Rate of orders fulfilled without incorrect or damaged items during the trailing 90-day observation window.
- **Numerator:** Orders with no known incorrect item or damaged item event.
- **Denominator:** Fulfilled orders during the same observation window.
- **Exclusions:** Cancelled orders, test orders, digital-only orders, and orders without sufficient fulfillment data.
- **Rounding:** Decimal ratio rounded to four decimal places unless a publisher declares greater precision.

### 1. Product Quality

Operational signals about product performance derived from post-purchase behaviour. These reflect what buyers actually did - returned, repurchased, reported defective - rather than what they said.

| Attribute | Type | Description |
|-----------|------|-------------|
| `disclose:repeat_purchase_rate` | decimal | Rate of buyers who make a second purchase within the observation window (0–1) |
| `disclose:product_return_rate` | decimal | Rate of units returned across all orders (0–1). Measured as returned units divided by shipped units. May be disclosed at SKU or category level. |
| `disclose:product_defect_rate` | decimal | Rate of units reported defective or dead-on-arrival at delivery (0–1). Distinct from return rate: captures manufacturing and quality control failures before buyer decision. |
| `disclose:size_accuracy_rate` | decimal | Rate of orders where the delivered item matched the size or fit specified at purchase (0–1). Primarily relevant for apparel, footwear, and sized goods. Derived from return reason codes where available. |

> **Measurement note - return rate:** Measured as returned units divided by total shipped units within the observation window. Exchanges (where the buyer selects a replacement item) are NOT counted as returns. Returnless refunds where no item is physically returned ARE counted. Where a Signatory attests this attribute, the Signatory's methodology governs.

---

### 2. Returns & Refunds

Policy and performance signals covering the full returns lifecycle: what the merchant promises (policy), what they deliver (processing time), and how buyers respond (exchange vs. refund).

| Attribute | Type | Description |
|-----------|------|-------------|
| `disclose:return_policy_type` | string | One of: `free`, `label_fee`, `buyer_pays`, `no_returns` |
| `disclose:return_window_days` | integer | Number of days a buyer has to initiate a return |
| `disclose:return_label_cost` | decimal | Cost of the return label in the merchant's primary currency, where `return_policy_type` is `label_fee`. Agents SHOULD surface this value alongside return policy type. |
| `disclose:refund_processing_time_median_days` | decimal | Median business days from warehouse receipt of returned item to refund completion. Clock starts at receipt at merchant's return facility, not at return initiation or carrier pickup. |
| `disclose:refund_processing_time_p90_days` | decimal | 90th percentile business days from warehouse receipt to refund completion (same clock-start as median) |
| `disclose:exchange_rate` | decimal | Rate of return transactions where the buyer selected a replacement item rather than a refund (0–1). A higher exchange rate signals product confidence and buyer intent to remain a customer. |
| `disclose:returnless_refund_rate` | decimal | Rate of refunds issued without requiring the buyer to return the item (0–1). A higher rate signals merchant confidence in product quality and low unit economics on returns. |
| `disclose:return_reason_top_category` | string | The most frequently cited return reason category within the observation window. Recommended values: `sizing`, `defective`, `not_as_described`, `changed_mind`, `arrived_late`, `other`. |
| `disclose:international_return_supported` | boolean | Whether the merchant supports returns from buyers outside the merchant's primary operating country. |

---

### 3. Fulfillment

Operational signals covering the merchant's warehouse-side fulfillment performance: whether orders leave correctly and on time. For signals covering what happens after carrier handoff, see [Shipping & Delivery Experience](#5-shipping--delivery-experience).

#### Shipment Reliability

| Attribute | Type | Description |
|-----------|------|-------------|
| `disclose:on_time_shipment_rate` | decimal | Rate of orders shipped within the merchant's stated fulfillment window (0–1) |
| `disclose:shipment_delay_median_hours` | decimal | Median hours by which late shipments missed the promised fulfillment window |
| `disclose:shipment_delay_p90_hours` | decimal | 90th percentile hours by which late shipments missed the promised fulfillment window |
| `disclose:same_day_fulfillment_rate` | decimal | Rate of orders shipped on the same calendar day as placement, for orders placed before the merchant's same-day cutoff time (0–1). |
| `disclose:fulfillment_location_count` | integer | Number of distinct warehouse or fulfillment locations the merchant ships from. A higher count signals distributed inventory and reduced average transit distance. |

#### Order Accuracy

| Attribute | Type | Description |
|-----------|------|-------------|
| `disclose:order_accuracy_rate` | decimal | Rate of orders fulfilled without incorrect or damaged items (0–1) |
| `disclose:incorrect_item_rate` | decimal | Rate of orders containing a wrong item (0–1) |
| `disclose:damaged_item_rate` | decimal | Rate of orders containing a damaged item at delivery (0–1) |
| `disclose:carrier_on_time_delivery_rate` | decimal | Rate of shipments delivered on time per the carrier's own estimated delivery date (0–1). Distinguishes merchant-side fulfillment delays from carrier-side delivery delays. |

---

### 4. Inventory & Availability

Signals about whether products are actually available when an agent attempts to purchase. Inventory failures are a critical agentic commerce failure mode - an agent that recommends an out-of-stock product, or places an order against inaccurate inventory, has failed the buyer regardless of all other merchant quality signals.

| Attribute | Type | Description |
|-----------|------|-------------|
| `disclose:in_stock_rate` | decimal | Rate at which listed products are in stock at the time of order placement (0–1), measured across all active SKUs within the observation window. |
| `disclose:stockout_frequency_rate` | decimal | Rate of active SKUs that experienced at least one stockout during the observation window (0–1). |
| `disclose:backorder_rate` | decimal | Proportion of orders placed against backordered inventory (0–1). Agents SHOULD surface this to buyers who have expressed time-sensitivity. |
| `disclose:inventory_accuracy_rate` | decimal | Rate at which displayed inventory levels match actual warehouse counts at the time of order (0–1). Mismatches result in post-order cancellations - a significant buyer trust failure. |
| `disclose:pre_order_fulfillment_rate` | decimal | For merchants who accept pre-orders: rate of pre-orders fulfilled on or before the stated availability date (0–1). Omit if the merchant does not offer pre-orders. |

---

### 5. Shipping & Delivery Experience

Post-handoff signals covering what the buyer actually experiences after an order leaves the merchant's facility. Distinct from Fulfillment, which measures warehouse-side operations. These signals require carrier tracking data and are natural attestation targets for post-purchase platforms such as Narvar and AfterShip.

| Attribute | Type | Description |
|-----------|------|-------------|
| `disclose:delivered_on_time_rate` | decimal | Rate of orders delivered by the date promised to the buyer at checkout (0–1). Distinct from `disclose:on_time_shipment_rate`, which measures warehouse departure. This is the signal buyers actually experience. |
| `disclose:tracking_provided_rate` | decimal | Rate of orders for which tracking information was provided to the buyer (0–1). |
| `disclose:delivery_attempt_success_rate` | decimal | Rate of shipments successfully delivered on the first carrier attempt (0–1). |
| `disclose:average_transit_days` | decimal | Median calendar days from ship date to confirmed delivery within the observation window. |
| `disclose:carrier_selection_count` | integer | Number of distinct carriers used by the merchant. A higher count signals redundancy and rate optimization capacity. |

---

### 6. Financial Risk

Signals about transaction integrity and payment reliability. Agents handling autonomous purchases on behalf of buyers have an elevated duty to assess financial risk before recommending a transaction.

| Attribute | Type | Description |
|-----------|------|-------------|
| `disclose:chargeback_rate` | decimal | Chargebacks as a proportion of total transactions (0–1) |
| `disclose:dispute_win_rate` | decimal | Rate of disputed transactions resolved in the merchant's favour (0–1). Provides context for chargeback rate: a merchant with low chargebacks and a high dispute win rate has a materially stronger financial risk profile. |
| `disclose:fraud_order_rate` | decimal | Rate of orders identified as fraudulent and cancelled prior to fulfillment (0–1). Signals the merchant's fraud detection maturity and platform security posture. |
| `disclose:payment_method_coverage` | array of strings | Payment methods accepted by the merchant. Recommended values: `card`, `paypal`, `apple_pay`, `google_pay`, `shop_pay`, `buy_now_pay_later`, `crypto`, `bank_transfer`. |

---

### 7. Customer Support

Signals about the quality, speed, and accessibility of the merchant's customer support. For agentic purchases, post-purchase support access is a material risk factor - an agent that cannot escalate a buyer issue has limited recourse.

| Attribute | Type | Description |
|-----------|------|-------------|
| `disclose:support_resolution_time_median_hours` | decimal | Median hours from support contact initiation to issue resolution |
| `disclose:support_resolution_time_p90_hours` | decimal | 90th percentile hours from support contact to resolution |
| `disclose:support_channel_availability` | array of strings | Support channels available to buyers. Recommended values: `live_chat`, `email`, `phone`, `sms`, `social`, `self_serve`. |
| `disclose:support_hours_coverage` | string | Hours during which live support is available. Recommended values: `24_7`, `business_hours`, `extended_hours`, `async_only`. |
| `disclose:first_contact_resolution_rate` | decimal | Rate of support contacts resolved without requiring a follow-up interaction (0–1). A strong signal of support quality and operational maturity. |

---

### 8. Pricing & Conversion

Signals about pricing integrity and buyer behaviour. These attributes help agents distinguish merchants with stable, honest pricing from those engaged in discount theater - artificial inflation followed by manufactured discounts.

| Attribute | Type | Description |
|-----------|------|-------------|
| `disclose:average_discount_rate` | decimal | Average discount applied across completed transactions as a proportion of list price (0–1) |
| `disclose:search_to_conversion_rate` | decimal | Rate of product page visits that result in a completed purchase (0–1). Signals demand authenticity and product-market fit. |
| `disclose:price_stability_rate` | decimal | Rate of active SKUs whose listed price did not change during the observation window (0–1). A low rate may indicate dynamic or promotional pricing practices that affect the reliability of displayed prices. |
| `disclose:dynamic_pricing_used` | boolean | Whether the merchant uses algorithmic or demand-based dynamic pricing. Agents SHOULD surface this to buyers when the purchase context is price-sensitive. |
| `disclose:promotional_frequency_rate` | decimal | Proportion of days within the observation window on which at least one active site-wide or category-level promotion was running (0–1). A rate approaching 1.0 is a discount theater signal. |

---

### 9. Subscriptions

Signals relevant to subscription products. These attributes apply only to merchants offering recurring purchase programmes. Agents evaluating subscription purchases face asymmetric risk: the buyer commits to ongoing charges while cancellation friction varies widely across merchants.

| Attribute | Type | Description |
|-----------|------|-------------|
| `disclose:subscription_churn_rate` | decimal | Rate of active subscriptions cancelled within the observation window (0–1) |
| `disclose:subscription_cancel_online` | boolean | Whether subscriptions can be cancelled without contacting support |
| `disclose:subscription_pause_available` | boolean | Whether subscriptions can be paused without cancelling |
| `disclose:subscription_trial_days` | integer | Free trial duration in days, if offered. Omit if no trial is available. |
| `disclose:subscription_price_change_notice_days` | integer | Minimum number of days notice the merchant provides to subscribers before a price increase takes effect. |
| `disclose:subscription_skip_available` | boolean | Whether subscribers can skip an individual delivery without pausing or cancelling the subscription. |

---

### 10. Sustainability & Ethics

Certification-based signals about the merchant's environmental and ethical practices. These are naturally suited to third-party attestation: certifying bodies are ideal Signatory candidates for this category.

| Attribute | Type | Description |
|-----------|------|-------------|
| `disclose:sustainability_certified` | boolean | Whether the merchant holds a recognized sustainability certification |
| `disclose:sustainability_certifier` | string | Name of the certifying body (e.g., `B Corp`, `1% for the Planet`) |
| `disclose:ethical_sourcing_certified` | boolean | Whether the merchant holds a recognized ethical sourcing certification |
| `disclose:carbon_neutral_certified` | boolean | Whether the merchant holds a recognized carbon neutral certification, distinct from general sustainability accreditation. |
| `disclose:carbon_neutral_certifier` | string | Name of the carbon neutral certifying body (e.g., `Climate Neutral`, `Carbon Trust`) |
| `disclose:living_wage_certified` | boolean | Whether the merchant holds a recognized living wage certification for their workforce. |
| `disclose:country_of_manufacture` | string or array | ISO 3166-1 alpha-2 country code(s) where the merchant's products are manufactured. Relevant for ethical sourcing context and geopolitical supply chain risk assessment. |

---

### 11. Identity & Legitimacy

Signals that help agents distinguish legitimate merchants from fraudulent storefronts, impersonation attempts, and fly-by-night operators. This is the category most resistant to gaming: the signals are grounded in external registries - business registration databases, domain history, trademark records - rather than behavioral data the merchant controls. As agentic commerce scales, counterfeit merchant risk becomes a material threat vector that no existing trust signal framework addresses.

> **Verification note:** Attributes in this category are particularly well-suited to third-party attestation. Business registry services, WHOIS data providers, and trademark database services are natural Signatory candidates. Self-reported values in this category carry meaningfully less evidential weight than attested values and SHOULD be weighted accordingly by agents.

| Attribute | Type | Description |
|-----------|------|-------------|
| `disclose:business_registration_verified` | boolean | Whether the merchant's legal business registration has been verified by a third party against a government business registry. |
| `disclose:domain_age_days` | integer | Age of the merchant's primary domain in days as of the disclosure document's `issued_at` date. Derived from WHOIS registration data. |
| `disclose:trademark_registered` | boolean | Whether the merchant's brand name is registered as a trademark in at least one major jurisdiction. |
| `disclose:platform_seller_tenure_days` | integer | Number of days the merchant has been an active seller on their primary commerce platform as of `issued_at`. Attested by the platform. |
| `disclose:platform_seller_tenure_platform` | string | The platform to which `disclose:platform_seller_tenure_days` refers (e.g., `shopify`, `amazon`, `etsy`). |

---

### 12. Review Signals

Signals derived from buyer reviews and ratings. These differ from operational metrics: they are human-assessed rather than operationally derived, and more susceptible to manipulation. Agents SHOULD weight review signals in combination with operational metrics rather than in isolation.

> **Recency matters:** A merchant with 10,000 lifetime reviews but minimal recent activity has a materially different trust profile than a merchant with comparable volume and active ongoing engagement. Agents SHOULD weight `disclose:review_recency_90d_rate` and `disclose:review_recency_365d_rate` when interpreting `disclose:review_rating`.

| Attribute | Type | Description |
|-----------|------|-------------|
| `disclose:review_rating` | decimal | Aggregate review score on a 0–5 scale |
| `disclose:review_count` | integer | Total number of reviews included in the aggregate rating |
| `disclose:review_verified_purchase_rate` | decimal | Proportion of reviews attributed to verified purchases (0–1). The most manipulation-resistant of the review signals. |
| `disclose:review_recency_90d_rate` | decimal | Proportion of total reviews submitted within the last 90 days (0–1). Signals active and ongoing customer engagement. |
| `disclose:review_recency_365d_rate` | decimal | Proportion of total reviews submitted within the last 365 days (0–1). Provides a longer-horizon view of review activity relative to lifetime review volume. |
| `disclose:review_platform` | string | The platform from which review data is derived. Recommended values: `own_site`, `google`, `trustpilot`, `yotpo`, `okendo`, `judge_me`, `other`. Agents SHOULD weight reviews from independent platforms higher than merchant-hosted reviews. |
| `disclose:review_response_rate` | decimal | Rate of reviews to which the merchant has posted a public response (0–1). Signals active merchant engagement with buyer feedback. |
| `disclose:negative_review_rate` | decimal | Proportion of total reviews rated 2 stars or below (0–1). More granular than aggregate rating alone. |

---

## Sources

### Purpose

A source declaration identifies the platform, API, or system from which disclosed attributes were derived. Sources are distinct from attestations: a source declares data origin, not cryptographic verification. Agents MAY use source declarations to calibrate confidence in a signal, but source declarations do not create Signatory accountability.

This specification distinguishes three roles:

| Role | Meaning |
|---|---|
| `source_of_record` | The platform, API, database, or system from which the underlying data was retrieved. |
| `computed_by` | The tool, service, or publisher that calculated the signal from the source data. |
| Signatory | An authorized third party that cryptographically signs specified signals within its approved scope. |

The sources array creates a legible upgrade path. A platform appearing in `sources` today MAY become a registered Signatory and appear in `attestations` once formal attestation is established. Agents SHOULD treat the same signal attested by a registered Signatory as materially stronger than the same signal declared only through source metadata.

### Source Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `source_id` | string | Yes | Identifier for the originating platform, for example `shopify`, `woocommerce`, or a primary domain. |
| `source_name` | string | Yes | Human-readable name of the platform or system. |
| `retrieved_at` | string | Yes | RFC 3339 timestamp of when the data was retrieved from the source. |
| `source_type` | string | No | Recommended values: `commerce_platform`, `returns_platform`, `payments_platform`, `shipping_platform`, `reviews_platform`, `registry`, `other`. |
| `attributed_attributes` | array of strings | Yes | List of `disclose:` attribute keys derived from this source. |

### Recommended `source_id` Values

| `source_id` value | Platform |
|---|---|
| `shopify` | Shopify |
| `adobe_commerce` | Adobe Commerce (Magento) |
| `agentforce_commerce` | Agentforce Commerce (Salesforce) |
| `bigcommerce` | BigCommerce |
| `commercetools` | commercetools |
| `woocommerce` | WooCommerce |
| `shopline` | Shopline |

Platforms not listed here SHOULD use their primary domain as the `source_id`, for example `acmeplatform.com`.

Example source entry:

```json
{
  "source_id": "shopify",
  "source_name": "Shopify",
  "source_type": "commerce_platform",
  "retrieved_at": "2026-03-26T00:00:00Z",
  "attributed_attributes": [
    "disclose:product_return_rate",
    "disclose:on_time_shipment_rate",
    "disclose:chargeback_rate",
    "disclose:order_accuracy_rate",
    "disclose:refund_processing_time_median_days"
  ]
}
```

## Attestations

### Purpose

An attestation is a cryptographically signed statement from an authorized Signatory confirming that one or more disclosed attributes have been independently verified against source data or an approved verification method. Attestations distinguish Signatory-accountable signals from self-reported or computed signals.

Merchants MAY publish disclosures without attestations. Unattested attributes may still be useful to agents, but they carry no Signatory accountability.

A Signatory attests only to the specific signals listed in `attested_attributes` and only within its authorized scope in the Signatory Registry. A Signatory does not certify the merchant, require complete Core Commerce Profile coverage, or determine how agents should interpret the signal.

A Signatory is accountable for:

- the signed attribute name
- the disclosed value at the time of attestation
- the source of record or approved verification method
- the methodology version applied
- the observation window, where applicable
- the generated timestamp and attestation timestamp
- signature validity
- revocation status

A Signatory is not accountable for:

- signals the merchant does not expose
- signals outside the Signatory's authorized scope
- agent interpretation
- buyer decisions
- merchant future performance
- commercial outcomes
- other Signatories' attestations

### Attestation Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `signatory_id` | string | Yes | Unique identifier for the Signatory, for example `loop-returns.com`. |
| `signatory_name` | string | Yes | Human-readable name of the Signatory. |
| `attested_attributes` | array of strings | Yes | List of `disclose:` attribute keys this attestation covers. |
| `methodology_versions` | array of strings | Recommended | Methodology versions applied to the attested attributes. |
| `attested_at` | string | Yes | RFC 3339 timestamp of when the attestation was issued. |
| `expires_at` | string | No | RFC 3339 timestamp after which the attestation should no longer be treated as current. |
| `signature` | string | Yes | Base64url-encoded cryptographic signature over the attestation payload. |
| `signing_key_id` | string | Yes | Key ID (`kid`) corresponding to the Signatory's published signing key. |
| `benchmark` | object | No | Optional benchmark context. See [Signatory Benchmarks](#signatory-benchmarks). |

`payment_commitment` is not part of the core attestation object in this version. Signatory compensation mechanisms MAY be defined in a future extension.

Example attestation:

```json
{
  "signatory_id": "loop-returns.com",
  "signatory_name": "Loop Returns",
  "attested_attributes": [
    "disclose:product_return_rate",
    "disclose:return_policy_type",
    "disclose:return_window_days",
    "disclose:refund_processing_time_median_days",
    "disclose:refund_processing_time_p90_days",
    "disclose:exchange_rate"
  ],
  "methodology_versions": ["core-commerce-v0.1"],
  "attested_at": "2026-02-01T00:00:00Z",
  "expires_at": "2026-02-03T00:00:00Z",
  "signature": "eyJhbGciOiJFUzI1NiIsImtpZCI6Imxvb3AtMjAyNiJ9...",
  "signing_key_id": "loop-2026"
}
```

### Attestation Payload

The payload signed by the Signatory is a canonical JSON object containing the merchant domain, Signatory ID, attested attribute values at time of attestation, methodology version, source of record or verification method, observation windows, and timestamps. The `attested_attributes` object contains actual attribute values, not just keys, preventing merchants from changing values after attestation without invalidating the signature.

### Signature Algorithm

Signatories MUST sign attestation payloads using ES256 (ECDSA with P-256 and SHA-256). Signatories MUST publish their signing keys as JWK (JSON Web Key) objects at:

```
/.well-known/disclose-signatory
```

### Future Extension: Signatory Compensation

The framework anticipates future extensions for Signatory compensation, including success-based or outcome-based commercial models. These mechanisms are intentionally excluded from the core disclosure and attestation specification.

## Signatory Registry

### Purpose

The Signatory Registry is the canonical list of authorized Disclose Signatories. Its existence ensures that an attested disclosure carries meaningful weight. Any party claiming to be a Signatory must be publicly listed, with authorized attributes, methodology versions, signing keys, and status visible to agents.

### Registry Discovery

During the maintainer-led phase, the Signatory Registry is published and maintained through the Disclose Framework repository. Once a formal working group, foundation, or standards body is established, registry authority is expected to transition to that governance body.

The registry is available at:

```
https://discloseframework.dev/registry/signatories.json
```

Agents SHOULD cache this registry and refresh it periodically. Agents MUST validate that the `signatory_id` in any attestation appears in the current registry with `status: active` before treating the attestation as Signatory-attested.

### Signatory Listing

| Field | Type | Description |
|-------|------|-------------|
| `signatory_id` | string | Unique identifier, typically matching the Signatory's domain. |
| `signatory_name` | string | Human-readable name. |
| `authorized_attributes` | array of strings | The `disclose:` attributes this Signatory is authorized to attest. |
| `methodology_versions_supported` | array of strings | Methodology versions this Signatory is authorized to use. |
| `keys_url` | string | URL to the Signatory's `/.well-known/disclose-signatory` endpoint. |
| `revocation_url` | string | Optional URL for revocation status or revocation list. |
| `status` | string | One of: `active`, `suspended`, `revoked`. |
| `listed_at` | string | RFC 3339 timestamp of when the Signatory was added to the registry. |
| `suspended_at` | string | Optional RFC 3339 timestamp of suspension. |
| `revoked_at` | string | Optional RFC 3339 timestamp of revocation. |
| `contact` | string | Optional contact or support endpoint for registry issues. |

Example listing:

```json
{
  "signatory_id": "example-payments.com",
  "signatory_name": "Example Payments",
  "authorized_attributes": [
    "disclose:chargeback_rate",
    "disclose:dispute_win_rate"
  ],
  "methodology_versions_supported": ["core-commerce-v0.1"],
  "keys_url": "https://example-payments.com/.well-known/disclose-signatory",
  "revocation_url": "https://example-payments.com/.well-known/disclose-revocations",
  "status": "active",
  "listed_at": "2026-02-01T00:00:00Z"
}
```

### Registry Governance

**Governance status.** Disclose is currently maintained as an open framework. It is intended to graduate into a protocol governed by a working group once there is sufficient participation from merchants, agents, platforms, and Signatories.

**Application.** Any organization seeking Signatory status MUST submit an application to the governing body via [GitHub Issues](https://github.com/disclose-framework/spec/issues) until the formal application process is established at `https://discloseframework.dev/registry/apply`. Applications must include: the applicant's domain, the `disclose:` attributes they seek authorization to attest, methodology versions supported, a description of their data access and verification methodology for each attribute, and their proposed signing key endpoint.

**Review.** The governing body reviews applications for methodology soundness, data access credibility, conflict of interest, signing infrastructure, and revocation process. Review outcomes are published publicly.

**Listing.** Approved Signatories are added to the registry with `status: active`. Signatories MAY NOT attest attributes outside their approved scope or methodology versions.

**Suspension and revocation.** The governing body MAY suspend a Signatory (`status: suspended`) pending investigation, or revoke a Signatory (`status: revoked`) for material misrepresentation, methodology failure, signing failure, or failure to maintain required revocation mechanisms. Agents MUST treat attestations from suspended or revoked Signatories as unverified.

**Appeals.** Signatories subject to suspension or revocation MAY appeal to the governing body within 30 days. The appeal process and outcomes are published publicly.

The eventual working group is expected to govern Core Profile changes, attribute definitions, methodology versions, Signatory registry rules, key rotation and revocation standards, and extension approval.

### Signatory Benchmarks

Signatories may accumulate aggregate data across their merchant base that gives individual merchant disclosures useful context. A return rate of 8% may mean something different in apparel than in consumer electronics. The `benchmark` object allows Signatories to publish that context alongside an attestation.

The `benchmark` object is OPTIONAL. Its absence does not affect attestation validity. Signatories who include it are providing interpretive context, not a score, badge, ranking, certification, endorsement, or recommendation.

| Field | Type | Required | Description |
|---|---|---|---|
| `vertical` | string | Yes | Category label for the merchant's vertical, for example `apparel`, `consumer_electronics`, or `beverage`. |
| `source` | string | Yes | Always `signatory_aggregate` in this version. |
| `p50` | decimal | No | Median value for this signal across the Signatory's merchant portfolio for the stated vertical. |
| `p90` | decimal | No | 90th percentile value for the same population. |
| `sample_size_band` | string | No | Population range, for example `1000-5000`. A band rather than exact count allows Signatories to publish context without exposing precise portfolio data. |

Example attestation with benchmark:

```json
{
  "signatory_id": "loop-returns.com",
  "signatory_name": "Loop Returns",
  "attested_attributes": ["disclose:product_return_rate"],
  "methodology_versions": ["core-commerce-v0.1"],
  "attested_at": "2026-02-01T00:00:00Z",
  "signature": "eyJhbGci...",
  "signing_key_id": "loop-2026",
  "benchmark": {
    "vertical": "apparel",
    "source": "signatory_aggregate",
    "p50": 0.18,
    "p90": 0.32,
    "sample_size_band": "1000-5000"
  }
}
```

## Complete Disclosure Document Example

The following example represents a computed publisher disclosure generated from Shopify API data. It exposes six of seven Core Commerce signals. The missing Core signal is not a conformance failure. Core coverage is descriptive only and is not a score, badge, ranking, certification, endorsement, or recommendation.

```json
{
  "disclose_version": "0.3",
  "merchant_domain": "merchant.example.com",
  "publication_mode": "automated",
  "refresh_frequency": "daily",
  "channel_scope": "dtc",
  "issued_at": "2026-05-14T00:00:00Z",
  "expires_at": "2026-05-16T00:00:00Z",
  "core_profile": {
    "name": "core-commerce",
    "version": "0.1",
    "signals_defined": 7,
    "signals_disclosed": 6,
    "coverage_note": "Core coverage is descriptive only and is not a score, badge, ranking, certification, endorsement, or recommendation."
  },
  "attributes": {
    "disclose:product_return_rate": {
      "value": 0.0006,
      "unit": "ratio",
      "observation_window_days": 90,
      "window_start": "2026-02-13T00:00:00Z",
      "window_end": "2026-05-13T23:59:59Z",
      "generated_at": "2026-05-14T00:00:00Z",
      "next_expected_refresh": "2026-05-15T00:00:00Z",
      "source_of_record": "shopify_api",
      "reported_by": "sure_signal",
      "computed_by": "sure_signal",
      "attestation_level": "computed",
      "methodology_version": "core-commerce-v0.1",
      "attestation": null
    },
    "disclose:on_time_shipment_rate": {
      "value": 0.95,
      "unit": "ratio",
      "observation_window_days": 90,
      "window_start": "2026-02-13T00:00:00Z",
      "window_end": "2026-05-13T23:59:59Z",
      "generated_at": "2026-05-14T00:00:00Z",
      "next_expected_refresh": "2026-05-15T00:00:00Z",
      "source_of_record": "shopify_api",
      "reported_by": "sure_signal",
      "computed_by": "sure_signal",
      "attestation_level": "computed",
      "methodology_version": "core-commerce-v0.1",
      "attestation": null
    },
    "disclose:refund_processing_time_median_days": {
      "value": 2.2,
      "unit": "days",
      "observation_window_days": 90,
      "window_start": "2026-02-13T00:00:00Z",
      "window_end": "2026-05-13T23:59:59Z",
      "generated_at": "2026-05-14T00:00:00Z",
      "next_expected_refresh": "2026-05-15T00:00:00Z",
      "source_of_record": "shopify_api",
      "reported_by": "sure_signal",
      "computed_by": "sure_signal",
      "attestation_level": "computed",
      "methodology_version": "core-commerce-v0.1",
      "attestation": null
    },
    "disclose:chargeback_rate": {
      "value": 0.0002,
      "unit": "ratio",
      "observation_window_days": 90,
      "window_start": "2026-02-13T00:00:00Z",
      "window_end": "2026-05-13T23:59:59Z",
      "generated_at": "2026-05-14T00:00:00Z",
      "next_expected_refresh": "2026-05-15T00:00:00Z",
      "source_of_record": "shopify_api",
      "reported_by": "sure_signal",
      "computed_by": "sure_signal",
      "attestation_level": "computed",
      "methodology_version": "core-commerce-v0.1",
      "attestation": null
    },
    "disclose:dispute_win_rate": {
      "value": 0.98,
      "unit": "ratio",
      "observation_window_days": 90,
      "window_start": "2026-02-13T00:00:00Z",
      "window_end": "2026-05-13T23:59:59Z",
      "generated_at": "2026-05-14T00:00:00Z",
      "next_expected_refresh": "2026-05-15T00:00:00Z",
      "source_of_record": "shopify_api",
      "reported_by": "sure_signal",
      "computed_by": "sure_signal",
      "attestation_level": "computed",
      "methodology_version": "core-commerce-v0.1",
      "attestation": null
    },
    "disclose:platform_seller_tenure_days": {
      "value": 3862,
      "unit": "days",
      "generated_at": "2026-05-14T00:00:00Z",
      "source_of_record": "shopify_api",
      "reported_by": "sure_signal",
      "computed_by": "sure_signal",
      "attestation_level": "computed",
      "methodology_version": "core-commerce-v0.1",
      "disclose:platform_seller_tenure_platform": "shopify",
      "attestation": null
    }
  },
  "signal_status": [
    {
      "attribute": "disclose:order_accuracy_rate",
      "status": "not_available",
      "reason": "source_system_does_not_provide_required_data"
    }
  ],
  "sources": [
    {
      "source_id": "shopify",
      "source_name": "Shopify",
      "source_type": "commerce_platform",
      "retrieved_at": "2026-05-14T00:00:00Z",
      "attributed_attributes": [
        "disclose:product_return_rate",
        "disclose:on_time_shipment_rate",
        "disclose:refund_processing_time_median_days",
        "disclose:chargeback_rate",
        "disclose:dispute_win_rate",
        "disclose:platform_seller_tenure_days"
      ]
    }
  ],
  "attestations": []
}
```

### Manual Snapshot Example

Manual snapshots MAY be used to validate that signals can be read by agents. A manual snapshot MUST declare that it is not automatically refreshed.

```json
{
  "disclose_version": "0.3",
  "merchant_domain": "merchant.example.com",
  "publication_mode": "manual_snapshot",
  "refresh_frequency": "none",
  "issued_at": "2026-05-14T00:00:00Z",
  "expires_at": "2026-05-21T00:00:00Z",
  "note": "Manual pull used for validation. This document does not imply daily refresh."
}
```

## Security

### Transport Security

All Disclose endpoints MUST be served over HTTPS. HTTP requests MUST be rejected or redirected.

### Freshness Verification

Agents SHOULD evaluate `issued_at`, `expires_at`, `generated_at`, `window_start`, `window_end`, and `refresh_frequency` before relying on a signal.

For automated Core Commerce disclosures, agents SHOULD treat a signal as stale when `generated_at` exceeds the expected refresh interval by more than 24 hours, unless the document explicitly declares a longer permitted interval.

Manual snapshots MUST declare `publication_mode: "manual_snapshot"` and MUST NOT imply daily refresh. Agents SHOULD treat manual snapshots as validation or demonstration artifacts unless their own policies allow manual snapshots in production decisioning.

### Signature Verification

Agents MUST verify attestation signatures before treating any attested attribute as Signatory-attested. The verification flow is:

1. Fetch the Signatory Registry and confirm the `signatory_id` is listed with `status: active`.
2. Confirm the attested attributes are within the Signatory's `authorized_attributes`.
3. Confirm the methodology version is within the Signatory's `methodology_versions_supported`.
4. Fetch the Signatory's signing keys from their `keys_url`.
5. Locate the key matching `signing_key_id`.
6. Reconstruct the canonical attestation payload.
7. Verify the ES256 signature against the payload using the public key.
8. Confirm `attested_at` is in the past and `expires_at` (if present) is in the future.
9. Check revocation status where the Signatory publishes a revocation endpoint.

Agents MUST reject attestations that fail any step of this verification flow.

### Domain Binding

The `merchant_domain` field in the disclosure document MUST match the domain from which the document was served. Agents MUST reject documents where these do not match.

### Replay Prevention

Attestations include `attested_at` and `expires_at` timestamps. Agents SHOULD treat expired attestations as unverified.

### Merchant Impersonation and Attestation Replay

A fraudster operating an impersonation domain MAY copy a legitimate merchant's disclosure document verbatim, including any attested signals. The `merchant_domain` field requirement invalidates copied documents where the field is present and correctly set. However, agents MUST NOT rely solely on the `merchant_domain` field as fraud protection. DNS-level verification that the serving domain is the legitimate merchant domain is a TLS and network concern outside the scope of this framework.

The primary defense against attestation replay is the domain-binding requirement in the Signatory signature payload. Signatories MUST include the merchant's canonical domain in the signed attestation payload. Copying an attestation to a different domain produces a signature that fails verification.

Agents MUST perform full signature verification as specified. Agents MUST NOT shortcut verification by trusting the `merchant_domain` field without also verifying the Signatory signature covers that domain.

### Multi-Domain Merchants

A merchant operating across multiple regional storefronts, for example `brandname.com`, `brandname.ca`, and `brandname.com.au`, MAY hold attestations covering more than one domain. In this case, the Signatory signature MUST cover an explicit `verified_domains` array rather than a single domain field. The serving domain MUST appear in the `verified_domains` array for the attestation to be considered valid.

Each domain's inclusion in `verified_domains` reflects explicit Signatory confirmation of data coverage for that storefront. It is not merchant self-declaration. Signatories MUST NOT include a domain in `verified_domains` unless they hold independent performance data for that storefront. Signatories SHOULD NOT treat regional storefronts and operationally distinct brand domains, such as a mainline store and an outlet store, as equivalent for attestation purposes.

### Attestation Revocation

Signatories MUST maintain a mechanism to revoke attestations before their `expires_at` date where a merchant's underlying data has changed materially, where the attestation was issued in error, or where the Signatory's authorization scope has changed. Signatories SHOULD publish a revocation endpoint or revocation list at a stable URL declared in the Signatory Registry entry.

Agents SHOULD check revocation status where a Signatory publishes a revocation endpoint. Agents MAY treat an unexpired attestation as valid where no revocation endpoint is available, but SHOULD note this limitation when surfacing attested signals.

### Verification Performance

Cryptographic signature verification is local computation performed against data already retrieved in the disclosure document fetch. It does not require an additional network request in the common case where the Signatory's public key is cached. Added latency is negligible and does not materially affect agent transaction timing. Agents SHOULD cache Signatory public keys with a refresh interval consistent with the Signatory's published key rotation policy.

## Governance Status

Disclose is currently published as the Disclose Framework, not the Disclose Protocol. This distinction is intentional.

The Framework is maintainer-led during early development while the Core Commerce Profile, reference implementations, merchant publishing model, agent consumption model, and Signatory model are validated through implementation. Protocol governance should be earned by implementation, not declared before adoption.

The Framework is intended to graduate into the Disclose Protocol once there is sufficient participation from merchants, agent developers, commerce platforms, infrastructure providers, and Signatories to support neutral working group governance.

During the maintainer-led phase, all material governance actions SHOULD be conducted publicly through the Disclose Framework repository. This includes specification updates, methodology changes, Signatory applications, registry additions, registry suspensions, registry revocations, and material changes to reference implementations.

The maintainer-led phase is transitional. It exists to validate the standard, establish the Core Commerce Profile, prove that agents can consume merchant operating signals, onboard early merchant publishers, and develop the Signatory Registry model before formal protocol governance is introduced.

### Future Working Group

A future Disclose Working Group is expected to govern:

- Core Profile changes
- Attribute definitions
- Methodology versions
- Signatory authorization rules
- Signatory Registry admission, suspension, and revocation rules
- Signing key rotation and revocation standards
- Extension approval
- Conformance and validation requirements
- Future protocol releases

The working group SHOULD include representation from multiple participant classes, including merchants, agent developers, commerce platforms, infrastructure providers, Signatories, and independent technical contributors.

No single merchant, platform, Signatory, agent provider, or commercial implementation SHOULD control the standard.

### Governance Principles

Disclose governance SHOULD follow these principles:

- Public process for material changes
- Attribute-level Signatory authorization rather than broad institutional approval
- Published methodology requirements for each authorized signal
- Clear separation between signal publication, signal attestation, and agent interpretation
- Appeal path for Signatory suspension or revocation
- Separation between commercial implementations and protocol governance
- Preservation of merchant sovereignty and selective disclosure
- No framework-assigned scores, badges, rankings, certifications, or recommendations

### Maintainer-Led Registry Operations

During the maintainer-led phase, the Signatory Registry is maintained through the Disclose Framework repository. Once a formal working group, foundation, or standards body is established, registry authority is expected to transition to that governance body.

Signatory approval is attribute-scoped. A Signatory MAY be authorized for one attribute, a group of attributes, or a methodology version. Signatory approval MUST NOT be interpreted as general certification of the Signatory or of any merchant.

Registry decisions SHOULD be public, scoped, and appealable. Agents SHOULD rely on the registry only to determine whether a Signatory is authorized to attest specific signals under specific methodology versions. The registry does not determine whether a merchant is reliable, preferred, trustworthy, or safe.

## Agent Consumption Guidelines

Agents consuming Disclose data operate with significant discretion. The framework does not mandate how agents weight or surface disclosure signals. This is intentionally left to the platform and agent developer. The following requirements and recommendations preserve the framework's neutrality:

- Agents MUST NOT represent Core coverage as a score, badge, ranking, certification, endorsement, or recommendation.
- Agents MUST NOT assume an absent Core signal indicates poor merchant performance, merchant concealment, or non-compliance.
- Agents MUST verify Signatory status, authorization scope, methodology version, and signature before treating a signal as Signatory-attested.
- Agents SHOULD distinguish disclosed signals from absent signals.
- Agents SHOULD distinguish `none`, `computed`, and `signatory` attestation levels when surfacing or weighting signals.
- Agents SHOULD evaluate `generated_at`, `window_start`, `window_end`, `expires_at`, and `refresh_frequency` before relying on a signal.
- Signals with `attestation_level: none` should be surfaced as merchant-reported and weighted accordingly.
- Signals with `attestation_level: computed` should be surfaced as platform-derived or computed, with higher confidence than merchant-entered data but below independently attested signals.
- Signals with `attestation_level: signatory` should be surfaced as independently attested, with the Signatory named when relevant to the buyer.
- Review signals should be distinguished from operational metrics when surfaced to buyers. Agents SHOULD treat `disclose:review_rating` as contextual rather than authoritative, and SHOULD surface `disclose:review_verified_purchase_rate` and recency signals alongside it wherever possible.
- Missing disclosures may be surfaced as `disclosure unavailable` or similar neutral language rather than assumed positive or negative.
- Agents SHOULD NOT represent Disclose-derived aggregations as Disclose scores, Disclose badges, Disclose certifications, or Disclose rankings.
- Agents SHOULD NOT penalize merchants for not disclosing specific attributes unless disclosure of that attribute is required by applicable law or platform policy.

Agents MAY use Disclose signals as inputs into their own recommendation logic, provided they do not imply that Disclose itself produced the recommendation or verdict.

## Reference Implementation

To support adoption and validate the specification, the Disclose Framework provides the following reference resources at `https://github.com/disclose-framework/spec`:

- **JSON Schema:** A machine-readable schema for validating disclosure documents against the specification.
- **Validator:** A reference validator that checks a disclosure document for schema compliance, domain binding, Core signal metadata completeness, 90-day trailing windows for Core signals, daily refresh declaration for automated publishers, manual snapshot declaration where applicable, methodology version presence, source-of-record structure, and attestation scope consistency.
- **Sample document:** A complete, valid example disclosure document suitable for testing agent consumption logic.
- **Signatory mock:** A lightweight mock Signatory endpoint for testing signature verification flows without a live Signatory integration.

Implementations that conform to the specification and pass the reference validator MAY self-identify as Disclose-compatible. They MUST NOT self-identify as Disclose-certified unless a future certification programme is formally defined.

## Versioning

Disclose uses semantic versioning in the format `MAJOR.MINOR`, for example `0.3` or `1.0`. The framework version is declared in the disclosure document via the `disclose_version` field.

Profiles and methodologies are versioned separately from the framework specification. For example:

```json
{
  "disclose_version": "0.3",
  "core_profile": {
    "name": "core-commerce",
    "version": "0.1"
  },
  "methodology_version": "core-commerce-v0.1"
}
```

The following changes MAY be introduced without a framework version increment: adding new optional attributes, adding new optional attestation fields, adding new Signatory entries to the registry, or adding a new optional profile.

The following changes SHOULD result in a new MINOR version: adding a new Core Commerce Profile version, adding new required metadata for newly defined profiles, or materially clarifying methodology requirements without breaking existing documents.

The following changes MUST result in a new MAJOR version: removing or renaming existing attributes, changing the attestation payload structure or signature algorithm, modifying the discovery endpoint path, or changing required fields in a way that breaks existing conformant documents.

## Glossary

| Term | Definition |
|------|------------|
| Agent | A platform, AI assistant, or automated system that queries Disclose data on behalf of a buyer. |
| Attestation | A cryptographically signed statement from a Signatory confirming that specific disclosed attributes have been independently verified against source data or an approved verification method. |
| Attestation Level | A field on every signal object declaring how the value was produced. One of: `none` (merchant self-reported), `computed` (derived from source data by a computed publisher), or `signatory` (cryptographically signed by an authorized Signatory). |
| Automated Publisher | A publisher that generates and refreshes disclosures through an automated process. Automated Core Commerce disclosures SHOULD refresh daily. |
| Benchmark Reference | An optional object within a Signatory attestation providing vertical or category-level signal distributions derived from the Signatory's merchant portfolio. Intended to give agents interpretive context, not a score. |
| Computed Publisher | A tool or service that calculates disclosed signals from a source of record without cryptographic Signatory accountability, for example Sure Signal computing Shopify API-derived signals. |
| Core Commerce Profile | The first standard Disclose profile for agentic commerce. Version 0.1 defines seven optional merchant operating signals. Merchants may disclose any subset. |
| Core Coverage | A descriptive count of how many Core Commerce signals are present in a disclosure document. Core coverage is not a score, badge, ranking, certification, endorsement, or recommendation. |
| Disclosure Document | The JSON document published by a merchant at `/.well-known/disclose`. |
| Emergent Trust | The principle that trustworthiness arises from visible, verifiable behaviour and agent interpretation rather than from framework-assigned scores or badges. |
| Exchange Rate | The proportion of return transactions where the buyer selected a replacement item rather than a refund; a signal of product confidence distinct from the return rate. |
| Item | The product or service being transacted. Maps to `schema:ItemOffered`, the schema.org parent type that encompasses both physical goods (`schema:Product`) and services (`schema:Service`). |
| Manual Snapshot | A disclosure document generated manually for testing, validation, onboarding, or demonstration. Manual snapshots MUST declare `publication_mode: "manual_snapshot"` and MUST NOT imply daily refresh. |
| Merchant | The seller or service provider publishing disclosure signals. Maps to `schema:Organization`. Signals published at Merchant scope reflect aggregate operational performance across the merchant's transactions. |
| Merchant Sovereignty | The principle that merchants retain full control over what they disclose, to whom, and when. |
| Methodology Version | A version identifier declaring the calculation method applied to a signal, for example `core-commerce-v0.1`. |
| Observation Window | The time period over which a metric is computed. Core Commerce signals MUST use a trailing 90-day observation window unless a future profile version explicitly defines otherwise. |
| Offer | The intersection of a specific Merchant and a specific Item. Maps to `schema:Offer`. Signals published at Offer scope reflect how a particular Merchant performs on a particular Item. |
| Payment Commitment | A future extension concept for Signatory compensation. It is not part of the core attestation object in this version. |
| Progressive Enhancement | The ability to begin participation with a single attribute and expand disclosures over time. |
| Review Recency | The proportion of a merchant's total reviews submitted within a recent time window, used to assess the freshness of aggregate review ratings. |
| Selective Disclosure | The ability to disclose specific attributes without an all-or-nothing requirement. A merchant may publish any subset of Core Commerce signals. |
| Signal Absence | The absence of a signal from a disclosure document. Absence has no protocol-defined meaning and MUST NOT be assumed to indicate poor performance, concealment, or non-compliance. |
| Signal Status | Optional metadata that explains why a Core signal is not disclosed, such as `not_available`, `insufficient_volume`, or `not_applicable`. |
| Signatory | An authorized third party that cryptographically signs attestations for specific merchant signals within an approved registry scope. A Signatory is accountable for signed signals, not for agent interpretation or merchant certification. |
| Signatory Registry | The canonical, publicly accessible list of authorized Disclose Signatories maintained by the framework governing body. |
| Source of Record | The platform, API, database, or system from which the underlying data for a signal was retrieved, for example Shopify API, a payment processor, or a returns platform. |

