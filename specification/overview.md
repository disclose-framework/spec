# Disclose Framework — Official Specification

## Overview

The Disclose Framework is an open standard for merchant disclosure attestations designed for the emerging era of agentic commerce. As AI agents increasingly act as intermediaries between buyers and merchants — researching products, comparing options, and making or informing purchasing recommendations — they require structured, machine-readable, and verifiable information about merchant practices before they can responsibly recommend where to buy.

Disclose provides that infrastructure layer. It enables AI agents, platforms, and automated systems to access verified, machine-readable information about merchant practices — including return policies, fulfillment performance, review authenticity, and other behavioural signals — when making or informing purchasing decisions on behalf of buyers.

Disclose operates as a disclosure layer that sits below discovery and above the transaction. Before an agent decides where to buy, Disclose provides the structured signal data needed to make a confident recommendation. It does not process payments, manage checkout sessions, or execute transactions. Its sole function is to standardize how merchants publish verified disclosures and how agents consume them.

---

## Overarching Guidelines

The key words MUST, MUST NOT, REQUIRED, SHALL, SHALL NOT, SHOULD, SHOULD NOT, RECOMMENDED, MAY, and OPTIONAL in this document are to be interpreted as described in RFC 2119 and RFC 8174.

Schema notes:

- **Date format:** Always specified as RFC 3339 unless otherwise specified.
- **Numeric values:** Expressed as decimals unless otherwise noted (e.g., 0.92 for 92%).
- **Rates and ratios:** Always expressed as a decimal between 0 and 1 (e.g., 0.06 for 6%).
- **Time-bounded metrics:** MUST include a `_period_days` companion field declaring the observation window. The default observation window is 90 days unless otherwise specified.
- **Measurement methodology:** Where a metric's value depends on how it is computed, the attesting Signatory's methodology governs. Agents SHOULD consider the Signatory's stated methodology when interpreting attested values, particularly for attributes where platform definitions vary.

---

## Design Philosophy

### Trust Is Emergent, Not Engineered

The Disclose Framework does not produce trust scores, badges, tiers, or rankings. It produces structured, verifiable facts about merchant behaviour. Trust emerges from those facts as agents and buyers draw their own conclusions.

This is a deliberate architectural choice with three consequences:

**Merchants disclose behaviour, not claims.** Every attribute in the Disclose schema is grounded in operational outcomes — repeat purchases, return rates, fulfillment accuracy, chargeback rates. These are things that happened, not assertions about quality or intent.

**The framework enforces structure, not interpretation.** Disclose defines what attributes mean, how they are measured, and how they are verified. It does not define how agents should weight them, combine them, or surface them to buyers. That discretion belongs to the platform.

**No centralized authority renders verdicts.** There is no "Disclose Score." There is no tier that grants a badge. A merchant that publishes a low return rate, high on-time shipment rate, and fast refund processing becomes intuitively trustworthy — not because a framework said so, but because the evidence is visible and verifiable.

This philosophy also protects against gaming. Scores and badges create targets. Raw, time-bounded, Signatory-attested metrics are far harder to manipulate without changing actual operations.

### Self-Reported Attribute Integrity

Merchants MAY publish disclosures without Signatories. Self-reported attributes carry no third-party verification and agents SHOULD treat them accordingly. Merchants MAY declare the platform origin of self-reported attributes using the sources array. Source declarations do not constitute attestation. The framework does not currently define a formal dispute process for false self-reported disclosures; however, platforms consuming Disclose data MAY implement their own policies for flagging or deprioritizing merchants whose self-reported attributes are demonstrably inconsistent with other observable signals. A future extension to this specification will define a community-based flagging and review process.

---

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

A core principle of the Disclose Framework is that merchants retain full sovereignty over their disclosures. Participation is voluntary. Merchants choose which attributes to disclose, which Signatories to authorize, and when disclosures are updated or removed. The framework standardizes the format and verification mechanism — not the content or extent of disclosure. By default, all signals reflect DTC performance only. Merchants with multi-channel operations can declare additional channels using channel_scope.

### Selective Disclosure

There is no all-or-nothing requirement. A merchant may publish a single attribute and add additional attributes over time as their business matures or as competitive incentives emerge. This progressive enhancement model lowers the barrier to participation while preserving the integrity of the standard.

### Attestation Tiers

