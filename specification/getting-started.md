# Getting Started with Disclose

### Publishing Your First Disclosure Document
**Disclose Framework — Quick Start Guide**

---

## Overview

A Disclose disclosure document is a JSON file merchants publish at a predictable location on their domain. Any AI agent, MCP server, or automated system can retrieve it without prior knowledge of the merchant's platform, tech stack, or API.

It is to AI agents what `robots.txt` is to web crawlers: a known address, a standard format, and a voluntary signal.

The full specification is in [`specification/overview.md`](overview.md). This guide covers what you need to publish a valid disclosure document and get discovered.

Disclose does not certify merchants. It does not produce scores, badges, tiers, rankings, or recommendations. Merchants publish operating evidence. Agents decide what the signals mean.

---

## File Location

Publish your disclosure document at:

```txt
https://www.merchantname.com/.well-known/disclose
```

This is the canonical path. Agents check here first. No registration or configuration is required.

If your hosting platform does not support the `/.well-known/` directory, agents will also check `/.well-known/disclose.json` before falling back to the domain root:

```txt
https://www.merchantname.com/.well-known/disclose.json
https://www.merchantname.com/disclose.json
```

Agents fall back to the root path only if both `/.well-known/` paths return a `404`.

---

## Minimal Valid Example

A merchant may disclose a single signal. No Signatory is required to get started.

```json
{
  "disclose_version": "0.3",
  "merchant_domain": "merchantname.com",
  "publication_mode": "automated",
  "issued_at": "2026-03-01T00:00:00Z",
  "expires_at": "2026-03-03T00:00:00Z",
  "core_profile": {
    "name": "core-commerce",
    "version": "0.1",
    "signals_defined": 7,
    "signals_disclosed": 1
  },
  "attributes": {
    "disclose:on_time_shipment_rate": {
      "value": 0.97,
      "unit": "ratio",
      "observation_window_days": 90,
      "window_start": "2025-12-01",
      "window_end": "2026-02-28",
      "generated_at": "2026-03-01T00:00:00Z",
      "refresh_frequency": "daily",
      "next_expected_refresh": "2026-03-02T00:00:00Z",
      "source_of_record": "shopify_api",
      "computed_by": "merchant",
      "reported_by": "merchant",
      "attestation_level": "none",
      "methodology_version": "core-commerce-v0.1",
      "attestation": null
    }
  }
}
```

That is a valid Disclose implementation. Publish it and any agent that knows the convention can find it.

Core coverage is descriptive only. It indicates how many defined Core Commerce signals are present in the file. It is not a score, badge, ranking, certification, endorsement, or recommendation.

---

## Core Commerce Profile

The Core Commerce Profile defines the first standard set of merchant operating signals for agentic commerce.

Merchants are not required to expose every Core signal. A merchant may publish one Core signal, all seven Core signals, or any subset in between. A disclosure document remains conformant if each published signal follows the required methodology, source, freshness, and attestation metadata rules.

The Core Commerce signal set is:

| Signal | What it tells agents |
|---|---|
| `disclose:product_return_rate` | How often fulfilled products are returned |
| `disclose:on_time_shipment_rate` | Whether orders leave within the merchant's stated fulfillment window |
| `disclose:refund_processing_time_median_days` | Median time from return receipt to refund completion |
| `disclose:chargeback_rate` | Chargebacks as a proportion of total transactions |
| `disclose:dispute_win_rate` | Rate of disputed transactions resolved in the merchant's favour |
| `disclose:platform_seller_tenure_days` | How long the merchant has been active on its primary commerce platform |
| `disclose:order_accuracy_rate` | Rate of orders fulfilled without incorrect or damaged items |

All Core Commerce signals use a trailing 90-day observation window, except `platform_seller_tenure_days`, which is measured as of `issued_at`.

Automated Core Commerce disclosures should refresh daily.

---

## Full Example: Computed Signals

This example shows six Core Commerce signals computed from a platform API by a third-party tool. The signals are not cryptographically signed, so their `attestation_level` is `computed`, not `signatory`.