Every signal in a disclosure document carries an `attestation_level` field declaring how the value was produced:

| `attestation_level` | Meaning |
|---|---|
| `none` | Merchant self-reported. No third-party computation or signature. Agents SHOULD weight accordingly. |
| `computed` | Pulled from a platform API and calculated by a third-party tool (e.g., Sure Signal from Shopify API). Not cryptographically signed. Harder to manipulate than merchant-entered data, but carries no Signatory accountability. |
| `signatory` | Cryptographically signed by an authorized Signatory with direct access to source data. The Signatory's reputation is staked on the value. |

Agents SHOULD use `attestation_level` as the primary signal weighting input before evaluating the value itself.

### Credentialed Query (Anticipated Extension)

Some merchants may hold operational signals they are willing to share with verified agents but not publish in a public disclosure document. The current specification does not define a mechanism for this. A future extension will define a credentialed query path — allowing agents with verified identity to request non-public attributes directly from a merchant's infrastructure. Merchants who wish to signal this capability in advance MAY include a disclose:credentialed_query_supported: true attribute in their public disclosure document. No further behaviour is defined for this attribute in the current version.

### Commerce Risk Coverage

The standard attribute set is designed to address the core risks an agent must evaluate before recommending a purchase:

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

---

## Disclosure Scopes

The Disclose Framework organizes disclosure signals across three scopes. Every `disclose:` property belongs to one or more scopes. The scope is determined by the schema.org node type to which the property is attached — no additional metadata is required.

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
  "disclose:product_return_rate": 0.07,
  "disclose:product_return_rate_period_days": 90,

  "makesOffer": [
    {
      "@type": "Offer",
      "itemOffered": {
        "@type": "Product",
        "gtin": "00012345678905"
      },
      "disclose:product_return_rate": 0.03,
      "disclose:product_return_rate_period_days": 90,
      "disclose:inventory_accuracy_rate": 0.99,
      "disclose:inventory_accuracy_rate_period_days": 90,
      "disclose:avg_ship_days_sku": 1.4
    }
  ]
}
```

In this example, the agent can observe that while the Merchant's overall return rate is 7%, the return rate for this specific SKU is 3% — a materially stronger signal for a purchase recommendation on this Item.

### Item-Scope Signals

The following attributes are particularly well-suited to Item scope, as they reflect properties intrinsic to the item rather than aggregate merchant behaviour. These are natural targets for brand registries, manufacturer databases, and product data platforms:

| Attribute | Item-scope meaning |
|---|---|
| `disclose:business_registration_verified` | Whether the seller is an authorized reseller of this Item's brand |
| `disclose:sustainability_certified` | Whether this specific Item carries a sustainability certification |
| `disclose:product_defect_rate` | Known defect rate for this Item across all sellers |
| `disclose:return_policy_type` | Return policy specific to this Item (e.g., non-returnable electronics) |

*The framework anticipates that dedicated Item-scope attributes — including authorized reseller status and product-level recall signals — will be formally defined in a future version of this specification.*

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

Agents MUST NOT require a disclosure document to be present in order to complete a transaction. The absence of a disclosure document is itself a signal; agents MAY surface this to buyers or use it in ranking logic.

---

## Disclosure Document Structure

### Top-Level Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `disclose_version` | string | Yes | Specification version (e.g., `"0.2"`) |
| `merchant_domain` | string | Yes | The canonical domain of the merchant (e.g., `"merchant.example.com"`) |
| `issued_at` | string | Yes | RFC 3339 timestamp of when this document was generated |
| `expires_at` | string | No | RFC 3339 timestamp after which agents SHOULD re-fetch |
| `channel_scope` | string | No | Declares the channel(s) reflected by signals in this document. Values: `dtc`, `all_direct`, `all_channels`. Default if absent: `dtc`. |
| `attributes` | object | Yes | Map of disclosed merchant attributes. Each attribute is an object containing `value`, `attestation_level`, and optional provenance fields. |
| `sources` | array | No | Array of platform source objects declaring the origin of specific self-reported attributes. Source declarations do not constitute attestation. Agents MAY use source declarations to calibrate confidence in self-reported signals. |
| `attestations` | array | No | Array of Signatory attestation objects |

### Attribute Namespace

All disclosure attributes exist in the `disclose:` namespace. Each attribute is published as an object with the following fields:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `value` | varies | Yes | The signal value |
| `observation_window_days` | integer | For time-bounded metrics | Observation window in days |
| `reported_by` | string | Yes | Who reported this value: `merchant` or the Signatory domain |
| `source` | string | No | Platform API the value was derived from (e.g., `shopify_api`) |
| `computed_by` | string | No | Tool or service that computed the value (e.g., `sure_signal`) |
| `attestation_level` | string | Yes | One of: `none`, `computed`, `signatory` |
| `attestation` | object or null | Yes | Null for `none` and `computed` tiers. Signatory attestation object for `signatory` tier. |

Each time-bounded metric MUST include `observation_window_days`. Agents MUST ignore unknown fields without error.

---

## Standard Attributes

The following attributes are defined in this version of the specification. All are optional unless noted. Time-bounded metrics default to a 90-day observation window unless `observation_window_days` specifies otherwise.

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

---

### 1. Product Quality

Operational signals about product performance derived from post-purchase behaviour. These reflect what buyers actually did — returned, repurchased, reported defective — rather than what they said.

| Attribute | Type | Description |
|-----------|------|-------------|
| `disclose:repeat_purchase_rate` | decimal | Rate of buyers who make a second purchase within the observation window (0–1) |
| `disclose:product_return_rate` | decimal | Rate of units returned across all orders (0–1). Measured as returned units divided by shipped units. May be disclosed at SKU or category level. |
| `disclose:product_defect_rate` | decimal | Rate of units reported defective or dead-on-arrival at delivery (0–1). Distinct from return rate: captures manufacturing and quality control failures before buyer decision. |
| `disclose:size_accuracy_rate` | decimal | Rate of orders where the delivered item matched the size or fit specified at purchase (0–1). Primarily relevant for apparel, footwear, and sized goods. Derived from return reason codes where available. |

> **Measurement note — return rate:** Measured as returned units divided by total shipped units within the observation window. Exchanges (where the buyer selects a replacement item) are NOT counted as returns. Returnless refunds where no item is physically returned ARE counted. Where a Signatory attests this attribute, the Signatory's methodology governs.

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

Signals about whether products are actually available when an agent attempts to purchase. Inventory failures are a critical agentic commerce failure mode — an agent that recommends an out-of-stock product, or places an order against inaccurate inventory, has failed the buyer regardless of all other merchant quality signals.

| Attribute | Type | Description |
|-----------|------|-------------|
| `disclose:in_stock_rate` | decimal | Rate at which listed products are in stock at the time of order placement (0–1), measured across all active SKUs within the observation window. |
| `disclose:stockout_frequency_rate` | decimal | Rate of active SKUs that experienced at least one stockout during the observation window (0–1). |
| `disclose:backorder_rate` | decimal | Proportion of orders placed against backordered inventory (0–1). Agents SHOULD surface this to buyers who have expressed time-sensitivity. |
| `disclose:inventory_accuracy_rate` | decimal | Rate at which displayed inventory levels match actual warehouse counts at the time of order (0–1). Mismatches result in post-order cancellations — a significant buyer trust failure. |
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

Signals about the quality, speed, and accessibility of the merchant's customer support. For agentic purchases, post-purchase support access is a material risk factor — an agent that cannot escalate a buyer issue has limited recourse.

| Attribute | Type | Description |
|-----------|------|-------------|
| `disclose:support_resolution_time_median_hours` | decimal | Median hours from support contact initiation to issue resolution |
| `disclose:support_resolution_time_p90_hours` | decimal | 90th percentile hours from support contact to resolution |
| `disclose:support_channel_availability` | array of strings | Support channels available to buyers. Recommended values: `live_chat`, `email`, `phone`, `sms`, `social`, `self_serve`. |
| `disclose:support_hours_coverage` | string | Hours during which live support is available. Recommended values: `24_7`, `business_hours`, `extended_hours`, `async_only`. |
| `disclose:first_contact_resolution_rate` | decimal | Rate of support contacts resolved without requiring a follow-up interaction (0–1). A strong signal of support quality and operational maturity. |

---

### 8. Pricing & Conversion

Signals about pricing integrity and buyer behaviour. These attributes help agents distinguish merchants with stable, honest pricing from those engaged in discount theater — artificial inflation followed by manufactured discounts.

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

Signals that help agents distinguish legitimate merchants from fraudulent storefronts, impersonation attempts, and fly-by-night operators. This is the category most resistant to gaming: the signals are grounded in external registries — business registration databases, domain history, trademark records — rather than behavioral data the merchant controls. As agentic commerce scales, counterfeit merchant risk becomes a material threat vector that no existing trust signal framework addresses.

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

A source declaration identifies the platform or system from which specific self-reported attributes were derived. Sources are distinct from attestations: a source declares data origin, not cryptographic verification. Agents MAY use source declarations to calibrate confidence in self-reported signals — platform-derived data is harder to manipulate than merchant-entered data, but carries no Signatory accountability.

The sources array creates a legible upgrade path. A platform appearing in `sources` today MAY become a registered Signatory and appear in `attestations` once formal attestation is established. Agents SHOULD treat the same signal attested by a registered Signatory as materially stronger than the same signal declared via a source entry.

### Source Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `source_id` | string | Yes | Identifier for the originating platform (e.g., `"shopify"`, `"lightspeed"`) |
| `source_name` | string | Yes | Human-readable name of the platform |
| `retrieved_at` | string | Yes | RFC 3339 timestamp of when the data was retrieved from the platform |
| `attributed_attributes` | array of strings | Yes | List of `disclose:` attribute keys derived from this source |

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

Platforms not listed here SHOULD use their primary domain as the `source_id` (e.g., `"acmeplatform.com"`).

Example source entry:
```json
{
  "source_id": "shopify",
  "source_name": "Shopify",
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

---

## Attestations

### Purpose

An attestation is a cryptographically signed statement from an authorized Signatory confirming that one or more disclosed attributes have been independently verified against source data. Attestations distinguish Disclose from self-reported signals that can be easily manipulated.

Merchants MAY publish disclosures without attestations. Unattested attributes are self-reported and agents SHOULD treat them accordingly. Attested attributes carry the reputational weight of the signing Signatory.

### Attestation Object

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `signatory_id` | string | Yes | Unique identifier for the Signatory (e.g., `"loop-returns.com"`) |
| `signatory_name` | string | Yes | Human-readable name of the Signatory |
| `attested_attributes` | array of strings | Yes | List of `disclose:` attribute keys this attestation covers |
| `attested_at` | string | Yes | RFC 3339 timestamp of when the attestation was issued |
| `expires_at` | string | No | RFC 3339 timestamp after which the attestation should no longer be trusted |
| `signature` | string | Yes | Base64url-encoded cryptographic signature over the attestation payload |
| `signing_key_id` | string | Yes | Key ID (`kid`) corresponding to the Signatory's published signing key |
| `payment_commitment` | object or null | No | Optional payment routing instruction for outcome-based Signatory compensation. When present, declares the Signatory's fee terms and routing destination. Full mechanism defined in a future extension. MAY be `null` in this version. |

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
  "attested_at": "2026-02-01T00:00:00Z",
  "expires_at": "2026-08-01T00:00:00Z",
  "signature": "eyJhbGciOiJFUzI1NiIsImtpZCI6Imxvb3AtMjAyNiJ9...",
  "signing_key_id": "loop-2026",
  "payment_commitment": null
}
```

### Attestation Payload

The payload signed by the Signatory is a canonical JSON object containing the merchant domain, Signatory ID, attested attribute values at time of attestation, and timestamps. The `attested_attributes` object contains actual attribute values — not just keys — preventing merchants from changing values after attestation without invalidating the signature.

### Signature Algorithm

Signatories MUST sign attestation payloads using ES256 (ECDSA with P-256 and SHA-256). Signatories MUST publish their signing keys as JWK (JSON Web Key) objects at:
```
/.well-known/disclose-signatory
```

---

## Signatory Registry

### Purpose

The Signatory Registry is the canonical list of authorized Disclose Signatories. Its existence ensures that an attested disclosure carries meaningful weight — any party claiming to be a Signatory must be publicly listed, with their signing keys published and auditable.

### Registry Discovery

The Signatory Registry is published and maintained by the Disclose Framework governing body at:
```
https://discloseframework.dev/registry/signatories.json
```

Agents SHOULD cache this registry and refresh it periodically. Agents MUST validate that the `signatory_id` in any attestation appears in the current registry before treating the attestation as trusted.

### Signatory Listing

| Field | Type | Description |
|-------|------|-------------|
| `signatory_id` | string | Unique identifier (matches the Signatory's domain) |
| `signatory_name` | string | Human-readable name |
| `signable_attributes` | array of strings | The `disclose:` attributes this Signatory is authorized to attest |
| `keys_url` | string | URL to the Signatory's `/.well-known/disclose-signatory` endpoint |
| `status` | string | One of: `active`, `suspended`, `revoked` |
| `listed_at` | string | RFC 3339 timestamp of when the Signatory was added to the registry |

### Registry Governance

**Application.** Any organization seeking Signatory status MUST submit an application to the governing body via [GitHub Issues](https://github.com/disclose-framework/spec/issues) until the formal application process is established at `https://discloseframework.dev/registry/apply`. Applications must include: the applicant's domain, the `disclose:` attributes they seek authorization to attest, a description of their data access and verification methodology for each attribute, and their proposed signing key endpoint.