```json
{
  "disclose_version": "0.3",
  "merchant_domain": "merchantname.com",
  "publication_mode": "automated",
  "channel_scope": "dtc",
  "issued_at": "2026-03-01T00:00:00Z",
  "expires_at": "2026-03-03T00:00:00Z",
  "core_profile": {
    "name": "core-commerce",
    "version": "0.1",
    "signals_defined": 7,
    "signals_disclosed": 6
  },
  "attributes": {
    "disclose:product_return_rate": {
      "value": 0.0006,
      "unit": "ratio",
      "observation_window_days": 90,
      "window_start": "2025-12-01",
      "window_end": "2026-02-28",
      "generated_at": "2026-03-01T00:00:00Z",
      "refresh_frequency": "daily",
      "next_expected_refresh": "2026-03-02T00:00:00Z",
      "source_of_record": "shopify_api",
      "computed_by": "sure_signal",
      "reported_by": "merchant",
      "attestation_level": "computed",
      "methodology_version": "core-commerce-v0.1",
      "attestation": null
    },
    "disclose:on_time_shipment_rate": {
      "value": 0.95,
      "unit": "ratio",
      "observation_window_days": 90,
      "window_start": "2025-12-01",
      "window_end": "2026-02-28",
      "generated_at": "2026-03-01T00:00:00Z",
      "refresh_frequency": "daily",
      "next_expected_refresh": "2026-03-02T00:00:00Z",
      "source_of_record": "shopify_api",
      "computed_by": "sure_signal",
      "reported_by": "merchant",
      "attestation_level": "computed",
      "methodology_version": "core-commerce-v0.1",
      "attestation": null
    },
    "disclose:refund_processing_time_median_days": {
      "value": 2.2,
      "unit": "days",
      "observation_window_days": 90,
      "window_start": "2025-12-01",
      "window_end": "2026-02-28",
      "generated_at": "2026-03-01T00:00:00Z",
      "refresh_frequency": "daily",
      "next_expected_refresh": "2026-03-02T00:00:00Z",
      "source_of_record": "shopify_api",
      "computed_by": "sure_signal",
      "reported_by": "merchant",
      "attestation_level": "computed",
      "methodology_version": "core-commerce-v0.1",
      "attestation": null
    },
    "disclose:chargeback_rate": {
      "value": 0.0002,
      "unit": "ratio",
      "observation_window_days": 90,
      "window_start": "2025-12-01",
      "window_end": "2026-02-28",
      "generated_at": "2026-03-01T00:00:00Z",
      "refresh_frequency": "daily",
      "next_expected_refresh": "2026-03-02T00:00:00Z",
      "source_of_record": "shopify_api",
      "computed_by": "sure_signal",
      "reported_by": "merchant",
      "attestation_level": "computed",
      "methodology_version": "core-commerce-v0.1",
      "attestation": null
    },
    "disclose:dispute_win_rate": {
      "value": 0.98,
      "unit": "ratio",
      "observation_window_days": 90,
      "window_start": "2025-12-01",
      "window_end": "2026-02-28",
      "generated_at": "2026-03-01T00:00:00Z",
      "refresh_frequency": "daily",
      "next_expected_refresh": "2026-03-02T00:00:00Z",
      "source_of_record": "shopify_api",
      "computed_by": "sure_signal",
      "reported_by": "merchant",
      "attestation_level": "computed",
      "methodology_version": "core-commerce-v0.1",
      "attestation": null
    },
    "disclose:platform_seller_tenure_days": {
      "value": 3862,
      "unit": "days",
      "generated_at": "2026-03-01T00:00:00Z",
      "refresh_frequency": "daily",
      "next_expected_refresh": "2026-03-02T00:00:00Z",
      "source_of_record": "shopify_api",
      "computed_by": "sure_signal",
      "reported_by": "merchant",
      "attestation_level": "computed",
      "methodology_version": "core-commerce-v0.1",
      "attestation": null
    }
  },
  "sources": [
    {
      "source_id": "shopify",
      "source_name": "Shopify",
      "retrieved_at": "2026-03-01T00:00:00Z",
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

---

## Manual Snapshot Example

Manual snapshots may be used for testing, validation, onboarding, or demonstration. They must not imply daily refresh.

```json
{
  "disclose_version": "0.3",
  "merchant_domain": "merchantname.com",
  "publication_mode": "manual_snapshot",
  "issued_at": "2026-03-01T00:00:00Z",
  "expires_at": "2026-04-01T00:00:00Z",
  "snapshot_note": "Manual pull used to validate agent readability.",
  "core_profile": {
    "name": "core-commerce",
    "version": "0.1",
    "signals_defined": 7,
    "signals_disclosed": 1
  },
  "attributes": {
    "disclose:product_return_rate": {
      "value": 0.0006,
      "unit": "ratio",
      "observation_window_days": 90,
      "window_start": "2025-12-01",
      "window_end": "2026-02-28",
      "generated_at": "2026-03-01T00:00:00Z",
      "refresh_frequency": "none",
      "source_of_record": "shopify_api",
      "computed_by": "sure_signal",
      "reported_by": "merchant",
      "attestation_level": "computed",
      "methodology_version": "core-commerce-v0.1",
      "attestation": null
    }
  }
}
```

---

## Top-Level Fields

| Field | Required | Description |
|---|---|---|
| `disclose_version` | Yes | Spec version. Use `"0.3"` |
| `merchant_domain` | Yes | Canonical merchant domain. Must match the domain serving the file |
| `publication_mode` | Recommended | One of `automated` or `manual_snapshot` |
| `channel_scope` | Optional | Channel reflected by the signals. Default is `dtc` |
| `issued_at` | Yes | When this document was generated, in RFC 3339 format |
| `expires_at` | Recommended | When agents should re-fetch |
| `core_profile` | Recommended for Core Commerce signals | Describes Core Commerce profile version and descriptive coverage |
| `attributes` | Yes | Map of disclosed merchant signals |
| `sources` | Optional | Platform or system sources used to compute disclosed signals |
| `attestations` | Optional | Cryptographically signed attestations from authorized Signatories |

---

## Attribute Fields

Each disclosed signal is published as an object.

| Field | Required | Description |
|---|---|---|
| `value` | Yes | The disclosed value |
| `unit` | Recommended | `ratio`, `days`, `hours`, `count`, `boolean`, `string`, or another appropriate unit |
| `observation_window_days` | Required for time-bounded Core signals | Core Commerce signals use `90` |
| `window_start` | Required for time-bounded Core signals | Start date of the trailing 90-day observation window |
| `window_end` | Required for time-bounded Core signals | End date of the trailing 90-day observation window |
| `generated_at` | Required for Core signals | Timestamp when the signal was generated |
| `refresh_frequency` | Recommended | Usually `daily` for automated Core signals; `none` for manual snapshots |
| `next_expected_refresh` | Recommended for automated signals | Timestamp when the signal is expected to refresh next |
| `source_of_record` | Recommended | Platform or system from which the underlying data was retrieved |
| `computed_by` | Recommended for computed signals | Tool or service that calculated the signal |
| `reported_by` | Yes | `merchant` or the Signatory domain |
| `attestation_level` | Yes | One of `none`, `computed`, or `signatory` |
| `methodology_version` | Required for Core signals | Use `core-commerce-v0.1` for Core Commerce signals |
| `attestation` | Yes | `null` unless `attestation_level` is `signatory` |
| `signal_status` | Optional | May explain absence or non-publication when a publisher chooses to include it |

---

## Choosing What to Disclose

All signals are optional. Publish what you have clean data for. A single accurate signal is better than ten inaccurate ones.

Disclose standardizes how a signal is expressed, not whether a merchant must expose it.

If a Core signal is absent, the protocol does not define that absence as positive or negative. Agents may decide how to interpret absence according to their own policies.

Publishers may optionally include `signal_status` metadata to explain why a signal is not disclosed. This is informational and not required.

Recommended `signal_status` values include:

| Status | Meaning |
|---|---|
| `not_disclosed` | The merchant chose not to expose the signal |
| `not_available` | The source system does not provide the required data |
| `insufficient_volume` | The sample size is too low for reliable calculation |
| `not_applicable` | The signal does not apply to the merchant's business model |
| `expired` | The signal was previously disclosed but is no longer fresh |
| `error` | The signal could not be generated because of a temporary issue |

---

## Attested, Computed, and Self-Reported Signals

Agents treat signals differently depending on `attestation_level`.

**Self-reported (`none`)**  
The merchant publishes the value with no third-party computation or signature. Agents should surface it as merchant-reported and weight it accordingly.

**Computed (`computed`)**  
The value was pulled from a platform API and calculated by a third-party tool, such as Sure Signal from Shopify API data. It is harder to manipulate than merchant-entered data, but carries no Signatory accountability.

**Signatory-attested (`signatory`)**  
An authorized Signatory with direct access to source data cryptographically signs the signal. The Signatory is accountable only for the specific signed signals within its authorized scope.

Signatories are listed in the [Disclose Signatory Registry](https://discloseframework.dev/registry/signatories.json). Signatories do not certify merchants, require complete Core Profile coverage, or determine how agents should interpret the signal.

---

## Caching and Freshness

- Automated Core Commerce disclosures should refresh daily
- Core Commerce signals use a trailing 90-day observation window
- Automated Core Commerce signals should include `generated_at` and `next_expected_refresh`
- Agents should treat automated Core Commerce signals as stale when `generated_at` exceeds the expected refresh interval by more than 24 hours, unless the file explicitly declares a longer interval
- Manual snapshots must declare `publication_mode: "manual_snapshot"` and must not imply daily refresh
- A missing or unreachable file is treated as no disclosure, not as a protocol error

For automated files, set `expires_at` to a short interval that reflects the daily refresh expectation, such as 24 to 48 hours after `issued_at`.

---

## JSON-LD in Storefront Head

For agents that browse pages rather than querying files directly, merchants may also embed Disclose signals as JSON-LD in the storefront `<head>`.

```html
<script type="application/ld+json">
{
  "@context": {
    "@vocab": "https://schema.org/",
    "disclose": "https://discloseframework.dev/vocab#"
  },
  "@type": "Organization",
  "disclose:product_return_rate": {
    "value": 0.0006,
    "unit": "ratio",
    "observation_window_days": 90,
    "window_start": "2025-12-01",
    "window_end": "2026-02-28",
    "generated_at": "2026-03-01T00:00:00Z",
    "source_of_record": "shopify_api",
    "computed_by": "sure_signal",
    "attestation_level": "computed",
    "methodology_version": "core-commerce-v0.1"
  }
}
</script>
```

The two approaches use the same schema and are complementary. Use `/.well-known/disclose` for agents querying directly and JSON-LD for agents parsing pages.

---

## Implementation Checklist

- [ ] Choose which signals to publish. Start with one if needed
- [ ] Use `disclose_version: "0.3"`
- [ ] Add `publication_mode`, usually `automated`
- [ ] Add `core_profile` metadata if publishing Core Commerce signals
- [ ] Use a trailing 90-day window for Core Commerce signals
- [ ] Include `generated_at`, `window_start`, `window_end`, and `methodology_version` for Core signals
- [ ] Include `source_of_record` and `computed_by` where applicable
- [ ] Set `refresh_frequency: "daily"` for automated Core Commerce disclosures
- [ ] Publish at `/.well-known/disclose` on your domain
- [ ] Set `expires_at` to reflect the refresh cadence
- [ ] Optionally embed JSON-LD in your storefront `<head>` for browser agents

---

## For Agent Developers

To query a merchant's disclosure:

```txt
GET https://{merchant_domain}/.well-known/disclose
Accept: application/json
```

Fall back to `https://{merchant_domain}/.well-known/disclose.json`, then `https://{merchant_domain}/disclose.json` if the canonical path returns a `404`.

Agents should verify Signatory signatures against the [Signatory Registry](https://discloseframework.dev/registry/signatories.json) before treating a signal as signatory-attested. The full verification flow is in [`specification/overview.md`](overview.md).

Agents should not treat absent Core signals as protocol-defined negative claims. Agents may decide how to interpret disclosed and absent signals according to their own policies.

---

*Disclose Framework is an open standard. Contribute at [github.com/disclose-framework](https://github.com/disclose-framework).*