**Review.** The governing body will review applications for methodology soundness, data access credibility, and potential conflicts of interest. Review outcomes are published publicly.

**Listing.** Approved Signatories are added to the registry with `status: active`. Signatories MAY NOT attest attributes outside their approved scope.

**Suspension and Revocation.** The governing body MAY suspend a Signatory (`status: suspended`) pending investigation, or revoke a Signatory (`status: revoked`) for material misrepresentation or methodology failure. Agents MUST treat attestations from suspended or revoked Signatories as unverified.

**Appeals.** Signatories subject to suspension or revocation MAY appeal to the governing body within 30 days. The appeal process and outcomes are published publicly.

### Signatory Benchmarks

Signatories accumulate aggregate data across their merchant base that gives individual merchant disclosures meaningful context. A return rate of 8% means something different in apparel than in consumer electronics. The `benchmark` object allows Signatories to publish that context alongside an attestation.

The `benchmark` object is OPTIONAL. Its absence does not affect attestation validity. Signatories who include it are providing interpretive context, not a scoring input.

| Field | Type | Required | Description |
|---|---|---|---|
| `vertical` | string | Yes | Category label for the merchant's vertical (e.g., `apparel`, `consumer_electronics`, `beverage`) |
| `source` | string | Yes | Always `signatory_aggregate` in this version |
| `p50` | decimal | No | Median value for this signal across the Signatory's merchant portfolio for the stated vertical |
| `p90` | decimal | No | 90th percentile value for the same population |
| `sample_size_band` | string | No | Population range (e.g., `"1000-5000"`). A band rather than exact count, allowing Signatories to publish context without exposing precise portfolio data. |

Example attestation with benchmark:
```json
{
  "signatory_id": "loop-returns.com",
  "signatory_name": "Loop Returns",
  "attested_attributes": ["disclose:product_return_rate"],
  "attested_at": "2026-02-01T00:00:00Z",
  "signature": "eyJhbGci...",
  "signing_key_id": "loop-2026",
  "benchmark": {
    "vertical": "apparel",
    "source": "signatory_aggregate",
    "p50": 0.18,
    "p90": 0.32,
    "sample_size_band": "1000-5000"
  },
  "payment_commitment": null
}
```

---

## Complete Disclosure Document Example

```json
{
  "disclose_version": "0.2",
  "merchant_domain": "merchant.example.com",
  "channel_scope": "dtc",
  "issued_at": "2026-02-24T00:00:00Z",
  "expires_at": "2026-05-24T00:00:00Z",
  "attributes": {
    "disclose:repeat_purchase_rate": {
      "value": 0.38,
      "observation_window_days": 90,
      "reported_by": "merchant",
      "attestation_level": "none",
      "attestation": null
    },
    "disclose:product_return_rate": {
      "value": 0.06,
      "observation_window_days": 90,
      "source": "shopify_api",
      "reported_by": "merchant",
      "computed_by": "sure_signal",
      "attestation_level": "computed",
      "attestation": null
    },
    "disclose:return_policy_type": {
      "value": "free",
      "reported_by": "merchant",
      "attestation_level": "none",
      "attestation": null
    },
    "disclose:return_window_days": {
      "value": 30,
      "reported_by": "merchant",
      "attestation_level": "none",
      "attestation": null
    },
    "disclose:refund_processing_time_median_days": {
      "value": 3.2,
      "observation_window_days": 90,
      "source": "shopify_api",
      "reported_by": "merchant",
      "computed_by": "sure_signal",
      "attestation_level": "computed",
      "attestation": null
    },
    "disclose:on_time_shipment_rate": {
      "value": 0.97,
      "observation_window_days": 90,
      "source": "loop_returns",
      "reported_by": "loop_returns",
      "computed_by": "loop_returns",
      "attestation_level": "signatory",
      "attestation": {
        "signatory_id": "loop-returns.com",
        "signatory_name": "Loop Returns",
        "attested_at": "2026-02-01T00:00:00Z",
        "expires_at": "2026-08-01T00:00:00Z",
        "signature": "eyJhbGciOiJFUzI1NiIsImtpZCI6Imxvb3AtMjAyNiJ9...",
        "signing_key_id": "loop-2026"
      }
    },
    "disclose:chargeback_rate": {
      "value": 0.003,
      "observation_window_days": 90,
      "source": "shopify_api",
      "reported_by": "merchant",
      "computed_by": "sure_signal",
      "attestation_level": "computed",
      "attestation": null
    },
    "disclose:review_rating": {
      "value": 4.7,
      "reported_by": "merchant",
      "attestation_level": "none",
      "attestation": null
    },
    "disclose:sustainability_certified": {
      "value": true,
      "reported_by": "merchant",
      "attestation_level": "none",
      "attestation": null
    },
    "disclose:business_registration_verified": {
      "value": true,
      "reported_by": "merchant",
      "attestation_level": "none",
      "attestation": null
    }
  },
  "sources": [
    {
      "source_id": "shopify",
      "source_name": "Shopify",
      "retrieved_at": "2026-02-24T00:00:00Z",
      "attributed_attributes": [
        "disclose:product_return_rate",
        "disclose:on_time_shipment_rate",
        "disclose:chargeback_rate",
        "disclose:order_accuracy_rate",
        "disclose:refund_processing_time_median_days"
      ]
    }
  ],
  "attestations": [
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
      "attested_at": "2026-02-01T00:00:00Z",
      "expires_at": "2026-08-01T00:00:00Z",
      "signature": "eyJhbGciOiJFUzI1NiIsImtpZCI6Imxvb3AtMjAyNiJ9...",
      "signing_key_id": "loop-2026",
      "payment_commitment": null
    },
    {
      "signatory_id": "narvar.com",
      "signatory_name": "Narvar",
      "attested_attributes": [
        "disclose:on_time_shipment_rate",
        "disclose:delivered_on_time_rate",
        "disclose:order_accuracy_rate"
      ],
      "attested_at": "2026-02-10T00:00:00Z",
      "expires_at": "2026-08-10T00:00:00Z",
      "signature": "eyJhbGciOiJFUzI1NiIsImtpZCI6Im5hcnZhci0yMDI2In0...",
      "signing_key_id": "narvar-2026",
      "payment_commitment": null
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

1. Fetch the Signatory Registry and confirm the `signatory_id` is listed with `status: active`.
2. Fetch the Signatory's signing keys from their `keys_url`.
3. Locate the key matching `signing_key_id`.
4. Reconstruct the canonical attestation payload.
5. Verify the ES256 signature against the payload using the public key.
6. Confirm `attested_at` is in the past and `expires_at` (if present) is in the future.

Agents MUST reject attestations that fail any step of this verification flow.

### Domain Binding

The `merchant_domain` field in the disclosure document MUST match the domain from which the document was served. Agents MUST reject documents where these do not match.

### Replay Prevention

Attestations include `attested_at` and `expires_at` timestamps. Agents SHOULD treat expired attestations as unverified, equivalent to self-reported attributes.

### Merchant Impersonation and Attestation Replay

A fraudster operating an impersonation domain MAY copy a legitimate merchant's disclosure document verbatim, including any attested signals. The `merchant_domain` field requirement (see Domain Binding) invalidates copied documents where the field is present and correctly set. However, agents MUST NOT rely solely on the `merchant_domain` field as fraud protection — DNS-level verification that the serving domain is the legitimate merchant domain is a TLS and network concern outside the scope of this framework.

The primary defense against attestation replay is the domain-binding requirement in the Signatory signature payload. Signatories MUST include the merchant's canonical domain in the signed attestation payload. Copying an attestation to a different domain produces a signature that fails verification at step 5 of the Signature Verification flow above.

Agents MUST perform full signature verification as specified. Agents MUST NOT shortcut verification by trusting the `merchant_domain` field without also verifying the Signatory signature covers that domain.

### Multi-Domain Merchants

A merchant operating across multiple regional storefronts (e.g., `brandname.com`, `brandname.ca`, `brandname.com.au`) MAY hold attestations covering more than one domain. In this case, the Signatory signature MUST cover an explicit `verified_domains` array rather than a single domain field. The serving domain MUST appear in the `verified_domains` array for the attestation to be considered valid.

Each domain's inclusion in `verified_domains` reflects explicit Signatory confirmation of data coverage for that storefront. It is not merchant self-declaration. Signatories MUST NOT include a domain in `verified_domains` unless they hold independent performance data for that storefront. Signatories SHOULD NOT treat regional storefronts and operationally distinct brand domains (e.g., a mainline store and an outlet store) as equivalent for attestation purposes.

### Attestation Revocation

Signatories MUST maintain a mechanism to revoke attestations before their `expires_at` date where a merchant's underlying data has changed materially. Signatories SHOULD publish a revocation endpoint or revocation list at a stable URL declared in the Signatory Registry entry.

Agents SHOULD check revocation status where a Signatory publishes a revocation endpoint. Agents MAY treat an unexpired attestation as valid where no revocation endpoint is available, but SHOULD note this limitation when surfacing attested signals.

### Verification Performance

Cryptographic signature verification is local computation performed against data already retrieved in the disclosure document fetch. It does not require an additional network request in the common case where the Signatory's public key is cached. Added latency is negligible and does not materially affect agent transaction timing. Agents SHOULD cache Signatory public keys with a refresh interval consistent with the Signatory's published key rotation policy.

---

## Agent Consumption Guidelines

Agents consuming Disclose data operate with significant discretion. The framework does not mandate how agents weight or surface disclosure signals — this is intentionally left to the platform and agent developer. The following are non-normative recommendations:

- Signals with `attestation_level: none` should be surfaced as merchant-reported and weighted accordingly.
- Signals with `attestation_level: computed` should be surfaced as platform-derived, with higher confidence than self-reported but below independently attested.
- Signals with `attestation_level: signatory` should be surfaced as independently verified, with the Signatory named when relevant to the buyer.
- Review signals should be distinguished from operational metrics when surfaced to buyers. Agents SHOULD treat `disclose:review_rating` as contextual rather than authoritative, and SHOULD surface `disclose:review_verified_purchase_rate` and recency signals alongside it wherever possible.
- Missing disclosures may be surfaced as "disclosure unavailable" rather than assumed positive or negative.
- Agents SHOULD NOT produce composite scores or trust tiers derived from Disclose attributes. Such aggregations undermine the principle that trust is emergent from raw, verifiable signals.
- Agents SHOULD NOT penalize merchants for not disclosing specific attributes unless disclosure of that attribute is required by applicable law or platform policy.

---

## Reference Implementation

To support adoption and validate the specification, the Disclose Framework provides the following reference resources at `https://github.com/disclose-framework/spec`:

- **JSON Schema:** A machine-readable schema for validating disclosure documents against the specification.
- **Validator:** A reference validator that checks a disclosure document for schema compliance, domain binding, and `observation_window_days` completeness.
- **Sample document:** A complete, valid example disclosure document suitable for testing agent consumption logic.
- **Signatory mock:** A lightweight mock Signatory endpoint for testing signature verification flows without a live Signatory integration.

Implementations that conform to the specification and pass the reference validator MAY self-identify as Disclose-compatible.

---

## Versioning

Disclose uses semantic versioning in the format `MAJOR.MINOR` (e.g., `0.2`, `1.0`). The version is declared in the disclosure document via the `disclose_version` field.

The following changes MAY be introduced without a version increment: adding new optional attributes, adding new optional attestation fields, adding new Signatory entries to the registry.

The following changes MUST result in a new MAJOR version: removing or renaming existing attributes, changing the attestation payload structure or signature algorithm, modifying the discovery endpoint path.

---

## Glossary

| Term | Definition |
|------|------------|
| Agent | A platform, AI assistant, or automated system that queries Disclose data on behalf of a buyer |
| Attestation | A cryptographically signed statement from a Signatory confirming that specific disclosed attributes have been independently verified against source data |
| Attestation Level | A field on every signal object declaring how the value was produced. One of: `none` (merchant self-reported), `computed` (derived from a platform API by a third-party tool), or `signatory` (cryptographically signed by an authorized Signatory). Agents SHOULD use this as the primary signal weighting input. |
| Benchmark Reference | An optional object within a Signatory attestation providing vertical or category-level signal distributions (p50, p90) derived from the Signatory's merchant portfolio. Intended to give agents interpretive context for attested values. Supported verticals are not enumerated in this version of the specification — Signatories use free-form category labels. See [Signatory Benchmarks](#signatory-benchmarks). |
| Disclosure Document | The JSON document published by a merchant at `/.well-known/disclose` |
| Emergent Trust | The principle that trustworthiness arises from visible, verifiable behaviour rather than from framework-assigned scores or badges |
| Exchange Rate | The proportion of return transactions where the buyer selected a replacement item rather than a refund; a signal of product confidence distinct from the return rate |
| Item | The product or service being transacted. Maps to `schema:ItemOffered`, the schema.org parent type that encompasses both physical goods (`schema:Product`) and services (`schema:Service`). Signals published at Item scope reflect attributes intrinsic to the item itself — such as manufacturer warranty terms, safety recall status, or authorized reseller eligibility — independent of any specific Merchant or Offer. Using `schema:ItemOffered` as the base type ensures the framework applies equally to physical goods, home services, B2B, and digital products. |
| Merchant | The seller or service provider publishing disclosure signals. Maps to `schema:Organization`. Signals published at Merchant scope reflect aggregate operational performance across all of the merchant's transactions — for example, overall return rate or average fulfillment time. Merchant-scope signals establish baseline seller confidence independent of any specific Item or Offer. The term "Merchant" is used throughout this specification in preference to "Organization" to signal commerce intent and to remain consistent with the concept of Merchant of Record. One of three disclosure scopes; see [Disclosure Scopes](#disclosure-scopes). |
| Merchant Sovereignty | The principle that merchants retain full control over what they disclose, to whom, and when |
| Observation Window | The time period over which a metric is computed, declared via the `observation_window_days` field on each signal object |
| Offer | The intersection of a specific Merchant and a specific Item — this seller, selling this item, under these conditions. Maps to `schema:Offer`. Signals published at Offer scope reflect how a particular Merchant performs on a particular Item: for example, the return rate for this SKU at this seller, or the inventory accuracy rate for this item. Offer-scope signals are the most precise unit of disclosure in the framework, and are the primary data layer an agent uses when comparing the same Item across multiple Merchants. Because Offers are inherently transient — prices and availability change — agents should treat Offer-scope signals as time-sensitive and respect the `attested_at` timestamp in any covering attestation. One of three disclosure scopes; see [Disclosure Scopes](#disclosure-scopes). |
| Payment Commitment | An optional field in an attestation object declaring a Signatory's fee terms and payment routing instruction for outcome-based compensation. Supports success-based fee models where Signatory compensation is tied to a completed transaction rather than a query. `null` in v0.2. Full mechanism defined in a future extension. |
| Progressive Enhancement | The ability to begin participation with a single attribute and expand disclosures over time |
| Review Recency | The proportion of a merchant's total reviews submitted within a recent time window (90 or 365 days), used to assess the freshness of aggregate review ratings |
| Selective Disclosure | The ability to disclose specific attributes without an all-or-nothing requirement |
| Signatory | An authorized third party with direct access to source data that cryptographically signs attestations confirming the accuracy of specific merchant signals. Signatories stake their own reputation on the values they attest. Listed in the public Signatory Registry. |
| Signatory Registry | The canonical, publicly accessible list of authorized Disclose Signatories maintained by the framework governing body at `https://discloseframework.dev/registry/signatories.json` |
| Source | A platform or system from which self-reported attributes were derived. Declared in the `sources` array. Distinct from a Signatory: a source carries no cryptographic accountability. Agents MAY treat platform-sourced attributes with higher confidence than merchant-entered attributes. A platform appearing in `sources` today MAY become a registered Signatory once formal attestation is established. Recommended `source_id` values: `shopify`, `lightspeed`, `woocommerce`, `bigcommerce`, `magento`, `squarespace`, `wix`, `salesforce_commerce`, `netsuite`. Additional values are permitted; platforms not on this list SHOULD use their primary domain as the `source_id`. |
